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

import importlib as mprt
import inspect as spct
import typing as h
from types import ModuleType as module_t

import docstring_parser as dcst

from pyvispr.catalog.constants import (
    ACTUAL_SOURCE,
    HINT_PLACEHOLDER,
    MISSING_IN_HINTS,
    MISSING_IN_INDICATORS,
    MISSING_IN_OUT_NAME_PREFIX,
    MISSING_OUT_HINT_INDICATOR,
    NODE_NAME,
)
from pyvispr.catalog.main import CATALOG_FOLDER

signature_t = spct.Signature
parameter_t = spct.Parameter

parameter_h = tuple[str, str]
parameter_w_default_h = tuple[str, str, h.Any]
parameters_h = list[parameter_h | parameter_w_default_h]
returns_h = list[parameter_h]
documentation_h = tuple[str, str, parameters_h, returns_h]
function_record_h = tuple[str, signature_t, tuple[bool, ...], bool, documentation_h]


UNSPECIFIED_PRM_KIND = (parameter_t.VAR_POSITIONAL, parameter_t.VAR_KEYWORD)


def InstallModuleFunctions(module_name: str, /, *, recursively: bool = False) -> None:
    """"""
    functions = AllFunctions(module_name, recursively=recursively)
    for function in functions:
        (
            full_name,
            signature,
            missing_in_indicators,
            missing_out_indicator,
            documentation,
        ) = function
        node_name = full_name.replace(".", " ").title().replace(" ", "")

        inputs = []
        missing_in_hints = []
        for p_idx, (parameter, missing) in enumerate(
            zip(signature.parameters.values(), missing_in_indicators)
        ):
            if missing:
                name = f"{MISSING_IN_OUT_NAME_PREFIX}{p_idx}"
                if parameter.kind is parameter_t.VAR_KEYWORD:
                    default = " = None"
                else:
                    default = ""
                missing_in_hints.append(name)
                inputs.append(f'{name}: "{HINT_PLACEHOLDER}"{default}')
            else:
                name = parameter.name
                hint = parameter.annotation
                if hint is parameter_t.empty:
                    hint = f': "{HINT_PLACEHOLDER}"'
                    missing_in_hints.append(name)
                elif isinstance(hint, str):
                    hint = f': "{hint}"'
                else:
                    # TODO: This is temporary since hint can also be a real hint like Any, not only a type.
                    hint = f": {hint.__name__}"
                default = parameter.default
                if default is parameter_t.empty:
                    default = ""
                elif isinstance(default, str):
                    default = f' = "{default}"'
                elif isinstance(default, type):
                    default = f" = {default.__name__}"
                elif str(default)[0] == "<":
                    default = f" = {type(default).__name__}"
                else:
                    default = f" = {default}"
                inputs.append(f"{name}{hint}{default}")
        inputs = ", ".join(inputs)

        if missing_out_indicator:
            outputs = f'"{HINT_PLACEHOLDER}"'
        else:
            outputs = signature.return_annotation
        outputs = f" -> {outputs}"

        missing_comments = []
        if any(missing_in_indicators):
            missing_comments.append(
                f"    {MISSING_IN_INDICATORS}: {missing_in_indicators}"
            )
        if missing_in_hints.__len__() > 0:
            missing_in_hints = ", ".join(missing_in_hints)
            missing_comments.append(f"    {MISSING_IN_HINTS}: {missing_in_hints}")
        if missing_out_indicator:
            missing_comments.append(f"    {MISSING_OUT_HINT_INDICATOR}: True")
        if missing_comments.__len__() > 0:
            missing_comments = "\n" + "\n".join(missing_comments)
        else:
            missing_comments = ""

        as_str = f'''
def Main({inputs}){outputs}:
    """
    {NODE_NAME}: {node_name}
    {ACTUAL_SOURCE}: {full_name}{missing_comments}
    """
    pass
'''

        where = CATALOG_FOLDER
        for piece in full_name.split("."):
            where /= piece
        where = where.with_suffix(".py")

        where.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        with open(where, "w") as accessor:
            accessor.write(as_str[1:])


def AllFunctions(
    module_name: str, /, *, recursively: bool = False
) -> tuple[function_record_h, ...]:
    """"""
    module = mprt.import_module(module_name)
    if recursively:
        output = []
        modules = []
        _AllFunctionsRecursively(f"{module_name}.", module, modules, output)
    else:
        output = _AllFunctions(module_name, module)
        if output.__len__() == 0:
            modules = []
            _AllFunctionsRecursively(f"{module_name}.", module, modules, output)

    return tuple(output)


def _AllFunctions(module_name: str, module: module_t, /) -> list[function_record_h]:
    """"""
    output = []

    for name in dir(module):
        if name[0] == "_":
            continue

        element = getattr(module, name)
        if (is_function := spct.isfunction(element)) or hasattr(element, "__call__"):
            if is_function:
                function = element
            else:
                function = element.__call__
            output.append(_FunctionRecord(module_name, name, function))

    return output


def _AllFunctionsRecursively(
    prefix: str,
    module: module_t,
    modules: list[module_t],
    output: list[function_record_h],
    /,
) -> None:
    """"""
    modules.append(module)

    for name, element in spct.getmembers(
        module, lambda _arg: spct.ismodule(_arg) or spct.isfunction(_arg)
    ):
        # Explicitly defined: spct.getmodule(function) == module
        if name[0] == "_":
            continue

        if spct.ismodule(element):
            if element not in modules:
                _AllFunctionsRecursively(prefix, element, modules, output)
        elif module.__name__.startswith(prefix):
            output.append(_FunctionRecord(module.__name__, name, element))


def _FunctionRecord(
    module_name: str, function_name: str, function, /
) -> function_record_h:
    """"""
    signature = spct.signature(function)
    missing_in_indicators = tuple(
        _prm.kind in UNSPECIFIED_PRM_KIND for _prm in signature.parameters.values()
    )
    missing_out_indicator = signature.return_annotation is signature_t.empty
    documentation = spct.getdoc(function)
    documentation = _ParsedDocumentation(documentation)

    return (
        f"{module_name}.{function_name}",
        signature,
        missing_in_indicators,
        missing_out_indicator,
        documentation,
    )


def _ParsedDocumentation(documentation: str, /) -> documentation_h:
    """"""
    parsed = dcst.parse(documentation)

    parameters = []
    for parameter in parsed.params:
        if parameter.is_optional:
            parameters.append(
                (parameter.arg_name, parameter.type_name, parameter.default)
            )
        else:
            parameters.append((parameter.arg_name, parameter.type_name))

    returns = []
    for parameter in parsed.many_returns:
        returns.append((parameter.return_name, parameter.type_name))

    return parsed.short_description, parsed.long_description, parameters, returns


if __name__ == "__main__":
    #
    MODULE = "numpy"
    InstallModuleFunctions(MODULE)
