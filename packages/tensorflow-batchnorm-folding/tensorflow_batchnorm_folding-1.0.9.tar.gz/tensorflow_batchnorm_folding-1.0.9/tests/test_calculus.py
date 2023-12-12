import numpy as np
import pytest

from batch_normalization_folding.TensorFlow.calculus import (
    fold_leaf_backward_bn,
    fold_leaf_backward_conv,
    fold_leaf_backward_dense,
    fold_leaf_backward_depthwiseconv,
    fold_leaf_forward_conv,
    fold_leaf_forward_dense,
    fold_leaf_forward_depthwiseconv,
    fold_root_backward_bn,
    fold_root_backward_conv,
    fold_root_backward_dense,
    fold_root_backward_depthwiseconv,
    fold_root_forward_conv,
    fold_root_forward_dense,
    fold_root_forward_depthwiseconv,
)

SEED = 42


@pytest.mark.parametrize(
    "w_exp,b_exp",
    [
        (
            np.array(
                [
                    [
                        [
                            [0.27976543, 0.71014287, 0.54676812, 0.44717225],
                            [0.53537613, 0.53529336, 0.19931323, 2.97227327],
                        ],
                        [
                            [0.44900717, 0.52889989, 0.01537574, 0.72448112],
                            [2.85651715, 0.72863917, 0.62393024, 0.62935042],
                        ],
                        [
                            [0.22725592, 0.39197058, 0.32264443, 0.21753569],
                            [2.09956602, 0.47867154, 1.00249093, 1.25716636],
                        ],
                    ],
                    [
                        [
                            [0.34066474, 0.58649281, 0.14914776, 0.3841111],
                            [2.03286364, 0.15939405, 2.08478303, 0.58515153],
                        ],
                        [
                            [0.04859075, 0.70877685, 0.72128577, 0.60383819],
                            [1.04527857, 0.33516071, 2.3479376, 1.51037811],
                        ],
                        [
                            [0.09115733, 0.36987594, 0.02568675, 0.67922339],
                            [0.88800047, 2.27343744, 1.0696329, 1.78460731],
                        ],
                    ],
                    [
                        [
                            [0.40836916, 0.13807836, 0.72423819, 0.57899102],
                            [3.22387959, 3.07058955, 2.05168676, 3.16340061],
                        ],
                        [
                            [0.06610011, 0.1463908, 0.03378285, 0.24300782],
                            [1.33374156, 0.93113102, 2.84380303, 1.22419485],
                        ],
                        [
                            [0.20984605, 0.40537073, 0.10526436, 0.59920679],
                            [0.25581966, 3.38649094, 2.64994886, 0.68189053],
                        ],
                    ],
                ]
            ),
            np.array([2.54197078, 5.29671329, 3.81337795, 5.77137972]),
        )
    ],
)
def test_fold_leaf_backward_conv(w_exp, b_exp):
    np.random.seed(SEED)
    w = np.random.rand(3, 3, 2, 4)
    b = np.random.rand(4)
    gamma = np.random.rand(2)
    beta = np.random.rand(2)
    mu = np.random.rand(2)
    sigma = np.random.rand(2)
    new_w, new_b = fold_leaf_backward_conv(w, b, gamma, beta, mu, sigma)
    np.testing.assert_array_almost_equal(new_w, w_exp)
    np.testing.assert_array_almost_equal(new_b, b_exp)


@pytest.mark.parametrize(
    "w_exp,b_exp",
    [
        (
            np.array(
                [
                    [0.45399734, 0.38034722, 3.03462887, 0.77323651],
                    [0.18911739, 0.0624079, 0.24079736, 1.11876644],
                    [0.72863922, 0.28327484, 0.08533718, 1.25275049],
                    [1.0090421, 0.08494938, 0.75379216, 0.23688809],
                    [0.36878605, 0.20993652, 1.7907154, 0.37615604],
                ]
            ),
            np.array([-0.61022104, 6.07357709, -0.24147781, 1.69116677]),
        )
    ],
)
def test_fold_leaf_backward_dense(w_exp, b_exp):
    np.random.seed(SEED)
    w = np.random.rand(5, 4)
    b = np.random.rand(4)
    gamma = np.random.rand(4)
    beta = np.random.rand(4)
    mu = np.random.rand(4)
    sigma = np.random.rand(4)
    new_w, new_b = fold_leaf_backward_dense(w, b, gamma, beta, mu, sigma)
    np.testing.assert_array_almost_equal(new_w, w_exp)
    np.testing.assert_array_almost_equal(new_b, b_exp)


