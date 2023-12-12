# SPDX-FileCopyrightText: 2023 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2023 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import os
import nips
from nips.fft import FileFormatTable


def print_element_format_records(element_format_records):
    print(
        f"|{'Element Name':<13}|{'Group':<6}|Control |{'System':<7}|Restricted |Location |Length |Mode |{'Label':<32}|"
    )
    print("|-------------|------|--------|-------|-----------|---------|-------|-----|--------------------------------|")
    for efr in element_format_records:
        print(
            f"|{efr.element_name:<13}|{str(efr.group):<6}|{str(efr.control):<8}|{str(efr.system):<7}|{str(efr.restricted):<11}|{efr.element_location:>8} |{efr.element_length:>6} |{efr.element_mode_specification:<5}|{efr.element_label:<32}|"
        )


def print_count(data_set):

    print(f"\n## Record Count\n")

    print(f"|Record Type |Count   |")
    print(f"|------------|--------|")

    total = 0

    for t in data_set.record_type_count:
        count = data_set.record_type_count[t]
        total = total + count
        print(f"|{t:<12}|{count:>8}|")

    print(f"|------------|--------|")
    print(f"|TOTAL       |{total:>8}|")

    print(f"\n## Data File Record Count\n")

    print(f"|Set             |Count   |")
    print(f"|----------------|--------|")

    count = len(data_set.fixed_set)
    total = count

    print(f"|{'Fixed Set':<16}|{count:>8}|")

    for ps_id in range(
        0, data_set.fft.data_file_control_record.number_of_periodic_sets
    ):
        count = len(data_set.periodic_sets[ps_id])
        total = total + count
        print(f"|Periodic Set {ps_id+1:>2} |{count:>8}|")

    if len(data_set.orphans) > 0:
        count = len(data_set.orphans)
        print(f"|{'Orphans':<16}|{count:>8}|")
        total = total + count

    print(f"|----------------|--------|")
    print(f"|TOTAL           |{total:>8}|")


def load_fft_only(file):
    fft = FileFormatTable()

    for logical_record in nips.logical_record.read(file):

        match logical_record.type:

            case "B":
                # Classification Record
                fft.feed(logical_record)

            case "C":
                # Data File Control Record
                fft.feed(logical_record)

            case "F":
                # Element Format Record
                fft.feed(logical_record)

            case _:
                # stop reading when other record type is encountered
                break

    return fft


def run(args):

    file_name = os.path.basename(args.nips_file.name)

    data_set = None
    fft = None
    if args.only_layout:
        fft = load_fft_only(args.nips_file)
    else:
        data_set = nips.DataSet(args.nips_file)
        fft = data_set.fft

    print(f"# {file_name}\n")

    print("## Classification Record\n")
    print(f"Classification: {fft.classification_record.classification}")

    print("\n## Data File Control Record\n")
    print(
        f"Number of Periodic Sets: {fft.data_file_control_record.number_of_periodic_sets}"
    )

    print("\n### Fixed Set\n")

    print_element_format_records(fft.element_format_records[0])

    for periodic_set_id in range(
        1, fft.data_file_control_record.number_of_periodic_sets + 1
    ):

        print(f"\n### Periodic Set {periodic_set_id}\n")

        print_element_format_records(fft.element_format_records[periodic_set_id])

    if data_set:
        print_count(data_set)
