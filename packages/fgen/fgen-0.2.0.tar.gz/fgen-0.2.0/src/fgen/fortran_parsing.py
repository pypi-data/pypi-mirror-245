"""
Support for parsing Fortran type declarations

We just want to make this as helpful as possible when auto-generating our wrappers while keeping the
implemenation here as minimal as possible because duplicating the Fortran implementation logic is
not the point of this module. The fortran compiler will catch any odd type declarations at
compile-time.

To understand what is going on, we start with the syntax for declaring fortran types as defined in
Section 5.1 of the `Fortran 2003 standard <https://j3-fortran.org/doc/year/04/04-007.pdf>`_.
It looks like the below:

.. syntax higlighting below is wrong, not sure what language the specs are given in
.. code-block:: fortran

    R501 type-declaration-stmt  is declaration-type-spec [ [ , attr-spec ] ... :: ] entity-decl-list
    R502 declaration-type-spec  is intrinsic-type-spec
                                or TYPE ( derived-type-spec )
                                or CLASS ( derived-type-spec )
                                or CLASS ( * )

In short, a type declaration statement is composed of a declaration type specification, a collection
of one or more attribute specifications and then an entity declaration list. The declaration type
specification can be either an intrinsic type that has been defined by the language, or a derived
type which has been declared using a ``type`` block elsewhere.

We focus on the combination of the declaration type specification (which we typically shorten to
type specification) and the attribute specifications i.e. we largely ignore the entity declarations.
In the absence of a defined term in the Fortran standard, we call this combination the type
attribute declaration throughout.

To illustrate, consider the following example

.. code-block:: fortran

    real(8), dimension(3), pointer :: heat_uptake

Here is how we would refer to the parts of this example:

- type declaration statement: ``real(8), dimension(3), pointer :: heat_uptake``
- declaration type specification (or simply type specification): ``real(8)``
- attribute specifications: ``dimension(3), pointer``
- type attribute declaration: ``real(8), dimension(3), pointer``
- entity declaration (largely ignored by this module, we treat the double colon ``::`` as part of
  the entity declaration): ``:: heat_uptake``

One other example using a derived type

.. code-block:: fortran

    type(my_calculator) :: heat_uptake_calculator

Here is how we would refer to the parts of this example:

- type declaration statement: ``type(my_calculator) :: heat_uptake_calculator``
- declaration type specification (or simply type specification): ``type(my_calculator)``
- attribute specifications: none
- type attribute declaration (same as type specification in this case): ``type(my_calculator)``
- entity declaration (largely ignored by this module, we treat the double colon ``::`` as part of
  the entity declaration): ``:: heat_uptake_calculator``

Notes
-----
Fortran type declaration statements (and Fortran in general) are case-insensitive

This module relies heavily on regular expressions. If needed, use an online tool like
`regex101.com <https://regex101.com/>`_ to help you understand them.
"""
from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Any, Optional, Union

from attrs import define, field

_AT_LEAST_ONE_ALPHANUMERIC_REGEXP: str = r"[a-z0-9]+"
"""Regex representing a search for at least one alphanumeric character"""

_DIMENSION_SPECIFICATION: str = f"(\\*|:|{_AT_LEAST_ONE_ALPHANUMERIC_REGEXP})"
"""
Regex representing a possible dimension attribute specification in a Fortran definition

This also captures deferred and assumed shaped arrays which are not currently supported by fgen, but may
be supported in future.

e.g. "(4, 3)", "(n, m)", "(5)", "(n, 4)"
"""

_DIMENSION_REGEX: str = (
    r"DIMENSION\("
    r"(?P<dimension>"
    f"{_DIMENSION_SPECIFICATION}(,\\s*{_DIMENSION_SPECIFICATION})*"
    ")"
    r"\)"
)
"""
Regex string used to check for dimension information within attribute specifications

e.g. "dimension(4, 3)", "dimension(n)"
"""

_KIND_SPECIFICATION: str = r"(\(.*\)|)$"
"""
Regex string to capture optional type modifiers

e.g. "(kind=8)" in "real(kind=8)"
"""

_INTRINSIC_TYPE_SPECIFICATIONS: tuple[str, ...] = (
    "INTEGER",
    "REAL",
    "DOUBLE PRECISION",
    "COMPLEX",
    "CHARACTER",
    "LOGICAL",
)
"""Intrinsic Fortran type specifications that we support (case insensitive)"""