@pytest.mark.parametrize(
    "w_exp,b_exp",
    [
        (
            np.array(
                [
                    [
                        [[2.97633343], [1.81719613], [16.47294075], [0.63246059]],
                        [[1.23982311], [0.29816806], [1.30712544], [0.91508312]],
                        [[4.77684129], [1.35341052], [0.46323765], [1.02467395]],
                    ],
                    [
                        [[6.61511741], [0.40586516], [4.09182609], [0.19376009]],
                        [[2.4177019], [1.00301989], [9.72057867], [0.30767284]],
                        [[4.86217132], [0.26662868], [6.57448267], [0.38704776]],
                    ],
                    [
                        [[3.62422147], [1.50078599], [4.49349946], [0.5432697]],
                        [[4.70770205], [0.08878536], [13.67231308], [0.18015244]],
                        [[0.51694123], [1.81370062], [21.73077994], [0.85404195]],
                    ],
                ]
            ),
            np.array([-0.45412748, -2.43256732, -0.25311954, 1.45896761]),
        )
    ],
)
def test_fold_leaf_backward_depthwiseconv(w_exp, b_exp):
    np.random.seed(SEED)
    w = np.random.rand(3, 3, 4, 1)
    b = np.random.rand(4)
    gamma = np.random.rand(4)
    beta = np.random.rand(4)
    mu = np.random.rand(4)
    sigma = np.random.rand(4)
    new_w, new_b = fold_leaf_backward_depthwiseconv(w, b, gamma, beta, mu, sigma)
    np.testing.assert_array_almost_equal(new_w, w_exp)
    np.testing.assert_array_almost_equal(new_b, b_exp)


@pytest.mark.parametrize(
    "gamma_exp, beta_exp, mu_exp, sigma_exp",
    [
        (
            np.array([0.9483266, 0.39465014, 1.3219813, 0.8513476]),
            np.array([0.15601864, 0.15599452, 0.05808361, 0.86617615]),
            np.array([0.46397315, 7.18492712, 0.10708174, 1.4989279]),
            np.array([0.83244264, 0.21233911, 0.18182497, 0.18340451]),
        )
    ],
)
def test_fold_leaf_backward_bn(gamma_exp, beta_exp, mu_exp, sigma_exp):
    np.random.seed(SEED)
    gamma_ = np.random.rand(4)
    beta_ = np.random.rand(4)
    mu_ = np.random.rand(4)
    sigma_ = np.random.rand(4)
    gamma = np.random.rand(4)
    beta = np.random.rand(4)
    mu = np.random.rand(4)
    sigma = np.random.rand(4)
    new_gamma, new_beta, new_mu, new_sigma = fold_leaf_backward_bn(gamma_, beta_, mu_, sigma_, gamma, beta, mu, sigma)
    np.testing.assert_array_almost_equal(new_gamma, gamma_exp)
    np.testing.assert_array_almost_equal(new_beta, beta_exp)
    np.testing.assert_array_almost_equal(new_mu, mu_exp)
    np.testing.assert_array_almost_equal(new_sigma, sigma_exp)


