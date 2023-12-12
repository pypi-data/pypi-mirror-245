# SPDX-FileCopyrightText: 2023 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2023 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import nips.logical_record


def run(args):
    count = 0
    for logical_record in nips.logical_record.read(args.nips_file):
        count = count + 1
        if args.limit and args.limit < count:
            break
        print(logical_record)
