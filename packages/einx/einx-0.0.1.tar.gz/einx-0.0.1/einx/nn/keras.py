import keras_core as keras

class Norm(keras.layers.Layer):
    def __init__(self, stats, params="b... [c]", mean=True, var=True, scale=True, bias=True, decay_rate=None, name=None, **kwargs):
        super().__init__(name=name)
        self.stats = stats
        self.params = params
        self.kwargs = kwargs

        if decay_rate is None:
            self.mean = mean
            self.var = var
        else:
            self.mean = hk.ExponentialMovingAverage(decay_rate, name="mean") if not mean is None else None
            self.var = hk.ExponentialMovingAverage(decay_rate, name="var") if not var is None else None
        self.scale = scale
        self.bias = bias
        self.decay_rate = decay_rate



    def __init__(self, units, activation=None, name=None):
        super().__init__(name=name)
        self.units = units
        self.activation = keras.activations.get(activation)

    def build(self, input_shape):
        input_dim = input_shape[-1]
        self.w = self.add_weight(
            shape=(input_dim, self.units),
            initializer=keras.initializers.GlorotNormal(),
            name="kernel",
            trainable=True,
        )

        self.b = self.add_weight(
            shape=(self.units,),
            initializer=keras.initializers.Zeros(),
            name="bias",
            trainable=True,
        )

    def call(self, inputs):
        # Use Keras ops to create backend-agnostic layers/metrics/etc.
        x = keras.ops.matmul(inputs, self.w) + self.b
        return self.activation(x)
