"""
The sigma protocol classes which are used to generate a proof of knowledge.
"""
from __future__ import annotations

import hashlib
import logging
import sys
from typing import Any, Generic, Iterable, TypeVar

from tno.zkp.templates.homomorphism import (
    ChallengeT,
    CompressibleHomomorphism,
    CompressibleHomomorphismInput,
    Homomorphism,
    HomomorphismInput,
    HomomorphismOutputT,
    InputElementT,
)

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

logger = logging.getLogger(__name__)

ResponseT = TypeVar("ResponseT", bound=HomomorphismInput[Any])
HomomorphismT = TypeVar("HomomorphismT", bound=Homomorphism[Any, Any, Any])


def create_challenge(
    hash_function_name: str,
    create_bytes_from: HomomorphismOutputT | Iterable[HomomorphismOutputT],
    homomorphism: Homomorphism[InputElementT, HomomorphismOutputT, ChallengeT],
) -> ChallengeT:
    """
    Create a challenge from homomorphism output using the hash function. The challenge is used
    in the sigma-protocol to make it non-interactive.

    :param hash_function_name: Name of hash function in the `hashlib` library
    :param create_bytes_from: homomorphism output(s) from which the challenge is made
    :param homomorphism: the corresponding homomorphism which creates a challenge from bytes
    :return: A challenge derived from the bytes of the hash function applied to the homomorphism
     output(s).
    """
    if not isinstance(create_bytes_from, Iterable):
        create_bytes_from = [create_bytes_from]

    hash_function = hashlib.new(hash_function_name)
    for homomorphism_output in create_bytes_from:
        bytes_for_challenge = homomorphism.output_to_bytes(homomorphism_output)
        hash_function.update(bytes_for_challenge)
    bytes_digest = hash_function.digest()
    return homomorphism.challenge_from_bytes(bytes_digest)


class BaseSigmaProtocol(
    Generic[InputElementT, HomomorphismOutputT, ChallengeT, ResponseT, HomomorphismT]
):
    """
    Abstract class defining the methods provided by a sigma protocol.
    """

    def __init__(
        self,
        homomorphism: HomomorphismT,
        image_to_prove: HomomorphismOutputT,
        commitment: HomomorphismOutputT,
        response: ResponseT,
        hash_algorithm: str,
    ):
        r"""
        Create a Sigma Protocol instantiation. The instantiation contains all elements needed for
        verification. To generate a proof of knowledge see the method `generate_proof`.

        :param homomorphism: Homomorphism which is used for the evaluation.
        :param image_to_prove: The image created by applying the homomorphism on the secret input.
        :param commitment: Evaluation of $\psi(r)$, where $r$ is the random input used during proof generation.
        :param response: The response $z$.
        :param hash_algorithm: The hash algorithm used to generate the challenge from the
            `hashlib` library.
        """
        self._homomorphism = homomorphism
        self._image_to_prove = image_to_prove
        self._commitment = commitment
        self._hash_algorithm = hash_algorithm
        self._response = response

    @property
    def homomorphism(
        self,
    ) -> HomomorphismT:
        """
        The homomorphism function used in this sigma protocol

        :return: `Homomorphism` corresponding to this sigma protocol
        """
        return self._homomorphism

    @property
    def image_to_prove(self) -> HomomorphismOutputT:
        r"""
        Evaluation of the input by the homomorphism. This evaluation results in the input $P$ for
        the sigma protocol.

        :return: A homomorphism output representing $\psi(x)$, where x is the input vector and
         $\psi$ the homomorphism.
        """
        return self._image_to_prove

    @property
    def response(self) -> ResponseT:
        """
        Response of the prover, which is used to verify the proof of knowledge. This corresponds to
        the variable $z$ of the sigma protocol. The evaluation of $z$ by the homomorphism is used to
        verify the proof of knowledge.

        In the basic sigma protocol the response corresponds to $z= r + cx$, where $r$ is a vector
        of random elements, $c$ is the challenge from the verifier and $x$ is the input vector.

        :return: A list of input elements representing the response of the prover.
        """
        return self._response

    @property
    def commitment(self) -> HomomorphismOutputT:
        r"""
        The commitment from the prover to a random vector $r$. The commitment is represented as
         variable $A$ in the basic sigma protocol.

        :return: Evaluation of $\psi(r)$, where $r$ is the random input used during proof generation.
        """
        return self._commitment

    @property
    def hash_algorithm(self) -> str:
        """
        Hash algorithm used for the Fiat-Shamir transformation. The Fiat-Shamir transformation
        makes the proof non-interactive.

        The choice of the hash algorithm determines the number of bytes, which are available to
        generate a challenge.

        :return: A string with the name of the hash algorithm
        """
        return self._hash_algorithm

    def verify(self) -> bool:
        """
        Validate the sigma protocol and determine whether the verifier is convinced of the proof of
        knowledge.

        :return: `True` if the verifier is convinced otherwise `False`
        """
        raise NotImplementedError()