@pytest.mark.parametrize(
    "w_exp,b_exp",
    [
        (
            np.array(
                [
                    [
                        [
                            [0.30651129, 0.10233272, 0.7555998, 0.0820773],
                            [0.12768051, 0.01679089, 0.05995673, 0.11875452],
                        ],
                        [
                            [0.49193272, 0.07621532, 0.02124832, 0.13297663],
                            [0.68124363, 0.0228557, 0.18768859, 0.02514513],
                        ],
                        [
                            [0.24898183, 0.05648358, 0.44587469, 0.03992811],
                            [0.50072025, 0.0150148, 0.30156594, 0.05022896],
                        ],
                    ],
                    [
                        [
                            [0.37323265, 0.08451455, 0.206113, 0.07050259],
                            [0.48481256, 0.00499982, 0.62713739, 0.02337921],
                        ],
                        [
                            [0.05323608, 0.10213587, 0.99677242, 0.11083293],
                            [0.24928587, 0.0105132, 0.70629866, 0.06034581],
                        ],
                        [
                            [0.09987207, 0.05329971, 0.03549751, 0.12466969],
                            [0.21177701, 0.07131239, 0.32176336, 0.07130239],
                        ],
                    ],
                    [
                        [
                            [
                                0.44740968,
                                0.01989731,
                                1.00085248,
                                0.1062723,
                            ],
                            [0.76885498, 0.09631717, 0.61718148, 0.12639085],
                        ],
                        [
                            [0.07241935, 0.02109515, 0.04668581, 0.04460345],
                            [0.31808069, 0.02920739, 0.85546322, 0.04891161],
                        ],
                        [
                            [0.22990755, 0.05841457, 0.14546885, 0.10998285],
                            [0.06100979, 0.10622626, 0.79714866, 0.02724433],
                        ],
                    ],
                ]
            ),
            np.array([0.61312486, 0.67607054, 0.30741557, 0.07609629]),
        )
    ],
)
def test_fold_root_backward_conv(w_exp, b_exp):
    np.random.seed(SEED)
    w = np.random.rand(3, 3, 2, 4)
    b = np.random.rand(4)
    gamma = np.random.rand(4)
    beta = np.random.rand(4)
    mu = np.random.rand(4)
    sigma = np.random.rand(4)
    new_w, new_b = fold_root_backward_conv(w, b, gamma, beta, mu, sigma)
    np.testing.assert_array_almost_equal(new_w, w_exp)
    np.testing.assert_array_almost_equal(new_b, b_exp)


@pytest.mark.parametrize(
    "w_exp,b_exp",
    [
        (
            np.array(
                [
                    [0.30898925, 2.37640144, 0.17656694, 0.46349594],
                    [0.12871274, 0.38992324, 0.01401056, 0.67061461],
                    [0.4959097, 1.76989521, 0.00496526, 0.75092776],
                    [0.68675108, 0.53076194, 0.04385867, 0.14199623],
                    [0.2509947, 1.31167895, 0.10419104, 0.22547667],
                ]
            ),
            np.array([1.04351638, -1.97670159, 0.44509049, -0.1717105]),
        )
    ],
)
def test_fold_root_backward_dense(w_exp, b_exp):
    np.random.seed(SEED)
    w = np.random.rand(5, 4)
    b = np.random.rand(4)
    gamma = np.random.rand(4)
    beta = np.random.rand(4)
    mu = np.random.rand(4)
    sigma = np.random.rand(4)
    new_w, new_b = fold_root_backward_dense(w, b, gamma, beta, mu, sigma)
    np.testing.assert_array_almost_equal(new_w, w_exp)
    np.testing.assert_array_almost_equal(new_b, b_exp)


@pytest.mark.parametrize(
    "w_exp,b_exp",
    [
        (
            np.array(
                [
                    [
                        [
                            [4.71319172e-02],
                            [4.97391382e-01],
                            [3.25269871e-02],
                            [5.66662948e-01],
                        ],
                        [
                            [1.96332977e-02],
                            [8.16126669e-02],
                            [2.58101167e-03],
                            [8.19883023e-01],
                        ],
                        [
                            [7.56439738e-02],
                            [3.70446932e-01],
                            [9.14695521e-04],
                            [9.18072641e-01],
                        ],
                    ],
                    [
                        [
                            [1.04754112e-01],
                            [1.11090832e-01],
                            [8.07960015e-03],
                            [1.73602384e-01],
                        ],
                        [
                            [3.82856721e-02],
                            [2.74540232e-01],
                            [1.91939704e-02],
                            [2.75664285e-01],
                        ],
                        [
                            [7.69952230e-02],
                            [7.29799095e-02],
                            [1.29817812e-02],
                            [3.46781491e-01],
                        ],
                    ],
                    [
                        [
                            [5.73915894e-02],
                            [4.10785610e-01],
                            [8.87273263e-03],
                            [4.86750978e-01],
                        ],
                        [
                            [7.45491150e-02],
                            [2.43017643e-02],
                            [2.69969496e-02],
                            [1.61410395e-01],
                        ],
                        [
                            [8.18605575e-03],
                            [4.96434613e-01],
                            [4.29089626e-02],
                            [7.65192236e-01],
                        ],
                    ],
                ]
            ),
            np.array([0.22831469, 0.61691053, 0.29903115, 0.20299085]),
        )
    ],
)
def test_fold_root_backward_depthwiseconv(w_exp, b_exp):
    np.random.seed(SEED)
    w = np.random.rand(3, 3, 4, 1)
    b = np.random.rand(4)
    gamma = np.random.rand(4)
    beta = np.random.rand(4)
    mu = np.random.rand(4)
    sigma = np.random.rand(4)
    new_w, new_b = fold_root_backward_depthwiseconv(w, b, gamma, beta, mu, sigma)
    np.testing.assert_array_almost_equal(new_w, w_exp)
    np.testing.assert_array_almost_equal(new_b, b_exp)


