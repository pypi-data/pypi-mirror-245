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

import PyQt6.QtWidgets as wdgt
from conf_ini_g.interface.window.parameter.main import TypeAndValueWidgetsForType
from PyQt6.QtCore import QPointF, QRectF

from pyvispr.flow.descriptive.socket import assignment_e
from pyvispr.flow.functional.node_linked import node_t as functional_t
from pyvispr.resource.appearance.backend import SCREEN_BACKEND
from pyvispr.resource.appearance.color import (
    BUTTON_BRUSH_CONFIG,
    BUTTON_BRUSH_REMOVE,
    BUTTON_BRUSH_STATE_TODO,
    INOUT_BRUSH_INACTIVE,
    NODE_BRUSH_RESTING,
    NODE_BRUSH_SELECTED,
    color_e,
)
from pyvispr.resource.appearance.geometry import (
    BUTTON_WIDTH,
    NODE_HEIGHT_TOTAL,
    NODE_WIDTH_TOTAL,
)


@dtcl.dataclass(slots=True, repr=False, eq=False)
class node_t(wdgt.QGraphicsRectItem):
    should_show_info_boxes: h.ClassVar[bool] = False

    functional: functional_t
    in_btn = None
    out_btn = None
    config_btn = None
    state_btn = None
    remove_btn = None

    position_has_changed: bool = False

    interactive_inputs: dict[str, wdgt.QWidget] | None = None
    ii_dialog: wdgt.QGraphicsProxyWidget | None = None

    def __post_init__(self) -> None:
        """"""
        # If using: self.setRect(QRectF(0, 0, NODE_WIDTH_TOTAL, NODE_HEIGHT_TOTAL)), Python complains about super-init not
        # having been called.
        wdgt.QGraphicsRectItem.__init__(
            self, QRectF(0, 0, NODE_WIDTH_TOTAL, NODE_HEIGHT_TOTAL)
        )
        self.SetupAndCreateElements()
        self.setZValue(2)
        self.setSelected(True)

    def __DescriptionForJSON__(self) -> tuple[str, float, float]:
        """"""
        return self.functional.unique_name, self.x(), self.y()

    def SetupAndCreateElements(self) -> None:
        """"""
        self.setFlag(wdgt.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(wdgt.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(wdgt.QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape)
        self.setFlag(wdgt.QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setToolTip(self.details)
        self.setBrush(NODE_BRUSH_RESTING)

        label = wdgt.QGraphicsTextItem(self)
        label.setHtml(self.functional.unique_name)
        label.setPos(BUTTON_WIDTH, 0)
        label.setTextWidth(NODE_WIDTH_TOTAL - 2 * BUTTON_WIDTH)
        # Causes a crash!
        # label.setTextInteractionFlags(constant_e.ItemSelectionMode.TextSelectableByMouse)

        width_of_lateral_buttons = BUTTON_WIDTH
        height_of_lateral_buttons = NODE_HEIGHT_TOTAL

        top_of_bottom_buttons = NODE_HEIGHT_TOTAL - BUTTON_WIDTH
        height_of_bottom_buttons = BUTTON_WIDTH

        if self.functional.description.n_inputs > 0:
            self.in_btn = wdgt.QGraphicsRectItem(
                QRectF(0, 0, width_of_lateral_buttons, height_of_lateral_buttons),
                self,
            )
            self.in_btn.setBrush(INOUT_BRUSH_INACTIVE)
        else:
            self.in_btn = None

        if self.functional.description.n_outputs > 0:
            self.out_btn = wdgt.QGraphicsRectItem(
                QRectF(
                    NODE_WIDTH_TOTAL - width_of_lateral_buttons,
                    0,
                    width_of_lateral_buttons,
                    height_of_lateral_buttons,
                ),
                self,
            )
            self.out_btn.setBrush(INOUT_BRUSH_INACTIVE)
        else:
            self.out_btn = None

        horizontal_free_space = NODE_WIDTH_TOTAL - 2 * width_of_lateral_buttons
        config_btn_width = int(horizontal_free_space / 2.5)
        self.config_btn = wdgt.QGraphicsRectItem(
            QRectF(
                width_of_lateral_buttons,
                top_of_bottom_buttons,
                config_btn_width,
                height_of_bottom_buttons,
            ),
            self,
        )
        self.config_btn.setBrush(BUTTON_BRUSH_CONFIG)

        self.state_btn = wdgt.QGraphicsRectItem(
            QRectF(
                width_of_lateral_buttons + config_btn_width,
                top_of_bottom_buttons,
                config_btn_width,
                height_of_bottom_buttons,
            ),
            self,
        )
        self.state_btn.setToolTip("Needs Running")
        self.state_btn.setBrush(BUTTON_BRUSH_STATE_TODO)

        self.remove_btn = wdgt.QGraphicsRectItem(
            QRectF(
                width_of_lateral_buttons + 2 * config_btn_width,
                top_of_bottom_buttons,
                horizontal_free_space - 2 * config_btn_width,
                height_of_bottom_buttons,
            ),
            self,
        )
        self.remove_btn.setBrush(BUTTON_BRUSH_REMOVE)

        self.ii_dialog = wdgt.QGraphicsProxyWidget()
        self.ii_dialog.setZValue(2)

    @property
    def input_anchor_coordinates(self) -> QPointF:
        """"""
        return self._SocketCoordinates(True)

    @property
    def output_anchor_coordinates(self) -> QPointF:
        """"""
        return self._SocketCoordinates(False)

    def _SocketCoordinates(self, endpoint_is_input: bool, /) -> QPointF:
        """"""
        output = self.scenePos()
        output.setY(output.y() + int(0.5 * self.boundingRect().height()))

        if not endpoint_is_input:
            output.setX(output.x() + self.boundingRect().width())

        return output

    @property
    def details(self) -> str:
        """"""
        functional = self.functional

        output = [f"Function: {functional.description.function_name}"]

        if functional.description.n_inputs > 0:
            output.append("Input(s):")
            for name, input_ in functional.description.inputs.items():
                if input_.has_default:
                    default = f" = {input_.default_value}"
                else:
                    default = ""
                output.append(f"    {name}:{input_.type.template_as_str}{default}")
        else:
            output.append("No Inputs")

        if functional.description.n_outputs > 0:
            output.append("Output(s):")
            for name, stripe in functional.description.outputs.items():
                output.append(f"    {name}:{stripe.template_as_str}")
        else:
            output.append("No Outputs")

        return "\n".join(output)

    def ToggleIIDialog(self) -> None:
        """
        IIDialog placement could be handled automatically with graphics anchors. Keeping manual management for the
        moment.
        """
        if self.interactive_inputs is not None:
            if self.ii_dialog.isVisible():
                self.ii_dialog.hide()
            else:
                self.ii_dialog.setPos(self.x(), self.y() + NODE_HEIGHT_TOTAL)
                self.ii_dialog.show()
            return

        interactive_inputs = {}
        n_widgets = 0
        layout = wdgt.QGridLayout()
        for i_idx, (name, record) in enumerate(
            self.functional.description.inputs.items()
        ):
            if record.assignment is assignment_e.full:
                type_wgt, value_wgt = TypeAndValueWidgetsForType(
                    record.type, SCREEN_BACKEND
                )
                interactive_inputs[name] = value_wgt
                n_widgets += 1

                layout.addWidget(wdgt.QLabel(name), i_idx, 0, 1, 1)
                layout.addWidget(type_wgt, i_idx, 1, 1, 1)
                layout.addWidget(value_wgt.library_wgt, i_idx, 2, 1, 1)

        if n_widgets > 0:
            self.interactive_inputs = interactive_inputs

            widget = wdgt.QWidget()
            widget.setLayout(layout)
            widget.setStyleSheet(f"background-color: {color_e.dodgerblue.name()};")

            self.ii_dialog.setWidget(widget)
            self.ii_dialog.setPos(self.x(), self.y() + NODE_HEIGHT_TOTAL)

    def itemChange(
        self, change: wdgt.QGraphicsItem.GraphicsItemChange, data: h.Any, /
    ) -> h.Any:
        """"""
        if change is wdgt.QGraphicsItem.GraphicsItemChange.ItemSelectedHasChanged:
            if data:
                self.setBrush(NODE_BRUSH_SELECTED)
            else:
                self.setBrush(NODE_BRUSH_RESTING)
        elif change is wdgt.QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            if self.ii_dialog.isVisible():
                self.ii_dialog.setPos(self.x(), self.y() + NODE_HEIGHT_TOTAL)
            self.position_has_changed = True

        return wdgt.QGraphicsRectItem.itemChange(self, change, data)
