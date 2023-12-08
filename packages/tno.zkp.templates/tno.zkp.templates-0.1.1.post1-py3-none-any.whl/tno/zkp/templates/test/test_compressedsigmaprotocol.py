"""
Test cases for the compression mechanism of the sigma protocols.
"""
import re

import pytest

from tno.zkp.modulus_linear_form import ModulusLinearForm

from tno.zkp.templates import StandardSigmaProtocol, compression, full_compression


def test_compressing_sigma_protocol(linear_form: ModulusLinearForm) -> None:
    """
    Testcase for the compression of the sigma protocol.

    :param linear_form: Linear form ti use as homomorphism
    """
    random_input = linear_form.random_input()
    sigma_protocol = StandardSigmaProtocol.generate_proof(
        linear_form, random_input, "sha256"
    )
    assert sigma_protocol.verify()

    if linear_form.input_size == 1:
        # input size  less or equal to 1 throws an exception
        expected_message = (
            "Sigma protocol can not be compressed, input size is less or equal to "
            "1 (1)"
        )
        with pytest.raises(ValueError, match=re.escape(expected_message)):
            compression(sigma_protocol)
        return

    homomorphism_size = sigma_protocol.homomorphism.input_size
    compressed = compression(sigma_protocol)
    assert compressed.homomorphism.input_size < homomorphism_size
    homomorphism_size = compressed.homomorphism.input_size
    assert compressed.verify()

    while compressed.homomorphism.input_size > 1:
        compressed = compression(compressed)
        assert compressed.homomorphism.input_size < homomorphism_size
        homomorphism_size = compressed.homomorphism.input_size
        assert compressed.verify()

    assert compressed.homomorphism.input_size == 1


def test_fully_compressing_sigma_protocol(linear_form: ModulusLinearForm) -> None:
    """
    Testcase for full compression of the sigma protocol.

    :param linear_form: Linear form to use as homomorphism
    """
    random_input = linear_form.random_input()
    sigma_protocol = StandardSigmaProtocol.generate_proof(
        linear_form, random_input, "sha256"
    )
    assert sigma_protocol.verify()
    if linear_form.input_size == 1:
        # input size  less or equal to 1 throws an exception
        expected_message = (
            "Sigma protocol can not be compressed, input size is less or equal to "
            "1 (1)"
        )
        with pytest.raises(ValueError, match=re.escape(expected_message)):
            full_compression(sigma_protocol)
        return
    compressed = full_compression(sigma_protocol)
    assert compressed.homomorphism.input_size == 1
    assert compressed.verify()
