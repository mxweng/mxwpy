__all__ = ['HermiteP', 'HermiteF', 'Hermite_Gauss']

"""
spectral.py

This module provides functions for working with spectral methods.
The implementation is mainly based on the book: 
    Shen, J., Tang, T. & Wang, L.-L. Spectral Methods: Algorithms, 
    Analysis and Applications. vol. 41 (Springer Science & Business 
    Media, 2011).
    https://link.springer.com/book/10.1007/978-3-540-71041-7
"""

import numpy as np
from scipy.special import roots_hermite
from scipy.special import gamma
from scipy.sparse import diags
from scipy.linalg import eigh

def JacobiP(x, alpha, beta, N):
    """
    This function evaluates the orthonormal Jacobi polynomial of order 
    up to N with parameters alpha and beta at points x.
    
    Parameters
    ----------
    x : array
        Points at which the Jacobi polynomial is to be computed.
    alpha : float
        The alpha parameter of the Jacobi polynomial. Must be greater than -1.
    beta : float
        The beta parameter of the Jacobi polynomial. Must be greater than -1.
    N : int
        The order of the Jacobi polynomial.

    Returns
    ----------
    PL: ndarray, shape (N + 1, len(x))
        The N-th row of PL is the values of orthonormal Jacobi 
        polynomial J_{N}^{alpha, beta}(x) / sqrt(gamma_{N}^{alpha, beta}).

    References:
    ----------
    1. Spectral Method P74
    2. Code-reproduction/Poisson-GPU.ipynb
    """

    xp = x.copy()
    if len(xp.shape) == 2 and xp.shape[1] == 1:
        xp = xp.T
    PL = np.zeros((N + 1, max(xp.shape)))
    gamma0 = np.power(2, alpha + beta + 1) * gamma(alpha + 1) * gamma(beta + 1) / gamma(alpha + beta + 2)
    PL[0, :] = 1.0 / np.sqrt(gamma0)
    if N == 0:
        return PL.T
    gamma1 = (alpha + 1) * (beta + 1) / (alpha + beta + 3) * gamma0
    PL[1, :] = ((alpha + beta + 2) * xp / 2 + (alpha - beta) / 2) / np.sqrt(gamma1)
    if N == 1:
        return PL[N, :].T
    aold = 2 / (2 + alpha + beta) * np.sqrt((alpha + 1) * (beta + 1) / (alpha + beta + 3))
    for i in range(1, N):
        h1 = 2 * i + alpha + beta
        anew = 2 / (h1 + 2) * np.sqrt((i + 1) * (i + 1 + alpha + beta) * (i + 1 + alpha) * (i + 1 + beta) / (h1 + 1) / (h1 + 3))
        bnew = -(alpha * alpha - beta * beta) / h1 / (h1 + 2)
        PL[i + 1, :] = 1 / anew * (-aold * PL[i - 1, :] + (xp - bnew) * PL[i, :])
        aold = anew
    return PL

