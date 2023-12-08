"""
Fixtures to use in all test files
"""
import pytest

from tno.zkp.modulus_linear_form import ModulusLinearForm


@pytest.fixture(
    name="linear_form", params=[1, 2, 3, 6, 10, 20, 50, 100, 200, 500, 1000]
)
def fixture_modulus_linear_form(request: pytest.FixtureRequest) -> ModulusLinearForm:
    """
    Generate a ModulusLinearForm of length $n$. Where $n$ is taken from the request parameter. The
    coefficients are taken from the range[1,length]. The modulus is equal to the length+2.

    :param request: request with parameters
    :return: ModulusLinearForm of length $n$
    """
    length = request.param
    random_values = [i for i in range(1, length + 1)]
    return ModulusLinearForm(random_values, modulus=length + 2)
