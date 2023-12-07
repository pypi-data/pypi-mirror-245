from dataclasses import dataclass
from datetime import datetime

from collections import namedtuple
from numpy import array
from numpy.typing import NDArray
from psycopg2.extras import NamedTupleCursor

from lvp_data.connections import conn_man


def handle_time_bounds(start=None, end=None, tz=None):
    """
    Forces end >= start and the datetimes to be timezone-aware.
    """
    if start is None and end is None:
        start, end = None, None
    elif start is not None and end is None:
        end = start
    elif start is None and end is not None:
        start = end

    if tz is not None:
        start = start.astimezone(tz)
        end = end.astimezone(tz)

    return start, end


def pull_lidar_series(
    edge_device_id: int, start: datetime, end: datetime, scans: bool = False, env: str = "prod"
) -> NDArray[namedtuple]:
    """
    Retrieves all lidar edge data between start and end.
    """
    # handle arguments
    start, end = handle_time_bounds(start=start, end=end)
    edge_message_str = "message_body as message," if scans is True else ""

    # create or use existing database connection
    connection = conn_man.connect("telemetry", "edge_telemetry", env=env)

    # run query
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:

        cursor.execute(
            f"""
            SELECT
                edge_device_id,
                dttm at time zone 'utc' as dttm,
                extract(epoch from dttm) as timestamp,
                edge_message_uuid as uuid,
                (message_body->'bottomBoardTempC') as temperature,
                (message_body->'ambientTempC') as ambient_temperature,
                (message_body->'relativeHumidity') as relative_humidity,
                (message_body->'supplyVoltage') as voltage,
                (message_body->'signalStrength') as signal_strength,
                {edge_message_str}
                coalesce(jsonb_array_length(message_body->'raw_scan_output'->'points'), 0) as m_points,
                coalesce(jsonb_array_length(message_body->'compressed_scan_output'->'points'), 0) as n_points
            FROM
                edge_message
            WHERE
                '{start}' <= dttm AND dttm <= '{end}'
            AND
                edge_device_id = {edge_device_id}
            ORDER BY dttm ASC
            """,
        )

        results = cursor.fetchall()

    return array([row for row in results])


@dataclass
class UtilityLoading:
    dttm: datetime
    loading: float


def pull_utility_loading(site_group_id: int, start: datetime, end: datetime, env: str = "prod"):
    """
    Retrieves all utility loading data between start and end.
    """
    # handle arguments
    start, end = handle_time_bounds(start=start, end=end)

    # create the connection
    connection = conn_man.connect("telemetry", "emf_telemetry")

    # run query
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:

        cursor.execute(
            f"""
            SELECT
                ulv.dttm, ulv.amps as loading
            FROM
                utility_loading_values ulv
            WHERE
                ulv.site_group_id = {site_group_id}
            AND
                '{start}' <= dttm AND dttm < '{end}'
            ORDER BY dttm ASC;
            """,
        )

        results = cursor.fetchall()

    return array([UtilityLoading(dttm=row.dttm, loading=row.loading) for row in results])


if __name__ == "__main__":

    from datetime import datetime
    from pytz import utc

    sgid = 126
    start = datetime(2021, 3, 8, 5, tzinfo=utc)
    end = datetime(2021, 5, 16, 3, 50, tzinfo=utc)
    scada = pull_utility_loading(site_group_id=sgid, start=start, end=end)
