"""
Compression mechanism which transforms a SigmaProtocol into a CompressedSigmaProtocol.
The compressed sigma protocol contains fewer elements in the input vector and is therefore more
performant in evaluation.
"""
from __future__ import annotations

import itertools
import logging
from typing import TYPE_CHECKING

from tno.zkp.templates.homomorphism import (
    CompressibleHomomorphism,
    CompressibleHomomorphismInput,
)
from tno.zkp.templates.sigma_protocol import (
    BaseSigmaProtocol,
    CompressedSigmaProtocol,
    HomomorphismT,
    ResponseT,
    create_challenge,
)

if TYPE_CHECKING:
    from tno.zkp.templates.homomorphism import (
        ChallengeT,
        HomomorphismOutputT,
        InputElementT,
    )

logger = logging.getLogger(__name__)


def compression(
    sigma_protocol: BaseSigmaProtocol[
        InputElementT, HomomorphismOutputT, ChallengeT, ResponseT, HomomorphismT
    ]
) -> CompressedSigmaProtocol[InputElementT, HomomorphismOutputT, ChallengeT]:
    """
    Compress a sigma protocol by using the folding technique described in the dissertation mentioned
    in the README.md

    :param sigma_protocol: the sigma protocol which will be compressed
    :return: A compressed sigma protocol
    :raise TypeError: When the homomorphism of the sigma protocol is not compressible
    :raise TypeError: When the homomorphism input of the sigma protocol is not compressible
    :raise ValueError: When the homomorphism is already as small as possible
    """
    homomorphism = sigma_protocol.homomorphism
    response = sigma_protocol.response

    if not isinstance(homomorphism, CompressibleHomomorphism):
        raise TypeError(
            "The homomorphism in the sigma protocol must be compressible "
            "(type `CompressibleHomomorphism`). Currently of type "
            f"{type(homomorphism)}."
        )

    if not isinstance(response, CompressibleHomomorphismInput):
        raise TypeError(
            "The homomorphism input in the sigma protocol must be compressible "
            "(type: `CompressibleHomomorphismInput`). Currently of type "
            f"{type(response)}"
        )

    if homomorphism.input_size <= 1:
        raise ValueError(
            f"Sigma protocol can not be compressed, input size is less or equal to 1 "
            f"({homomorphism.input_size})"
        )

    x_l, x_r = response.split_in_half()

    (homomorphism_l, homomorphism_r) = homomorphism.split_in_half()
    logging.debug("Calculating the cross-terms")
    # The A in the compressed sigma protocol of the dissertation
    cross_termr = homomorphism_r.evaluate(x_l)
    # The B in the compressed sigma protocol of the dissertation
    cross_terml = homomorphism_l.evaluate(x_r)

    if isinstance(sigma_protocol, CompressedSigmaProtocol):
        # ignoring type see https://github.com/python/mypy/issues/12949
        transcript = sigma_protocol.transcript  # type: ignore
    else:
        transcript = []

    transcript.append((cross_termr, cross_terml))

    challenge_input = [sigma_protocol.image_to_prove, sigma_protocol.commitment] + list(
        itertools.chain(*transcript)
    )
    challenge = create_challenge(
        sigma_protocol.hash_algorithm,
        challenge_input,
        sigma_protocol.homomorphism,
    )
    compressed_homomorphism = homomorphism_l * challenge + homomorphism_r

    compressed_response = x_l + challenge * x_r
    logger.debug(f"New response is: {compressed_response}")
    return CompressedSigmaProtocol(
        compressed_homomorphism,
        image_to_prove=sigma_protocol.image_to_prove,
        response=compressed_response,
        commitment=sigma_protocol.commitment,
        transcript=transcript,
        hash_algorithm=sigma_protocol.hash_algorithm,
    )


def full_compression(
    sigma_protocol: BaseSigmaProtocol[
        InputElementT, HomomorphismOutputT, ChallengeT, ResponseT, HomomorphismT
    ]
) -> CompressedSigmaProtocol[InputElementT, HomomorphismOutputT, ChallengeT]:
    """
    Compress a sigma protocol until it can not be compressed any further.

    :param sigma_protocol: the sigma protocol which will be compressed
    :return: A compressed sigma protocol if the protocol could be compressed otherwise the sigma
        protocol itself
    :raise TypeError: When the homomorphism of the sigma protocol is not compressible
    :raise TypeError: When the homomorphism input of the sigma protocol is not compressible
    :raise ValueError: When the homomorphism is already as small as possible
    """
    compressed = compression(sigma_protocol)
    while compressed.homomorphism.input_size > 1:
        compressed = compression(compressed)

    return compressed
