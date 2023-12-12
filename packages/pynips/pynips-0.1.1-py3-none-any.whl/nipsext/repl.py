# SPDX-FileCopyrightText: 2023 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2023 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import code
import readline
import rlcompleter

import nips

def run(args):

    data_set = nips.DataSet(args.nips_file)

    vars = {"data_set": data_set}

    readline.set_completer(rlcompleter.Completer(vars).complete)
    readline.parse_and_bind("tab: complete")
    code.InteractiveConsole(vars).interact(
        banner="""Starting the NIPSEXT REPL.
NIPS data set has been loaded to the variable "data_set". Type "help(data_set)" for more information.""",
        exitmsg="Bye.",
    )
