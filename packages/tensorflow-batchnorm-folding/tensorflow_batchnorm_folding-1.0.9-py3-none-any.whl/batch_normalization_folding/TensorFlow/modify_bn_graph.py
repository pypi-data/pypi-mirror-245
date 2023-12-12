from batch_normalization_folding.TensorFlow.lambda_layers import call_lambda_layer
import tensorflow as tf
from typing import Dict, Tuple


def get_input_tensors_dict(
    model: tf.keras.Model,
) -> Tuple[Dict[str, tf.Tensor], tf.keras.Input]:
    """
    this is a fix for multiple inputs

    Args:
        model: tf keras model from which we extract the input dict
    """
    inputs = []
    output = {}
    
    if isinstance(model, tf.keras.Sequential):
        # With sequential models the first layer is used as input layer.
        # Since this library outputs functional models, a explicit
        # input layer is added.
        config = model.layers[0].get_config()
        name = model.layers[0].name
        name = "sequential_input"
        output[name] = tf.keras.Input(
            shape=model.layers[0].input_shape[1:],
            dtype=config["dtype"],
            name=name,
        )
        inputs.append(output[name])
    else:
        # For functional models (tf.keras.Model).
        for layer in model.layers:
            if isinstance(layer, tf.keras.layers.InputLayer):
                config = layer.get_config()
                output[layer.name] = tf.keras.Input(
                    shape=config["batch_input_shape"][1:],
                    dtype=config["dtype"],
                    sparse=config["sparse"],
                    ragged=config["ragged"],
                    name=config["name"],
                )
                inputs.append(output[layer.name])
    if len(inputs) == 1:
        inputs = inputs[0]
    return output, inputs


def remove_folded_layers(
    model: tf.keras.Model, backward_graph: Dict[str, list], fold_dict: Dict[str, tuple]
) -> tf.keras.Model:
    """
    This function edits a neural network graph by removing the target layers
    Here the layers will systematically be batch-normalization layers
    """
    network_dict = {}
    network_dict["input_layers_of"] = backward_graph
    network_dict["new_output_tensor_of"], model_inputs = get_input_tensors_dict(
        model=model
    )
    model_outputs = []
    intermediate_outputs = {}
    
    if isinstance(model, tf.keras.Sequential):
        intermediate_outputs = {model.layers[0].name: model.layers[0].output}
        model_enumeration_begin = 0
        network_dict["input_layers_of"].update({model.layers[0].name : ["sequential_input"]})
    else:
        # Model must be a Functional model (tf.keras.Model).
        if not isinstance(model.input, list):
            # Model has a single input
            intermediate_outputs = {model.layers[0].name: model.input}
            model_enumeration_begin = 1
        else:
            # Model has many inputs.
            for e in model.input:
                intermediate_outputs[e.name] = [e]
            model_enumeration_begin = 0
            
    
    for cpt, layer in enumerate(model.layers[model_enumeration_begin:]):
        if isinstance(layer, tf.keras.layers.InputLayer):
            # Input layers are already added to intermediate_outputs.
            continue
        
        layer_input = [
            network_dict["new_output_tensor_of"][layer_aux]
            for layer_aux in network_dict["input_layers_of"][layer.name]
        ]
        if len(layer_input) == 1:
            layer_input = layer_input[0]
        if layer.name in fold_dict:
            x = intermediate_outputs[network_dict["input_layers_of"][layer.name][0]]
            intermediate_outputs[layer.name] = x
        else:
            if (
                len(network_dict["input_layers_of"][layer.name]) == 1
                or isinstance(layer, tf.keras.layers.Lambda)
                or "tfoplambda" in type(layer).__name__.lower()
            ):
                copied_layer = type(layer).from_config(layer.get_config())
                if "weights" in dir(copied_layer):
                    try:
                        layer_input_shape = layer.input_shape
                    except AttributeError:
                        layer_input_shape = layer.get_input_shape_at(0)
                    copied_layer.build(layer_input_shape)
                    copied_layer.set_weights(layer.get_weights())
                x = call_lambda_layer(
                    layer_input=layer_input,
                    model=model,
                    layer=copied_layer,
                    layer_cpt=cpt + 1,
                )
                intermediate_outputs[layer.name] = x
            else:
                if (
                    isinstance(layer, tf.keras.layers.Add)
                    or isinstance(layer, tf.keras.layers.Multiply)
                    or isinstance(layer, (tf.keras.layers.Concatenate))
                ):
                    copied_layer = type(layer).from_config(layer.get_config())
                    x = copied_layer(
                        [
                            intermediate_outputs[elem]
                            for elem in network_dict["input_layers_of"][layer.name]
                        ]
                    )
                else:
                    try:
                        copied_layer = type(layer).from_config(layer.get_config())
                        x = copied_layer(
                            intermediate_outputs[
                                network_dict["input_layers_of"][layer.name][0]
                            ],
                            intermediate_outputs[
                                network_dict["input_layers_of"][layer.name][1]
                            ],
                        )
                    except (TypeError):
                        # Some layers require their input as list.
                        x = copied_layer(
                            [
                            intermediate_outputs[
                                network_dict["input_layers_of"][layer.name][0]
                            ],
                            intermediate_outputs[
                                network_dict["input_layers_of"][layer.name][1]
                            ]]
                        )
                intermediate_outputs[layer.name] = x
        network_dict["new_output_tensor_of"].update({layer.name: x})
        if layer.name in model.output_names:
            model_outputs.append(x)
    if len(model_outputs) == 0:
        model_outputs = model_outputs[0]
    output_model = tf.keras.Model(inputs=model_inputs, outputs=model_outputs)
    output_model._name = model.name
    return output_model
