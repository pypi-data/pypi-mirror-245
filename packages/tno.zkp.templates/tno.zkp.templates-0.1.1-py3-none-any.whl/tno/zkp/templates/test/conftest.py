"""
Fixtures to use in all test files
"""
import random as rand
import sys

import pytest
import sympy

from tno.zkp.modulus_linear_form import ModulusLinearForm


@pytest.fixture(
    name="linear_form", params=[1, 2, 3, 6, 10, 20, 50, 100, 200, 500, 1000]
)
def fixture_modulus_linear_form(request: pytest.FixtureRequest) -> ModulusLinearForm:
    """
    Generate a ModulusLinearForm of length $n$. Where $n$ is taken from the request parameter. The
    coefficients used are chosen at random. The modulus is a random prime.

    :param request: request with parameters
    :return: ModulusLinearForm of length$n$
    """
    random_prime = sympy.ntheory.generate.randprime(0, sys.maxsize)
    length = request.param
    random_values = [rand.randint(0, random_prime) for _ in range(0, length)]
    return ModulusLinearForm(random_values, random_prime)
