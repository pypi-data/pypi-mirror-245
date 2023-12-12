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

import ast as prsr
import dataclasses as dtcl
import importlib as mprt
import inspect as spct
from enum import Enum as enum_t
from pathlib import Path as path_t
from types import ModuleType as module_t
from typing import Any, Callable

from conf_ini_g.phase.specification.parameter.type import type_t
from str_to_obj.type.hint import any_hint_h

from pyvispr.catalog.constants import (
    ACTUAL_SOURCE,
    FUNCTION_NAME,
    MISSING_IN_HINTS,
    MISSING_IN_INDICATORS,
    MISSING_IN_OUT_NAME_PREFIX,
    MISSING_OUT_HINT_INDICATOR,
    NODE_NAME,
    OUTPUT_NAMES,
)
from pyvispr.flow.descriptive.socket import (
    ASSIGN_WHEN_ACTIVATING,
    VALUE_NOT_SET,
    assign_when_importing_t,
    assignment_e,
    input_t,
)
from pyvispr.python.module import ModuleForPath


class source_e(enum_t):
    not_set = 0
    local = 1
    referenced = 2
    system = 3


@dtcl.dataclass(slots=True, repr=False, eq=False)
class node_t:
    path: str | path_t
    name: str = ""
    keywords: str = ""
    short_description: str = ""
    long_description: str = ""
    source: source_e = source_e.not_set
    function_name: str | None = None
    missing_in_indicators: tuple[bool, ...] | None = None
    missing_in_hints: tuple[str, ...] | None = None
    inputs: dict[str, input_t] | None = None
    outputs: dict[str, any_hint_h | str | assign_when_importing_t | None] | None = None
    #
    module: module_t | None = None
    Function: Callable[..., Any] | None = None

    def __post_init__(self) -> None:
        """"""
        if self.name.__len__() > 0:
            return

        if isinstance(self.path, str):
            self.path = path_t(self.path)
        self.path = self.path.expanduser()
        with open(self.path) as accessor:
            tree = prsr.parse(accessor.read())
        for node in prsr.walk(tree):
            if not isinstance(node, prsr.FunctionDef) or (node.name[0] == "_"):
                continue

            documentation = prsr.get_docstring(node, clean=False)

            (
                self.name,
                actual,
                self.function_name,
                output_names,
                self.missing_in_indicators,
                missing_in_hints,
                missing_out_hint_indicator,
                assignments,
            ) = _N_A_F_A(documentation, node.name)
            if actual is None:
                self.source = source_e.local
            elif actual.endswith(".py"):
                self.source = source_e.referenced
                self.path = path_t(actual)
            else:
                self.source = source_e.system
                self.path = actual

            if self.missing_in_indicators is None:
                inputs = {}
                arguments_sets = node.args
                for arguments, defaults in (
                    (
                        arguments_sets.posonlyargs,
                        arguments_sets.posonlyargs.__len__() * (VALUE_NOT_SET,),
                    ),
                    (arguments_sets.args, arguments_sets.defaults),
                    (arguments_sets.kwonlyargs, arguments_sets.kw_defaults),
                ):
                    for argument, default in zip(arguments, defaults):
                        assignment = assignments.get(argument.arg, "link")
                        assignment = assignment_e[assignment]

                        if default is not VALUE_NOT_SET:
                            default = ASSIGN_WHEN_ACTIVATING

                        inputs[argument.arg] = input_t(
                            assignment=assignment,
                            default_value=default,
                        )
                self.inputs = inputs

            if missing_in_hints is not None:
                self.missing_in_hints = _SplitAndStriped(missing_in_hints, ",")

            if missing_out_hint_indicator is None:
                outputs = node.returns.value
                if outputs is None:
                    assert output_names is None
                    self.outputs = {}
                elif output_names is None:
                    pass
                else:
                    self.outputs = {
                        _elm.strip(): ASSIGN_WHEN_ACTIVATING
                        for _elm in output_names.split(",")
                    }
            elif output_names is None:
                pass
            else:
                # TODO: Explain what None means.
                self.outputs = {_elm.strip(): None for _elm in output_names.split(",")}

            break  # Use the first function whose name does not start with "_".

    @property
    def misses_hints(self) -> bool:
        """"""
        return (
            (self.missing_in_hints is not None)
            or (self.outputs is None)
            or any(_elm is None for _elm in self.outputs.values())
        )

    @property
    def misses_in_out_prms(self) -> bool:
        """"""
        return (
            (self.inputs is None)
            or any(
                _elm.startswith(MISSING_IN_OUT_NAME_PREFIX)
                for _elm in self.inputs.keys()
            )
            or (self.outputs is None)
            or any(
                _elm.startswith(MISSING_IN_OUT_NAME_PREFIX)
                for _elm in self.outputs.keys()
            )
        )

    @property
    def n_inputs(self) -> int:
        """"""
        return self.inputs.__len__()

    @property
    def input_names(self) -> tuple[str, ...]:
        """"""
        return tuple(self.inputs.keys())

    @property
    def input_types(self) -> tuple[any_hint_h | str, ...]:
        """"""
        return tuple(_elm.type for _elm in self.inputs.values())

    @property
    def n_outputs(self) -> int:
        """"""
        return self.outputs.__len__()

    @property
    def output_names(self) -> tuple[str, ...]:
        """"""
        return tuple(self.outputs.keys())

    @property
    def output_types(self) -> tuple[any_hint_h | str, ...]:
        """"""
        return tuple(self.outputs.values())

    def Activate(self) -> None:
        """"""
        if self.module is not None:
            return

        if self.source is source_e.system:
            self.module, self.Function = _M_F_FromPyPath(self.path)
        else:  # source_e.local or source_e.referenced
            self.module, self.Function = _M_F_FromPathAndName(
                self.path, self.function_name
            )

        signature = spct.signature(self.Function)

        if self.inputs is None:
            raise RuntimeError("User must be asked to complete signature.")
        else:
            parameters = signature.parameters
            for name in self.inputs:
                parameter = parameters[name]
                # TODO: if self.inputs[name].type is ASSIGN_WHEN_ACTIVATING, Always True, right?
                self.inputs[name].type = type_t.NewFromTypeHint(parameter.annotation)
                if self.inputs[name].default_value is ASSIGN_WHEN_ACTIVATING:
                    self.inputs[name] = parameter.default

        if (self.outputs is None) or any(
            _elm is None for _elm in self.outputs.values()
        ):
            raise RuntimeError("User must be asked to complete signature.")
        elif self.outputs.__len__() > 0:
            hint = type_t.NewFromTypeHint(signature.return_annotation)
            if hint.type is tuple:
                hints = hint.elements
            else:
                hints = (hint,)
            assert hints.__len__() == self.outputs.__len__(), (
                self.name,
                hints,
                self.outputs,
            )
            for name, hint in zip(self.outputs, hints):
                self.outputs[name] = hint


