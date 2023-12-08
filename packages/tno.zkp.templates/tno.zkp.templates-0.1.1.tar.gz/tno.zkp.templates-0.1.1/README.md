# TNO PET Lab - Zero-Knowledge Proofs (ZKP) - Templates

The TNO PET Lab consists of generic software components, procedures, and
functionalities developed and maintained on a regular basis to facilitate and
aid in the development of PET solutions. The lab is a cross-project initiative
allowing us to integrate and reuse previously developed PET functionalities to
boost the development of new protocols and solutions.

The package tno.zkp.templates is part of the TNO Python Toolbox.

The research activities that led to this implementation is made possible by

- The Alliance of Privacy Preserving Detection of Financial Crime, consisting of
  De Volksbank, TMNL, CWI, ABN AMRO, Rabobank, TNO.
- The confidential 6G project
- The Early Research Project of TNO "Next generation crypto"

_Limitations in (end-)use: the content of this software package may solely be
used for applications that comply with international export control laws._  
_This implementation of cryptographic software has not been audited. Use at your
own risk._

## Documentation

Documentation of the tno.mpc.encryption_schemes.shamir package can be found
[here](https://docs.pet.tno.nl/zkp/templates/0.1.1).

## Install

Easily install the tno.mpc.encryption_schemes.shamir package using pip:

```console
$ python -m pip install tno.zkp.templates
```

If you wish to run the tests you can use:

```console
$ python -m pip install 'tno.zkp.templates[tests]'
```

## Usage

This library contains the templates with which we can create a zero-knowledge
proof(ZKP). The templates are protocols, which should to be inherited by any of
the classes to support ZKPs. An example has been added in this repository. The
example is the modulus linear form. The modulus linear form is a separate
module, which is a basic building block that can be used to create ZKPs.

The ZKP library is based on Thomas Attema's dissertation Compressed
$`\Sigma`$-protocol Theory, which can be found
[here](https://scholarlypublications.universiteitleiden.nl/handle/1887/3619596).
Many concepts are taken from it, and there will be references throughout the
code to the dissertation. In this README the crucial concepts from the
dissertation needed to use this library will be explained in short. If anything
is unclear, feel free to raise an issue at the code repository.

### Preliminaries

Before explaining how to use the library several concepts need to be explained.
The concepts are used throughout the interface and knowing them beforehand makes
it easier to use the library.

A zero-knowledge proof of knowledge (referred to as ZKP in this README) can be
used to show you possess information without revealing the information itself.
This can be used in many different settings, but currently uses with a
distributed ledger are common.

#### Homomorphism

A homomorphism is a fundamental building block of the ZKP. The homomorphism
evaluates a function on a vector of input elements. A homomorphism is
represented in the literature as $`\psi_n`$, where $`n`$ is the length of the
input vector.

The homomorphism maps the input vector from an abelian group $`\mathbb{G}^n`$ to
a single element of another group $`\mathbb{H}`$. In particular the original
domain and target image groups can have different group operators. In the
dissertation a mapping is made from an additive group $`\mathbb{G}`$ to a
multiplicative group $`\mathbb{H}`$.

#### Sigma Protocol

A sigma protocol is a three-step process which creates a zero knowledge proof.
The three-step process uses a homomorphism, an input vector and random elements
from a group.

The three steps are shown in the sequence diagram below. Each step is explained
in this section.

<figure>
  <img src="raw.githubusercontent.com/TNO-ZKP/templates/main/assets/BasicSigmaProtocol.png" width=100% alt="Basic sigma Protocol high level overview"/>
  <figcaption>

**Figure 1.** _Two parties exchange information in which the Prover wants to
convince the Verifier that he knows secret input $`x`$ without revealing $`x`$._

  </figcaption>
</figure>

##### Initial information

Before starting a sigma protocol certain pieces of information are calculated.
The information consists of the following:

- **Private input**: $`x`$ secret of the prover
- **Public input**: $`P`$ and the homomorphism
  $`\psi \in \texttt{Hom}(\mathbb{G}^n,\mathbb{H})`$
- **Prover's claim**: $`P=\psi(x)`$

##### First step

In the first a commitment is made by the prover. The commitment is made by
generating a random input $`r$. The random input $r`$ is evaluated by the
homomorphism $`\psi$ giving $A$. $A`$ is the commitment sent to the verifier.

##### Second step

The verifier sends a challenge $`c`$ to the prover. The challenge is a single
element (as opposed to a vector). The challenge needs to be able to do the
following operations:

- Multiply with homomorphism input, which is a vector of elements from group
  $`\mathbb{G}`$. This operation is needed to create the response mentioned in
  the third step.
- Take to the power of the resulting group $`\mathbb{H}`$. This operation is
  needed to verify the proof.

In this library the homomorphism maps input from additive group operation to a
group with multiplicative operations. Depending on your use-case and the chosen
implementation different operations might be needed.

##### Third step

Create the response by calculating a new input for the homomorphism. The input
is based on $`r`$, the challenge $`c`$ and the secret input $`x`$. The response
is calculated as follows: $`z=r+cx`$.

##### Verification

The verifier can now check the proof of knowledge by testing if $`\psi(z)`$ is
equal to $`A\cdot P^c`$.

##### Making it non-interactive

To be able to make the proof of knowledge non-interactive we need to be able to
replace the challenge of the verifier. Replacing the challenge can not be done
by just picking one as the prover. To replace the challenge we use the
Fiat-Shamir transformation. The transformation uses a hashing algorithm to
create the challenge.

Making the proof non-interactive prevents communication overhead and enables the
option for the prover to create a proof of knowledge without the verifier being
present. The verifier can then check the proof of knowledge on its own when the
necessary information has been retrieved.

### Creating a Sigma Protocol

To support the creation of a sigma protocol the template classes have been
created. The template classes can be split into two categories.

The first category are the classes needed to create a basic sigma protocol. The
basic sigma protocol creates a proof of knowledge in a non-interactive way. The
`StandardSigmaProtocol` object contains all the information needed for the
verification and none of the private information. The object can therefore be
shared with the verifier for verification.

To create a `StandardSigmaProtocol` you need some random input and a
homomorphism. For this example we will use the `ModulusLinearForm` homomorphism
included in this package. The `ModulusLinearForm` implements the `Homomorphism`
object and is located in the namespace `tno.zkp.modulus_linear_form`.

In the code snippet below we create a `ModulusLinearForm` corresponding to the
following formula $`1\cdot x_1 + 2\cdot x_2 + 3 \cdot x_3`$ with the modulus
$`13`$. The secret input is a random input generated by the homomorphism.

Generating the proof of knowledge is relatively straight forward. You call the
method `generate_proof` with the homomorphism, the secret input and the hash
function. The class will handle the process as described in the steps above.

To verify the proof of knowledge you only need to call the `verify` function.

```python
from tno.zkp.modulus_linear_form import ModulusLinearForm
from tno.zkp.templates import StandardSigmaProtocol

homomorphism = ModulusLinearForm([1, 2, 3], 13)
secret_input_x = homomorphism.random_input()

proof_of_knowledge = StandardSigmaProtocol.generate_proof(
  homomorphism, secret_input_x, "sha256"
)

assert proof_of_knowledge.verify()
```

### Compressing a Sigma Protocol

To compress a proof of knowledge there are some requirements on the homomorphism
and the input. The requirements are enforced using the
`CompressibleHomomorphism` and the `CompressibleHomomorphismInput` abstract
classes.

> Compressing a proof of knowledge makes the verification of the protocol
> cheaper. The cost savings occur due to a compression mechanism. The
> compression mechanism is described in detail in the dissertation.

The `ModulusLinearForm` from the previous example satisfies the requirements.
Therefore, we can use the previous proof of knowledge for compression.

To apply the compression we need to use a compression mechanism. The compression
mechanism from the dissertation has been implemented in this template. To apply
it you need to do the following:

```python
from tno.zkp.templates import full_compression

# compress the proof of knowledge as much as possible
compressed_protocol = full_compression(proof_of_knowledge)
assert compressed_protocol.verify()
```

The function `full_compression` reduces the ZKP from length $`n`$ until it can
not be compressed anymore, which is a length of 1. The function used for the
compression is called `compression` and is available to the user as well. The
`compression` function halves the length of the ZKP.
