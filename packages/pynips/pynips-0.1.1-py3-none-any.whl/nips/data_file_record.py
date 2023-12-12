# SPDX-FileCopyrightText: 2023 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2023 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import struct
import dataclasses
from collections.abc import Mapping

import ebcdic

from nips.logical_record import LogicalRecord
from nips.element_format_record import ElementFormatRecord
from nips.data_value_mode import (
    DataValueMode,
    AlphamericMode,
    NumericMode,
    GeographicCoordinateMode,
    DecimalMode,
    SingleByteSystemGeneratedFieldsMode,
)

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Field:
    """A field of a Data File Record holding an Element value.

    Attributes:
        raw (bytes): The physical representation of the field.
        data_value_mode (DataValueMode): The Data Value Mode of the field.
        element_format_record (ElementFormatRecord): The Element Format Record that defines this Element and field.
    """

    def __init__(self, raw, element_format_record):
        self.raw = raw
        self.element_format_record = element_format_record

        match element_format_record.element_mode_specification:
            case "A":
                self.data_value_mode = AlphamericMode

            case "B":
                self.data_value_mode = NumericMode

            case "C":
                raise Exception("GeographicCoordinateMode")
                self.data_value_mode = GeographicCoordinateMode

            case "D":
                self.data_value_mode = DecimalMode

            case _:
                raise Exception("Unknown Data Value Mode")

        if element_format_record.element_name in ["+BSZ", "+PCN"]:
            self.data_value_mode = SingleByteSystemGeneratedFieldsMode

    raw: bytes
    data_value_mode: DataValueMode
    element_format_record: ElementFormatRecord

    def __bytes__(self):
        return self.raw

    def value(self):
        """Returns the decoded value of the field"""
        return self.data_value_mode.value(self.raw)

    def __str__(self):
        return str(self.value())

    def __repr__(self):
        return str(self)


@dataclasses.dataclass
class DataFileRecord(LogicalRecord, Mapping):
    """Data File Record

    Represents a NIPS 360 FFS Data File Record - a record that
    contains user data.

    Attributes
    ----------

    key : str
        Record key.

    record_control_group : str
        Record Control Group.

    subset_control_group : str
        Subset Control Group.

    set_id : int
        The Set ID. For Fixed Set 0 and for Periodic Sets the Periodic Sets the Periodic Set ID.

    fields : dict
        A mapping from element names to fields.
    """

    key: str
    record_control_group: str
    subset_control_group: str
    set_id: int
    fields: dict

    def __init__(
        self, logical_record, data_file_control_record, element_format_records
    ):

        super(DataFileRecord, self).__init__(
            logical_record.offset,
            logical_record.length,
            logical_record.os_control,
            logical_record.delete_code,
            logical_record.type,
            logical_record.raw,
        )

        # Note the Record Control Group and Set ID position and lenght
        # is specified in multiple places:
        #
        #   1. In the Data File Control Record
        #   2. In the system generated field +RCN and +PCN
        #
        # We use what is specified in the Data File Control Record.
        #
        # TODO: check that +RCN and +PCN fields correspond with Data
        # File Control Record

        # Record Control Group
        offset = data_file_control_record.record_control_group_position
        self.record_control_group = self.raw[
            offset : offset + data_file_control_record.record_control_group_length
        ].decode("cp037")

        # Set Id
        offset = data_file_control_record.set_id_position
        (self.set_id,) = struct.unpack(">B", self.raw[offset : offset + 1])

        # Make sure Set ID length is really 1 byte
        assert data_file_control_record.set_id_length == 1

        # Subset Control Group
        offset = data_file_control_record.subset_control_group_position
        self.subset_control_group = (
            self.raw[
                offset : offset + data_file_control_record.subset_control_group_length
            ]
            .rstrip(b"\x00")
            .decode("cp037")
        )

        # Record key
        self.key = (
            self.type
            + self.record_control_group
            + str(self.set_id)
            + self.subset_control_group
        )

        # Read the Fields

        self.fields = {}

        if self.set_id > len(element_format_records):
            logger.warning(
                f"Record at offset {self.offset} has set id {self.set_id} but we do not  have any Element Format Records for that set. Ignoring record."
            )
            return

        for element_format_record in element_format_records[self.set_id]:

            element_name = element_format_record.element_name

            # Get the raw field
            location = element_format_record.element_location

            length = element_format_record.element_length

            # "For numeric mode elements (B), a binary word (4 bytes)
            # will appear in the logical record regardless of the
            # length specified."
            # --- Section A.3.3 of User's Manual Volume 1 (Page 85,
            #     description of field 11)
            if element_format_record.element_mode_specification == "B":
                length = 4

            raw = self.raw[location : location + length]

            field = Field(raw, element_format_record)

            self.fields[element_name] = field

    # Implement the Mapping class methods

    def __iter__(self):
        yield from self.fields.keys()

    def __getitem__(self, name):
        return self.fields[name]

    def __len__(self):
        return len(self.fields)
