# SPDX-FileCopyrightText: 2023 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2023 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later


"""Data Value Modes

Implements functionality for decoding the NIPS Data Value Modes:

- Numeric Mode
- Alphanumeric Mode
- Geographic Coordinate Mode (TODO)

See also section 2.3 of the NIPS 360 FFS User's Manual Volume 1 -
Introduction to File Concepts.
"""

import struct
import ebcdic


class DataValueMode:
    def value(raw):
        return raw


class AlphamericMode(DataValueMode):
    def value(raw):
        # Strip trailing blanks and decode form EBCDIC
        return raw.rstrip(b"\x00").decode("cp037")


class NumericMode(DataValueMode):
    def value(raw):
        (value,) = struct.unpack(">L", raw)
        return value


class GeographicCoordinateMode(DataValueMode):
    # TODO
    pass


class DecimalMode(DataValueMode):
    def value(raw):
        # Strip trailing blanks and decode form EBCDIC
        return raw.rstrip(b"\x00").decode("cp037")


class SingleByteSystemGeneratedFieldsMode(DataValueMode):
    """A special data value mode for reading the +BSZ and +PCN fields.

    System-generated elements +BSZ, +PCN and +SC(*) are defined using
    regular element format records with the mode code 'A'
    (alphanumeric). However they are stored as a binary integer in a
    single byte.

    Instead of implementing special logic to handle these
    system-generated fields we define a special data value. This data
    value mode is not defined by NIPS and is an implementation detail
    of this library.
    """

    def value(raw):
        return ord(raw)
