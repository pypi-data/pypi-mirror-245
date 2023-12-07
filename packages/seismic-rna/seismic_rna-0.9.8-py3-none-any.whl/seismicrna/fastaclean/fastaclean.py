"""

FASTA Cleaner Module

"""

import re
from functools import cached_property
from logging import getLogger
from pathlib import Path

from ..core.seq import (BASEN,
                        BASET,
                        BASEU,
                        DNA,
                        RNA,
                        XNA,
                        extract_fasta_seqname,
                        format_fasta_name_line)
from ..core.write import need_write, write_mode

logger = getLogger(__name__)


def get_non_seq_regex(seq_type: type[XNA]):
    return re.compile("[" + "".join(seq_type.get_other_iupac()) + "]")


class FastaCleaner(object):

    def __init__(self, seq_type: type[XNA]):
        self._seq_type = seq_type

    @cached_property
    def _non_seq_regex(self):
        return get_non_seq_regex(self._seq_type)

    def _clean_initial(self, line: str):
        # Remove whitespace characters.
        line = "".join(line.split())
        # Convert to uppercase.
        line = line.upper()
        # Correct the type of the sequence.
        if self._seq_type is DNA:
            return line.replace(BASEU, BASET)
        if self._seq_type is RNA:
            return line.replace(BASET, BASEU)
        raise TypeError(f"Invalid sequence type: {self._seq_type.__name__}")

    def _clean_fasta_seq_line(self, line: str):
        cleaned = self._non_seq_regex.sub(BASEN, self._clean_initial(line))
        try:
            return f"{str(self._seq_type(cleaned))}\n"
        except ValueError:
            raise ValueError("Line contains sequence characters other than "
                             f"whitespace or IUPAC codes:\n{repr(line)}")

    def _clean_fasta_line(self, line: str):
        return (format_fasta_name_line(name)
                if (name := extract_fasta_seqname(line))
                else self._clean_fasta_seq_line(line))

    def run(self, ifasta: Path, ofasta: Path, force: bool = False):
        if ofasta.is_file() and ofasta.samefile(ifasta):
            raise FileExistsError(f"The output FASTA {ofasta} and the input "
                                  f"FASTA {ifasta} are the same file")
        if need_write(ofasta, force):
            with open(ifasta) as fi, open(ofasta, write_mode(force)) as fo:
                for line in fi:
                    fo.write(self._clean_fasta_line(line))

########################################################################
#                                                                      #
# Copyright ©2023, the Rouskin Lab.                                    #
#                                                                      #
# This file is part of SEISMIC-RNA.                                    #
#                                                                      #
# SEISMIC-RNA is free software; you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation; either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# SEISMIC-RNA is distributed in the hope that it will be useful, but   #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANT- #
# ABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General     #
# Public License for more details.                                     #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with SEISMIC-RNA; if not, see <https://www.gnu.org/licenses>.  #
#                                                                      #
########################################################################
