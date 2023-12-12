import tensorflow as tf
import numpy as np
from typing import Tuple
from enum import Enum

class TestStatus(Enum):
    FAIL = 0
    PASS = 1
    


def test_model_changes(
    model: tf.keras.Model,
    folded_model: tf.keras.Model,
    input_shape: Tuple[int]=None
) -> Tuple[str, TestStatus]:
    """
    Measure the difference between the original and folded model on a random input.

    Parameters
    ----------
    model : tf.keras.Model
        original model (model before folding).
    folded_model : tf.keras.Model
        new model (after folding).
    input_shape : Tuple[int], optional
        Input shape of the model, if not given, it is determined
                     from the models properties. For models with a single input,
                     always pass a tuple. For models with multiple inputs pass
                     list of tuples. The default is None.

    Returns
    -------
    Tuple[str, TestStatus]
        Name of the model and the tests result.

    """
    if input_shape is None:
        if isinstance(model.input_shape, list):
            input_shape = list()
            for in_shape in model.input_shape:
                input_shape.append([1] + list(
                    item for item in in_shape if item is not None))
        else:
            input_shape = [1] + list(
                item for item in model.input_shape if item is not None)
    
    err = 0
    for _ in range(100):
        if isinstance(input_shape[0], list):
            x = list()
            for i in input_shape:
                x.append(np.random.normal(size=i))
                #x.append(np.zeros(shape=i))
        else:
            x = np.random.normal(size=input_shape)
        y_original = model(x)
        y_folded = folded_model(x)
        err += np.sum(np.abs(y_folded - y_original))
    result_color = "\033[92m"
    result = TestStatus.PASS
    if err > 0.01:
        result_color = "\033[91m"
        result = TestStatus.FAIL
    print(
        f"[\033[94m{model.name}\033[0m]"
        f" error = {result_color}{err:.3f}\033[0m"
    )
    return (model.name, result)
