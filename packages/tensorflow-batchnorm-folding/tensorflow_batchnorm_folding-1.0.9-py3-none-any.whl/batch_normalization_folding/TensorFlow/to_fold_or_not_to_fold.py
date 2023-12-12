import tensorflow as tf
from typing import Dict, Tuple


def is_expressive_layer(layer: tf.keras.layers.Layer) -> bool:
    """
    In the folding mechanism a BN layer can be folded
    only in conv, dense, depthwise conv or other bn
    layers.
    """
    return (
        isinstance(layer, tf.keras.layers.Dense)
        or isinstance(layer, tf.keras.layers.Conv1D)
        or isinstance(layer, tf.keras.layers.DepthwiseConv2D)
        or isinstance(layer, tf.keras.layers.Conv2D)
        or isinstance(layer, tf.keras.layers.BatchNormalization)
    )


def is_non_affine(layer: tf.keras.layers.Layer, forward: bool) -> bool:
    """
    In the folding mechanism, affine transformations don't
    hold through activation functions
    """
    if (
        isinstance(layer, tf.keras.layers.Dense)
        or isinstance(layer, tf.keras.layers.DepthwiseConv2D)
        or isinstance(layer, tf.keras.layers.Conv2D)
    ) and not forward:
        return layer.get_config()["activation"] != "linear"
    return isinstance(layer, tf.keras.layers.Activation)


def search_end_nodes(
    current_node: str, model: tf.keras.Model, graph: Dict[str, list], forward=bool
) -> list:
    """
    search for end nodes as defined in the article.
    """
    output = []
    if len(graph[current_node]) == 0:
        return [None]
    for next_node in graph[current_node]:
        l = model.get_layer(next_node)
        if is_non_affine(layer=l, forward=forward):
            return [None]
        elif is_expressive_layer(layer=l):
            output.append(next_node)
        else:
            output += search_end_nodes(
                current_node=next_node, model=model, graph=graph, forward=forward
            )
    return output


def remove_duplicates(l: list) -> list:
    return list(dict.fromkeys(l))


def merge_lists(old_list: list, new_list: list) -> (list):
    """
    when finding new roots or leaves, we add them to previous ones
    """
    return remove_duplicates(l=new_list + old_list)


def check_sanity(roots: list, leaves: list) -> bool:
    """
    checks that the roots and leaves are disjoint
    """
    return set(roots).isdisjoint(leaves)


def clear_leaves(leaves: list, target_layer: str) -> list:
    """
    the target layer can't be a leaf
    """
    if target_layer in leaves:
        leaves.remove(target_layer)
    return leaves


def clear_new_leaves(leaves: list, new_leaves: list) -> list:
    """
    we only keep leaves that were never seen
    """
    output = []
    for leaf in new_leaves:
        if leaf not in leaves:
            output.append(leaf)
    return output


def check_layer_can_be_folded(
    model: tf.keras.Model,
    layer: tf.keras.layers.Layer,
    forward_graph: Dict[str, list],
    backward_graph: Dict[str, list],
    forward: bool,
) -> Tuple[bool, list, list]:
    """
    check if a layer can be folded
    """
    new_roots = remove_duplicates(
        search_end_nodes(
            current_node=layer.name, model=model, graph=forward_graph, forward=forward
        )
    )
    roots = []
    leaves = [layer.name]
    while len(new_roots) != 0:
        roots = merge_lists(old_list=roots, new_list=new_roots)
        if None in roots:
            return False, [], []
        current_root = new_roots[0]
        new_roots.pop(0)
        new_leaves = remove_duplicates(
            search_end_nodes(
                current_node=current_root,
                model=model,
                graph=backward_graph,
                forward=(not forward),
            )
        )
        new_leaves = clear_new_leaves(leaves=leaves, new_leaves=new_leaves)
        leaves = merge_lists(old_list=leaves, new_list=new_leaves)
        if None in leaves:
            return False, [], []
        for leaf in new_leaves:
            new_roots = merge_lists(
                old_list=new_roots,
                new_list=remove_duplicates(
                    search_end_nodes(
                        current_node=leaf,
                        model=model,
                        graph=forward_graph,
                        forward=forward,
                    )
                ),
            )
            if None in new_roots:
                return False, [], []
            roots = merge_lists(old_list=roots, new_list=new_roots)
            if not check_sanity(roots=roots, leaves=leaves):
                return False, [], []
    leaves = clear_leaves(leaves=leaves, target_layer=layer.name)
    return True, roots, leaves


def is_expressive_layer_simple(layer: tf.keras.layers.Layer) -> bool:
    """
    In the simple folding mechanism a BN layer can be folded
    only in conv, dense, depthwise conv layers.

    Parameters
    ----------
    layer : tf.keras.layers.Layer
        Layer to analyze.

    Returns
    -------
    bool
        True if the layer is expressive and can be used to fold in bn weights.

    """
    return (
        isinstance(layer, tf.keras.layers.Dense)
        or isinstance(layer, tf.keras.layers.Conv1D)
        or isinstance(layer, tf.keras.layers.DepthwiseConv2D)
        or isinstance(layer, tf.keras.layers.Conv2D)
    )

def check_layer_can_be_folded_simple(
    model: tf.keras.Model,
    layer: tf.keras.layers.Layer,
    forward_graph: Dict[str, list],
    backward_graph: Dict[str, list],
) -> Tuple[bool, list, bool]:
    """
    Check if a layer can be folded by analyzing the previous and the
    following layer. Leaves are not considered.
    Only recommended for simple sequential networks.

    Parameters
    ----------
    model : tf.keras.Model
        Model to be fold.
    layer : tf.keras.layers.Layer
        Layer to analyze.
    forward_graph : Dict[str, list]
        Graph in forward direction.
    backward_graph : Dict[str, list]
        Graph in backward direction.

    Returns
    -------
    Tuple[bool, list, bool]
        foldable, roots, forward
        foldable is True, when the layer is foldable
        roots is a list with the root layer (the one to fold into).
        forward is True when the layer is fold towards an output of the model.
    """
    
    roots = list()
    forward = False
    foldable = False
    # Get layer before and after current layer.
    near_output = forward_graph[layer.name][0]
    near_input = backward_graph[layer.name][0]
    # Search layers within model, check foldability.
    for l in model.layers:
        if (l.name == near_input and is_expressive_layer_simple(l)):
            forward = False
            roots.append(l.name)
            foldable = True
        elif (l.name == near_output and is_expressive_layer_simple(l)):
            forward = True
            roots.append(l.name)
            foldable = True
    return foldable, roots, forward
    