_DERIVED_TYPE_REGEX: str = r"type\(\s?(?P<derived_type_name>[a-z]+)\s?\)"
"""
Regex string to capture derived type specifications

Matches things like "type(my_derived_type)" and "type(calculator)". The derived type
is captured in a group called "derived_type_name". We currently don't support "class(abc)"
specifications.
"""

SUPPORTED_TYPE_SPECIFICATIONS: tuple[str, ...] = (
    *[
        f"^{intrinsic_type_spec}{_KIND_SPECIFICATION}"
        for intrinsic_type_spec in _INTRINSIC_TYPE_SPECIFICATIONS
    ],
    _DERIVED_TYPE_REGEX,
)
"""
The collection of valid type specifications that are supported

This covers both intrinsic type specifications and derived type specifications.
"""


SUPPORTED_ATTRIBUTE_SPECIFICATIONS: tuple[Union[str, re.Pattern[str]], ...] = (
    "ALLOCATABLE",
    # "ASYNCHRONOUS",
    _DIMENSION_REGEX,
    # "INTENT",
    # "INTRINSIC",
    # "language-binding-spec"
    # "OPTIONAL",
    "POINTER",
    # "PROTECTED",
    # "SAVE",
    "TARGET",
    # "VALUE",
    # "VOLATILE",
)
"""
The collection of valid attribute specifications that are supported

In the type declaration, "type(my_calculator), pointer", the attribute specification is "pointer"
(the other part, "type(my_calculator)", is simply the type specification
(or declaration type specification if you're being very precise))

Note that only a subset of valid attributes can be specified. The more esoteric attributes have been excluded
until the use case for these attributes is better understood.
"""


def _get_type_attribute_declaration(type_declaration_statement: str) -> str:
    """
    Get type attribute declaration from a type declaration statement

    Simply removes the entity declaration
    """
    return type_declaration_statement.split("::")[0]


def _get_parts(type_declaration_statement: str) -> tuple[str, tuple[str, ...]]:
    """
    Split a type declaration statement into a type specification and a collection of attribute specifications

    This function is used below by :meth:`FortranDataType.as_str`. That method takes care of validating
    the different parts of a Fortran type declaration statement.

    See the docstring of :mod:`fgen.fortran_parsing` for further details on how we interpret Fortran
    type declaration statements.

    Parameters
    ----------
    type_declaration_statement
        Type declaration statement to parse

        The entity declaration component (any parts including and after the "::") is optional
        and will be ignored

    Returns
    -------
        The type specification and any additional attribute specifications

    Examples
    --------
    >>> _get_parts("real :: my_variable")
    ('real', ())
    >>> _get_parts("real, dimension(5)")
    ('real', ('dimension(5)',))
    >>> _get_parts("real, dimension(5, 3)")
    ('real', ('dimension(5, 3)',))
    >>> _get_parts("integer, dimension(:, :)")
    ('integer', ('dimension(:, :)',))
    >>> _get_parts("logical, dimension(2, :)")
    ('logical', ('dimension(2, :)',))
    >>> _get_parts("logical, dimension(2, :), pointer")
    ('logical', ('dimension(2, :)', 'pointer'))
    """
    type_attribute_declaration = _get_type_attribute_declaration(
        type_declaration_statement
    )

    part_regexp_including_brackets = r"[^,\s]+(?:\([^\(]*?\))"
    part_regexp_no_brackets = r"[^,\s]+"
    part_regexp: str = "|".join(
        [part_regexp_including_brackets, part_regexp_no_brackets]
    )
    """
    Regular expression that captures the parts of the type declaration statement

    It effectively just splits the string into comma separated pieces without
    surrounding whitespace (with a little extra piece to make sure you don't
    get nested brackets (e.g. "dimension((4, 3))") in any part, which is invalid
    Fortran as far as we know anyway)

    e.g. this can be used to split "real, dimension(2, 3, 4)"
    into ["real", "dimension(2, 3, 4)"]
    """
    parts = re.findall(part_regexp, type_attribute_declaration)

    if not len(parts):
        raise ValueError(  # noqa: TRY003
            f"An invalid type attribute declaration was provided: {type_attribute_declaration!r}"
        )

    # The Fortran spec states that the first part must be the type specification and
    # the rest are attribute specifications so we can safely assume order here
    return parts[0], tuple(parts[1:])


