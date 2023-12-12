# SPDX-FileCopyrightText: 2023 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2023 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import os

import nips.logical_record
from nips.fft import FileFormatTable
from nips.data_file_record import DataFileRecord


def clean(name):
    """Make element name Recfile friendly"""
    return name.replace("+", "%").replace("(", "_").replace(")", "")


def print_data_file_record(record):
    print(f"KEY: {record.key}")
    print(f"RECORD_CONTROL_GROUP: {record.record_control_group}")
    print(f"SUBSET_CONTROL_GROUP: {record.subset_control_group}")
    print(f"Set_ID: {record.set_id}")
    for element_name in record:
        value = record[element_name]
        print(f"{clean(element_name)}: {value}")
    print("")


def run(args):

    file_name = os.path.basename(args.nips_file.name)
    print("# -*- mode: rec -*-")
    print(f"# {file_name}\n")

    fft = FileFormatTable()

    count = 1

    for logical_record in nips.logical_record.read(args.nips_file):

        if args.limit and args.limit < count:
            break

        record = fft.feed(logical_record)

        if (
            isinstance(record, DataFileRecord)
            and (args.set_id == None or record.set_id == args.set_id)
            and (args.rcn == None or record.record_control_group.startswith(args.rcn))
        ):

            print_data_file_record(record)
            count = count + 1
