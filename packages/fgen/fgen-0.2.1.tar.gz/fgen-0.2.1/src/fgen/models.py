"""
Configuration models

These models describe the configuration that are used by this package and describe the schema used to
serialize and validate configuration that is loaded.

Each module that is being wrapped is represented using a :class:`ModuleDefinition` and can be loaded from
disk using :func:`load_module_definition`.
"""
from __future__ import annotations

from typing import Any, Optional, TypeVar

from attrs import define, field, fields, validators
from cattrs.preconf.pyyaml import make_converter

from .fortran_parsing import FortranDataType

T = TypeVar("T")

converter = make_converter(detailed_validation=False, forbid_extra_keys=True)


@define
class ValueDefinition:
    """
    Definition of a value

    This defines the value's unit, Fortran data type and other metadata. It also allows us to get the
    equivalent Python type.

    The following built-in Fortran types are supported:

    * integer
    * real
    * real(8)
    * character

    Some additional attributes are supported including:

    * fixed length dimensions
    * automatic explicit length dimensions (e.g. using a variable "n" to specify the size of a dimension)
    """

    name: str
    description: str
    fortran_type: str = field(validator=[validators.instance_of(str)])
    unit: Optional[str] = field(default=None)
    """
    Unit of the value

    The unit must be able to parsed by `pint` and present in the :attr:`~fgen.units.unit_registry`. Some
    examples include: "ppm", "1 / month".

    A unit is required for all numeric-types (i.e. integer, real, complex). For non-numeric values, the unit
    is unused.
    """
    expose_to_python: bool = True
    truncated_name: Optional[str] = None

    @unit.validator
    def _check_unit(self, attribute: Any, value: str | None) -> None:
        pt = self.python_type_as_str()
        if value is None and any(t in pt for t in ["float", "int"]):
            raise ValueError(f"A unit is required for: {self.name}")  # noqa: TRY003

    @fortran_type.validator
    def _check_fortran_type(self, attribute: Any, value: str) -> None:
        try:
            FortranDataType.from_str(value)
        except Exception as exc:
            raise ValueError(  # noqa: TRY003
                f"Unsupported fortran type: {value}"
            ) from exc

    def as_fortran_data_type(self) -> FortranDataType:
        """
        Convert ``self`` to its equivalent ``FortranDataType``
        """
        return FortranDataType.from_str(self.fortran_type)

    def python_type_as_str(self) -> str:
        """
        Determine the string representation of the Python type

        The python templator uses this function to translate a Python
        type to a string so that it can correctly be read by Python.
        If these type hints are converted to a string naively, the
        corresponding string will not be able to be read by Python as a valid type hint.

        Returns
        -------
            String representation of :attr:`python_type`
        """
        return self.as_fortran_data_type().equivalent_python_type


def _add_name(inp: dict[str, dict[str, str]], cls: type[dict[str, T]]) -> dict[str, T]:
    """
    Add the name to attributes and methods automatically

    This avoids having to write schemas like

    .. ::code-block

    Attributes
    ----------
          k:
            name: k
            description: something

    Methods
    -------
          calculate:
            name: calculate
            description: something else

    Instead we can just write

    .. ::code-block

    Attributes
    ----------
          k:
            description: something

    Methods
    -------
          calculate:
            description: something else

    Where the name is inferred automatically
    """
    value_type = cls.__args__[1]  # type: ignore

    res = {}

    if inp is None:
        raise ValueError(f"Unexpected None when structuring {cls}")  # noqa: TRY003

    for k, v in inp.items():
        for f in fields(value_type):
            if str(f.type).startswith("dict") and v.get(f.name) is None:
                raise ValueError(  # noqa: TRY003
                    f"{f.name!r} in {k!r} is None but a dict was expected: {v}"
                )
        if "name" in v:
            if v["name"] != k:
                raise ValueError(  # noqa: TRY003
                    f"Inconsistent name for value: {k!r} and {v['name']!r}"
                )
        res[k] = converter.structure({"name": k} | v, value_type)

    return res


converter.register_structure_hook_func(
    lambda t: t == dict[str, ValueDefinition], _add_name
)


@define
class MethodDefinition:
    """
    Definition of a Fortran method

    This method is assumed to be part of a `Calculator` (See: :class:`CalculatorDefinition`) and used
    to perform an action on the Calculator.

    This function can have multiple :attr:`parameters` and a single, optional
    :attr:`returns` value.
    """

    name: str
    """Name of the function in Fortran"""
    description: str
    """Description of what the function does"""
    parameters: dict[str, ValueDefinition]
    """Collection of named parameters of the function"""
    returns: Optional[ValueDefinition]
    """Return value of the function"""

    def units(self) -> dict[str, str]:
        """
        Units used in the method

        Includes units from of the parameters and the return value.

        Raises
        ------
        ValueError
            If different units are supplied for a given parameter name

        Returns
        -------
            Collection of parameter names and associated units
        """
        res = {key: parameter.unit for key, parameter in self.parameters.items()}

        if self.returns:
            k = self.returns.name
            if k in res and res[k] != self.returns.unit:
                raise ValueError(  # noqa: TRY003
                    f"Inconsistent units for attribute '{k}'. In the input parameters it "
                    f"has units '{res[k]}' whereas in the returns it has units '{self.returns.unit}'"
                )

            res[self.returns.name] = self.returns.unit

        # Drop any None units
        return {k: v for k, v in res.items() if v is not None}


