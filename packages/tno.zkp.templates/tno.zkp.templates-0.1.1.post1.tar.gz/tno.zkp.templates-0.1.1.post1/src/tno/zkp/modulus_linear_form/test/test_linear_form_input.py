"""
Test cases for the linear form input
"""

from __future__ import annotations

import pytest

from tno.zkp.modulus_linear_form import LinearFormInput


@pytest.fixture(
    name="linear_form_input", params=[1, 2, 3, 6, 10, 20, 50, 100, 200, 500, 1000]
)
def fixture_linear_form_input(request: pytest.FixtureRequest) -> LinearFormInput:
    """
    Create a linear form input of length n with values 1...n

    :param request: pytest fixture request with parameter for the length of the input
    :return: LinearFormInput of length n with values 1...n
    """
    return LinearFormInput([*range(1, request.param + 1)])


def test_linear_form_output_addition(linear_form_input: LinearFormInput) -> None:
    """
    Addition of two linear form inputs results in a new linear form input with the result being
    an array where element i is x_i+y_i.

    :param linear_form_input: LinearFormInput of 1,2,3...n, where n is the input length
    """
    result = linear_form_input + linear_form_input
    for i, z_i in enumerate(result.input_vector):
        assert (
            z_i == linear_form_input.input_vector[i] + linear_form_input.input_vector[i]
        )


def test_linear_form_input_different_length(linear_form_input: LinearFormInput) -> None:
    """
    If the modulus of two linear form inputs are of differet length during addition the shortest is
    prepended with zeros.

    :param linear_form_input: LinearFormInput of 1,2,3...n, where n is the input length
    """
    result = linear_form_input + LinearFormInput(linear_form_input.input_vector + [1])
    assert result.input_vector[0] == linear_form_input.input_vector[0]
    for i, z_i in enumerate(result.input_vector[1:-1]):
        assert (
            z_i
            == linear_form_input.input_vector[i] + linear_form_input.input_vector[i + 1]
        )
    assert result.input_vector[-1] == linear_form_input.input_vector[-1] + 1


def test_linear_form_input_multiplication(linear_form_input: LinearFormInput) -> None:
    """
    Multiplication of a linear form input results in a new linear form input with the result being
    an array with value i being c*x_i, where c is the constant to multiply with and x is the input
    array.

    :param linear_form_input: LinearFormInput of 1,2,3...n, where n is the input length
    """
    result = linear_form_input * 3
    for i, z_i in enumerate(result.input_vector):
        assert z_i == linear_form_input.input_vector[i] * 3
