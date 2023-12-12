# -*- coding: utf-8 -*-
# 
# author:    paspf
# date:      2023-09-22
# license:   MIT
#
# This file contains example models using batch normalization.

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers


def functional_dense_only():
    initializer = keras.initializers.RandomUniform(minval=-0.2, 
                                                   maxval=0.2, 
                                                   seed=42)
    inputs = keras.Input(shape=[20])
    x = layers.Dense(40,
                     activation="relu",
                     kernel_initializer=initializer, 
                     bias_initializer=initializer)(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(30,
                     activation="relu",
                     kernel_initializer=initializer, 
                     bias_initializer=initializer)(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(10, 
                     activation="softmax",
                     kernel_initializer=initializer, 
                     bias_initializer=initializer)(x)
    model = keras.Model(inputs, outputs=x, name="functional_dense_only")
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    return model

def sequantial_dense_only():
    initializer = keras.initializers.RandomUniform(minval=-0.2, 
                                                   maxval=0.2, 
                                                   seed=42)
    
    model = keras.Sequential(name="sequential_dense_only")
    model.add(keras.Input(shape=[20]))
    model.add(layers.Dense(40,
                     activation="relu",
                     kernel_initializer=initializer, 
                     bias_initializer=initializer,
                     name="Dense_1"))
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(30,
                     activation="relu",
                     kernel_initializer=initializer, 
                     bias_initializer=initializer,
                     name="Dense_2"))
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(10, 
                     activation="softmax",
                     kernel_initializer=initializer, 
                     bias_initializer=initializer,
                     name="Dense_3"))
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    return model


def functional_conv2d_simple():
    initializer = keras.initializers.RandomUniform(minval=-0.2, 
                                                   maxval=0.2, 
                                                   seed=42)
    inputs = keras.Input(shape=[20,20,3])
    x = layers.Conv2D(32, 
                      kernel_size=(3, 3), 
                      activation="relu", 
                      kernel_initializer=initializer, 
                      bias_initializer=initializer)(inputs)
    x = layers.MaxPooling2D(pool_size=(2, 2))(x)
    x = layers.BatchNormalization()(x)
    x = layers.Conv2D(64, 
                      kernel_size=(3, 3), 
                      activation="relu", 
                      kernel_initializer=initializer, 
                      bias_initializer=initializer)(x)
    x = layers.MaxPooling2D(pool_size=(2, 2))(x)
    x = layers.Flatten()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(40,
                     activation="relu",
                     kernel_initializer=initializer, 
                     bias_initializer=initializer)(x)
    x = layers.Dense(10, 
                     activation="softmax",
                     kernel_initializer=initializer, 
                     bias_initializer=initializer)(x)
    model = keras.Model(inputs, outputs=x, name="functional_conv2d_simple")
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    return model

def sequantial_conv2d_simple():
    initializer = keras.initializers.RandomUniform(minval=-0.2, 
                                                   maxval=0.2, 
                                                   seed=42)
    
    model = keras.Sequential(name="sequential_conv2d_simple")
    model.add(keras.Input(shape=[20,20,3]))
    model.add(layers.Conv2D(32, 
                      kernel_size=(3, 3), 
                      activation="relu", 
                      kernel_initializer=initializer, 
                      bias_initializer=initializer))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(64, 
                      kernel_size=(3, 3), 
                      activation="relu", 
                      kernel_initializer=initializer, 
                      bias_initializer=initializer))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Flatten())
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(40,
                     activation="relu",
                     kernel_initializer=initializer, 
                     bias_initializer=initializer,
                     name="Dense_2"))
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(10,
                     activation="softmax",
                     kernel_initializer=initializer, 
                     bias_initializer=initializer,
                     name="Dense_3"))
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    return model

def functional_conv1d_simple_01():
    initializer = keras.initializers.RandomUniform(minval=-0.2, 
                                                   maxval=0.2, 
                                                   seed=42)
    inputs = keras.Input(shape=[40,1])
    x = layers.Conv1D(10, kernel_size=(3), 
                      activation="relu",
                      kernel_initializer=initializer, 
                      bias_initializer=initializer)(inputs)
    x = layers.BatchNormalization(epsilon=0.01)(x)
    x = layers.Flatten()(x)
    x = layers.Dense(16, 
                     activation="relu",
                     kernel_initializer=initializer, 
                     bias_initializer=initializer)(x)
    x = layers.Dense(10, 
                     activation="softmax",
                     kernel_initializer=initializer, 
                     bias_initializer=initializer)(x)
    model = keras.Model(inputs, outputs=x, name="functional_conv1d_forward_simple_01")
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    
    return model

def functional_conv1d_simple_02():
    initializer = keras.initializers.RandomUniform(minval=-0.2, 
                                                   maxval=0.2, 
                                                   seed=42)
    input1 = keras.Input(shape=[40,1])
    input2 = keras.Input(shape=[40,1])
    x1 = layers.Dense(40, 
                      activation="selu",
                      kernel_initializer=initializer, 
                      bias_initializer=initializer)(input1)
    x2 = layers.Dense(40, 
                      activation="sigmoid",
                      kernel_initializer=initializer, 
                      bias_initializer=initializer)(input2)
    x = keras.layers.Add()([x1, x2])
    x = layers.BatchNormalization(epsilon=0.01)(x)
    x = layers.Conv1D(10, kernel_size=(3), 
                      activation="sigmoid",
                      kernel_initializer=initializer, 
                      bias_initializer=initializer)(x)
    x = layers.Flatten()(x)
    x = layers.Dense(16, 
                     activation="sigmoid",
                     kernel_initializer=initializer, 
                     bias_initializer=initializer)(x)
    # x = layers.BatchNormalization()(x)
    x = layers.Dense(10, 
                     activation="softmax",
                     kernel_initializer=initializer, 
                     bias_initializer=initializer)(x)
    model = keras.Model([input1, input2], outputs=x, name="functional_conv1d_forward_simple_02")
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    
    # np.random.seed(42)
    # x_train = np.random.rand(160).reshape(4,40) * 2
    # y_train = np.array([[0,1,0,0,0,0,0,0,0,0],
    #                     [0,0,1,0,0,0,0,0,0,0],
    #                     [0,1,0,1,0,0,0,0,0,0], 
    #                     [0,1,0,0,0,0,0,0,0,0]], dtype=np.float32).reshape(4,10)
    # model.fit(x_train, y_train, batch_size=1, epochs=10, verbose=0)
    
    return model