@pytest.mark.parametrize(
    "w_exp,b_exp",
    [
        (
            np.array([0.36736661, 4.79148859, 0.05140031, 1.58057994]),
            np.array([0.68705794, -1.64617767, 0.15557258, 1.70138134]),
        )
    ],
)
def test_fold_root_backward_bn(w_exp, b_exp):
    np.random.seed(SEED)
    w = np.random.rand(4)
    b = np.random.rand(4)
    gamma = np.random.rand(4)
    beta = np.random.rand(4)
    mu = np.random.rand(4)
    sigma = np.random.rand(4)
    new_w, new_b = fold_root_backward_bn(w, b, gamma, beta, mu, sigma)
    np.testing.assert_array_almost_equal(new_w, w_exp)
    np.testing.assert_array_almost_equal(new_b, b_exp)


@pytest.mark.parametrize(
    "w_exp,b_exp",
    [
        (
            np.array(
                [
                    [
                        [
                            [0.45766764, 8.83253875, 0.70912556, 4.36651744],
                            [0.19064629, 1.44925519, 0.05626901, 6.31774768],
                        ],
                        [
                            [0.73452983, 6.57829428, 0.01994141, 7.07436443],
                            [1.01719961, 1.97272031, 0.17614453, 1.33772261],
                        ],
                        [
                            [
                                0.37176746,
                                4.8752096,
                                0.41845053,
                                2.1241779,
                            ],
                            [0.74765094, 1.29595707, 0.28301769, 2.67218359],
                        ],
                    ],
                    [
                        [
                            [0.5572927, 7.29461738, 0.19343573, 3.75074221],
                            [0.72389837, 0.43154402, 0.58856441, 1.24377517],
                        ],
                        [
                            [0.07948951, 8.81554871, 0.93546451, 5.89631854],
                            [0.37222145, 0.90741533, 0.66285675, 3.21040058],
                        ],
                        [
                            [0.14912408, 4.60040331, 0.03331418, 6.63243486],
                            [0.31621506, 6.15511275, 0.30197284, 3.79329141],
                        ],
                    ],
                    [
                        [
                            [0.66805021, 1.71737622, 0.93929362, 5.65369252],
                            [1.14801658, 8.31332525, 0.57922085, 6.72400047],
                        ],
                        [
                            [0.10813302, 1.82076383, 0.04381433, 2.37290643],
                            [0.4749425, 2.52094748, 0.80284674, 2.60210064],
                        ],
                        [
                            [0.34328668, 5.04187657, 0.13652158, 5.85109408],
                            [
                                0.09109683,
                                9.16859781,
                                0.7481189,
                                1.4493998,
                            ],
                        ],
                    ],
                ]
            ),
            np.array([-0.60408662, -0.50052173, 1.15188959, 0.12380046]),
        )
    ],
)
def test_fold_leaf_forward_conv(w_exp, b_exp):
    np.random.seed(SEED)
    w = np.random.rand(3, 3, 2, 4)
    b = np.random.rand(4)
    gamma = np.random.rand(4)
    beta = np.random.rand(4)
    mu = np.random.rand(4)
    sigma = np.random.rand(4)
    new_w, new_b = fold_leaf_forward_conv(w, b, gamma, beta, mu, sigma)
    np.testing.assert_array_almost_equal(new_w, w_exp)
    np.testing.assert_array_almost_equal(new_b, b_exp)