def _validate_fortran_type_attribute_declaration(
    type_specification: str, attribute_specifications: tuple[str, ...]
) -> None:
    """
    Validate that a fortran type attribute declaration is supported by fgen

    The type attribute declaration must have been split (using e.g. :func:`_get_parts`) before using
    this function.

    We don't support all valid fortran. See the examples below and the tests for examples of
    supported options.

    This validation is pretty crude as invalid Fortran will be caught at compile time.

    See the docstring of :mod:`fgen.fortran_parsing` for further details on how we interpret Fortran
    type declaration statements.

    Parameters
    ----------
    type_specification
        Type specification

    attribute_specifications
        Attribute specifications

        See :data:`SUPPORTED_ATTRIBUTE_SPECIFICATIONS` for the attributes that are currently supported by fgen

    Raises
    ------
    ValueError
        An unsupported fortran type specification is supplied

    Examples
    --------
    Below are some examples of (split) fortran type declarations that pass

    >>> _validate_fortran_type_attribute_declaration("integer", ())
    >>> _validate_fortran_type_attribute_declaration("real", ("dimension(5)",))
    >>> _validate_fortran_type_attribute_declaration(
    ...     "type(calculator)", ("dimension(5)", "pointer")
    ... )

    See Also
    --------
    :func:`_get_parts`
    """
    # Any attributes must match the regex of a supported attribute
    if not any(
        re.match(supported_type, type_specification, flags=re.IGNORECASE)
        for supported_type in SUPPORTED_TYPE_SPECIFICATIONS
    ):
        raise ValueError(  # noqa: TRY003
            f"Unsupported type specification: {type_specification}"
        )

    # Any attributes must match the regex of a supported attribute
    for attribute_specification in attribute_specifications:
        if not any(
            re.match(attribute_regex, attribute_specification, flags=re.IGNORECASE)
            for attribute_regex in SUPPORTED_ATTRIBUTE_SPECIFICATIONS
        ):
            raise ValueError(  # noqa: TRY003
                f"Unsupported attribute specification: {attribute_specification}"
            )


def _convert_complex_attribute_specifications(
    attribute_specifications: Sequence[str],
) -> tuple[Union[str, DimensionAttributeSpecification], ...]:
    """
    Convert any complex attribute specifications to their supporting classes

    For example, a dimension attribute specification is converted to a
    :class:`DimensionAttributeSpecification` which holds additional information about the attribute.
    If the attribute specification doesn't have a matching class than it will remain as a string.

    Parameters
    ----------
    attribute_specifications
        Collection of attribute specifications

    Returns
    -------
        Tuple that contains a combination of strings and classes in the case of the more
        complicated attributes
    """
    attributes: list[Union[str, DimensionAttributeSpecification]] = list(
        attribute_specifications
    )

    for i in range(len(attribute_specifications)):
        match = re.search(
            _DIMENSION_REGEX, attribute_specifications[i], flags=re.IGNORECASE
        )
        if match:
            attributes[i] = DimensionAttributeSpecification.from_dimension_info(
                match.group("dimension")
            )

    return tuple(attributes)


