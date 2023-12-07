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

import PyQt6.QtWidgets as wg
from conf_ini_g.interface.window.parameter.main import TypeAndValueWidgetsForType
from PyQt6.QtCore import QPointF, QRectF, pyqtBoundSignal
from PyQt6.QtWidgets import QApplication as qtapp_t

from pyvispr.flow.descriptive.socket import assignment_e
from pyvispr.flow.functional.node_linked import node_t as functional_t
from pyvispr.resource.appearance.backend import SCREEN_BACKEND
from pyvispr.resource.appearance.color import (
    config_brush_c,
    inactive_inout_brush_c,
    next_run_brush_needs_c,
    next_run_brush_normal_c,
    next_run_brush_running_c,
    remove_brush_c,
    resting_brush_c,
    running_brush_c,
    selected_brush_c,
)
from pyvispr.resource.appearance.geometry import (
    button_width_c,
    total_height_c,
    total_width_c,
)


@dtcl.dataclass(slots=True, repr=False, eq=False)
class node_t(wg.QGraphicsRectItem):
    should_show_info_boxes: h.ClassVar[bool] = False

    functional: functional_t
    in_btn = None
    out_btn = None
    config_btn = None
    next_run_btn = None
    remove_btn = None

    position_has_changed: bool = False

    ii_dialog: wg.QDialog | None = None
    interactive_inputs: dict[str, wg.QWidget] = dtcl.field(
        init=False, default_factory=dict
    )

    def __post_init__(self) -> None:
        """"""
        # If using: self.setRect(QRectF(0, 0, total_width_c, total_height_c)), Python complains about super-init not
        # having been called.
        wg.QGraphicsRectItem.__init__(self, QRectF(0, 0, total_width_c, total_height_c))
        self.SetupAndCreateElements()
        # self.setFlag(wg.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setAcceptHoverEvents(True)
        self.setSelected(True)

    def SetupAndCreateElements(self) -> None:
        """"""
        self.setFlag(wg.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(wg.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(wg.QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape)
        self.setFlag(wg.QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setBrush(resting_brush_c)

        label = wg.QGraphicsTextItem(self)
        label.setHtml(self.functional.unique_name)
        label.setPos(button_width_c, 0)
        label.setTextWidth(total_width_c - 2 * button_width_c)
        # Causes a crash!
        # label.setTextInteractionFlags(constant_e.ItemSelectionMode.TextSelectableByMouse)

        width_of_lateral_buttons = button_width_c
        height_of_lateral_buttons = total_height_c

        top_of_bottom_buttons = total_height_c - button_width_c
        height_of_bottom_buttons = button_width_c

        if self.functional.description.n_inputs > 0:
            self.in_btn = wg.QGraphicsRectItem(
                QRectF(0, 0, width_of_lateral_buttons, height_of_lateral_buttons),
                self,
            )
            self.in_btn.setBrush(inactive_inout_brush_c)
        else:
            self.in_btn = None

        if self.functional.description.n_outputs > 0:
            self.out_btn = wg.QGraphicsRectItem(
                QRectF(
                    total_width_c - width_of_lateral_buttons,
                    0,
                    width_of_lateral_buttons,
                    height_of_lateral_buttons,
                ),
                self,
            )
            self.out_btn.setBrush(inactive_inout_brush_c)
        else:
            self.out_btn = None

        horizontal_free_space = total_width_c - 2 * width_of_lateral_buttons
        config_btn_width = int(horizontal_free_space / 2.5)
        self.config_btn = wg.QGraphicsRectItem(
            QRectF(
                width_of_lateral_buttons,
                top_of_bottom_buttons,
                config_btn_width,
                height_of_bottom_buttons,
            ),
            self,
        )
        self.config_btn.setBrush(config_brush_c)

        self.next_run_btn = wg.QGraphicsRectItem(
            QRectF(
                width_of_lateral_buttons + config_btn_width,
                top_of_bottom_buttons,
                config_btn_width,
                height_of_bottom_buttons,
            ),
            self,
        )
        self.next_run_btn.setBrush(next_run_brush_needs_c)

        self.remove_btn = wg.QGraphicsRectItem(
            QRectF(
                width_of_lateral_buttons + 2 * config_btn_width,
                top_of_bottom_buttons,
                horizontal_free_space - 2 * config_btn_width,
                height_of_bottom_buttons,
            ),
            self,
        )
        self.remove_btn.setBrush(remove_brush_c)

    def ShowIIDialog(self) -> None:
        """"""
        layout = wg.QGridLayout()
        interactive_inputs = {}
        n_widgets = 0
        for i_idx, (name, record) in enumerate(
            self.functional.description.inputs.items()
        ):
            if record.assignment is assignment_e.full:
                type_wgt, value_wgt = TypeAndValueWidgetsForType(
                    record.type, SCREEN_BACKEND
                )
                layout.addWidget(wg.QLabel(name), i_idx, 0, 1, 1)
                layout.addWidget(type_wgt, i_idx, 1, 1, 1)
                layout.addWidget(value_wgt.library_wgt, i_idx, 2, 1, 1)
                interactive_inputs[name] = value_wgt
                n_widgets += 1

        if n_widgets > 0:
            if self.ii_dialog is None:
                button = wg.QPushButton("Done")
                layout.addWidget(button, n_widgets, 0, 1, 3)
                interactive_inputs["__Done_button__"] = button
                parent = None
                for widget in qtapp_t.topLevelWidgets():
                    if isinstance(widget, wg.QMainWindow):
                        parent = widget
                        break
                self.ii_dialog = wg.QDialog(parent=parent)
                self.ii_dialog.setWindowTitle(self.functional.unique_name)
                self.ii_dialog.close = self.ii_dialog.hide
                self.ii_dialog.setLayout(layout)
                h.cast(pyqtBoundSignal, button.clicked).connect(self.ii_dialog.hide)
                self.interactive_inputs = interactive_inputs

            self.ii_dialog.show()
            self.ii_dialog.raise_()
            self.ii_dialog.activateWindow()

    @property
    def input_anchor_coordinates(self) -> QPointF:
        """"""
        return self._SocketCoordinates(True)

    @property
    def output_anchor_coordinates(self) -> QPointF:
        """"""
        return self._SocketCoordinates(False)

    @property
    def info_text(self):
        """"""
        text = "Function: " + self.functional.description.function_name + "\n"

        if self.functional.needs_running:
            text += "Needs Running: True\n"
            if self.functional.can_run:
                text += "Can Run: True\n"
            else:
                text += "Can Run: False\n"
        else:
            text += "Needs Running: False\n"

        if self.functional.description.n_inputs > 0:
            text += "Input(s):\n"

            for name in self.functional.description.inputs:
                text += f"    {name}:{self.functional.description.inputs[name].type} = {self.functional.description.inputs[name].default_value}\n"
        else:
            text += "No Inputs\n"

        if self.functional.description.n_outputs > 0:
            text += "Output(s):\n"

            for name in self.functional.description.outputs:
                text += f"    {name}:{self.functional.description.outputs[name]}\n"
        else:
            text += "No Outputs\n"

        return text[:-1]

    def paint(self, painter, options, widget=None):
        """"""
        # TODO: Certainly a bad way to paint (multiple calls of paint()???).
        if self.functional.is_running:
            self.setBrush(running_brush_c)
        elif self.isSelected():
            self.setBrush(selected_brush_c)
        else:
            self.setBrush(resting_brush_c)
        wg.QGraphicsRectItem.paint(self, painter, options, widget)

    def ChangeAppearanceToRunning(self, state_is_running):
        """"""
        if state_is_running:
            self.setBrush(running_brush_c)
            self.next_run_btn.setBrush(next_run_brush_running_c)
        else:
            self.setBrush(resting_brush_c)
            self.next_run_btn.setBrush(next_run_brush_normal_c)

    def itemChange(
        self, change: wg.QGraphicsItem.GraphicsItemChange, data: h.Any, /
    ) -> h.Any:
        """"""
        if change == wg.QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            self.position_has_changed = True

        return wg.QGraphicsRectItem.itemChange(self, change, data)

    def _SocketCoordinates(self, endpoint_is_input: bool, /) -> QPointF:
        """"""
        endpoint_pos = self.scenePos()
        endpoint_pos.setY(endpoint_pos.y() + int(0.5 * self.boundingRect().height()))

        if not endpoint_is_input:
            endpoint_pos.setX(endpoint_pos.x() + self.boundingRect().width())

        return endpoint_pos
