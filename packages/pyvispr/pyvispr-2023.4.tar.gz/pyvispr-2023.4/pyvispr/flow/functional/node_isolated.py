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
import typing as h
from enum import Enum as enum_t

from pyvispr.flow.descriptive.node import node_t as description_t
from pyvispr.flow.functional.socket import input_t, output_t
from pyvispr.flow.messenger import MESSENGER


class state_e(enum_t):
    disabled = 1
    todo = 2
    running = 3
    done = 4


@dtcl.dataclass(slots=True, repr=False, eq=False)
class node_t:
    """
    The description is shared among all the functional nodes.

    links[idx]: Outbound links of node of index idx in list "nodes":
        - None if node has no outbound links.
        - If not None, dictionary with:
            - key=name of output and...
            - value=list of alternating target nodes and name of target inputs.
    """

    description: description_t
    inputs: dict[str, input_t]
    outputs: dict[str, output_t]
    unique_name: str | None = None
    state: state_e = state_e.todo

    @classmethod
    def NewForDescription(cls, description: description_t, /) -> node_t:
        """"""
        description.Activate()

        inputs = {_nme: input_t() for _nme in description.input_names}
        outputs = {_nme: output_t() for _nme in description.output_names}

        return cls(
            description=description,
            inputs=inputs,
            outputs=outputs,
        )

    def UniqueNameWithPostfix(self, postfix: str, /) -> str:
        """"""
        return self.unique_name + "_" + postfix

    def InvalidateInputValue(self, /, *, name: str | None = None) -> None:
        """"""
        if self.state is state_e.disabled:
            return

        if name is None:
            for input_ in self.inputs.values():
                input_.Invalidate()
        else:
            self.inputs[name].Invalidate()
        self.state = state_e.todo
        MESSENGER.TransmitMessage(state_e.todo, (self,))

    def InvalidateOutputValues(self) -> None:
        """"""
        if self.state is state_e.disabled:
            return

        for output in self.outputs.values():
            output.Invalidate()
        self.state = state_e.todo
        MESSENGER.TransmitMessage(state_e.todo, (self,))
        MESSENGER.TransmitMessage("output unset", (self,))

    def ToggleAbility(self) -> None:
        """"""
        if self.state is state_e.disabled:
            self.state = state_e.todo
            MESSENGER.TransmitMessage(state_e.todo, (self,))
        else:
            self.state = state_e.disabled
            MESSENGER.TransmitMessage(state_e.disabled, (self,))

    @property
    def can_run(self) -> bool:
        """
        It must have been checked that the state is not disabled.

        This method is meant to be called from functional.graph.Run,
        i.e., after visual.Run has read the ii_values
        to set the corresponding node input values if appropriate.
        Appropriate means: the corresponding inputs have mode "full" (actually,
        not "link") and they are not linked to outputs.
        """
        return (self.description.n_inputs == 0) or all(
            self.inputs[_elm].has_value or self.description.inputs[_elm].has_default
            for _elm in self.inputs
        )

    def Run(self, script_accessor=None):
        """
        It must have been checked that the state is not disabled.
        """

        def _FakeOutputs(n_outputs: int, fake_value: object) -> object | tuple:
            """"""
            return n_outputs * (fake_value,) if n_outputs > 1 else fake_value

        self.state = state_e.running
        MESSENGER.TransmitMessage(state_e.running, (self,))

        try:
            if self.description.n_inputs > 0:
                anonymous_args = []
                named_args = {}
                anonymous_args_as_str = []
                named_args_as_str = []

                for name, description in self.description.inputs.items():
                    if self.inputs[name].has_value:
                        value = self.inputs[name].value
                        if description.has_default:
                            named_args[name] = value
                            if script_accessor is not None:
                                named_args_as_str.append(
                                    f"{name}={self.inputs[name].source_output_name}"
                                )
                        else:
                            anonymous_args.append(value)
                            if script_accessor is not None:
                                anonymous_args_as_str.append(
                                    self.inputs[name].source_output_name
                                )
                    elif description.has_default:
                        named_args[name] = description.default_value
                        if script_accessor is not None:
                            named_args_as_str.append(
                                f"{name}={description.default_value}"
                            )
                    else:
                        raise ValueError("Should not have happened, I think...")

                if script_accessor is None:
                    output_values = self.description.Function(
                        *anonymous_args, **named_args
                    )
                else:
                    arguments = ", ".join(anonymous_args_as_str + named_args_as_str)
                    script_accessor.write(
                        f"{self.description.Function.__name__}({arguments})\n"
                    )
                    output_values = _FakeOutputs(self.description.n_outputs, "Done")
            #
            elif script_accessor is None:
                output_values = self.description.Function()
            else:
                script_accessor.write(f"{self.description.Function.__name__}()\n")
                output_values = _FakeOutputs(self.description.n_outputs, "Done")
        except Exception as exception:
            output_values = _FakeOutputs(self.description.n_outputs, None)
            print(f"Exception while running {self.unique_name}:", exception)

        self.state = state_e.done
        MESSENGER.TransmitMessage(state_e.done, (self,))

        return output_values

    # TODO: Re-think the value setting (here hidden, partially explicit in node_linked), maybe with
    #     a TransmitValue from out to in method.
    def SetInputValue(self, name: str, value: h.Any, /) -> None:
        """"""
        self.inputs[name].value = value

    def SetOutputValue(self, name: str, value: h.Any, /) -> None:
        """"""
        self.outputs[name].value = value
        MESSENGER.TransmitMessage("output set", (self,))
