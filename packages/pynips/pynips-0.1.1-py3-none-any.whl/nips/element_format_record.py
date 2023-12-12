# SPDX-FileCopyrightText: 2023 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2023 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import struct
import dataclasses

import ebcdic


from nips.logical_record import LogicalRecord

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


@dataclasses.dataclass
class FieldStructure:
    name: str
    location: int
    length: int
    character_set_specification: str


@dataclasses.dataclass
class ElementFormatRecord(LogicalRecord):
    """Element Format Record

    Attributes
    ----------
    element_name : str
        Element name.

    element_set_identification : int
        Element set identification that is set to 0 for the Fixed Set
        and the Periodic Set identifier for Periodic Sets.

    element_type_identification : int
        Element type identification byte. This contains various flags
        that are decoded to attributes such as `group`.

    group : bool
        True if the element format record defines a group. Decoded
        from the element type identification byte.

    control : bool
        True if field or group is used for record or subset
        control. Decoded from the element type identification byte.

    system : bool
        True if element format record defines a system-generated
        field/group. Decoded from the element type identification
        byte.

    restricted : bool
        Field/group may not be used by the analyst. Decoded from the
        element type identifcation byte.

    fixed_length_field : bool
        True if element format record defines a fixed length
        field. Decoded from the element type identification byte.

    variable_length_field : bool
        True if element format record defines a variable length
        field. Decoded from the element type identiication byte.

    variable_set_field : bool
        True if element format record defines a variable set
        field. Decoded from the element type identification byte.

    element_location : int
        Location of Element in Data File Record.

    element_length : int
        Length of Element.

    element_mode_specification : str
        Data Value Mode specification.

    input_subroutine_conversion_name : str
    
    output_subroutine_conversion_name : str

    element_label_location : int

    element_label_length : int

    element_label : str

    edit_mask_location : int

    edit_mask_length : int

    size_on_output : int

    field_names_location : int

    number_of_fields_making_up_the_group : int

    field_structure: list[FieldStructure]
    """

    element_name: str
    element_set_identification: int
    element_type_identification: int

    group: bool
    control: bool
    system: bool
    restricted: bool
    fixed_length_field: bool
    variable_length_field: bool
    variable_set_field: bool

    element_location: int
    element_length: int
    element_mode_specification: str
    input_subroutine_conversion_name: str
    output_subroutine_conversion_name: str
    element_label_location: int
    element_label_length: int
    element_label: str
    edit_mask_location: int
    edit_mask_length: int
    size_on_output: int
    field_names_location: int
    number_of_fields_making_up_the_group: int
    field_structure: list[FieldStructure]

    def __init__(self, logical_record, data_file_control_record):

        super(ElementFormatRecord, self).__init__(
            logical_record.offset,
            logical_record.length,
            logical_record.os_control,
            logical_record.delete_code,
            logical_record.type,
            logical_record.raw,
        )

        # ignore the header
        offset = 6

        # Element Name

        self.element_name = (
            self.raw[
                offset : offset + data_file_control_record.record_control_group_length
            ]
            .rstrip(b"\x00")  # strip padding
            .decode("cp037")  # decode EBCDIC
            # For unknown reasons the element names seem to be padded to 7
            # characters with whitespace (in addition to the nulls that
            # are stripped above). We strip them here.
            .rstrip()
        )

        # Handle system generated element names that are prefixed with NULL
        if self.element_name[0] == "\x00":
            self.element_name = "+" + self.element_name[1:]

        # Handle +SC element names
        if self.element_name.startswith("+SC") and len(self.element_name) > 3:
            id = ord(self.element_name[3])
            self.element_name = "+SC(" + str(id) + ")"

        offset = offset + data_file_control_record.record_control_group_length

        # Boundary Allignment Byte

        # TODO: this seems to be more than a byte. Figure out why.

        # Expected to be all zeroes
        if not all(
            [
                b == 0
                for b in self.raw[
                    offset : data_file_control_record.element_format_record_significant_data_position
                ]
            ]
        ):
            boundary_allignment_bytes = self.raw[
                offset : data_file_control_record.element_format_record_significant_data_position
            ]
            logger.warning(
                f"Boundary allignment bytes are not all zeroes: {boundary_allignment_bytes}"
            )

        offset = (
            data_file_control_record.element_format_record_significant_data_position
        )

        # Dummy Parameter

        # Four bytes of zeroes in non-coninuation records.
        assert all([b == 0 for b in self.raw[offset : offset + 4]])

        offset = offset + 4

        # Element Set Identification and Element Type Identification
        fields_length = 1 + 1
        (
            self.element_set_identification,
            self.element_type_identification,
        ) = struct.unpack(">BB", self.raw[offset : offset + fields_length])

        # Extract field sfrom the Element Set Identification bytes
        self.group = 0 == 0b10000000 & self.element_type_identification
        self.control = 0 < 0b01000000 & self.element_type_identification
        self.system = 0 < 0b00100000 & self.element_type_identification
        self.restricted = 0 < 0b00010000 & self.element_type_identification
        self.fixed_length_field = 0 < 0b00001000 & self.element_type_identification
        self.variable_length_field = 0 < 0b00000100 & self.element_type_identification
        self.variable_set_field = 0 < 0b00000010 & self.element_type_identification

        # The final bit should always be 0
        assert 0 == 0b00000001 & self.element_type_identification

        # shift offset
        offset = offset + fields_length

        # Element Location
        self.element_location = int(self.raw[offset : offset + 4].decode("cp037"))
        offset = offset + 4

        # Element Length
        self.element_length = int(self.raw[offset : offset + 3].decode("cp037"))
        offset = offset + 3

        # Element Mode Specification
        self.element_mode_specification = self.raw[offset : offset + 1].decode("cp037")
        offset = offset + 1

        # Input Subroutine Conversion Name
        self.input_subroutine_conversion_name = (
            self.raw[offset : offset + 8].rstrip(b"\x00").decode("cp037")
        )
        offset = offset + 8

        # Output Subroutine Conversion Name
        self.output_subroutine_conversion_name = (
            self.raw[offset : offset + 8].rstrip(b"\x00").decode("cp037")
        )
        offset = offset + 8

        # Element Label
        fields_length = 2 + 2
        (self.element_label_location, self.element_label_length) = struct.unpack(
            ">HH", self.raw[offset : offset + fields_length]
        )
        offset = offset + fields_length

        # Edit Mask
        fields_length = 2 + 2
        (self.edit_mask_location, self.edit_mask_length) = struct.unpack(
            ">HH", self.raw[offset : offset + fields_length]
        )
        offset = offset + fields_length

        # Size of Element on Output, Location of the String of Field
        # Names in the Record Making up the Group (wtf is this?) and
        # Number of Fields Making up the Group
        fields_length = 2 + 2 + 2
        (
            self.size_on_output,
            self.field_names_location,
            self.number_of_fields_making_up_the_group,
        ) = struct.unpack(">HHH", self.raw[offset : offset + fields_length])
        offset = offset + fields_length

        self.field_structure = []
        if self.field_names_location:

            # check that we haven't missed anything
            assert offset == self.field_names_location

            # Read the Field specifications
            for i in range(0, self.number_of_fields_making_up_the_group):

                field_name = (
                    self.raw[offset : offset + 8]
                    .rstrip(b"\x00")
                    .decode("cp037")
                    .rstrip()
                )
                offset = offset + 8

                location = self.raw[offset : offset + 4].decode("cp037")
                offset = offset + 4

                lenght = self.raw[offset : offset + 3].decode("cp037")
                offset = offset + 3

                character_set_specification = self.raw[offset : offset + 1].decode(
                    "cp037"
                )
                offset = offset + 1

                self.field_structure.append(
                    FieldStructure(
                        field_name, location, lenght, character_set_specification
                    )
                )

        self.element_label = ""
        if self.element_label_location:
            assert offset == self.element_label_location
            self.element_label = (
                self.raw[offset : offset + self.element_label_length]
                .rstrip(b"\x00")
                .decode("cp037")
            )
            offset = offset + self.element_label_length

        remaining_bytes = self.length - offset

        # Records are aligned to word size, output warning if there are more unread bytes
        if remaining_bytes >= 4:
            unread_b = self.raw[offset:]
            logger.warning(
                f"Element Format Record at offset {self.offset} has {self.length - offset} unread bytes at end. record length: {self.length} offset in record: {offset}, unread bytes: {unread_b}."
            )
