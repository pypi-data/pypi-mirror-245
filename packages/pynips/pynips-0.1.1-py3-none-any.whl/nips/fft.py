# SPDX-FileCopyrightText: 2023 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2023 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""File Format Table

The *File Format Table* Describes the format of a NIPS data set. This
module provides Python structures to represent the FFT and the format
of a NIPS data set."""

import struct
import dataclasses

import ebcdic

from nips.logical_record import LogicalRecord
from nips.element_format_record import ElementFormatRecord
from nips.data_file_record import DataFileRecord

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


@dataclasses.dataclass
class ClassificationRecord(LogicalRecord):
    """NIPS 360 FFS Classification Record

    Carries user-defined classification label"""

    classification: str

    def __init__(self, logical_record):
        super(ClassificationRecord, self).__init__(
            logical_record.offset,
            logical_record.length,
            logical_record.os_control,
            logical_record.delete_code,
            logical_record.type,
            logical_record.raw,
        )

        self.classification = logical_record.raw[6 : (32 + 6)].decode("cp037").rstrip()


@dataclasses.dataclass
class UserDataFileRecordStructure:
    length: int
    binary_words: int
    binary_block_position: int


def ensure_end_of_record_reached(record, offset):
    record_length = len(record.raw)
    if record_length > offset:
        unread_bytes = record.raw[offset:]
        # TODO: investigate
        # logging.warning(
        #     f"End of record not reached while reading {record}, offset is {offset} while record length is {record_length}. The unread bytes are: {unread_bytes}. Good luck figuring out what that's all about."
        # )


@dataclasses.dataclass
class DataFileControlRecord(LogicalRecord):
    """Data File Control Record

    Holds necessary information on the organization and format of the
    element format records.

    Attributes:
        record_control_group_position (int):
        record_control_group_length (int):
        set_id_position (int):
        set_id_length (int):
        subset_control_group_position (int):
        subset_control_group_length (int):
        number_of_periodic_sets (int):
        element_format_record_significant_data_position (int):
        fixed_set_structure (UserDataFileRecordStructure):
        periodic_set_structure (list[UserDataFileRecordStructure]):
    """

    record_control_group_position: int
    record_control_group_length: int
    set_id_position: int
    set_id_length: int
    subset_control_group_position: int
    subset_control_group_length: int
    number_of_periodic_sets: int
    element_format_record_significant_data_position: int
    fixed_set_structure: UserDataFileRecordStructure
    periodic_set_structure: list[UserDataFileRecordStructure]

    def __init__(self, logical_record):
        super(DataFileControlRecord, self).__init__(
            logical_record.offset,
            logical_record.length,
            logical_record.os_control,
            logical_record.delete_code,
            logical_record.type,
            logical_record.raw,
        )

        # ignore the header
        offset = 6

        # Control Record Key Padding (254 bytes of binary zeroes)
        _ = logical_record.raw[offset : offset + 254]

        offset = offset + 254

        # total length of 8 fields
        fields_length = 7 * 2 + 1

        (
            self.record_control_group_position,
            self.record_control_group_length,
            self.set_id_position,
            self.set_id_length,
            self.subset_control_group_position,
            self.subset_control_group_length,
            self.number_of_periodic_sets,
            self.element_format_record_significant_data_position,
        ) = struct.unpack(
            ">HHHHHHHB", logical_record.raw[offset : offset + fields_length]
        )

        # shift offset
        offset = offset + fields_length

        # Dummy entry
        _ = logical_record.raw[offset : offset + 3]

        # shift offset
        offset = offset + 3

        # Read structure information about Fixed Set Logical Record
        structure_fields_length = 1 + 1 + 2
        (
            fixed_set_logical_record_length,
            fixed_set_logical_record_binary_words,
            fixed_set_logical_record_binary_block_position,
        ) = struct.unpack(
            ">BBH", logical_record.raw[offset : offset + structure_fields_length]
        )

        self.fixed_set_structure = UserDataFileRecordStructure(
            fixed_set_logical_record_length,
            fixed_set_logical_record_binary_words,
            fixed_set_logical_record_binary_block_position,
        )

        offset = offset + structure_fields_length

        # Read structure information about Peridoc Sets
        self.periodic_set_structure = []

        for i in range(0, self.number_of_periodic_sets):
            (length, binary_words, binary_block_position) = struct.unpack(
                ">BBH", logical_record.raw[offset : offset + structure_fields_length]
            )

            self.periodic_set_structure.append(
                UserDataFileRecordStructure(length, binary_words, binary_block_position)
            )

            offset = offset + structure_fields_length

        # make sure we read everything or warn
        ensure_end_of_record_reached(self, offset)


class FileFormatTable:
    """NIPS File Format Table

    The File Format Table holds the description of the format of the data set.

    Attributes
    ----------

    classification_record : ClassificationRecord)
        Classification Record.

    data_file_control_record : DataFileControlRecord
        Data File Control Record.

    element_format_records : list(list(ElementFormatRecords)))
        Holds the Element Format Records for the Fixed Set and any Periodic Sets.
    """

    def __init__(self):

        self.classification_record = None
        self.data_file_control_record = None
        self.element_format_records = None

        self.fed_data_file_record = False

    def feed(self, logical_record):
        """Feed a logical record to the File Format Table.

        If the logical record is a classification record, data file
        control record or element format record the file format table
        will be updated accordingly and this function will return the
        record (as `ClassificationRecord`, `DataFileControlRecord` or
        `ElementFormatRecord`).

        If the logical record is a data file record it will be parsed
        and returned as a DataFileRecord.

        If the logical record is of another type it will be returned as is.
        """

        match logical_record.type:
            case "B":
                self.classification_record = ClassificationRecord(logical_record)

                logger.debug(self.classification_record)

                return self.classification_record

            case "C":

                # TODO better errors
                if self.data_file_control_record:
                    logger.warning(
                        f"Duplicate Data File Record encountered at offset {logical_record.offset}. Ignoring it."
                    )

                    return logical_record

                else:
                    self.data_file_control_record = DataFileControlRecord(
                        logical_record
                    )

                    logger.debug(self.data_file_control_record)

                    # initialize correct number of lists to collect
                    # the element format records
                    self.element_format_records = [
                        []
                        for _ in range(
                            0, self.data_file_control_record.number_of_periodic_sets + 1
                        )
                    ]

                    return self.data_file_control_record

            case "F":

                if not self.data_file_control_record:
                    raise Exception(
                        "We don't know what to do with the Element Format Record as we have not yet received a Data File Record."
                    )

                if self.fed_data_file_record:
                    logger.warn(
                        "Fed a Element Format Record after already having being fed a data file record. Ignoring Element Format Record."
                    )
                    return logical_record

                element_format_record = ElementFormatRecord(
                    logical_record, self.data_file_control_record
                )

                logger.debug(element_format_record)

                # Add to element format records of the Fixed Set or Periodic Set
                set_id = element_format_record.element_set_identification
                self.element_format_records[set_id].append(element_format_record)

                # Sort the element format records according to offset
                self.element_format_records[set_id].sort(
                    key=lambda efr: efr.element_location
                )

                return element_format_record

            case "R":
                user_data_file_record = DataFileRecord(
                    logical_record,
                    self.data_file_control_record,
                    self.element_format_records,
                )

                logger.debug(user_data_file_record)

                # remember that we have received a data file record
                self.fed_data_file_record = True

                return user_data_file_record

            case _:
                logger.debug(logical_record)
                return logical_record
