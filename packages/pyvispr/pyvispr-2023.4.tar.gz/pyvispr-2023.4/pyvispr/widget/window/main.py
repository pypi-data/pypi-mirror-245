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

from os.path import dirname as ExtractPathPart
from pathlib import Path as path_t
from typing import cast

import PyQt6.QtWidgets as wdgt
from PyQt6.QtCore import Qt as constant_e
from PyQt6.QtCore import pyqtBoundSignal

from pyvispr import __version__
from pyvispr.flow.visual.container import container_t
from pyvispr.flow.visual.graph import graph_t
from pyvispr.flow.visual.link import link_t
from pyvispr.flow.visual.node import node_t
from pyvispr.widget.general.menu import AddEntryToMenu
from pyvispr.widget.window.node_list import node_list_wgt_t


class pyflow_wdw_t(wdgt.QMainWindow):
    workflow_extension = "pyvispr"

    def __init__(self) -> None:
        """"""
        super().__init__()

        home_folder = path_t.home()
        self.last_install_from_location = home_folder
        self.last_save_location = home_folder
        self.last_load_location = home_folder
        self.last_save_as_script_location = home_folder

        self.setWindowTitle("pyVispr")

        self.graph = graph_t()
        self.graph_container = container_t(self.graph)
        self.node_list_wgt = node_list_wgt_t()

        cast(pyqtBoundSignal, self.node_list_wgt.itemClicked).connect(
            self.AddNodeToGraph
        )

        node_list_lyt = wdgt.QVBoxLayout()
        node_list_lyt.addWidget(self.node_list_wgt)
        node_list_lyt.addWidget(self.node_list_wgt.filter_wgt)
        node_list_lyt.setAlignment(constant_e.AlignmentFlag.AlignTop)

        graph_container_lyt = wdgt.QVBoxLayout()
        graph_container_lyt.addWidget(self.graph_container)
        graph_container_lyt.setAlignment(constant_e.AlignmentFlag.AlignTop)

        main_layout = wdgt.QHBoxLayout()
        main_layout.addLayout(node_list_lyt)
        main_layout.addLayout(graph_container_lyt, 3)

        main_container = wdgt.QWidget(self)
        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

        # self.statusBar()
        self._AddMenuBar()

    def _AddMenuBar(self) -> None:
        """"""
        menu_bar = self.menuBar()

        menu = menu_bar.addMenu("py&Vispr")
        AddEntryToMenu(menu, self, "Get Info", self.OpenAboutDialog)
        AddEntryToMenu(menu, self, "Configure", self.OpenConfiguration)
        menu.addSeparator()
        AddEntryToMenu(
            menu, self, "&Quit", lambda checked_u: self.close(), shortcut="Ctrl+Q"
        )

        menu = menu_bar.addMenu("&Workflow")
        AddEntryToMenu(
            menu,
            self,
            "&Run",
            self.RunWorkflow,
            shortcut="Ctrl+R",
        )
        menu.addSeparator()
        AddEntryToMenu(menu, self, "&Save", self.SaveWorkflowToFile, shortcut="Ctrl+S")
        AddEntryToMenu(
            menu, self, "L&oad", self.LoadWorkflowFromFile, shortcut="Ctrl+O"
        )
        menu.addSeparator()
        AddEntryToMenu(menu, self, "Save As Script", self.SaveWorkflowAsScript)
        menu.addSeparator()
        submenu = menu.addMenu("Reset...")
        AddEntryToMenu(
            submenu,
            self,
            "Now",
            lambda checked_u: self.graph.functional.InvalidateAllNodes(),
        )
        submenu = menu.addMenu("Clear...")
        AddEntryToMenu(submenu, self, "Now", lambda checked_u: self.graph.Clear())

        menu = menu_bar.addMenu("&View")
        submenu = menu.addMenu("Show Info Boxes...")
        AddEntryToMenu(
            submenu,
            self,
            "For Nodes (toggle)",
            pyflow_wdw_t.ToggleShowInfoBoxesForNodes,
            checkable=True,
            checked=node_t.should_show_info_boxes,
        )
        AddEntryToMenu(
            submenu,
            self,
            "For Links (toggle)",
            pyflow_wdw_t.ToggleShowInfoBoxesForLinks,
            checkable=True,
            checked=link_t.should_show_info_boxes,
        )
        AddEntryToMenu(
            menu,
            self,
            "Merged Ins/Outs (toggle)",
            self.ToggleMergedInsOutsPresentation,
            checkable=True,
        )

        menu = menu_bar.addMenu("&Catalog")
        AddEntryToMenu(
            menu,
            self,
            "Refresh",
            lambda checked_u: self.node_list_wgt.Reload(),
        )

    @staticmethod
    def ToggleShowInfoBoxesForNodes(checked: bool) -> None:
        node_t.should_show_info_boxes = checked

    @staticmethod
    def ToggleShowInfoBoxesForLinks(checked: bool) -> None:
        link_t.should_show_info_boxes = checked

    def ToggleMergedInsOutsPresentation(self, checked: bool):
        """"""
        if checked:
            wdgt.QMessageBox.about(
                cast(wdgt.QWidget, self), "Merged Ins/Outs", "Merged Ins/Outs: YES\n"
            )
        else:
            wdgt.QMessageBox.about(
                cast(wdgt.QWidget, self), "Merged Ins/Outs", "Merged Ins/Outs: NO\n"
            )

    def AddNodeToGraph(self, item, /) -> None:
        """"""
        self.graph.AddNode(item.text())
        # self.graph_container.ensureVisible(self.graph.nodes[-1], xMargin=0, yMargin=0)

    def RunWorkflow(self) -> None:
        """"""
        self.graph.Run()
        # for node in self.graph.nodes:
        #     node.state_btn.setBrush(BUTTON_BRUSH_STATE_DONE)

    def SaveWorkflowToFile(self, _: bool, /):
        """"""
        filename = wdgt.QFileDialog.getSaveFileName(
            cast(wdgt.QWidget, self),
            "Save Workflow",
            str(self.last_save_location),
            "pyVispr Workflows (*." + pyflow_wdw_t.workflow_extension + ")",
        )
        if (filename is None) or (len(filename[0]) == 0):
            return
        filename = filename[0]

        self.last_save_location = ExtractPathPart(filename)
        self.last_load_location = self.last_save_location

        self.graph.SaveToFile(filename)

    def LoadWorkflowFromFile(self, _: bool, /):
        """"""
        filename = wdgt.QFileDialog.getOpenFileName(
            cast(wdgt.QWidget, self),
            "Load Workflow",
            str(self.last_load_location),
            "pyVispr Workflows (*." + pyflow_wdw_t.workflow_extension + ")",
        )
        if (filename is None) or (len(filename[0]) == 0):
            return
        filename = filename[0]

        self.last_load_location = ExtractPathPart(filename)

        n_nodes = len(self.graph.nodes)
        if n_nodes > 0:
            loading_question_wdw = wdgt.QMessageBox(self)
            loading_question_wdw.setWindowTitle("Loading Options")
            loading_question_wdw.setText(
                "About to load a workflow while the current workflow is not empty\nLoading options are:"
            )
            # merge_option_btn_u = loading_question_wdw.addButton(
            #     "Merge Workflows", wdgt.QMessageBox.YesRole
            # )
            # del merge_option_btn_u # /!\ why deleting the button? seen in a forum answer???
            replace_option_btn = loading_question_wdw.addButton(
                "Replace Workflow", wdgt.QMessageBox.ButtonRole.NoRole
            )

            loading_question_wdw.exec()

            if loading_question_wdw.clickedButton() == replace_option_btn:
                node_idx_offset = 0
                self.graph.Clear()
            else:
                node_idx_offset = n_nodes
        else:
            node_idx_offset = 0

        self.graph.LoadFromFile(filename, node_idx_offset)

    def SaveWorkflowAsScript(self, _: bool, /):
        """"""
        filename = wdgt.QFileDialog.getSaveFileName(
            cast(wdgt.QWidget, self),
            "Save Workflow as Script",
            str(self.last_save_as_script_location),
            "Python Scripts (*.py)",
        )
        if (filename is None) or (len(filename[0]) == 0):
            return
        filename = filename[0]

        self.last_save_as_script_location = ExtractPathPart(filename)

        self.graph.SaveAsScript(filename)

    def OpenAboutDialog(self, _: bool, /) -> None:
        """"""
        wdgt.QMessageBox.about(
            cast(wdgt.QWidget, self), "About pyVispr", f"pyVispr {__version__}\n"
        )

    def OpenConfiguration(self, _: bool, /) -> None:
        """"""
        wdgt.QMessageBox.about(
            cast(wdgt.QWidget, self),
            "pyVispr Configuration",
            "No configuration options yet\n",
        )
