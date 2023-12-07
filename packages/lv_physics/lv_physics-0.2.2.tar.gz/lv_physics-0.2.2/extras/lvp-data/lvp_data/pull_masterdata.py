from typing import List, Union

from numpy import array, float_, nan, zeros
from psycopg2.extras import NamedTupleCursor

from lv_physics.core.dynamic_objects import DynamicConductor, DynamicInsulator
from lv_physics.core.ohl_objects import ConductorBundle, ConductorMaterial, ConductorShape
from lv_physics.core.scene_objects import Geography
from lv_physics.core.catenaries import fit_catenary_3d
from lv_physics.general.objects import CircuitSpan, Span

from lvp_data.conductor_types import calc_conductor_material
from lvp_data.connections import conn_man


def pull_span(site_group_ids: List[int], env: str = "prod") -> Span:
    """
    Retrieves all circuit-spans in a span.
    """
    return {
        site_group_id: pull_circuit_span(site_group_id, env=env)
        for site_group_id in site_group_ids
    }


def pull_circuit_span(site_group_id: int, env: str = "prod") -> CircuitSpan:
    """
    Retrieves circuit-span data from the masterdata database.
    """
    # create or use existing database connection
    connection = conn_man.connect("masterdata", "masterdata", env=env)

    # run query
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:

        cursor.execute(
            f"""
            SELECT
                sg.site_group_id,
                sg.site_group_name,
                c.conductor_id,
                c.phase,
                c.name,
                c.type,
                CAST(c.num_bundled_subconductors AS int),
                ARRAY[
                    CAST(css.survey_structure_start_x AS float),
                    CAST(css.survey_structure_start_y AS float),
                    CAST(css.survey_structure_start_z AS float)
                ] AS survey_start,
                ARRAY[
                    CAST(css.survey_conductor_x AS float),
                    CAST(css.survey_conductor_y AS float),
                    CAST(css.survey_conductor_z AS float)
                ] AS survey_mid,
                ARRAY[
                    CAST(css.survey_structure_end_x AS float),
                    CAST(css.survey_structure_end_y AS float),
                    CAST(css.survey_structure_end_z AS float)
                ] AS survey_end
            FROM site_group sg
            FULL JOIN span sp ON sg.span_id = sp.span_id
            FULL JOIN section se ON se.section_id = sg.section_id
            FULL JOIN line ln ON se.line_id = ln.line_id
            FULL JOIN conductor c ON se.section_id = c.section_id
            FULL JOIN conductor_span cs ON cs.conductor_id = c.conductor_id AND cs.span_id = sg.span_id
            FULL JOIN conductor_span_survey css ON css.conductor_span_id = cs.conductor_span_id
            WHERE sg.site_group_id = {site_group_id}
            ORDER BY sg.site_group_id
            """
        )

        results = cursor.fetchall()

    # get conductor material properties
    material = pull_conductor_material(results[0].name, results[0].type, env=env)

    # build conductors
    conductors_dict = {}

    for row in results:

        # conductor bundle
        if row.num_bundled_subconductors > 1:
            bundle = pull_conductor_bundle(row.conductor_id)
        else:
            bundle = ConductorBundle(offsets=zeros((row.num_bundled_subconductors, 3)))

        # insulators
        insulator_a = DynamicInsulator(
            connect=array(row.survey_start, float_),
            mounts=array([[nan, nan, nan]]),
        )

        insulator_b = DynamicInsulator(
            connect=array(row.survey_end, float_),
            mounts=array([[nan, nan, nan]]),
        )

        # initial conductor shape
        survey_points = array([row.survey_mid], float_)

        swing_angle, curvature = fit_catenary_3d(
            survey_points,
            end_point_a=insulator_a.connect,
            end_point_b=insulator_b.connect,
        )

        # conductor
        conductors_dict[row.conductor_id] = DynamicConductor(
            id=row.conductor_id,
            bundle=bundle,
            insulators=[insulator_a, insulator_b],
            material=material,
            shape=ConductorShape(
                curvature=curvature,
                swing_angle=swing_angle,
            )
        )

    # get geography
    geography = pull_geography(site_group_id, env=env)

    return CircuitSpan(
        id=site_group_id,
        name=results[-1].site_group_name,
        conductors=conductors_dict,
        geography=geography,
    )


def pull_conductor_bundle(conductor_id: int, env="prod") -> ConductorBundle:

    connection = conn_man.connect("masterdata", "masterdata", env=env)

    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:

        cursor.execute(
            f"""
            SELECT
            c.conductor_id,
            CAST(csb.bundle_index AS int),
            ARRAY[
                CAST(csb.survey_offset_x AS float),
                CAST(csb.survey_offset_y AS float),
                CAST(csb.survey_offset_z AS float)
            ] AS survey_offset
            FROM site_group sg
            FULL JOIN span sp ON sp.span_id = sg.span_id
            FULL JOIN section se ON se.section_id = sg.section_id
            FULL JOIN conductor c ON c.section_id = sg.section_id
            FULL JOIN conductor_span_bundle csb ON csb.conductor_id = c.conductor_id
            WHERE
                c.conductor_id = {conductor_id}
            ORDER BY
                csb.bundle_index ASC
            """
        )

        results = cursor.fetchall()

    return ConductorBundle(
        offsets=array([row.survey_offset for row in results], float_)
    )


