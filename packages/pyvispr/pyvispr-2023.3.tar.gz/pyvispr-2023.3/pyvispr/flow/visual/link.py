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

from PyQt6.QtCore import QPoint, QPointF
from PyQt6.QtCore import Qt as constant_e
from PyQt6.QtGui import QColor, QPainterPath, QPen
from PyQt6.QtWidgets import QGraphicsPathItem, QMenu

from pyvispr.flow.visual.node import node_t
from pyvispr.resource.appearance.geometry import button_width_c

horizontal_shift_c = 3 * button_width_c

pen_for_empty_c = QPen(QColor(255, 0, 0), 2, constant_e.PenStyle.SolidLine)
pen_for_full_c = QPen(QColor(0, 255, 0), 2, constant_e.PenStyle.SolidLine)


@dtcl.dataclass(slots=True, repr=False, eq=False)
class link_t(QGraphicsPathItem):
    should_show_info_boxes: h.ClassVar[bool] = True

    source_node: node_t
    target_node: node_t
    source_point: QPointF | None = None
    target_point: QPointF | None = None
    # TODO: Currently, not used.
    # functional: dict[str, str] = dtcl.field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        """"""
        # Otherwise, complaint about super-init not having been called.
        QGraphicsPathItem.__init__(self)

        self.SetPath(self.source_point, self.target_point)
        self.setPen(pen_for_empty_c)

    # @property
    # def info_text(self):
    #     """"""
    #     text = ""
    #     for link in self.underlying_links:
    #         text += link[0] + "->" + link[1] + "\n"
    #
    #     return text[:-1]

    def SetPath(self, source_point: QPointF, target_point: QPointF, /) -> None:
        """"""
        self.source_point = source_point
        self.target_point = target_point

        direction = self.target_point - self.source_point

        dir_1 = 0.4 * direction
        dir_2 = 0.4 * direction

        dir_1.setY(0)
        if dir_1.x() < 0:
            dir_1.setX(-dir_1.x())
        if dir_1.x() < horizontal_shift_c:
            dir_1.setX(horizontal_shift_c)

        dir_2.setY(0)
        if dir_2.x() < 0:
            dir_2.setX(-dir_2.x())
        if dir_2.x() < horizontal_shift_c:
            dir_2.setX(horizontal_shift_c)

        path = QPainterPath(self.source_point)
        path.cubicTo(
            self.source_point + dir_1, self.target_point - dir_2, self.target_point
        )
        self.setPath(path)

    def UnderlyingFunctionals(self) -> tuple[tuple[str, str], ...]:
        """"""
        output = []

        source = self.source_node.functional
        target = self.target_node.functional
        for output_name, sockets in source.links.items():
            output.extend(
                (output_name, _elm[1]) for _elm in sockets if _elm[0] is target
            )

        return tuple(output)

    def LinksToBeRemoved(
        self, position: QPoint, /
    ) -> tuple[tuple[str, str] | None, bool] | None:
        """
        /!\ strange behavior (Qt bug): sometimes a mouse press on a different link (or even in the background)
        calls the mousePressEvent callback of the previously pressed link; and this repeats several times,
        until clicking far away from any link!!!
        """
        underlying_links = self.UnderlyingFunctionals()

        menu = QMenu()
        cancel_action = menu.addAction("Close Menu")
        no_action = menu.addAction("or Remove Link(s):")
        no_action.setEnabled(False)

        menu_actions = len(underlying_links) * [None]
        for link_idx, link in enumerate(underlying_links):
            menu_actions[link_idx] = menu.addAction(link[0] + "->" + link[1])
        if underlying_links.__len__() > 1:
            all_action = menu.addAction("Remove All")
            menu_actions.append(all_action)
        else:
            all_action = None

        selected_action = menu.exec(position)

        if (selected_action is None) or (selected_action is cancel_action):
            return None

        if selected_action is all_action:
            return None, True

        return (
            underlying_links[menu_actions.index(selected_action)],
            len(underlying_links) == 1,
        )