def Jacobi_Gauss(alpha, beta, N):
    """
    This function computes the Gauss Jacobi quadrature first order 
    derivative matrix, nodes and weights of Jacobi polynomial J_{N}^{alpha, beta}.

    Parameters
    ----------
    alpha : float
        The alpha parameter of the Gauss Jacobi quadrature. alpha > -1.
    beta : float
        The beta parameter of the Gauss Jacobi quadrature. beta > -1.
        If alpha = beta = 0, the Jacobi polynomial is Legendre polynomial.
    N : int
        The order of the Gauss Jacobi quadrature.

    Returns
    ----------
    D: ndarray, shape (N, N)
        The first order derivative matrix of the Gauss Jacobi quadrature.
    r: ndarray, shape (N,)
        The Gauss Jacobi quadrature nodes.
    w: ndarray, shape (N,)
        The Gauss Jacobi quadrature weights.

    References
    ----------
    1. Spectral Method P84
    """

    if N == 1:
        r = np.array([-(alpha - beta) / (alpha + beta + 2)])
        w = np.array([2])
        return r, w
    
    h1 = 2 * np.arange(N) + alpha + beta
    h11, h12, h13 = h1 + 1, h1 + 2, h1 + 3
    h2 = np.arange(1, N)
    # Adjust h1, h11, h12 values based on alpha and beta
    # to avoid division by zero
    if abs(alpha + beta) < 10 * np.finfo(float).eps:
        h1[0] = 1.0
    elif abs(alpha + beta + 1) < 10 * np.finfo(float).eps:
        h11[0] = 1.0
    elif abs(alpha + beta + 2) < 10 * np.finfo(float).eps:
        h1[1], h12[0] = 1.0, 1.0

    # equation (3.142) symmetric tridiagonal matrix A_{N+1}
    A = diags(0.5 * (beta**2 - alpha**2) / h12 / h1).toarray() + \
        diags(2 / h12[:-1] * np.sqrt(h2 * (h2 + alpha + beta) * \
        (h2 + alpha) * (h2 + beta) / h11[:-1] / h13[:-1]), 1).toarray()
    if alpha + beta < 10 * np.finfo(float).eps:
        A[0, 0] = 0.0

    r, V = eigh(A + A.T)
    # equation (3.144)
    w = np.power(V[0, :], 2) * np.power(2, alpha + beta + 1) * \
        gamma(alpha + 1) * gamma(beta + 1) / gamma(alpha + beta + 2)
    
    l = JacobiP(r, alpha + 1, alpha + 1, N - 1)[-1]
    # construct first order JG derivative matrix D by equation (3.164)
    Distance = r[:, None] - r[None, :] + np.eye(N)
    D = l[:, None] / l[None, :] / Distance
    np.fill_diagonal(D, 0)

    # for program stability, we force row sum of D to be 0
    # which ensure the derivative of constants to be zero matrix
    np.fill_diagonal(D, -np.sum(D, axis=1))
    return D, r, w


def Jacobi_Gauss_Lobatto(alpha, beta, N):
    """
    This function computes the Gauss-Lobatto quadrature first order
    derivative matrix, nodes and weights of Jacobi polynomial J_{N}^{alpha, beta}.
    The nodes are {-1, 1, zeros of dx(J_N^{alpha, beta}(x))}

    Parameters
    ----------
    alpha : float
        The alpha parameter of the Gauss-Lobatto quadrature. alpha > -1.
    beta : float
        The beta parameter of the Gauss-Lobatto quadrature. beta > -1.
        If alpha = beta = 0, the Jacobi polynomial is Legendre polynomial.
    N : int
        The order of the Gauss-Lobatto quadrature.

    Returns
    ----------
    D: ndarray, shape (N + 1, N + 1)
        The first order derivative matrix of the Gauss-Lobatto quadrature.
    r: ndarray, shape (N + 1,)
        The Gauss-Lobatto quadrature nodes.
    w: ndarray, shape (N + 1,)
        The Gauss-Lobatto quadrature weights.

    References
    ----------
    1. Code-reproduction/Poisson-GPU.ipynb
    2. https://en.wikipedia.org/wiki/Gaussian_quadrature#Gauss%E2%80%93Lobatto_rules
    """

    r = np.zeros((N + 1,))
    r[0], r[-1] = -1.0, 1.0
    if N == 1:
        return r
    # dx(J_N^{alpha, beta}(x)) = C(alpha, beta, N) * J_{N-1}^{alpha+1, beta+1}(x)
    # thus have same zeros
    r[1:-1] = Jacobi_Gauss(alpha + 1, beta + 1, N - 1)[1]

    w = (2 * N + 1) / (N * N + N) / np.power(JacobiP(r, 0, 0, N)[-1], 2)
    # construct first order LGL derivative matrix D
    Distance = r[:, None] - r[None, :] + np.eye(N + 1)
    omega = np.prod(Distance, axis=1)
    # equation (3.75)
    D = diags(omega) @ (1 / Distance) @ diags(1 / omega)
    # for program stability, we force row sum of D to be 0
    # which ensure the derivative of constants to be zero matrix
    np.fill_diagonal(D, 0)
    np.fill_diagonal(D, -np.sum(D, axis=1))
    return D, r, w


