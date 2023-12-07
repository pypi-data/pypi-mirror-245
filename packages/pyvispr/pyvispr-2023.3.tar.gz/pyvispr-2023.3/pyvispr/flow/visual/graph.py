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

import PyQt6.QtWidgets as wg
from conf_ini_g.phase.specification.parameter.type import type_t
from PyQt6.QtCore import QRectF, pyqtBoundSignal
from str_to_obj.task.comparison import TypesAreCompatible

import pyvispr.widget.event.main as evnt
from pyvispr.catalog.main import NODE_CATALOG
from pyvispr.flow.descriptive.socket import VALUE_NOT_SET, assignment_e
from pyvispr.flow.functional.graph import graph_t as graph_functional_t
from pyvispr.flow.functional.node_linked import node_t as functional_t
from pyvispr.flow.visual.link import link_t
from pyvispr.flow.visual.node import node_t
from pyvispr.flow.visual.socket import active_plug_t
from pyvispr.resource.appearance.color import (
    active_inout_brush_c,
    gray_pen_c,
    inactive_inout_brush_c,
)


@dtcl.dataclass(slots=True, repr=False, eq=False)
class graph_t(wg.QGraphicsScene):
    functional: graph_functional_t = dtcl.field(init=False)
    nodes: list[node_t] = dtcl.field(init=False, default_factory=list)
    links: list[link_t] = dtcl.field(init=False, default_factory=list)

    _active_src: active_plug_t | None = dtcl.field(init=False, default=None)
    _active_dst: active_plug_t | None = dtcl.field(init=False, default=None)

    def __post_init__(self) -> None:
        """"""
        wg.QGraphicsScene.__init__(self)
        # Does not seem to have an effet.
        # self.setSceneRect(QRectF(-500, -500, 1000, 1000))
        self.functional = graph_functional_t()

        for row in range(-300, 601, 100):
            self.addLine(-500, row, 1000, row, gray_pen_c)
        for col in range(-500, 1001, 100):
            self.addLine(col, -300, col, 600, gray_pen_c)

        h.cast(pyqtBoundSignal, self.changed).connect(self.UpdateLinks)

    def AddNode(self, name: str, /) -> None:
        """"""
        description = NODE_CATALOG.NodeDescription(name)
        functional = functional_t.NewForDescription(description)
        self.functional.AddNode(functional)

        node = node_t(functional=functional)
        self.nodes.append(node)

        self.clearSelection()  # Otherwise the newly created visual node replaces the selection.
        self.addItem(node)

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

    def Clear(self) -> None:
        """"""
        # Do not iterate over nodes since RemoveNode modifies self.
        while self.nodes.__len__() > 0:
            self.RemoveNode(self.nodes[0])

    def Run(self, /, *, script_accessor=None) -> None:
        """"""
        for node in self.nodes:
            functional = node.functional

            for input_name in functional.description.input_names:
                if (
                    (
                        functional.description.inputs[input_name].assignment
                        is not assignment_e.link
                    )
                    and (not self.functional.ContainsLinkTo(functional, input_name))
                    and (input_name in node.interactive_inputs)
                ):
                    value_as_str = node.interactive_inputs[input_name].Text()
                    value, issues = functional.description.inputs[
                        input_name
                    ].type.InterpretedValueOf(value_as_str)
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

    def SaveToFile(self, filename: str, /) -> None:
        """"""
        pass

    def LoadFromFile(self, filename: str, node_idx_offset: int, /) -> None:
        """"""
        pass

    def SaveAsScript(self, filename: str, /) -> None:
        """"""
        pass

    def SetNodeAsActive(self, node: node_t, which: h.Literal["src", "dst"], /) -> None:
        """"""
        plug = active_plug_t(node=node)
        if which == "src":
            self._active_src = plug
        else:
            self._active_dst = plug

    def is_active_src(self, node: node_t, /) -> bool:
        """"""
        return (self._active_src is not None) and (self._active_src.node is node)

    def is_active_dst(self, node: node_t, /) -> bool:
        """"""
        return (self._active_dst is not None) and (self._active_dst.node is node)

    def SelectNodeForLinkCreation(
        self, node: node_t, event, endpoint_is_input: bool, /
    ) -> None:
        """"""
        if endpoint_is_input:
            if self.is_active_dst(node):
                self.DeselectSrcOrDstForLinkCreation(False)
                return

            if self.is_active_src(node):
                return

            possible_names = node.functional.description.input_names
            if self._active_src is None:
                possible_names = tuple(
                    name
                    for name in possible_names
                    if not node.functional.inputs[name].is_linked
                )
            else:
                possible_names = tuple(
                    name
                    for name in possible_names
                    if (not node.functional.inputs[name].is_linked)
                    and _TypesAreCompatible(
                        self._active_src.in_out_types,
                        node.functional.description.inputs[name].type,
                    )
                )

            if len(possible_names) == 0:
                return

            if self._active_dst is not None:
                self.DeselectSrcOrDstForLinkCreation(False)

            self.SetNodeAsActive(node, "dst")
            node.in_btn.setBrush(active_inout_brush_c)
        #
        else:  # this else could be merged with the following if, but kept as is for aesthetics
            if self.is_active_src(node):
                self.DeselectSrcOrDstForLinkCreation(True)
                return

            if self.is_active_dst(node):
                return

            possible_names = node.functional.description.output_names
            if self._active_dst is not None:
                possible_names = tuple(
                    name
                    for name in possible_names
                    if _TypesAreCompatible(
                        node.functional.description.outputs[name],
                        self._active_dst.in_out_types,
                    )
                )
                if len(possible_names) == 0:
                    return

            if self._active_src is not None:
                self.DeselectSrcOrDstForLinkCreation(True)

            self.SetNodeAsActive(node, "src")
            node.out_btn.setBrush(active_inout_brush_c)

        if possible_names.__len__() > 1:
            menu = wg.QMenu()

            if endpoint_is_input and (self._active_src is not None):
                no_act = menu.addAction(self._active_src.in_out_name + " ->")
                no_act.setEnabled(False)
            #
            elif (not endpoint_is_input) and (self._active_dst is not None):
                no_act = menu.addAction("-> " + self._active_dst.in_out_name)
                no_act.setEnabled(False)

            menu_actions = len(possible_names) * [None]
            for name_idx, name in enumerate(possible_names):
                menu_actions[name_idx] = menu.addAction(name)

            if endpoint_is_input:
                selected_act = menu.exec(
                    evnt.TranslateEventPositionOnChild(event, node.in_btn)
                )
            else:
                selected_act = menu.exec(
                    evnt.TranslateEventPositionOnChild(event, node.out_btn)
                )
            if selected_act is None:
                self.DeselectSrcOrDstForLinkCreation(True)
                self.DeselectSrcOrDstForLinkCreation(False)
            else:
                self.SelectInOrOutForLinkCreation(
                    possible_names[menu_actions.index(selected_act)], endpoint_is_input
                )
        else:
            self.SelectInOrOutForLinkCreation(possible_names[0], endpoint_is_input)

    def SelectInOrOutForLinkCreation(self, name: str, name_is_input: bool, /) -> None:
        """"""
        if name_is_input:
            self._active_dst.in_out_name = name
            self._active_dst.in_out_types = (
                self._active_dst.node.functional.description.inputs[name].type
            )
        else:
            self._active_src.in_out_name = name
            self._active_src.in_out_types = (
                self._active_src.node.functional.description.outputs[name]
            )

        if not ((self._active_src is None) or (self._active_dst is None)):
            self.AddLink(
                self._active_src.node,
                self._active_src.in_out_name,
                self._active_dst.node,
                self._active_dst.in_out_name,
            )

            self.DeselectSrcOrDstForLinkCreation(True)
            self.DeselectSrcOrDstForLinkCreation(False)

    def DeselectSrcOrDstForLinkCreation(self, should_deselect_src: bool, /) -> None:
        """"""
        if should_deselect_src:
            if self._active_src is not None:
                self._active_src.node.out_btn.setBrush(inactive_inout_brush_c)
                self._active_src = None
        elif self._active_dst is not None:
            self._active_dst.node.in_btn.setBrush(inactive_inout_brush_c)
            self._active_dst = None


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