def _N_A_F_A(
    documentation: str, function_name: str, /
) -> tuple[
    str, str | None, str, str | None, str | None, str | None, str | None, dict[str, str]
]:
    """
    Returned "description" on last position should be interpreted as assignment types of the inputs.
    """
    description = documentation.strip().splitlines()
    description = dict(_SplitAndStriped(_lne, ":") for _lne in description)

    function_name = description.get(FUNCTION_NAME, function_name)
    node_name = description.get(NODE_NAME, function_name)

    return (
        node_name,
        description.get(ACTUAL_SOURCE),
        function_name,
        description.get(OUTPUT_NAMES),
        description.get(MISSING_IN_INDICATORS),
        description.get(MISSING_IN_HINTS),
        description.get(MISSING_OUT_HINT_INDICATOR),
        description,
    )


def _M_F_FromPathAndName(path: str, function_name: str, /) -> tuple[module_t, Callable]:
    """"""
    # TODO: Add error management.
    module = ModuleForPath(path_t(path))
    Function = getattr(module, function_name)

    return module, Function


def _M_F_FromPyPath(py_path: str, /) -> tuple[module_t, Callable]:
    """"""
    # TODO: Add error management.
    last_dot_idx = py_path.rfind(".")
    module = mprt.import_module(py_path[:last_dot_idx])
    Function = getattr(module, py_path[(last_dot_idx + 1) :])

    return module, Function


def _SplitAndStriped(text: str, separator: str, /) -> tuple[str, str] | tuple[str, ...]:
    """"""
    return tuple(_elm.strip() for _elm in text.split(sep=separator))


# from inspect import getdoc as GetFunctionDoc
# from inspect import signature as GetFunctionSignature
# signature = GetFunctionSignature(function)
# documentation = GetFunctionDoc(function)
