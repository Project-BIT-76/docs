import tensorflow as tf

class BaseAttention(tf.keras.layers.Layer):

    def build(self, input_shape):
        # Provide query_shape and value_shape separately
        self.mha.build(input_shape, input_shape)  # Assuming query_shape = value_shape for self-attention
        super().build(input_shape)

    def __init__(self, **kwargs):
        super().__init__()
        self.mha = tf.keras.layers.MultiHeadAttention(**kwargs)
        self.layernorm = tf.keras.layers.LayerNormalization()
        self.add = tf.keras.layers.Add()