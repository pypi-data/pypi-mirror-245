import argparse
from typing import Union

from lvp_data.pull_masterdata import pull_circuit_span, search_site_groups


def run_pull_circuit_span(args):

    circuit_span = pull_circuit_span(site_group_id=args.site_group_id, env=args.env)

    print()
    print(f"circuit span {circuit_span.id}: {circuit_span.name}")
    print()
    print(circuit_span.geography)
    print()
    for cond in circuit_span.conductors.values():
        print(cond)
        print()


def run_search_site_groups(args):

    site_groups = search_site_groups(
        column=args.column, contains=args.contains, operator=args.operator, env=args.env
    )

    for row in site_groups:
        print()
        for k, v in row._asdict().items():
            print(f"{k}: {v}")


def main():

    parser = argparse.ArgumentParser(description="Execute functions from lvp_data")
    parser.add_argument("action", type=str, choices=["pull", "search"])
    parser.add_argument("-sg", "--site_group_id", type=int)
    parser.add_argument("-col", "--column", type=str, default="site_group_name")
    parser.add_argument("-con", "--contains", type=str, nargs="+")
    parser.add_argument(
        "-op", "--operator", type=str, default="AND", choices=["AND", "OR"]
    )
    parser.add_argument("--env", type=str, default="prod")
    args = parser.parse_args()

    if args.action == "pull":

        if args.site_group_id is None:
            raise ValueError("site_group_id must be provided for pull action")

        run_pull_circuit_span(args)

    elif args.action == "search":

        if args.contains is None:
            raise ValueError("contains must be provided for search action")

        if len(args.contains) == 1:
            args.contains = args.contains[0]

        run_search_site_groups(args)


if __name__ == "__main__":
    main()