@define
class DimensionAttributeSpecification:
    """
    Dimension attribute specification

    Defines the shape of a data type. See Section 5.1.2.5 of the
    `Fortran 2003 standard <https://j3-fortran.org/doc/year/04/04-007.pdf>`_ for a description of the
    dimension attribute specification.

    Currently, we only support explicit dimensions where the size of the dimension is explicitly declared
    at compile-time with an integer or execution-time using a variable provided to a procedure (e.g. using
    "n" which is a variable that is also provided to a procedure).
    The later form is an automatic explicit dimension and will rely upon the Fortran compiler to validate the
    attribute declaration since additional context is required about where the attribute is used.

    Assumed-sized dimensions ("*") are not currently supported.
    """

    dimensions: tuple[Union[str, int], ...] = field()
    """
    Collection of dimensions of the attribute specification

    Can include explicit dimensions (e.g. 5) or automatic explicit dimensions (e.g. "n"). Deferred
    dimensions (e.g. ":") are allowed.
    """

    @dimensions.validator
    def _check_dimensions(
        self, attribute: Any, value: tuple[Union[str, int], ...]
    ) -> None:
        for dimension in value:
            if dimension == "*":
                raise ValueError(  # noqa: TRY003
                    "Assumed-sized dimensions are not supported"
                )

    @classmethod
    def from_dimension_info(
        cls, dimension_info: str
    ) -> DimensionAttributeSpecification:
        """
        Create a DimensionAttributeSpecification from the dimension information

        The dimension information describes the shape and dimensionality of a variable.

        Parameters
        ----------
        dimension_info
            The dimension information is the content between the () for a dimension attribute. For example,
            for an attribute "dimension(8, n)" the dimension_info would be `"8, n"`.

            Static dimensions are converted to integers before initialising.

        Returns
        -------
            New DimensionAttributeSpecification
        """
        toks = dimension_info.split(",")

        type_info: list[Union[str, int]] = []
        for tok in toks:
            try:
                size: int | str = int(tok)
            except ValueError:
                # assume : or n or something i.e. not static size
                size = tok.strip()

            type_info.append(size)

        return DimensionAttributeSpecification(dimensions=tuple(type_info))

    @property
    def ndim(self) -> int:
        """
        Number of dimensions of the attribute
        """
        return len(self.dimensions)

    def __str__(self) -> str:
        dimensions_as_str = ", ".join(str(dim) for dim in self.dimensions)
        return f"dimension({dimensions_as_str})"


def _get_python_type_with_dimensions(
    dimension_info: Sequence[Union[str, int]],
    base: str,
) -> str:
    """
    Get a Python type that supports dimension information

    See [#1](https://gitlab.com/magicc/fgen/-/issues/1) for ongoing discussions about updating this
    to return more sophisticated Python types

    Parameters
    ----------
    dimension_info
        Dimension information (e.g. extracted elsewhere from a Fortran type declaration statement)

    base
        Base Python type to which the dimension information applies (e.g. "float", "int", "str")

    Returns
    -------
        Python type with dimension information

    Examples
    --------
    >>> _get_python_type_with_dimensions([2], "float")
    'tuple[float, float]'
    >>> _get_python_type_with_dimensions(["n"], "int")
    'tuple[int, ...]'
    >>> _get_python_type_with_dimensions([2, 3], "float")
    'tuple[tuple[float, float, float], tuple[float, float, float]]'
    >>> _get_python_type_with_dimensions([2, 1], "float")
    'tuple[tuple[float], tuple[float]]'
    >>> _get_python_type_with_dimensions(["n", "m", 2], "Quantity")
    'tuple[tuple[tuple[Quantity, Quantity], ...], ...]'
    """

    def _dimension(inner_type: str, dimension_len: Union[int, str]) -> str:
        if isinstance(dimension_len, str):
            content = [inner_type, "..."]
        else:
            content = [inner_type] * dimension_len

        return f"tuple[{', '.join(content)}]"

    # Start with base
    res = base

    # then wrap dimension information on top as it applies
    for dim in dimension_info[::-1]:
        res = _dimension(res, dim)

    return res


