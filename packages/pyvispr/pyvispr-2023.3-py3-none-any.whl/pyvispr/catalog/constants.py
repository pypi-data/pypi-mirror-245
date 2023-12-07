# Copyright CNRS/Inria/UniCA
# Contributor(s): Eric Debreuve (since 2017)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

# NODE_NAME: Node name as it will appear in interface.
# ACTUAL_SOURCE: Where is the node implemented? See node_t.path and node_t.source.
# FUNCTION_NAME: Node function.
# OUTPUT_NAMES: Sequence of names.
# MISSING_IN_INDICATORS: Sequence of booleans indicating the presence of *args and **kwargs arguments.
# MISSING_IN_HINTS: Sequence of arguments with missing type hint.
# MISSING_OUT_HINT_INDICATOR: Boolean indicating the presence of output type hint.
#
# MISSING_IN_OUT_NAME_PREFIX: With integer postfix, replaces *args and **kwargs in argument list.
# HINT_PLACEHOLDER: Replaces missing type hints.
#
NODE_NAME = "_node_name"
ACTUAL_SOURCE = "_actual"
FUNCTION_NAME = "_function_name"
OUTPUT_NAMES = "_outputs"
MISSING_IN_INDICATORS = "_missing_in"
MISSING_IN_HINTS = "_missing_in_hint"
MISSING_OUT_HINT_INDICATOR = "_missing_out_hint"
MISSING_IN_OUT_NAME_PREFIX = "_missing_"
HINT_PLACEHOLDER = "no_hint"
