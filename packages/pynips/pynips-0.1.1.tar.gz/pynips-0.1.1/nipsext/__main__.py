# SPDX-FileCopyrightText: 2023 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2023 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later


import sys
import argparse

import nips
import nipsext.info
import nipsext.rec
import nipsext.logical
import nipsext.sqlite
import nipsext.repl


# Setup Logging

import logging


def main():

    # Setup Argument parsing
    parser = argparse.ArgumentParser(
        prog="nipsext",
        description="NIPS EXtraction Tool",
        epilog="Danger's over, Banana Breakfast is saved.",
    )

    parser.add_argument(
        "--version", action="version", version=f"PyNIPS {nips.__version__}"
    )

    # Logger level
    parser.add_argument(
        "-d",
        "--debug",
        help="Print debugging statements",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Print verbose information",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )

    subparsers = parser.add_subparsers(title="commands")

    # Parser for the info command
    parser_info = subparsers.add_parser(
        "info", help="Output information about the NIPS file."
    )
    parser_info.add_argument("nips_file", type=argparse.FileType("rb"))
    parser_info.add_argument(
        "--only-layout",
        help="only display layout information (faster)",
        action="store_true",
    )
    parser_info.set_defaults(func=nipsext.info.run)

    # Parser for the rec command
    parser_rec = subparsers.add_parser(
        "rec",
        help="Output records in the recfiles file format. This is a format usable by the GNU Recutils tools.",
    )
    parser_rec.add_argument("nips_file", type=argparse.FileType("rb"))
    parser_rec.add_argument(
        "-i",
        "--set-id",
        help="output records from provided Set ID (0 for Fixed Set)",
        type=int,
    )
    parser_rec.add_argument(
        "-l",
        "--limit",
        help="limit output to LIMIT number of records",
        type=int,
    )
    parser_rec.add_argument(
        "--rcn",
        help="limit output to records that start with provided record control group",
        type=str,
    )
    parser_rec.set_defaults(func=nipsext.rec.run)

    # Parser for the physical command
    parser_logical = subparsers.add_parser(
        "logical",
        help="Read and display logical records in a NIPS data file. Useful for debugging physical format.",
    )
    parser_logical.add_argument("nips_file", type=argparse.FileType("rb"))
    parser_logical.add_argument(
        "-l",
        "--limit",
        help="limit output to LIMIT number of records",
        type=int,
    )
    parser_logical.set_defaults(func=nipsext.logical.run)

    # Parser for the sqlite command
    parser_sqlite = subparsers.add_parser(
        "sqlite", help="Export records from NIPS file to an SQLite database."
    )
    parser_sqlite.add_argument("nips_file", type=argparse.FileType("rb"))
    parser_sqlite.add_argument(
        "--db", help="SQLite3 database", metavar="SQLITE_DATABASE", required=True
    )
    parser_sqlite.set_defaults(func=nipsext.sqlite.run)

    # Parser for the repl command
    parser_info = subparsers.add_parser(
        "repl", help="Load the NIPS file and start an interactive REPL."
    )
    parser_info.add_argument("nips_file", type=argparse.FileType("rb"))
    parser_info.set_defaults(func=nipsext.repl.run)

    # Get arguments and run the appropriate command
    args = parser.parse_args()

    logging.basicConfig(
        format="%(levelname)s - %(name)s: %(message)s", level=args.loglevel
    )

    if "func" in args:
        try:
            args.func(args)
        except Exception as err:
            logging.critical(
                f"Encountered an error. This might mean that the NIPS file is not (yet) parseable by PyNIPS. If you think that PyNIPS should be able to parse the provided file, please consider reporting the error to the PyNIPS issue tracker (https://codeberg.org/ctrlall/pynips/issues). Thanks!\n"
            )
            raise err
    else:
        parser.print_help()


if __name__ == "__main__":
    sys.exit(main())
