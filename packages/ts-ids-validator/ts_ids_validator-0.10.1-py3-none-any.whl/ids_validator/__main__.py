import argparse
import sys
from pathlib import Path

from ids_validator.ids_validator import validate_ids


def main():
    parser = argparse.ArgumentParser(description="Validate IDS Artifacts")

    parser.add_argument(
        "-i",
        "--ids_dir",
        type=str,
        default=".",
        required=True,
        help="Path to the IDS folder",
    )
    parser.add_argument(
        "-p",
        "--previous_ids_dir",
        type=str,
        default=None,
        required=False,
        help=(
            "Path to the folder containing the previous version of the IDS, used for "
            "validating breaking changes between versions"
        ),
    )
    args = parser.parse_args()
    ids_dir = Path(args.ids_dir)
    previous_ids_dir = Path(args.previous_ids_dir) if args.previous_ids_dir else None

    result = validate_ids(ids_dir=ids_dir, previous_ids_dir=previous_ids_dir)
    return_code = 0 if result else 1

    sys.exit(return_code)


if __name__ == "__main__":
    main()