def pull_conductor_material(name: str, type: str, env="prod") -> ConductorMaterial:

    connection = conn_man.connect("masterdata", "masterdata", env=env)

    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:

        cursor.execute(
            f"""
            SELECT
                conductor_name AS name,
                conductor_type AS type,
                CAST(stranding_outer AS int),
                CAST(stranding_core AS int),
                CAST(cross_sectional_area_outer AS float) * 0.0006452       -- [in^2] -> [m^2]
                    AS area_outer,
                CAST(cross_sectional_area_core AS float) * 0.0006452        -- [in^2] -> [m^2]
                    AS area_core,
                CAST(diameter_total AS float) * 0.0254                      -- [in] -> [m]
                    AS diameter,
                CAST(weight_outer AS float) * 4.448 * 3.28084 / 1000.0      -- [lbs(1kft)] -> [N(1m)]
                    AS weight_outer,
                CAST(weight_core AS float) * 4.448 * 3.28084 / 1000.0       -- [lbs(1kft)] -> [N(1m)]
                    AS weight_core,
                CAST(rating_breaking_strength AS float) * 4.448             -- [lbs] -> [N]
                    AS rating_breaking_strength,
                CAST(ac_resistance_25c AS float) * 3.28084 / 5280.0         -- [ohms(1kft)] -> [ohms(1m)]
                    AS resistance_25c,
                CAST(ac_resistance_slope AS float) * 3.28084 / 5280.0       -- [ohms(1kft)/C] -> [ohms(1m)/C]
                    AS resistance_slope
            FROM
                conductor_properties
            WHERE
                conductor_name = '{name}'
                AND
                conductor_type = '{type}'
            """
        )

        results = cursor.fetchone()

    if results is None:
        raise Exception(f"No conductor properties found for {name} - {type}.")

    return calc_conductor_material(results)


def pull_geography(site_group_id: int, env: str = "prod") -> Geography:
    """
    Retrieves site geography data from the masterdata database.
    """
    connection = conn_man.connect("masterdata", "masterdata", env=env)

    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:

        cursor.execute(
            f"""
            SELECT
                sg.site_group_id,
                CAST(sp.elevation AS float),
                CAST(sp.heading AS float),
                CAST(sp.latitude AS float),
                CAST(sp.longitude AS float)
            FROM
                site_group sg
            FULL JOIN
                span sp ON sg.span_id = sp.span_id
            WHERE
                sg.site_group_id = {site_group_id}
            ORDER
                BY sg.site_group_id
            """
        )

        row = cursor.fetchone()

    return Geography(
        elevation=row.elevation,
        heading=row.heading,
        latitude=row.latitude,
        longitude=row.longitude,
    )


def search_site_groups(
    column: str = "site_group_name",
    contains: Union[str, List[str]] = None,
    operator="AND",
    env="prod",
):
    """
    This function queries site-group information for all entries in the site-group table that
    contain the provided string or strings with either the AND or the OR operator.  The match is
    case-insensitive and ignores white spaces.

    :param contains: a string or an iterable of strings to be searched in the column
    :param operator: the operator to use for the query, can be 'AND' or 'OR'
    :return: a list of NamedTuples containing the matching outpu
    """
    if operator.lower() not in ["and", "or"]:
        raise ValueError(
            f"The operator provided must be either 'AND' or 'OR', not {operator}"
        )

    if isinstance(contains, str):
        search_string = f"""
            WHERE REPLACE(LOWER({column}), ' ', '')
            LIKE REPLACE(LOWER('%{contains}%'), ' ', '')
        """

    elif isinstance(contains, list):
        search_strings = [
            f"""
            REPLACE(LOWER({column}), ' ', '')
            LIKE REPLACE(LOWER('%{item}%'), ' ', '')
            """
            for item in contains
        ]
        search_string = "WHERE " + f" {operator} ".join(search_strings)

    elif contains is None:
        search_string = ""

    else:
        raise TypeError(
            "contains argument must be either a string or a list of strings"
        )

    connection = conn_man.connect("masterdata", "masterdata", env=env)

    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:

        cursor.execute(
            f"""
            SELECT
                site_group_id,
                site_group_name,
                short_name,
                section_id,
                span_id,
                model_type,
                status,
                weather_station_id,
                online_date,
                retirement_date
            FROM
                site_group

            {search_string}
            """
        )

        results = cursor.fetchall()

    return results


if __name__ == "__main__":

    SITE_GROUP_ID = 192

    print("CIRCUIT-SURVEY")
    circuit_span = pull_circuit_span(site_group_id=SITE_GROUP_ID)
    print(circuit_span.to_json(indent=2))
    print(flush=True)
