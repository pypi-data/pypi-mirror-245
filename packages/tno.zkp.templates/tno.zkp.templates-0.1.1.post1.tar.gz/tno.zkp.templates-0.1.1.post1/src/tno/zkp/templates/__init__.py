"""
Module containing the templates for the sigma-protocol zero-knowledge proofs.
"""

# Explicit re-export of all functionalities, such that they can be imported properly. Following
# https://www.python.org/dev/peps/pep-0484/#stub-files and
# https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-no-implicit-reexport
from .compression_mechanism import compression as compression
from .compression_mechanism import full_compression as full_compression
from .homomorphism import CompressibleHomomorphism as CompressibleHomomorphism
from .homomorphism import Homomorphism as Homomorphism
from .homomorphism import HomomorphismOutputT as HomomorphismOutputT
from .homomorphism import InputElementT as InputElementT
from .sigma_protocol import BaseSigmaProtocol as BaseSigmaProtocol
from .sigma_protocol import CompressedSigmaProtocol as CompressedSigmaProtocol
from .sigma_protocol import StandardSigmaProtocol as StandardSigmaProtocol
from .sigma_protocol import create_challenge as create_challenge

__all__ = [
    "CompressibleHomomorphism",
    "Homomorphism",
    "HomomorphismOutputT",
    "InputElementT",
    "StandardSigmaProtocol",
    "CompressedSigmaProtocol",
    "BaseSigmaProtocol",
    "create_challenge",
    "compression",
    "full_compression",
]
__version__ = "0.1.1.post1"