def HermiteP(x, N, normalized=False, return_full=True):
    """
    Evaluate orthognormal Hermite polynomial of degree N at x by recurrence relation.

    Parameters
    ----------
    x : ndarray
        The input array.
    N : int
        The degree of Hermite polynomial.
    normalized : bool, optional
        Whether to normalize PL[N] to have L2 norm 1. Default is False.
    return_full : bool, optional
        Whether to return the full PL array. Default is True.

    Returns
    ----------
    PL[N] or PL : ndarray, shape (N + 1, len(x))
        The value of Hermite polynomial of degree N at x, or the full PL array if return_full is True.

    References
    ----------
    Spectral Method P254
    """
    
    xp = x.copy()
    if len(xp.shape) == 2 and xp.shape[1] == 1:
        xp = xp.T
    PL = np.ones((N + 1, max(xp.shape)))
    if normalized:
        Norm = np.zeros(N + 1)
        Norm[0] = np.linalg.norm(PL[0])
    if N == 0:
        return PL[0] / Norm[0] if normalized else PL[0]
    PL[1] = 2 * xp
    if normalized:
        Norm[1] = np.linalg.norm(PL[1])
    if N == 1 and normalized:
        PL[0] /= Norm[0]
    for i in range(1, N):
        PL[i + 1] = 2 * xp * PL[i] - 2 * i * PL[i - 1]
        if normalized:
            if i == 1:
                PL[0] /= Norm[0]
            PL[i] /= Norm[i]
            PL[i + 1] /= Norm[i]
            Norm[i + 1] = np.linalg.norm(PL[i + 1])
    if normalized:
        PL[N] /= Norm[N]
    return PL if return_full else PL[N]


def HermiteF(x, N, return_full=True):
    """
    Evaluate modified Hermite Function of degree N at x by recurrence relation.

    Parameters
    ----------
    x : ndarray
        The input array.
    N : int
        The degree of Hermite polynomial.
    return_full : bool, optional
        Whether to return the full PL array. Default is True.

    Returns
    ----------
    PL[N] or PL : ndarray, shape (N + 1, len(x))
        The value of modified Hermite polynomial of degree N at x, or the full PL array if return_full is True.

    References
    ----------
    Spectral Method P256
    """

    xp = x.copy()
    if len(xp.shape) == 2 and xp.shape[1] == 1:
        xp = xp.T
    PL = np.ones((N + 1, max(xp.shape)))
    PL[0] = np.exp(-xp ** 2 / 2) / np.pi ** 0.25    # underflow may occur for large r
    if N == 0:
        return PL[0]
    PL[1] = np.sqrt(2) * xp * PL[0]
    for i in range(1, N):
        PL[i + 1] = np.sqrt(2 / (i + 1)) * xp * PL[i] - np.sqrt(i / (i + 1)) * PL[i - 1]
    return PL if return_full else PL[N]


def Hermite_Gauss(N, c=1 / np.sqrt(2)):
    """
    Generate the Hermite-Gauss(HG) quadrature points r and weights w w.r.t Hermite function.

    Parameters
    ----------
    N : int
        Number of points, underflow will occur for N > 740 with default c.
    c : float, optional
        The decay factor for v = exp(-(cx)^2) * u(x). Default is 1 / sqrt(2).
        If c = 0, it degenerates to Hermite-ploynomial case.

    Returns
    ----------
    D : ndarray, shape (N, N)
        The first order derivative matrix of Hermite-Gauss quadrature points. 
    r : ndarray, shape (N,)
        The Hermite-Gauss quadrature points.
    w : ndarray, shape (N,)
        The weights of Hermite-Gauss quadrature points.

    References
    ----------
    Spectral Method P261
    """

    r, w = roots_hermite(N)
    if c != 0:
        w = 1 / (HermiteF(r, N - 1, False)**2 * N)  # equ(7.81), modified weights for Hermite function
    H = HermiteP(r, N - 1, True, False) * np.exp(-(c * r) ** 2)  # equ(7.93), underflow may occur for large r
    dis = r[:, np.newaxis] - r[np.newaxis, :]
    np.fill_diagonal(dis, 1)
    D = H[:, np.newaxis] / H[np.newaxis, :] / dis
    np.fill_diagonal(D, r * (1 - 2 * c**2))
    return D, r, w