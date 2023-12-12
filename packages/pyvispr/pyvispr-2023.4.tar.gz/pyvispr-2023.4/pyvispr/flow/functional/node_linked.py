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

from __future__ import annotations

import dataclasses as dtcl

from pyvispr.flow.functional.link import outbound_links_t
from pyvispr.flow.functional.node_isolated import node_t as base_t
from pyvispr.flow.functional.node_isolated import state_e


@dtcl.dataclass(slots=True, repr=False, eq=False)
class node_t(base_t):
    """
    links[idx]: Outbound links of node of index idx in list "nodes":
        - None if node has no outbound links.
        - If not None, dictionary with:
            - key=name of output and...
            - value=list of alternating target nodes and name of target inputs.
    """

    links: outbound_links_t = dtcl.field(init=False, default_factory=outbound_links_t)

    def AddLink(self, output_name: str, target: node_t, input_name: str, /) -> None:
        """"""
        self.links.Add(
            output_name,
            self.UniqueNameWithPostfix(output_name),
            self.outputs[output_name].value,
            target,
            input_name,
        )

    def RemoveLink(
        self, output_name: str | None, target: node_t | None, input_name: str | None, /
    ) -> None:
        """"""
        self.links.Remove(output_name, target, input_name)

    def OutputIsLinked(self, name: str, /) -> bool:
        """"""
        return name in self.links

    @property
    def needs_running(self) -> bool:
        """
        Note: the decision is based on whether the outputs are valid for use downward in the workflow,
        not on whether the inputs have changed since the last run.
        """
        if self.state is state_e.disabled:
            return False

        if self.description.n_outputs == 0:
            return True

        return any(
            self.OutputIsLinked(_nme) and (not _rcd.has_value)
            for _nme, _rcd in self.outputs.items()
        )
