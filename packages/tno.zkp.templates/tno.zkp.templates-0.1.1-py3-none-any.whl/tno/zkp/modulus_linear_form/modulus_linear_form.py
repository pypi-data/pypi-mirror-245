from __future__ import annotations

import itertools
import logging
import math
import random
from functools import reduce

from tno.zkp.templates.homomorphism import (
    CompressibleHomomorphism,
    CompressibleHomomorphismInput,
    HomomorphismInput,
)


class LinearFormInput(CompressibleHomomorphismInput[int]):
    """
    Input for the linear form homomorphism. Can be split into two (almost) equal parts.
    """

    def __init__(self, input_list: list[int]):
        self._input_vector = input_list

    def split_in_half(self) -> tuple[LinearFormInput, LinearFormInput]:
        """
        Split the input vector into two equal halves.

        :return: left and right half of the input vector
        """
        left = self.input_vector[: len(self) // 2]
        right = self.input_vector[len(self) // 2 :]
        return LinearFormInput(left), LinearFormInput(right)

    @property
    def input_vector(self) -> list[int]:
        """
        The input vector for a `LinearForm`.

        :return: List of integers representing the input to a `LinearForm`
        """
        return self._input_vector

    def __add__(self, other: object) -> LinearFormInput:
        """
        Add two `LinearFormInput`-objects together. If the length of the forms are of different sizes the smallest will be zero-padded to the same size. When the objects have the same length the resulting `LinearFormInput` will consist of the elements $x_i+z_i$, where $x$ and $z$ are the linear form inputs and $i$ i-th element of the input vector.

        :param other: LinearFormInput to be added
        :return: LinearFormInput representing the addition of the two linear forms.
        :raise TypeError: When the input object is not of type `LinearFormInput`
        """
        if not isinstance(other, LinearFormInput):
            raise TypeError(
                f"Linear form input can only be added to object of same type not to {type(other)}"
            )
        input_vector = self.input_vector
        other_input_vector = other.input_vector
        if len(self) < len(other):
            # ensure the input vector is the same length by prepending it with 0's
            input_vector = [0 for _ in range(len(other) - len(self))] + input_vector
        if len(other) < len(self):
            # ensure the input vector of the other object is the same length by prepending with 0's
            other_input_vector = [
                0 for _ in range(len(other) - len(self))
            ] + other_input_vector
        addition = [x + y for x, y in zip(input_vector, other_input_vector)]
        return LinearFormInput(addition)

    def __mul__(self, other: object) -> LinearFormInput:
        """
        Perform a scalar multiplication with input vector.

        :param other: the scalar
        :return: The linear form input which has been multiplied by the scalar.
        :raise TypeError: When the multiplication object is not of type `int`
        """
        if not isinstance(other, int):
            raise TypeError(
                f"LinearFormInput can only be multiplied with object of same type or a Number "
                f"not to {type(other)}."
            )
        multiplication = [x * other for x in self.input_vector]
        return LinearFormInput(multiplication)

    __rmul__ = __mul__

    def __str__(self) -> str:
        return f"Input vector: {self.input_vector}"


class LinearFormOutput:
    """
    Output for the linear form. A separate class in which all additions and multiplications
    are performed under the specified modulus.
    """

    def __init__(self, value: int, modulus: int):
        self._value = value
        self._modulus = modulus

    @property
    def modulus(self) -> int:
        """
        The modulus under which all operations are performed.

        :return: the modulus
        """
        return self._modulus

    @property
    def value(self) -> int:
        """
        The value which is represented by this class.

        :return: an integer less than the modulus
        """
        return self._value

    def __add__(self, other: object) -> LinearFormOutput:
        r"""
        Add two `LinearFormOutput`-objects together. The result will be a new `LinearFormOutput` where the value is $x+y\mod m$, where $x$ and $y$ are the object to be added and $m$ is the modulus

        :param other: LinearFormOutput to be added
        :return: LinearFormOutput representing the addition of outputs.
        :raise TypeError: When the input object is not of type `LinearFormOutput`
        :raise ValueError: When the modulus of both `LinearFormOutput` objects are not the same
        """
        if isinstance(other, LinearFormOutput):
            if other.modulus != self.modulus:
                raise ValueError(
                    "The modulus must be the same between linear form outputs"
                )
            return LinearFormOutput(
                (self.value + other.value) % self.modulus, self.modulus
            )
        else:
            raise TypeError(f"Can not add to object of type {type(other)}")

    def __mul__(self, other: object) -> LinearFormOutput:
        """
        Perform a scalar multiplication with the value the result reduced using the modulus.

        :param other: the scalar
        :return: The linear form output which has been multiplied by the scalar modulo the modulus.
        :raise TypeError: When the multiplication object is not of type `int`
        """
        if not isinstance(other, int):
            raise TypeError(
                f"Can only multiply with a scalar of type `int`, current type {type(other)}"
            )
        return LinearFormOutput((self.value * other) % self.modulus, self.modulus)

    __rmul__ = __mul__

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LinearFormOutput):
            return False
        return self.value == other.value and self.modulus == other.modulus


class ModulusLinearForm(CompressibleHomomorphism[int, LinearFormOutput, int]):
    """
    A linear form which operates on a group of modulus $m$. The linear form evaluates the result
    by multiplying the input element of $x_i$ with the corresponding coefficient. All the
    multiplications are summed and reduced modulo $m$.

    The linear form can also be split into two halves. If the length is unequal a 0 is prepended to
    make the linear form of even length.
    """

    def __init__(self, coeffs: list[int], modulus: int):
        """
        Initialize a LinearForm with a list of coefficients and a modulus.

        :param coeffs: The coefficients for the LinearForm
        :param modulus: The modulus used during additions and multiplications
        """
        reduced_coeffs = [i % modulus for i in coeffs]
        self.modulus = modulus
        self._reduced_coeffs = reduced_coeffs

    def split_in_half(self) -> tuple[ModulusLinearForm, ModulusLinearForm]:
        """
        Split the LinearForm into two equal parts. The split is realized by dividing the
        coefficients over two new `ModulusLinearForm`. If the length is odd a zero is prepended.

        :return: Tuple containing the two halves of the `ModuluesLinearForm`
        """
        coeffs = self.coeffs
        if len(self.coeffs) % 2 != 0:
            coeffs = [0] + coeffs
        left_coeffs = coeffs[: len(coeffs) // 2]
        right_coeffs = coeffs[len(coeffs) // 2 :]
        return ModulusLinearForm(left_coeffs, self.modulus), ModulusLinearForm(
            right_coeffs, self.modulus
        )

    @property
    def input_size(self) -> int:
        """
        The expected input size for this homomorphism.

        :return: the maximum length of the input vector
        """
        return len(self._reduced_coeffs)

    def evaluate(self, homomorphism_input: HomomorphismInput[int]) -> LinearFormOutput:
        """
        Apply the LinearForm to the homomorphism input. The input is evaluated by summing the
        multiplication of $coeff[i]$ by $input[i]$.
        If the input length is less than the expected input size 0's are prepended to the input.

        :param homomorphism_input: The input for the LinearForm
        :return: LinearFormOutput representing the result of the input applied to the homomorphism
        :raise ValueError: When the input length is larger than the expected input size
        """
        if len(homomorphism_input) > len(self.coeffs):
            raise ValueError("Input length must always be less or equal")
        if len(homomorphism_input) < len(self.coeffs):
            vector_input = [
                0 for _ in range(len(self.coeffs) - len(homomorphism_input))
            ] + homomorphism_input.input_vector
        else:
            vector_input = homomorphism_input.input_vector
        logging.debug(
            f"Evaluating the result of {list(zip(vector_input, self.coeffs))}"
        )
        result = reduce(
            lambda x, y: (x + y) % self.modulus,
            [
                (value * coeff) % self.modulus
                for value, coeff in zip(vector_input, self.coeffs)
            ],
            0,
        )
        return LinearFormOutput(result, self.modulus)

    def random_input(self) -> LinearFormInput:
        """
        Generate a random input vector where the values are at most the value of the modulus.

        :return: LinearFormInput with random input vectors
        """
        random_vector = [
            random.randint(0, self.modulus) for _ in range(self.input_size)
        ]
        return LinearFormInput(random_vector)

    def output_to_bytes(self, output: LinearFormOutput) -> bytes:
        """
        Transform the output to set of bytes. The bytes represent the output in big endian form.

        :param output: The LinearFormOutput which needs to be represented in bytes.
        :return: bytes in big endian form representing the output.
        """
        bytes_length = math.ceil(output.value.bit_length() / 8)
        return output.value.to_bytes(bytes_length, "big")

    def challenge_from_bytes(self, hash_bytes: bytes) -> int:
        """
        Turn bytes into a challenge. The conversion from bytes to int uses the big endian form.
        The value will be taken modulo the modulus of this homomorphism.

        :param hash_bytes: the bytes to transform
        :return: an integer representing the challenge
        """
        return int.from_bytes(hash_bytes, "big") % self.modulus

    @property
    def coeffs(self) -> list[int]:
        """
        The coefficients used by the linear form during the evaluation.

        :return: a list of integers representing the coefficients
        """
        return self._reduced_coeffs

    def __add__(self, other: object) -> ModulusLinearForm:
        """
        Add two `ModulusLinearForm`'s together. The addition adds the corresponding coefficients
        together and the result is taken by the modulo the modulus of the linear form.

        :param other: `ModulusLinearForm` to add to this object
        :return: A new modulus linear form with the coefficients added together
        :raise TypeError: When other is not of type `ModulusLinearForm`
        :raise ValueError: When the modulus is not the same between both objects
        """
        if not isinstance(other, ModulusLinearForm):
            raise TypeError(f"Expected a ModulusLinearForm got {type(other)}")
        if self.modulus != other.modulus:
            raise ValueError(
                f"The modulus are not the same for both ModulusLinearForms got "
                f"({self.modulus} and {other.modulus}"
            )
        new_coeffs = [
            (i + j) % self.modulus
            for i, j in itertools.zip_longest(self.coeffs, other.coeffs)
        ]
        return ModulusLinearForm(new_coeffs, self.modulus)

    def __mul__(self, other: object) -> ModulusLinearForm:
        """
        Multiply the coefficients of the modulus linear form with a scalar. The result is taken
        modulu the modulus.

        :param other: The scalar to multiply the linear form with
        :return: A new `ModulusLinearForm` with coefficients $(coeff[i]*scalar)%modulo$
        """
        if not isinstance(other, int):
            raise TypeError(
                f"Can only multiply with a scalar of type `int`, current type {type(other)}"
            )

        new_coeffs = [(i * other) % self.modulus for i in self.coeffs]
        return ModulusLinearForm(new_coeffs, self.modulus)

    __rmul__ = __mul__

    def __eq__(self, other: object) -> bool:
        """
        Check if two Modulus Linear Forms have the same modulus and coefficients.

        :param other: The object to compare against.
        :return: True if the coefficients and the modulus are the same. False otherwise
        """
        if not isinstance(other, ModulusLinearForm):
            return False
        return self.coeffs == other.coeffs and self.modulus == other.modulus
