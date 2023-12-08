from __future__ import annotations

import random

import pytest

from tno.zkp.modulus_linear_form import LinearFormOutput


@pytest.fixture(
    name="linear_form_output", params=[1, 2, 3, 6, 10, 20, 50, 100, 200, 500, 1000]
)
def fixture_linear_form_output(request: pytest.FixtureRequest) -> LinearFormOutput:
    value = request.param
    return LinearFormOutput(value, value + 5)


def test_linear_form_output_addition(linear_form_output: LinearFormOutput) -> None:
    """
    Addition of two linear form output results in a new linear form output with the result being
    value_1+value_2 modulo m, where value_i and modulo are stored in the LinearFormOutput and the
    modulo is the same.

    :param linear_form_output: LinearFormOutput where the modulus is the value + 5
    """
    value = linear_form_output.value
    random_value = random.randint(0, value + 5)
    linear_form_output_2 = LinearFormOutput(random_value, value + 5)
    result = linear_form_output_2 + linear_form_output
    assert result.value == (random_value + value) % (value + 5)


def test_linear_form_output_different_modulus(
    linear_form_output: LinearFormOutput,
) -> None:
    """
    If the modulus of two linear form outputs are different during addition an exception is expected.

    :param linear_form_output: LinearFormOutput where the modulus is the value + 5
    """
    with pytest.raises(ValueError) as excp:
        linear_form_output + LinearFormOutput(
            linear_form_output.value, linear_form_output.modulus + 1
        )
        assert "The modulus must be the same between linear form outputs" == str(
            excp.value
        )


def test_linear_form_output_multiplication(
    linear_form_output: LinearFormOutput,
) -> None:
    """
    Multiplication of a linear form output results in a new linear form output with the result being
    r*value modulo m, where value and modulo are stored in the LinearFormOutput and the r is a
    random value with which the LinearFormOutput is multiplied

    :param linear_form_output: LinearFormOutput where the modulus is the value + 5
    """
    value = linear_form_output.value
    random_value = random.randint(0, value + 5)
    result = random_value * linear_form_output
    assert result.value == (random_value * value) % (value + 5)


def test_linear_form_output_equality(linear_form_output: LinearFormOutput) -> None:
    """
    Two linear form output are determined equal if they have the same value and modulus. This test
    checks if the equality function adheres to this and rejects values with either a different value
    or modulus.

    :param linear_form_output: LinearFormOutput where the modulus is the value + 5
    """
    value = linear_form_output.value
    assert LinearFormOutput(value, value + 5) == linear_form_output
    assert LinearFormOutput(value, value + 3) != linear_form_output
    assert LinearFormOutput(value + 1, value + 5) != linear_form_output