class StandardSigmaProtocol(
    Generic[InputElementT, HomomorphismOutputT, ChallengeT],
    BaseSigmaProtocol[
        InputElementT,
        HomomorphismOutputT,
        ChallengeT,
        HomomorphismInput[InputElementT],
        Homomorphism[InputElementT, HomomorphismOutputT, ChallengeT],
    ],
):
    """
    Sigma protocol which consists of three steps. The sigma protocol enables the user to generate a
    proof of knowledge and verify it. The proof of knowledge is over a vector of `InputElement`'s.
    """

    @classmethod
    def generate_proof(
        cls,
        homomorphism: Homomorphism[InputElementT, HomomorphismOutputT, ChallengeT],
        private_input: HomomorphismInput[InputElementT],
        hash_function: str,
    ) -> Self:
        """
        Generate a zero-knowledge proof for the provided input and the homomorphism.

        :param homomorphism: The homomorphism used during the sigma protocol
        :param private_input: The input for which a proof is generated
        :param hash_function: The hash function name from `hashlib` used to create the challenge
        :return: A sigma protocol which can be verified.
        :raise ValueError: When the input length vector is not equal to the expected input size
        """
        if len(private_input.input_vector) != homomorphism.input_size:
            raise ValueError(
                f"The length of the private input (len: {len(private_input.input_vector)} is not "
                f"the same as the size expected by the homomorphism (expected length: "
                f"{homomorphism.input_size})."
            )
        logger.debug("Calculating the public information P=homomorphism(private_input)")
        image_P = homomorphism.evaluate(private_input)

        random_input = homomorphism.random_input()
        logger.debug(
            f"Generated random input commitment (Do not share with others): {random_input}"
        )
        commitment = homomorphism.evaluate(random_input)

        generated_challenge = create_challenge(
            hash_function, [image_P, commitment], homomorphism
        )

        response: HomomorphismInput[InputElementT] = (
            random_input + private_input * generated_challenge
        )
        logger.debug(f"Response consists of the following:\n {response}")
        logger.debug("Calculating the P")
        return cls(
            homomorphism,
            image_P,
            commitment,
            response,
            hash_function,
        )

    def verify(self) -> bool:
        challenge = create_challenge(
            self.hash_algorithm,
            [self.image_to_prove, self.commitment],
            self.homomorphism,
        )
        logger.debug(f"Verify: recreating challenge {challenge}")
        logger.debug(
            f"Reconstructed: {self.commitment + self.image_to_prove * challenge}"
        )

        response_evaluation = self.homomorphism.evaluate(self.response)
        logger.debug(f"Calculating the response evaluation {response_evaluation}")
        return response_evaluation == (
            self.commitment + self.image_to_prove * challenge
        )


class CompressedSigmaProtocol(
    Generic[InputElementT, HomomorphismOutputT, ChallengeT],
    BaseSigmaProtocol[
        InputElementT,
        HomomorphismOutputT,
        ChallengeT,
        CompressibleHomomorphismInput[InputElementT],
        CompressibleHomomorphism[InputElementT, HomomorphismOutputT, ChallengeT],
    ],
):
    """
    Sigma protocol which has been compressed. A compressed sigma protocol can be created by applying
    the compression mechanism to the sigma-protocol.
    """

    def __init__(
        self,
        homomorphism: CompressibleHomomorphism[
            InputElementT, HomomorphismOutputT, ChallengeT
        ],
        image_to_prove: HomomorphismOutputT,
        response: CompressibleHomomorphismInput[InputElementT],
        commitment: HomomorphismOutputT,
        transcript: list[tuple[HomomorphismOutputT, HomomorphismOutputT]],
        hash_algorithm: str,
    ):
        """
        Initialization function for a compressed sigma protocol. To create a compressed sigma-
        protocol use the `compress` function from the compression mechanism.

        :param homomorphism: The compressible homomorphism used by the sigma protocol.
        :param image_to_prove: image generated by applying the homomorphism to the secret input
        :param response: a compressed response
        :param commitment: the initial commitment from the sigma protocol
        :param transcript: the transcript of $A_i$ and $B_i$
        :param hash_algorithm: the hash algorithm used to generate the challenges
        """
        super().__init__(
            homomorphism, image_to_prove, commitment, response, hash_algorithm
        )

        self._transcript = transcript

    @property
    def transcript(self) -> list[tuple[HomomorphismOutputT, HomomorphismOutputT]]:
        """
        Transcript of the tuple consisting of the $A_i$ and $B_i$ elements. The elements are used
        during the verification to generate the corresponding challenges and to verify the result.

        :return: A list of tuples corresponding to the $A$'s and $B$'s.
        """
        return self._transcript

    def verify(self) -> bool:
        challenge_input = [self.image_to_prove, self.commitment]
        c_0: ChallengeT = create_challenge(
            self.hash_algorithm, challenge_input, self.homomorphism
        )

        reconstructed_image = self.commitment + self.image_to_prove * c_0
        compressed_homomorphism = self.homomorphism

        for A, B in self.transcript:
            challenge_input += [A, B]
            challenge: ChallengeT = create_challenge(
                self.hash_algorithm, challenge_input, self.homomorphism
            )
            logger.debug(f"A, B, challenge are {A},{B},{challenge}")

            reconstructed_image = (
                A + reconstructed_image * challenge + B * challenge * challenge
            )

        return compressed_homomorphism.evaluate(self.response) == reconstructed_image