@pytest.mark.parametrize(
    "w_exp,b_exp",
    [
        (
            np.array(
                [
                    [
                        [[2.97633343], [1.81719613], [16.47294075], [0.63246059]],
                        [[1.23982311], [0.29816806], [1.30712544], [0.91508312]],
                        [[4.77684129], [1.35341052], [0.46323765], [1.02467395]],
                    ],
                    [
                        [[6.61511741], [0.40586516], [4.09182609], [0.19376009]],
                        [[2.4177019], [1.00301989], [9.72057867], [0.30767284]],
                        [[4.86217132], [0.26662868], [6.57448267], [0.38704776]],
                    ],
                    [
                        [[3.62422147], [1.50078599], [4.49349946], [0.5432697]],
                        [[4.70770205], [0.08878536], [13.67231308], [0.18015244]],
                        [[0.51694123], [1.81370062], [21.73077994], [0.85404195]],
                    ],
                ]
            ),
            np.array([-0.15164984, -0.51471102, -0.2382218, 0.6302659]),
        )
    ],
)
def test_fold_leaf_forward_depthwiseconv(w_exp, b_exp):
    np.random.seed(SEED)
    w = np.random.rand(3, 3, 4, 1)
    b = np.random.rand(4)
    gamma = np.random.rand(4)
    beta = np.random.rand(4)
    mu = np.random.rand(4)
    sigma = np.random.rand(4)
    new_w, new_b = fold_leaf_forward_depthwiseconv(w, b, gamma, beta, mu, sigma)
    np.testing.assert_array_almost_equal(new_w, w_exp)
    np.testing.assert_array_almost_equal(new_b, b_exp)


@pytest.mark.parametrize(
    "w_exp,b_exp",
    [
        (
            np.array(
                [
                    [0.45399734, 0.38034722, 3.03462887, 0.77323651],
                    [0.18911739, 0.0624079, 0.24079736, 1.11876644],
                    [0.72863922, 0.28327484, 0.08533718, 1.25275049],
                    [1.0090421, 0.08494938, 0.75379216, 0.23688809],
                    [0.36878605, 0.20993652, 1.7907154, 0.37615604],
                ]
            ),
            np.array([-0.03397983, 2.67405811, -0.30415193, 0.73900297]),
        )
    ],
)
def test_fold_leaf_forward_dense(w_exp, b_exp):
    np.random.seed(SEED)
    w = np.random.rand(5, 4)
    b = np.random.rand(4)
    gamma = np.random.rand(4)
    beta = np.random.rand(4)
    mu = np.random.rand(4)
    sigma = np.random.rand(4)
    new_w, new_b = fold_leaf_forward_dense(w, b, gamma, beta, mu, sigma)
    np.testing.assert_array_almost_equal(new_w, w_exp)
    np.testing.assert_array_almost_equal(new_b, b_exp)


def test_fold_leaf_forward_bn():
    pass


@pytest.mark.parametrize(
    "w_exp,b_exp",
    [
        (
            np.array(
                [
                    [
                        [
                            [0.50142114, 1.27278289, 0.97996776, 0.80146293],
                            [0.04546676, 0.04545973, 0.01692665, 0.25241996],
                        ],
                        [
                            [0.80475165, 0.94794268, 0.0275578, 1.29848121],
                            [0.24258939, 0.0618796, 0.0529872, 0.05344751],
                        ],
                        [
                            [0.40730882, 0.70252546, 0.57827281, 0.38988734],
                            [0.1783054, 0.04065113, 0.08513643, 0.10676471],
                        ],
                    ],
                    [
                        [
                            [0.61057046, 1.05116598, 0.26731624, 0.68843899],
                            [0.17264071, 0.01353652, 0.17704996, 0.04969393],
                        ],
                        [
                            [0.08708879, 1.2703346, 1.29275422, 1.08225395],
                            [0.08877016, 0.02846348, 0.19939833, 0.12826869],
                        ],
                        [
                            [0.1633805, 0.66292544, 0.04603814, 1.21736619],
                            [0.07541334, 0.19307141, 0.09083845, 0.15155757],
                        ],
                    ],
                    [
                        [
                            [0.7319165, 0.24747665, 1.29804582, 1.03772058],
                            [0.2737876, 0.26076946, 0.17423926, 0.26865143],
                        ],
                        [
                            [0.11847065, 0.26237497, 0.0605487, 0.43554081],
                            [0.11326785, 0.07907619, 0.24150964, 0.10396461],
                        ],
                        [
                            [0.37610525, 0.72654244, 0.1886644, 1.07395312],
                            [0.02172545, 0.28759735, 0.2250466, 0.05790947],
                        ],
                    ],
                ]
            ),
            np.array([-2.53092655, -3.66579043, -2.39966326, -4.31336539]),
        )
    ],
)
def test_fold_root_forward_conv(w_exp, b_exp):
    np.random.seed(SEED)
    w = np.random.rand(3, 3, 2, 4)
    b = np.random.rand(4)
    gamma = np.random.rand(2)
    beta = np.random.rand(2)
    mu = np.random.rand(2)
    sigma = np.random.rand(2)
    new_w, new_b = fold_root_forward_conv(w, b, gamma, beta, mu, sigma)
    np.testing.assert_array_almost_equal(new_w, w_exp)
    np.testing.assert_array_almost_equal(new_b, b_exp)