@define
class FortranDataType:
    """
    A fortran data type including its attributes

    See the docstring of :mod:`fgen.fortran_parsing` for further details on Fortran type declaration
    statements and how we handle and describe them.

    We are only interested in the type attribute declaration so anything including and after a "::"
    should be stripped before initialising this class.
    """

    type_specification: str
    """
    This can be either an intrinsic type, or a derived type.

    For example, "real(8)", "logical", "type(my_calculator)"
    """

    attribute_specifications: tuple[
        Union[str, DimensionAttributeSpecification], ...
    ] = field()
    """
    List of attribute specifications that apply to the Fortran data type

    These are our internal representation of attribute specifications e.g. "pointer", "target",
    "dimension(3, 3)"
    """

    @attribute_specifications.validator
    def _check_attribute_specifications(
        self,
        attribute: Any,
        value: tuple[Union[str, DimensionAttributeSpecification], ...],
    ) -> None:
        dimension_count = sum(
            isinstance(a, DimensionAttributeSpecification) for a in value
        )
        if dimension_count > 1:
            raise ValueError(  # noqa: TRY003
                "More than one dimension attribute specification (can Fortran be compiled with "
                "more than one dimension attribute specification?)"
            )

    @classmethod
    def from_str(cls, fortran_type_attribute_declaration: str) -> FortranDataType:
        """
        Create :obj:`FortranDataType` from type declaration statement

        Parses and validates a type declaration statement

        Parameters
        ----------
        fortran_type_attribute_declaration
            Fortran type declaration statement e.g. "real(8), dimension(2) :: heat_uptake_sensitivity"

            The entity declaration component (including and after "::") is ignored hence is optional.

            See the docstring of :mod:`fgen.fortran_parsing` for further details.

        Raises
        ------
        ValueError
            The type declaration statement is invalid
        """
        type_specification, attribute_specifications = _get_parts(
            fortran_type_attribute_declaration
        )
        _validate_fortran_type_attribute_declaration(
            type_specification, attribute_specifications
        )

        return cls(
            type_specification=type_specification,
            attribute_specifications=_convert_complex_attribute_specifications(
                attribute_specifications
            ),
        )

    @property
    def fortran_type_attribute_declaration(self) -> str:
        """
        Fortran type attribute declaration, including attribute specifications if applicable.

        See the docstring of :mod:`fgen.fortran_parsing` for further details.
        """
        if not self.attribute_specifications:
            return self.type_specification

        attribute_specifications = ", ".join(
            str(item) for item in self.attribute_specifications
        )
        return f"{self.type_specification}, {attribute_specifications}"

    def __str__(self) -> str:
        return self.fortran_type_attribute_declaration

    @property
    def equivalent_python_type(self) -> str:
        """
        Python type-hint for the data type

        The "base" type of the equivalent Python type will be:

        * `str` for `character`-based types
        * `bool` for `logical`-based types
        * `pint.Quantity` for other intrinsic types such as `real` and `integer`
        * a custom type for (Fortran) derived types

        If the Fortran type has a "dimension" attribute specification, this modifies the "base" type
        to a `tuple` that respects the intended shape of the value. n-dimensional variables are supported.
        """
        base_type = self._base_python_type()
        dimension_attribute_specification = (
            self._get_dimension_attribute_specification()
        )

        if base_type != "Quantity" and dimension_attribute_specification:
            # Pint doesn't support dimension attributes so we only do this if the Python type is not
            # a pint type
            return _get_python_type_with_dimensions(
                dimension_attribute_specification.dimensions, base_type
            )

        return base_type

    def _base_python_type(self) -> str:
        """
        Determine the "base" Python type that represents the Fortran type declaration

        This focuses on the base type (float, int etc.) and ignores the modification of this type
        from attributes such as "dimension" (which mean the 'full' python type is some sort of array
        or iterable). Such dimension handling is done in :attr:`~equivalent_python_type`.

        Returns
        -------
            The string representation of the python type that is equivalent to the base type
            (i.e. ignoring any array or other container) of ``self``
        """
        if self.is_derived_type():
            match = re.match(
                _DERIVED_TYPE_REGEX, self.type_specification, flags=re.IGNORECASE
            )
            if not match:
                raise ValueError(  # noqa: TRY003
                    f"Could not determine python type for {self.type_specification}"
                )

            return match.group("derived_type_name").strip()

        else:
            tsl = self.type_specification.lower()

            if tsl.startswith("real"):
                return "float"

            if tsl.startswith("integer"):
                return "int"

            if tsl.startswith("character"):
                return "str"

            if tsl.startswith("logical"):
                return "bool"

            if tsl.startswith("complex"):
                msg = (
                    "We have not yet worked out how to support "
                    f"{self.type_specification}, please raise an issue"
                )
                raise NotImplementedError(msg)

            raise ValueError(self.type_specification)

    def is_derived_type(self) -> bool:
        """
        Check if the fortran type is a derived type

        Returns
        -------
            True if a type is a derived type, False if it is an intrinsic type
        """
        return self.type_specification.startswith("type(")

    def is_deferred_array(self) -> bool:
        """
        Check if the fortran type is an array with at least one deferred dimension
        """
        dim_attrs = self._get_dimension_attribute_specification()

        if dim_attrs is None:
            return False
        return ":" in dim_attrs.dimensions

    def _get_dimension_attribute_specification(
        self,
    ) -> Optional[DimensionAttributeSpecification]:
        """
        Get the dimension attribute of the type if it exists

        Returns
        -------
            The dimension attribute if it is present otherwise None
        """
        for attr in self.attribute_specifications:
            if isinstance(attr, DimensionAttributeSpecification):
                # there can only be one dimension attribute so as soon as we
                # find it, we can stop looking
                return attr

        return None
