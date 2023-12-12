import numpy as np
from typing import Tuple


def fold_leaf_backward_conv(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    epsilon: float = 1.0e-3,
) -> Tuple[np.ndarray, np.ndarray]:
    new_W = W / np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + epsilon), axis=(0, 1, 3)),
        [W.shape[0], W.shape[1], 1, W.shape[3]],
    )
    gamma = np.tile(
        np.expand_dims(gamma, axis=(0, 1, 3)), [W.shape[0], W.shape[1], 1, W.shape[3]]
    )
    beta = np.tile(
        np.expand_dims(beta, axis=(0, 1, 3)), [W.shape[0], W.shape[1], 1, W.shape[3]]
    )
    mu = np.tile(
        np.expand_dims(mu, axis=(0, 1, 3)), [W.shape[0], W.shape[1], 1, W.shape[3]]
    )
    sigma = np.tile(
        np.expand_dims(sigma, axis=(0, 1, 3)), [W.shape[0], W.shape[1], 1, W.shape[3]]
    )
    new_b = (
        b
        - np.sum(beta * W, axis=(0, 1, 2))
        + np.sum(W * gamma * (mu / np.sqrt(sigma + epsilon)), axis=(0, 1, 2))
    )
    return (new_W, new_b)


def fold_leaf_backward_dense(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    epsilon: float = 1.0e-3,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W / np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + epsilon), axis=0), [W.shape[0], 1]
    )
    new_b = (
        b
        - np.sum(beta * W, axis=0)
        + np.sum(W * gamma * (mu / np.sqrt(sigma + epsilon)), axis=0)
    )
    return (new_W, new_b)


def fold_leaf_backward_depthwiseconv(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    epsilon: float = 1.0e-3,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W / np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + epsilon), axis=(0, 1, 3)),
        [W.shape[0], W.shape[1], 1, 1],
    )
    gamma = np.tile(
        np.expand_dims(gamma, axis=(0, 1, 3)), [W.shape[0], W.shape[1], 1, W.shape[3]]
    )
    beta = np.tile(
        np.expand_dims(beta, axis=(0, 1, 3)), [W.shape[0], W.shape[1], 1, W.shape[3]]
    )
    mu = np.tile(
        np.expand_dims(mu, axis=(0, 1, 3)), [W.shape[0], W.shape[1], 1, W.shape[3]]
    )
    sigma = np.tile(
        np.expand_dims(sigma, axis=(0, 1, 3)), [W.shape[0], W.shape[1], 1, W.shape[3]]
    )
    new_b = (
        b
        - np.sum(beta * W, axis=(0, 1, 3))
        + np.sum(W * gamma * (mu / np.sqrt(sigma + epsilon)), axis=(0, 1, 3))
    )
    return (new_W, new_b)


