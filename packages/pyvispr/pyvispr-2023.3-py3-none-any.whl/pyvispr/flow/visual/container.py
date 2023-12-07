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
from PyQt6.QtCore import Qt as constant_e
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtGui import QPainter as painter_t

from pyvispr.flow.visual.graph import graph_t
from pyvispr.flow.visual.link import link_t
from pyvispr.flow.visual.node import node_t


@dtcl.dataclass(slots=True, repr=False, eq=False)
class container_t(wg.QGraphicsView):
    zoom_factor_c: h.ClassVar[float] = 1.25

    graph: graph_t

    def __post_init__(self) -> None:
        """"""
        # Otherwise, complaint about super-init not having been called.
        wg.QGraphicsView.__init__(self)

        self.setScene(self.graph)
        self.setRenderHint(painter_t.RenderHint.Antialiasing)
        self.setMinimumSize(640, 480)
        self.setSizePolicy(
            wg.QSizePolicy.Policy.MinimumExpanding,
            wg.QSizePolicy.Policy.MinimumExpanding,
        )
        # Used to not work in conjunction with selectable RectItems.
        self.setDragMode(wg.QGraphicsView.DragMode.RubberBandDrag)

    def mousePressEvent(self, event: QMouseEvent, /) -> None:
        """"""
        if event.buttons() != constant_e.MouseButton.LeftButton:
            wg.QGraphicsView.mousePressEvent(self, event)
            return

        view_position = event.pos()
        scene_position = self.mapToScene(view_position)
        item = self.graph.itemAt(scene_position, self.graph.views()[0].transform())
        while not (
            (item is None) or isinstance(item, node_t) or isinstance(item, link_t)
        ):
            item = item.parentItem()
        if item is None:
            wg.QGraphicsView.mousePressEvent(self, event)
            return

        item: node_t | link_t
        if isinstance(item, node_t):
            item_position = item.mapFromScene(scene_position)
            if (item.in_btn is not None) and item.in_btn.contains(item_position):
                self.graph.SelectNodeForLinkCreation(item, event, True)
            elif (item.out_btn is not None) and item.out_btn.contains(item_position):
                self.graph.SelectNodeForLinkCreation(item, event, False)
            elif item.config_btn.contains(item_position):
                item.ShowIIDialog()
            elif item.next_run_btn.contains(item_position):
                pass
            elif item.remove_btn.contains(item_position):
                item_global_pos = self.mapToGlobal(view_position)
                menu = wg.QMenu()
                no_action = menu.addAction("or")
                no_action.setEnabled(False)
                remove_action = menu.addAction("Remove Node")
                selected_action = menu.exec(item_global_pos)
                if selected_action is remove_action:
                    self.graph.RemoveNode(item)
            else:
                wg.QGraphicsView.mousePressEvent(self, event)
        else:
            links = item.LinksToBeRemoved(self.mapToGlobal(view_position))
            if isinstance(links, h.Sequence):
                if links[0] is None:
                    self.graph.RemoveLink(item)
                else:
                    self.graph.RemoveLink(
                        item, output_name=links[0][0], input_name=links[0][1]
                    )

    def wheelEvent(self, event, /) -> None:
        """"""
        if event.modifiers() == constant_e.KeyboardModifier.ControlModifier:
            scale_factor = (
                1 / container_t.zoom_factor_c
                if event.angleDelta().y() > 0
                else container_t.zoom_factor_c
            )
            self.scale(scale_factor, scale_factor)
