# SPDX-FileCopyrightText: 2023 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2023 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import os

import nips.logical_record
from nips.fft import DataFileControlRecord, FileFormatTable
from nips.data_file_record import DataFileRecord

import progressbar


class DataSet:
    """NIPS Data Set

    A Python representation of a NIPS Data Set with all data loaded into memory.

    This class is useful for loading an entire NIPS Data Set for
    interactive or programmatic inspection.

    Note that the entire data set is loaded into memory. To process
    records without loading them all into memory use
    :meth:`nips.logical_record.read` and the
    :class:`nips.fft.FileFormatTable` class.

    Parameters
    ----------
    nips_file : file-like object
        File from where data is loaded.

    Attributes
    ----------
    fft : FileFormatTable
        File Format Table of the data set.
    fixed_set : list(DataFileRecord))
        Fixed Set.
    periodic_sets : list(list(DataFileRecord)))
        Periodic Sets. Note that the list is 0-indexed. So the
        Periodic Set 1 is at periodic_sets[0].
    orphans : list(DataFileRecord)
        Data file records that could not be assigned to a set. Maybe an invalid set id?
    record_type_count : dict
        A dictionary from record type code to count of records in NIPS file.
    """

    def __init__(self, nips_file):

        self.fft = FileFormatTable()

        self.fixed_set = []
        self.periodic_sets = None
        self.record_type_count = {}

        self.orphans = []

        # Attempt to get size of input
        nips_file_size = None
        if nips_file.seekable():
            nips_file.seek(0, os.SEEK_END)
            nips_file_size = nips_file.tell()
            nips_file.seek(0)

        widgets = [
            "Loading NIPS file",
            progressbar.Percentage(),
            progressbar.Bar(),
            progressbar.Variable(
                "record_count", format=" records: {formatted_value}, "
            ),
            progressbar.AdaptiveETA(),
        ]

        with progressbar.ProgressBar(max_value=nips_file_size, widgets=widgets) as bar:

            record_count = 0

            for logical_record in nips.logical_record.read(nips_file):

                if logical_record.type in self.record_type_count:
                    self.record_type_count[logical_record.type] = (
                        self.record_type_count[logical_record.type] + 1
                    )
                else:
                    self.record_type_count[logical_record.type] = 1

                record_count = record_count + 1

                record = self.fft.feed(logical_record)

                bar.update(record.offset, record_count=record_count)

                if isinstance(record, DataFileControlRecord):
                    # initialize the sets to hold records
                    self.periodic_sets = [
                        [] for _ in range(0, record.number_of_periodic_sets)
                    ]

                elif isinstance(record, DataFileRecord):

                    if record.set_id == 0:
                        self.fixed_set.append(record)
                    elif record.set_id <= len(self.periodic_sets):
                        self.periodic_sets[record.set_id - 1].append(record)
                    else:
                        self.orphans.append(record)
