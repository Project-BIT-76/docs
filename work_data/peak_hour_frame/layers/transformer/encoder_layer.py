import tensorflow as tf
from .global_self_attention import GlobalSelfAttention
from .feed_forward import FeedForward

class EncoderLayer(tf.keras.layers.Layer):

    def build(self, input_shape):
        # Build each sublayer
        self.self_attention.build(input_shape)
        self.ffn.build(input_shape)
        super().build(input_shape)

    def __init__(self, *, d_model, num_heads, dff, dropout_rate=0.1, **kwargs):
        super().__init__(**kwargs)

        self.self_attention = GlobalSelfAttention(
            num_heads=num_heads,
            key_dim=d_model,
            dropout=dropout_rate)

        self.ffn = FeedForward(d_model, dff)

    def call(self, x):
        x = self.self_attention(x)
        x = self.ffn(x)
        return x