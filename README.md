# mxwpy
mxwpy is an under development Python library that provides efficient numerical schemes and some useful tools. It consists of the following modules:

- `spectral`: Provides functions for working with spectral methods, specifically for evaluating orthonormal Jacobi polynomials, as described in the book [Spectral Methods: Algorithms, Analysis and Applications](https://link.springer.com/book/10.1007/978-3-540-71041-7) by Shen, Tang, and Wang.
- `linalg`: This module primarily focuses on numerical algebra methods.
- `tools`: A collection of utility functions for system and package information retrieval, time measurement, and other potential functionalities to be added in the future.
- `npde`: Hosts functions for handling numerical partial differential equations.

## Dependencies

When you install this library using pip, most dependencies will be automatically handled. However, please note that the `npde` module requires PyTorch, which needs to be installed separately.

You can install PyTorch by following the instructions on the [official PyTorch website](https://pytorch.org/get-started/locally/). Please ensure that you select the correct installation command based on your operating system, package manager, Python version, and the specifications of your CUDA toolkit if you are planning to use PyTorch with GPU support.

If you are not planning to use the `npde` module, you do not need to install PyTorch.

## Installation

To install this library, you can use pip:

```bash
pip install mxwpy