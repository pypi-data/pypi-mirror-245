"""
Test case for the standard sigma protocol. The standard sigma protocol is tested using the linear form
from the init file.
"""
from tno.zkp.modulus_linear_form import ModulusLinearForm

from tno.zkp.templates import StandardSigmaProtocol


def test_standard_sigma_protocol(linear_form: ModulusLinearForm) -> None:
    """
    Test case to check the standard sigma protocol.

    :param linear_form: The linear form used to test the sigma protocol
    """
    random_input = linear_form.random_input()
    sigma_protocol = StandardSigmaProtocol.generate_proof(
        linear_form, random_input, "sha256"
    )
    assert sigma_protocol.verify()

    # check a standard sigma protocol fails if the response is incorrect.
    sigma_protocol._response = linear_form.random_input()
    assert not sigma_protocol.verify()
