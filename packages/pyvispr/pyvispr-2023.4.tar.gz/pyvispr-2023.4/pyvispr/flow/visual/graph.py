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

import dataclasses as dtcl
import typing as h
from datetime import datetime as date_time_t

import PyQt6.QtWidgets as wdgt
from conf_ini_g.phase.specification.parameter.type import type_t
from json_any import JsonStringOf
from PyQt6.QtCore import QCoreApplication, QPoint, QRectF, pyqtBoundSignal
from str_to_obj.task.comparison import TypesAreCompatible

from pyvispr.catalog.main import NODE_CATALOG
from pyvispr.flow.descriptive.socket import VALUE_NOT_SET
from pyvispr.flow.functional.graph import graph_t as graph_functional_t
from pyvispr.flow.functional.node_isolated import state_e
from pyvispr.flow.functional.node_linked import node_t as functional_t
from pyvispr.flow.messenger import MESSENGER
from pyvispr.flow.visual.link import link_t
from pyvispr.flow.visual.node import node_t
from pyvispr.flow.visual.socket import active_socket_t
from pyvispr.resource.appearance.color import (
    BUTTON_BRUSH_STATE_DISABLED,
    BUTTON_BRUSH_STATE_DOING,
    BUTTON_BRUSH_STATE_DONE,
    BUTTON_BRUSH_STATE_TODO,
    INOUT_BRUSH_ACTIVE,
    INOUT_BRUSH_INACTIVE,
    LINK_PEN_EMPTY,
    LINK_PEN_FULL,
    NODE_BRUSH_RESTING,
    NODE_BRUSH_RUNNING,
    QBrush,
    QPen,
)