converter.register_structure_hook_func(
    lambda t: t == dict[str, MethodDefinition], _add_name
)


@define
class CalculatorDefinition:
    """
    Definition of a calculator

    TODO: document concepts
    """

    name: str
    description: str
    attributes: dict[str, ValueDefinition]
    methods: dict[str, MethodDefinition]

    def exposed_attributes(self) -> dict[str, ValueDefinition]:
        """
        Get the attributes that are marked to be exposed to python

        Returns
        -------
            Collection of exposed attributes
        """
        return dict(
            filter(lambda item: item[1].expose_to_python, self.attributes.items())
        )

    def units(self) -> dict[str, str]:
        """
        Get the unit for each declared value in the calculator

        The unit for a given named value must be consistent across the calculator.
        This includes the unit for ``attributes``, and in the ``parameter`` and
        ``return`` values for each ``method``.

        Raises
        ------
        ValueError
            Inconsistent units were found

        Returns
        -------
            Dictionary containing value names' as keys and the associated units
            as values.
        """
        # We are tracking the units for each unique `ValueDefinition.name` in `unit_sources`
        # For each name we keep track of a tuple containing the method name where
        # the unit was declared and the unit

        # Collect units from the attributes
        # For calculator attributes the "method name" is None
        # Dropping any None's
        unit_sources: dict[str, tuple[Optional[str], str]] = {
            key: (None, attr.unit)
            for key, attr in self.attributes.items()
            if attr.unit is not None
        }

        # Collect units from the methods
        for method_name, method in self.methods.items():
            method_units = method.units()

            # Check that the method units are consistent with any previous declared units
            for name, method_unit in method_units.items():
                if name in unit_sources and unit_sources[name][1] != method_unit:
                    # Inconsistent unit declarations found

                    previous_source, previous_value = unit_sources[name]
                    if previous_source is not None:
                        previous_source_type = "method"
                    else:
                        previous_source_type = "calculator"
                        previous_source = self.name

                    raise ValueError(  # noqa: TRY003
                        f"Inconsistent units for attribute '{name}'. "
                        f"In the method '{method_name}' it has units '{method_unit}' whereas in the "
                        f"{previous_source_type} '{previous_source}' it has units '{previous_value}'"
                    )
                unit_sources[name] = (method_name, method_unit)
        return {key: value[1] for key, value in unit_sources.items()}

    def has_any_attribute_deferred_array(self) -> bool:
        """
        Identify whether any attribute is related to a deferred array

        Only looks at attributes that are to be exposed to Python

        Returns
        -------
            ``True`` if any attribute is related to a deferred array, otherwise
            ``False``
        """
        return any(
            attr.as_fortran_data_type().is_deferred_array()
            for attr in self.exposed_attributes().values()
        )


@define
class LinkDefinition:
    """
    Reference to another wrapped module

    These links are used to define the references to other wrapped modules when generating the wrappers.

    We don't currently validate these at generation-time. If they are wrong the module with fail to compile or
    in the case of an incorrect :attr:`~python_module` will raise an ImportError at run-time.
    """

    provides: str
    """
    Name of the calculator defined in the target wrapper
    """

    fortran_module: str
    """
    Name of the fortran module that contains the definition of the calculator

    This should be the same as :attr:`ModuleDefinition.name`.
    """

    python_module: str
    """
    Name of the python module that exposes the calculator

    This module should declare a class that is named the same as the value of :attr:`~provides`.
    """


@define
class ModuleDefinition:
    """
    Definition of a Fortran Module

    It is assumed that each fortran module defines a single Calculator

    TODO: document concepts
    """

    name: str
    description: str
    provides: CalculatorDefinition
    prefix: str = "mod_"
    truncated_name: Optional[str] = None
    links: list[LinkDefinition] = field(factory=list)

    @property
    def wrapper_module_name(self) -> str:
        """
        Name for the Fortran wrapper module

        By default the module name is derived from the :attr:`name`, but in
        some cases, the complete module name can be too long leading to the
        wrapper module not being able to be built. In this case a
        :attr:`truncated_name` can be used to derive a shorted module name.
        Given that this module is only used by autogenerated code the
        readability of the name isn't as important as the full module.
        """
        return f"w_{self.truncated_name or self.short_name}"

    @property
    def short_name(self) -> str:
        """
        Short module name

        Some fortran modules have a prefix, typically `"mod_"` which isn't used in all cases
        when referring to the module, e.g. when writing filenames. ``short_name``
        removes this prefix if it is there.

        Returns
        -------
            Shortened module name
        """
        if self.name.startswith(self.prefix):
            return self.name[len(self.prefix) :]
        return self.name


def load_module_definition(filename: str) -> ModuleDefinition:
    """
    Read a YAML module definition file

    This module definition contains a description of the Fortran module that
    is being wrapped.

    Parameters
    ----------
    filename
        Filename to read

    Returns
    -------
        Loaded module definition
    """
    with open(filename, encoding="utf-8") as fh:
        txt = fh.read()

    return converter.loads(txt, ModuleDefinition)