def fold_leaf_backward_bn(
    gamma_: np.ndarray,
    beta_: np.ndarray,
    mu_: np.ndarray,
    sigma_: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    epsilon: float = 1.0e-3,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """ """
    new_gamma = gamma_ * np.sqrt(sigma + epsilon) / gamma
    new_beta = beta_
    new_mu = beta - mu + gamma * mu_ / (sigma + epsilon)
    new_sigma = sigma_
    return (new_gamma, new_beta, new_mu, new_sigma)



def fold_root_backward_conv1D(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    epsilon: float = 1.0e-3,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Fold bn backwards into a conv1d layer.
    
    An alternative solution of the weights folding would be:
        gamma = gamma.reshape((1, 1, gamma.shape[0]))
        sigma = sigma.reshape((1, 1, sigma.shape[0]))
        new_W = ((gamma / np.sqrt(sigma + epsilon)) * W)

    Parameters
    ----------
    W : np.ndarray
        Weights of the original 1D convolution.
    b : np.ndarray
        Biases of the original 1D convolution..
    gamma : np.ndarray
        Gamma weight.
    beta : np.ndarray
        Beta weight.
    mu : np.ndarray
        Moving mean.
    sigma : np.ndarray
        Moving variance.
    epsilon : float, optional
        Small float added to variance to avoid dividing by zero. 
        The default is 1.0e-3.

    Returns
    -------
    new_W : TYPE
        Weights with folded batch normaization parameters.
    new_b : TYPE
        Bias with folded batch normalization parameters.

    """
    new_W = W * np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + epsilon), axis=(0,1)),
        [W.shape[0], W.shape[1], 1]
    )
    new_b = (gamma * (b - mu) / np.sqrt(sigma + epsilon)) + beta
    return (new_W, new_b)


def fold_root_backward_conv2D(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    epsilon: float = 1.0e-3,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W * np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + epsilon), axis=(0, 1, 2)),
        [W.shape[0], W.shape[1], W.shape[2], 1],
    )
    new_b = (gamma * (b - mu) / np.sqrt(sigma + epsilon)) + beta
    return (new_W, new_b)


def fold_root_backward_dense(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    epsilon: float = 1.0e-3,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W * np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + epsilon), axis=0), [W.shape[0], 1]
    )
    new_b = (gamma * (b - mu) / np.sqrt(sigma + epsilon)) + beta
    return (new_W, new_b)


def fold_root_backward_depthwiseconv2D(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    epsilon: float = 1.0e-3,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W * np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + epsilon), axis=(0, 1, 3)),
        [W.shape[0], W.shape[1], 1, W.shape[3]],
    )
    new_b = (gamma * (b - mu) / np.sqrt(sigma + epsilon)) + beta
    return (new_W, new_b)


def fold_root_backward_bn(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    epsilon: float = 1.0e-3,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = gamma * (W / (sigma + epsilon))
    new_b = gamma * (b - mu) / (sigma + epsilon) + beta
    return (new_W, new_b)


def fold_leaf_forward_conv(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    epsilon: float = 1.0e-3,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W / np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + epsilon), axis=(0, 1, 2)),
        [W.shape[0], W.shape[1], W.shape[2], 1],
    )
    new_b = (gamma * (b + mu) / np.sqrt(sigma + epsilon)) - beta
    return (new_W, new_b)


def fold_leaf_forward_depthwiseconv2D(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    epsilon: float = 1.0e-3,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W / np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + epsilon), axis=(0, 1, 3)),
        [W.shape[0], W.shape[1], 1, 1],
    )
    new_b = (gamma * (b + mu) / np.sqrt(sigma + epsilon)) - beta
    return (new_W, new_b)


def fold_leaf_forward_dense(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    epsilon: float = 1.0e-3,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W / np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + epsilon), axis=0), [W.shape[0], 1]
    )
    new_b = (gamma * (b + mu) / np.sqrt(sigma + epsilon)) - beta
    return (new_W, new_b)


def fold_leaf_forward_bn(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    epsilon: float = 1.0e-3,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    return (W, b)


def fold_root_forward_conv2D(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    epsilon: float = 1.0e-3,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W * np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + epsilon), axis=(0, 1, 3)),
        [W.shape[0], W.shape[1], 1, W.shape[3]],
    )
    new_b = (
        b
        + np.sum(
            np.tile(
                np.expand_dims(beta, axis=(0, 1, 3)),
                [W.shape[0], W.shape[1], 1, W.shape[3]],
            )
            * W,
            axis=(0, 1, 2),
        )
        - np.sum(
            W
            * np.tile(
                np.expand_dims(gamma * (mu / np.sqrt(sigma + epsilon)), axis=(0, 1, 3)),
                [W.shape[0], W.shape[1], 1, W.shape[3]],
            ),
            axis=(0, 1, 2),
        )
    )
    return (new_W, new_b)

def fold_root_forward_conv1D(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    epsilon: float = 1.0e-3,
) -> Tuple[np.ndarray, np.ndarray]:
    new_W = W * np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + epsilon), axis=(0, 2)),
        [W.shape[0], 1, W.shape[2]],
    )
    new_b = (
        b
        + np.sum(
            np.tile(
                np.expand_dims(beta, axis=(0, 2)),
                [W.shape[0], 1, W.shape[2]],
            )
            * W,
            axis=(0, 1),
        )
        - np.sum(
            W
            * np.tile(
                np.expand_dims(gamma * (mu / np.sqrt(sigma + epsilon)), axis=(0, 2)),
                [W.shape[0], 1, W.shape[2]],
            ),
            axis=(0, 1),
        )
    )
    return (new_W, new_b)


def fold_root_forward_depthwiseconv(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    epsilon: float = 1.0e-3,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W * np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + epsilon), axis=(0, 1, 3)),
        [W.shape[0], W.shape[1], 1, 1],
    )
    new_b = (
        b
        + np.sum(beta * W, axis=(0, 1, 3))
        - np.sum(W * gamma * (mu / np.sqrt(sigma + epsilon)), axis=(0, 1, 3))
    )
    return (new_W, new_b)


def fold_root_forward_dense(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    epsilon: float = 1.0e-3,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W * np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + epsilon), axis=1), [1, W.shape[1]]
    )
    new_b = (
        b
        + np.sum(np.tile(np.expand_dims(beta, axis=1), [1, W.shape[1]]) * W, axis=0)
        - np.sum(
            W
            * np.tile(
                np.expand_dims(gamma * (mu / np.sqrt(sigma + epsilon)), axis=1),
                [1, W.shape[1]],
            ),
            axis=0,
        )
    )
    return (new_W, new_b)


def fold_root_forward_bn(
    gamma_: np.ndarray,
    beta_: np.ndarray,
    mu_: np.ndarray,
    sigma_: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    epsilon: float = 1.0e-3,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """ """
    new_gamma = 0
    new_beta = 0
    new_mu = 0
    new_sigma = 0
    return (new_gamma, new_beta, new_mu, new_sigma)
