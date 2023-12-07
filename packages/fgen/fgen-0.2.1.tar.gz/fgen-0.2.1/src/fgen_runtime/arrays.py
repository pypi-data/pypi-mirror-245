"""
Handle the translation of a fortran pointer into a numpy array
"""
import functools
import re
from typing import Any

import numpy as np
from numpy.typing import NDArray

KIND_REGEX = r"\((?:kind=)?([1-8])\)"
"""Regex for extracting the kind information from a type specification

Only supports real, integer, logical and double precision types where "kind" is the only
available argument.
"""


def _ctype_ndarray(element_type: Any, shape: tuple[int, ...]) -> Any:
    """
    Create a ndarray of the given element type and shape

    This took some inspiration from np.ctypeslib
    """
    for dim in shape:
        element_type = dim * element_type
        # prevent the type name include np.ctypeslib
        element_type.__module__ = None
    return element_type


def _ptr_to_ndarray(ptr: int, dtype: str, shape: tuple[int, ...]) -> NDArray[Any]:
    """
    Convert a c pointer for a fortran array into a numpy array

    Any changes made to the numpy array will change the same memory used by fortran
    """
    ctype_scalar = np.ctypeslib.as_ctypes_type(dtype)
    result_type = _ctype_ndarray(ctype_scalar, shape)
    result = result_type.from_address(ptr)

    d = np.ascontiguousarray(result).T

    if d.__array_interface__["data"] != (ptr, False):
        raise AssertionError(  # noqa: TRY003
            "Pointer has been incorrectly cast to a numpy array"
        )

    return d


@functools.lru_cache(128)
def ftype_to_np(type_specification: str) -> str:
    """
    Convert a fortran type specification into a numpy dtype

    Only supports logical, integer and real types.

    Parameters
    ----------
    type_specification
        Type specification

        See :mod:`fgen.fortran_parsing` for more information about fortran type specifications

    Returns
    -------
        A numpy equivalent dtype (where possible)

    Raises
    ------
    ValueError
        If the dtype cannot be parsed
    """
    supported_types = {"real": "f", "integer": "i", "logical": "b"}
    # Assumes no additional compiler flags are specified
    # https://gcc.gnu.org/onlinedocs/gfortran/KIND-Type-Parameters.html
    default_kind = 4

    tokens = type_specification.split("(")

    try:
        f_type = tokens[0]

        np_type = supported_types[f_type]
    except KeyError as exc:
        raise ValueError(  # noqa: TRY003
            f"Unsupported type: {type_specification}"
        ) from exc

    if len(tokens) > 1:
        match = re.search(
            # Strip out any whitespace before checking
            KIND_REGEX,
            type_specification.replace(" ", ""),
            flags=re.IGNORECASE,
        )
        if match:
            kind = match.group(1)
        else:
            raise ValueError("Could not determine kind information")  # noqa: TRY003

        if f_type == "real" and int(kind) not in [4, 8]:
            raise ValueError("real only supports 4 and 8 byte types")  # noqa: TRY003
    else:
        kind = default_kind

    return f"{np_type}{kind}"
