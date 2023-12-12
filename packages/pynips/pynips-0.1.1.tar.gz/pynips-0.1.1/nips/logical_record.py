# SPDX-FileCopyrightText: 2023 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2023 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Data Set

NIPS 360 FFS data is stored as a data set which is a collection of
*logical records*.

This module provides functionality for reading logical records from a
binary stream. In particular it can read logical records from a file.
"""


import dataclasses
import os
import struct
import ebcdic  # for decoding the type code

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

MAX_LOGICAL_RECORD_LENGTH = 1000
MAX_PHYSICAL_RECORD_LENGTH = 1004


@dataclasses.dataclass
class LogicalRecord:
    """Logical Record

    Data stored in NIPS 360 FFS data files are stored in variable
    length *logical records*. This class is a Python representation of
    logical records.

    See also Appendix A.1 of the NIPS 360 FFS User's Manual Volume 1 -
    Introduction to File Concepts.

    Attributes
    ----------
    offset : int
        Position of record in input file/stream. This is useful for
        debugging and finding the location of records in the original
        file.

    length : int
        Length of record.

    os_control : bytes
        Two bytes reserved for OS usage (OS Control bytes).

    delete_code : bytes
        Deletion Code Field (one byte).

    type : chr
        Type of the record in ASCII (decoded from EBCDIC).

    raw : bytes
        Binary representation of the entire record.
    """

    offset: int
    length: int
    os_control: bytes
    delete_code: bytes
    type: chr
    raw: bytes = dataclasses.field(repr=False)


def __read_logical_record(io, max_bytes=False, ascii_record_length=False):

    remaining_bytes = max_bytes

    while (not max_bytes) or remaining_bytes > 0:
        # remember the offset in the input (useful for debugging)
        if io.seekable():
            offset = io.tell()
        else:
            offset = None

        raw_header = io.read(6)

        # break on end-of-input
        if len(raw_header) < 6:
            return

        logger.debug(f"Reading logical record at offset {offset}.")

        if ascii_record_length:
            length_b, delete_code, type_code = struct.unpack(">4scc", raw_header)
            length_s = length_b.decode("ascii")

            if length_s.isdecimal():
                length = int(length_s)
                os_control = False
            else:
                return
        else:
            length, os_control, delete_code, type_code = struct.unpack(
                ">HHcc", raw_header
            )

        if length > MAX_LOGICAL_RECORD_LENGTH:
            logger.warning(
                f"Logical record at offset {offset} seems to have length {length}. This is more than the allowed maximum length {MAX_LOGICAL_RECORD_LENGTH}. Aborting."
            )
            return

        # decode the type code to ASCII from EBCDIC
        type_code = type_code.decode("cp037")[0]

        # read the remaining data
        remainder = io.read(length - 6)

        # concat the header and the remainder for the raw record
        raw = raw_header + remainder

        yield LogicalRecord(offset, length, os_control, delete_code, type_code, raw)

        if max_bytes:
            remaining_bytes = remaining_bytes - length


def read(io, fixed_physical_record_length=None, ascii_record_length=False):
    """Read logical records from a binary stream or file.

    This function reads all logical records from all physical records
    in the provided input.

    Logical records are blocked into *physical records* (also known as
    blocks) that contain multiple logical records. The length of
    physical records is encoded in the first four bytes of the
    physical record.

    In some cases the first four bytes indicating the length of the
    physical record is not present, instead blocks have a fixed
    size. This can be set with `fixed_physical_record_length`.

    In some cases the logical record lenght is encoded as ASCII
    digits. The argument `ascii_record_length` can be set to read
    logical record lenght as ASCII digits.

    The function will check if the first four characters are valid
    ASCII digits. If this is the case, `ascii_record_length` will be
    automatically set to `True` and `fixed_physical_record_length` to
    `1004`.

    Parameters
    ----------
    io : io.RawIOBase
        File from where to read Logical Records. Must be seekable.

    fixed_physical_record_length: None | int
        If specified

    ascii_record_length: bool

    Yields
    ------
    LogicalRecord
        Logical records contained in the input stream.
    """

    # Attempt to get the initial block_count_h

    # read the Block Count field (4 bytes)
    block_count_b = io.read(4)
    # and rewind selectah
    io.seek(-4, os.SEEK_CUR)

    # break on end-of-input
    if len(block_count_b) < 4:
        return

    try:
        # Check if first four characters are an ACII numeric
        (first_four_b,) = struct.unpack(">4s", block_count_b)
        first_four_s = first_four_b.decode("ascii")

        if first_four_s.isdecimal():
            fixed_physical_record_length = 1004
            ascii_record_length = True
            logger.info(
                f"First four characters in data file are ASCII numbers. Attempting to read logical record length as ASCII and fixing block size to 1004."
            )
    except UnicodeDecodeError:
        pass  # when first four characters can not be decoded as ASCII

    # Get size of the input
    io.seek(0, os.SEEK_END)
    file_size = io.tell()
    io.seek(0)

    # loop over blocks
    while True:

        block_start = io.tell()

        if fixed_physical_record_length:
            block_length = fixed_physical_record_length
        else:
            # read the Block Count field (4 bytes)
            block_length_b = io.read(4)

            # break on end-of-input
            if len(block_length_b) < 4:
                break

            # unpack the Block Count
            block_length, _, _ = struct.unpack(">Hcc", block_length_b)

        if block_length > MAX_PHYSICAL_RECORD_LENGTH:
            logger.warning(
                f"Physical record at offset {block_start} seems to have length {block_length}. This is more than the allowed maximum length {MAX_PHYSICAL_RECORD_LENGTH}. Aborting."
            )
            return

        logger.debug(
            f"Reading physical record at offset {block_start} with size {block_length}."
        )

        # substract 4 bytes for block count header and read the logical records
        yield from __read_logical_record(
            io, max_bytes=block_length - 4, ascii_record_length=ascii_record_length
        )

        expected_block_end = block_start + block_length

        if file_size < expected_block_end:
            return
        else:
            io.seek(expected_block_end)