@pytest.mark.parametrize(
    "w_exp,b_exp",
    [
        (
            np.array(
                [
                    [
                        [
                            [4.71319172e-02],
                            [4.97391382e-01],
                            [3.25269871e-02],
                            [5.66662948e-01],
                        ],
                        [
                            [1.96332977e-02],
                            [8.16126669e-02],
                            [2.58101167e-03],
                            [8.19883023e-01],
                        ],
                        [
                            [7.56439738e-02],
                            [3.70446932e-01],
                            [9.14695521e-04],
                            [9.18072641e-01],
                        ],
                    ],
                    [
                        [
                            [1.04754112e-01],
                            [1.11090832e-01],
                            [8.07960015e-03],
                            [1.73602384e-01],
                        ],
                        [
                            [3.82856721e-02],
                            [2.74540232e-01],
                            [1.91939704e-02],
                            [2.75664285e-01],
                        ],
                        [
                            [7.69952230e-02],
                            [7.29799095e-02],
                            [1.29817812e-02],
                            [3.46781491e-01],
                        ],
                    ],
                    [
                        [
                            [5.73915894e-02],
                            [4.10785610e-01],
                            [8.87273263e-03],
                            [4.86750978e-01],
                        ],
                        [
                            [7.45491150e-02],
                            [2.43017643e-02],
                            [2.69969496e-02],
                            [1.61410395e-01],
                        ],
                        [
                            [8.18605575e-03],
                            [4.96434613e-01],
                            [4.29089626e-02],
                            [7.65192236e-01],
                        ],
                    ],
                ]
            ),
            np.array([3.5426725, 3.72339411, 3.5133979, 4.30668742]),
        )
    ],
)
def test_fold_root_forward_depthwiseconv(w_exp, b_exp):
    np.random.seed(SEED)
    w = np.random.rand(3, 3, 4, 1)
    b = np.random.rand(4)
    gamma = np.random.rand(4)
    beta = np.random.rand(4)
    mu = np.random.rand(4)
    sigma = np.random.rand(4)
    new_w, new_b = fold_root_forward_depthwiseconv(w, b, gamma, beta, mu, sigma)
    np.testing.assert_array_almost_equal(new_w, w_exp)
    np.testing.assert_array_almost_equal(new_b, b_exp)


@pytest.mark.parametrize(
    "w_exp,b_exp",
    [
        (
            np.array(
                [
                    [0.25717898, 0.65281053, 0.5026256, 0.41107045],
                    [0.34923956, 0.34918557, 0.13001713, 1.93888999],
                    [0.17039637, 0.20071533, 0.00583503, 0.2749376],
                    [2.27553893, 0.58044349, 0.49703099, 0.50134878],
                    [0.18890702, 0.32582647, 0.26819894, 0.18082706],
                ]
            ),
            np.array([0.23530335, -0.34251163, -0.03765195, -0.84670421]),
        )
    ],
)
def test_fold_root_forward_dense(w_exp, b_exp):
    np.random.seed(SEED)
    w = np.random.rand(5, 4)
    b = np.random.rand(4)
    gamma = np.random.rand(5)
    beta = np.random.rand(5)
    mu = np.random.rand(5)
    sigma = np.random.rand(5)
    new_w, new_b = fold_root_forward_dense(w, b, gamma, beta, mu, sigma)
    np.testing.assert_array_almost_equal(new_w, w_exp)
    np.testing.assert_array_almost_equal(new_b, b_exp)


def test_fold_root_forward_bn():
    pass
