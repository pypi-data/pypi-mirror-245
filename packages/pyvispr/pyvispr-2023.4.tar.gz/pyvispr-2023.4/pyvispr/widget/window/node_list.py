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

from re import search as SearchRegEx
from typing import cast

import PyQt6.QtGui as gui
import PyQt6.QtWidgets as wdgt
from PyQt6.QtCore import Qt as constant_e
from PyQt6.QtCore import pyqtBoundSignal

from pyvispr.catalog.main import NODE_CATALOG
from pyvispr.widget.general.style import GetSelectionBackgroundRGB

style_c = "QListView::item:hover{{background-color: rgb({}, {}, {}); color: white;}}"
col_size_padding_c = 20

_ORANGE_BRUSH = gui.QBrush(gui.QColor("orange"))
_RED_BRUSH = gui.QBrush(gui.QColor("red"))


class node_list_wgt_t(wdgt.QListWidget):
    def __init__(self) -> None:
        """"""
        super().__init__()
        self.setSelectionMode(wdgt.QAbstractItemView.SelectionMode.NoSelection)
        self.setStyleSheet(style_c.format(*GetSelectionBackgroundRGB()))

        self.filter_wgt = wdgt.QLineEdit()
        self.filter_wgt.setPlaceholderText("Filter nodes")
        self.filter_wgt.setClearButtonEnabled(True)
        cast(pyqtBoundSignal, self.filter_wgt.textEdited).connect(self._Filter)

        self.Reload()

    def Reload(self) -> None:
        """"""
        self.clear()

        for node_description in NODE_CATALOG:
            self.addItem(node_description.name)
            if (
                node_description.misses_hints
                and not node_description.misses_in_out_prms
            ):
                self.item(self.count() - 1).setForeground(_ORANGE_BRUSH)
            elif node_description.misses_in_out_prms:
                self.item(self.count() - 1).setForeground(_RED_BRUSH)

        self.sortItems()

        self.setFixedWidth(self.sizeHintForColumn(0) + col_size_padding_c)

    @property
    def node_names(self):
        return NODE_CATALOG.node_names

    def _Filter(self, new_filter: str, /) -> None:
        """"""
        if len(new_filter) > 0:
            matched_items = self.findItems(
                new_filter, constant_e.MatchFlag.MatchContains
            )

            for item_idx in range(self.count()):
                node_item = self.item(item_idx)
                node_description = NODE_CATALOG.NodeDescription(node_item.text())

                if node_description.keywords is None:
                    mismatches_key_xpressions = True
                else:
                    mismatches_key_xpressions = (
                        new_filter not in node_description.keywords
                    )

                if node_description.short_description is None:
                    mismatches_short_description = True
                else:
                    mismatches_short_description = (
                        SearchRegEx(
                            "\b" + new_filter + "\b", node_description.short_description
                        )
                        is None
                    )

                if (
                    (node_item not in matched_items)
                    and mismatches_key_xpressions
                    and mismatches_short_description
                ):
                    node_item.setHidden(True)
                else:
                    node_item.setHidden(False)
        else:
            for item_idx in range(self.count()):
                self.item(item_idx).setHidden(False)
