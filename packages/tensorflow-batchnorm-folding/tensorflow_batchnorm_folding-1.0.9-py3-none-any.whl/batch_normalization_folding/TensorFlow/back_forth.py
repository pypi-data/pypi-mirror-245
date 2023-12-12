from batch_normalization_folding.TensorFlow.to_fold_or_not_to_fold import (
    check_layer_can_be_folded,
)
from typing import Dict, Tuple
import tensorflow as tf


def check_layer(
    model: tf.keras.Model,
    layer: tf.keras.layers.Layer,
    forward_graph: Dict[str, list],
    backward_graph: Dict[str, list],
) -> Tuple[bool, list, list, bool]:
    """
    

    Parameters
    ----------
    model : tf.keras.Model
        Model to be folded.
    layer : tf.keras.layers.Layer
        Layer to be folded.
    forward_graph : Dict[str, list]
        Graph in forward direction.
    backward_graph : Dict[str, list]
        Graph in backward direction.

    Returns
    -------
    Tuple[bool, list, list, bool]
        foldeable is True when the layer is foldable.
        roots is a list containing the nodes the be folded to.
        leaves is a list of leaves, inferencing with the folding.
        forward is True when the layer is fold towards an output of the model.

    """
    forward = False
    foldeable, roots, leaves = check_layer_can_be_folded(
        model=model,
        layer=layer,
        forward_graph=backward_graph,
        backward_graph=forward_graph,
        forward=forward,
    )
    if not foldeable:
        forward = True
        foldeable, roots, leaves = check_layer_can_be_folded(
            model=model,
            layer=layer,
            forward_graph=forward_graph,
            backward_graph=backward_graph,
            forward=forward,
        )
    return foldeable, roots, leaves, forward
