# SPDX-FileCopyrightText: 2023 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2023 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import nips.logical_record
from nips.fft import FileFormatTable
from nips.data_file_record import DataFileRecord

import os
import sqlite3
import progressbar

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def table_name_for_id(set_id):
    if set_id == 0:
        return "FixedSet"
    else:
        return f"PeriodicSet{set_id}"


def create_schema(fft, con):

    for i in range(0, fft.data_file_control_record.number_of_periodic_sets + 1):

        table_name = table_name_for_id(i)

        statement = f"CREATE TABLE IF NOT EXISTS {table_name} ( KEY TEXT PRIMARY KEY, RECORD_CONTROL_GROUP TEXT, SUBSET_CONTROL_GROUP TEXT "

        for efr in fft.element_format_records[i]:
            statement = statement + f', "{efr.element_name}" TEXT'

        statement = statement + ");"

        logger.debug(f'Creating SQL table with statement "{statement}"')

        con.execute(statement)


def insert_data_file_record(record, con):

    table_name = table_name_for_id(record.set_id)

    values = [record.key, record.record_control_group, record.subset_control_group] + [
        str(v) for v in record.values()
    ]

    placeholders = ",".join(["?" for _ in values])

    statement = f"INSERT INTO {table_name} VALUES({placeholders})"

    logger.debug(
        f'Inserting record {record.record_control_group} with SQL statement "{statement}" and values {values}.'
    )

    try:
        con.execute(statement, values)
    except Exception as e:
        logger.error(f"Error while inserting record: {record}")
        raise e


def run(args):

    # Open Connection to SQLite3 database
    con = sqlite3.connect(args.db)

    # Schema is created on first data file record, remember that it is
    # not yet created.
    schema_created = False

    # Init FFT
    fft = FileFormatTable()

    # Attempt to get size of input
    args.nips_file.seek(0, os.SEEK_END)
    nips_file_size = args.nips_file.tell()
    args.nips_file.seek(0)

    widgets = [
        f"Writing records to SQLite database {args.db}",
        progressbar.Percentage(),
        progressbar.Bar(),
        progressbar.Variable("record_count", format=" records: {formatted_value}, "),
        progressbar.AdaptiveETA(),
    ]

    with progressbar.ProgressBar(max_value=nips_file_size, widgets=widgets) as bar:

        record_count = 0

        for logical_record in nips.logical_record.read(args.nips_file):

            record = fft.feed(logical_record)

            record_count = record_count + 1
            bar.update(record.offset, record_count=record_count)

            try:
                if isinstance(record, DataFileRecord):

                    # Create the tables if not already created
                    if not schema_created:
                        create_schema(fft, con)
                        schema_created = True

                    insert_data_file_record(record, con)
            except Exception as e:
                # commit any pending inserts
                con.commit()
                raise e

            # Commit to SQL database every 250 records
            if record_count % 250 == 0:
                con.commit()