@dtcl.dataclass(slots=True, repr=False, eq=False)
class graph_t(wdgt.QGraphicsScene):
    functional: graph_functional_t = dtcl.field(
        init=False, default_factory=graph_functional_t
    )
    nodes: list[node_t] = dtcl.field(init=False, default_factory=list)
    links: list[link_t] = dtcl.field(init=False, default_factory=list)

    _active_socket: active_socket_t = dtcl.field(
        init=False, default_factory=active_socket_t
    )

    def __post_init__(self) -> None:
        """"""
        wdgt.QGraphicsScene.__init__(self)
        # Does not seem to have an effet.
        # self.setSceneRect(QRectF(-500, -500, 1000, 1000))

        h.cast(pyqtBoundSignal, self.changed).connect(self.UpdateLinks)

        MESSENGER.AddCanal(state_e.disabled, self.AcknowledgeDisabled)
        MESSENGER.AddCanal(state_e.todo, self.AcknowledgeToDo)
        MESSENGER.AddCanal(state_e.running, self.AcknowledgeRunningStarted)
        MESSENGER.AddCanal(state_e.done, self.AcknowledgeRunningEnded)
        MESSENGER.AddCanal("output set", self.AcknowledgeLinkFull)
        MESSENGER.AddCanal("output unset", self.AcknowledgeLinkEmpty)

    def __DescriptionForJSON__(
        self,
    ) -> tuple[graph_functional_t, tuple[tuple[str, float, float], ...]]:
        """"""
        nodes = tuple(_elm.__DescriptionForJSON__() for _elm in self.nodes)
        return self.functional, nodes

    def AddNode(self, name: str, /) -> None:
        """"""
        description = NODE_CATALOG.NodeDescription(name)
        functional = functional_t.NewForDescription(description)
        self.functional.AddNode(functional)

        node = node_t(functional=functional)
        self.nodes.append(node)

        self.clearSelection()  # Otherwise the newly created visual node replaces the selection.
        self.addItem(node)
        self.addItem(node.ii_dialog)

    def AddLinkMaybe(
        self, node: node_t, node_is_source: bool, position: QPoint, /
    ) -> None:
        """"""
        if self._active_socket.node is None:
            functional = node.functional
            if node_is_source:
                sockets = functional.description.outputs
                possible_names = functional.description.output_names
                button = node.out_btn
            else:
                sockets = functional.description.inputs
                possible_names = tuple(
                    _nme
                    for _nme, _rcd in functional.inputs.items()
                    if not _rcd.is_linked
                )
                button = node.in_btn
            if possible_names.__len__() > 1:
                selected = _SocketSelection(possible_names, position)
            else:
                selected = possible_names[0]
            if selected is not None:
                stripe = sockets[selected]
                if not isinstance(stripe, type_t):
                    stripe = stripe.type
                self._active_socket.node = node
                self._active_socket.is_source = node_is_source
                self._active_socket.name = selected
                self._active_socket.type = stripe
                button.setBrush(INOUT_BRUSH_ACTIVE)

            return

        same_kind = (node_is_source and self._active_socket.is_source) or not (
            node_is_source or self._active_socket.is_source
        )

        if node is self._active_socket.node:
            if same_kind:
                if node_is_source:
                    button = self._active_socket.node.out_btn
                else:
                    button = self._active_socket.node.in_btn
                self._active_socket.node = None
                button.setBrush(INOUT_BRUSH_INACTIVE)
            return

        if same_kind:
            return

        current = active_socket_t(node=node)
        current_functional = node.functional
        if node_is_source:
            source = current
            target = self._active_socket
            possible_names = tuple(
                _nme
                for _nme, _tpe in current_functional.description.outputs.items()
                if _TypesAreCompatible(_tpe, target.type)
            )
        else:
            source = self._active_socket
            target = current
            possible_names = tuple(
                _nme
                for _nme, _rcd in current_functional.inputs.items()
                if (not _rcd.is_linked)
                and _TypesAreCompatible(
                    current_functional.description.inputs[_nme].type,
                    source.type,
                )
            )
        if (n_names := possible_names.__len__()) == 0:
            return

        if n_names > 1:
            selected = _SocketSelection(possible_names, position)
        else:
            selected = possible_names[0]
        if selected is None:
            return

        if node_is_source:
            source.name = selected
            button = target.node.in_btn
        else:
            target.name = selected
            button = source.node.out_btn
        self.AddLink(source.node, source.name, target.node, target.name)
        self._active_socket.node = None
        button.setBrush(INOUT_BRUSH_INACTIVE)

    def AddLink(
        self,
        source: node_t,
        output_name: str,
        target: node_t,
        input_name: str,
        /,
    ) -> None:
        """"""
        self.functional.AddLink(
            source.functional, output_name, target.functional, input_name
        )
        if not any(
            (_lnk.source_node is source) and (_lnk.target_node is target)
            for _lnk in self.links
        ):
            link = link_t(
                source_node=source,
                source_point=source.output_anchor_coordinates,
                target_node=target,
                target_point=target.input_anchor_coordinates,
            )
            self.links.append(link)
            self.addItem(link)
            self.addItem(link.arrow)

    def RemoveNode(self, node: node_t, /) -> None:
        """"""
        if node.ii_dialog is not None:
            node.ii_dialog.close()

        for link in self.links:
            if (link.source_node is node) or (link.target_node is node):
                self.RemoveLink(link)

        self.functional.RemoveNode(node.functional)
        self.nodes.remove(node)
        self.removeItem(node)
        self.removeItem(node.ii_dialog)

    def RemoveLink(
        self,
        link: link_t,
        /,
        output_name: str | None = None,
        input_name: str | None = None,
    ) -> None:
        """"""
        if output_name is None:  # input_name must also be None.
            for output_name, input_name in link.UnderlyingFunctionals():
                self.functional.RemoveLink(
                    link.source_node.functional,
                    output_name,
                    link.target_node.functional,
                    input_name,
                )
            should_be_actually_removed = True
        else:  # Both names are not None.
            self.functional.RemoveLink(
                link.source_node.functional,
                output_name,
                link.target_node.functional,
                input_name,
            )
            should_be_actually_removed = link.UnderlyingFunctionals().__len__() == 0

        if should_be_actually_removed:
            self.links.remove(link)
            self.removeItem(link)
            self.removeItem(link.arrow)

    def UpdateLinks(self, _: h.Sequence[QRectF], /) -> None:
        """"""
        for node in self.selectedItems():
            if isinstance(node, node_t) and node.position_has_changed:
                for link in self.links:
                    if node is link.source_node:
                        link.SetPath(
                            link.source_node.output_anchor_coordinates,
                            link.target_point,
                        )
                    elif node is link.target_node:
                        link.SetPath(
                            link.source_point,
                            link.target_node.input_anchor_coordinates,
                        )
                node.position_has_changed = False

    def Clear(self) -> None:
        """"""
        # Do not iterate over nodes since RemoveNode modifies self.
        while self.nodes.__len__() > 0:
            self.RemoveNode(self.nodes[0])

    def Run(self, /, *, script_accessor=None) -> None:
        """"""
        for node in self.nodes:
            functional = node.functional

            for input_name, input_ in functional.inputs.items():
                if (not input_.is_linked) and (input_name in node.interactive_inputs):
                    expected_type = functional.description.inputs[input_name].type
                    value_as_str = node.interactive_inputs[input_name].Text()
                    value, issues = expected_type.InterpretedValueOf(value_as_str)
                    if issues.__len__() > 0:
                        raise RuntimeError("Log issues for later review.")
                    else:
                        functional.SetInputValue(input_name, value)
                        if script_accessor is not None:
                            # Fake self-backlink (since actually not linked).
                            script_accessor.write(
                                f"{functional.UniqueNameWithPostfix(input_name)} = {value}\n"
                            )

        self.functional.Run(script_accessor=script_accessor)

        for node in self.nodes:
            for idx, output_name in enumerate(node.functional.description.output_names):
                output_value = node.functional.outputs[output_name].value

                if output_value is not VALUE_NOT_SET:
                    if script_accessor is not None:
                        variable_name = node.functional.UniqueNameWithPostfix(
                            output_name
                        )
                        script_accessor.write(
                            f"# print('{variable_name} =', {variable_name})\n"
                        )
                        # TODO: Replace print with save for default python type.

    def SaveToFile(self, filename: str, /) -> None:
        """"""
        encoded, history = JsonStringOf(self)
        if history is not None:
            print("\n".join(history))

    def LoadFromFile(self, filename: str, node_idx_offset: int, /) -> None:
        """"""
        pass

    def SaveAsScript(self, filename: str, /) -> None:
        """"""
        pass

    def AcknowledgeDisabled(self, functional: functional_t, /) -> None:
        """"""
        self.AcknowledgeNodeState(
            functional, "Disabled", (NODE_BRUSH_RESTING, BUTTON_BRUSH_STATE_DISABLED)
        )

    def AcknowledgeToDo(self, functional: functional_t, /) -> None:
        """"""
        self.AcknowledgeNodeState(
            functional, "Needs Running", (NODE_BRUSH_RESTING, BUTTON_BRUSH_STATE_TODO)
        )

    def AcknowledgeRunningStarted(self, functional: functional_t, /) -> None:
        """"""
        self.AcknowledgeNodeState(
            functional,
            f"Running since {date_time_t.now()}",
            (NODE_BRUSH_RUNNING, BUTTON_BRUSH_STATE_DOING),
        )

    def AcknowledgeRunningEnded(self, functional: functional_t, /) -> None:
        """"""
        self.AcknowledgeNodeState(
            functional,
            f"Run Successfully ({date_time_t.now()})",
            (NODE_BRUSH_RESTING, BUTTON_BRUSH_STATE_DONE),
        )

    def AcknowledgeNodeState(
        self, functional: functional_t, message: str, brushes: tuple[QBrush, QBrush], /
    ) -> None:
        """"""
        for node in self.nodes:
            if node.functional is functional:
                node.setBrush(brushes[0])
                node.state_btn.setBrush(brushes[1])
                node.state_btn.setToolTip(message)
                QCoreApplication.processEvents()
                break

    def AcknowledgeLinkEmpty(self, functional: functional_t, /) -> None:
        """"""
        self.AcknowledgeLinkState(functional, LINK_PEN_EMPTY)

    def AcknowledgeLinkFull(self, functional: functional_t, /) -> None:
        """"""
        self.AcknowledgeLinkState(functional, LINK_PEN_FULL)

    def AcknowledgeLinkState(self, functional: functional_t, pen: QPen, /) -> None:
        """"""
        for link in self.links:
            if link.source_node.functional is functional:
                link.setPen(pen)
                QCoreApplication.processEvents()
                break


def _SocketSelection(
    possible_names: tuple[str, ...], position: QPoint, /
) -> str | None:
    """"""
    menu = wdgt.QMenu()
    actions = [menu.addAction(_elm) for _elm in possible_names]
    selected_action = menu.exec(position)
    if selected_action is None:
        return None

    return possible_names[actions.index(selected_action)]


def _TypesAreCompatible(
    source: type_t | str,
    target: type_t | str,
    /,
) -> bool:
    """"""
    if isinstance(source, type_t):
        if isinstance(target, type_t):
            return TypesAreCompatible(
                source, target, strict_mode=False, second_should_be_wider=True
            )
        else:
            return str(source) == target
    else:
        if isinstance(target, type_t):
            return source == str(target)
        else:
            return source == target
