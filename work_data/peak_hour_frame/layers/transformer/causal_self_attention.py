from .base_attention import BaseAttention

class CausalSelfAttention(BaseAttention):

    def build(self, input_shape):
        # This will trigger the internal build of `MultiHeadAttention`
        self.mha.build(input_shape, input_shape)

    def call(self, x):
        attn_output = self.mha(
            query=x,
            value=x,
            key=x,
            use_causal_mask=True)
        x = self.add([x, attn_output])
        x = self.layernorm(x)
        return x