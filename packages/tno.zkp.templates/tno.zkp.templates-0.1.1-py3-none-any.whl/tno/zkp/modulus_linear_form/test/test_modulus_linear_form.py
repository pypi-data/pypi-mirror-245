"""
File to test the functionality of the modulus linear form
"""

from __future__ import annotations

import pytest

from tno.zkp.modulus_linear_form import LinearFormInput, ModulusLinearForm


def test_modulus_linear_form(linear_form: ModulusLinearForm) -> None:
    """
    Check if the modulus linear form returns the expected result. The expected result is the
    summation 1+2+3...n modulo n+2

    :param linear_form: ModulusLinearForm with coefficients 1...n and modulo n+2
    """
    n = linear_form.input_size
    ones_input = [1 for _ in range(n)]
    linear_form_input = LinearFormInput(ones_input)
    # summation of 1 until length modulo (n+2)
    result = linear_form.evaluate(linear_form_input)
    # 1+2+3...n=n*(n+1)/2
    summation_result = int(n * (n + 1) / 2)
    expected_result = summation_result % (n + 2)
    assert result.value == expected_result


def test_adding_forms_together(linear_form: ModulusLinearForm) -> None:
    """
    Check if two linear form are added correctly by adding the linear form to itself. The addition
    of the two linear forms results in a new linear form with coefficients 2...2*n and modulo n+2

    :param linear_form: ModulusLinearForm with coefficients 1...n and modulo n+2
    """
    # double all the coefficients
    linear_form = linear_form + linear_form
    n = linear_form.input_size
    ones_input = [1 for _ in range(n)]
    linear_form_input = LinearFormInput(ones_input)
    # summation of coefficients
    result = linear_form.evaluate(linear_form_input)
    # 2+4+6...2*n
    summation_result = sum(range(2, n * 2 + 1, 2))
    expected_result = summation_result % (n + 2)
    assert result.value == expected_result


@pytest.mark.parametrize("constant", [*range(1, 10)])
def test_multiply_form_with_constant_together(
    linear_form: ModulusLinearForm, constant: int
) -> None:
    """
    Check if two linear form multiply with a constant correctly. The multiplication results in a
    new linear form with coefficients c,2c,3c...c*n and modulo n+2

    :param linear_form: ModulusLinearForm with coefficients 1...n and modulo n+2
    :param constant: Multiplication factor for the linear form
    """
    # double all the coefficients
    linear_form = linear_form * constant
    n = linear_form.input_size
    ones_input = [1 for _ in range(n)]
    linear_form_input = LinearFormInput(ones_input)
    # summation of coefficients
    result = linear_form.evaluate(linear_form_input)
    # c+2c+3c...c*n
    summation_result = sum(range(constant, n * constant + 1, constant))
    expected_result = summation_result % (n + 2)
    assert result.value == expected_result


def test_splitting_form(linear_form: ModulusLinearForm) -> None:
    """
    Split a linear form in two halves. The left half will be prepended with a 0 coefficient if the
    length of the linear form is odd.

    :param linear_form: ModulusLinearForm with coefficients 1...n and modulo n+2
    """
    left_half, right_half = linear_form.split_in_half()
    odd = linear_form.input_size % 2 != 0
    n = linear_form.input_size
    half_n = right_half.input_size
    ones_input = [1 for _ in range(half_n)]
    linear_form_input = LinearFormInput(ones_input)

    # check the right result
    right_result = right_half.evaluate(linear_form_input)
    # n/2+(n/2+1)...n
    start = half_n if odd else half_n + 1
    right_summation = sum(range(start, n + 1))
    right_expected_result = right_summation % (n + 2)
    assert right_result.value == right_expected_result

    # check the left result
    left_result = left_half.evaluate(linear_form_input)
    # 1+2+3...floor(n/2)
    end = half_n if odd else half_n + 1
    left_summation = sum(range(end))
    left_expected_result = left_summation % (n + 2)
    assert left_result.value == left_expected_result


def test_equality(linear_form: ModulusLinearForm) -> None:
    """
    Check if two linear forms are determined to be equal if they have the same coefficients and
    modulus. If they are not the same the equality should fail.

    :param linear_form: ModulusLinearForm with coefficients 1...n and modulo n+2
    """

    # same coefficients and modulus
    coefficients = [*range(1, linear_form.input_size + 1)]
    new_linear_form = ModulusLinearForm(coefficients, linear_form.input_size + 2)
    assert new_linear_form == linear_form

    # different modulus
    new_linear_form = ModulusLinearForm(coefficients, linear_form.input_size)
    assert new_linear_form != linear_form

    # different coefficients
    coefficients = [*range(2, linear_form.input_size + 2)]
    new_linear_form = ModulusLinearForm(coefficients, linear_form.input_size + 2)
    assert new_linear_form != linear_form
