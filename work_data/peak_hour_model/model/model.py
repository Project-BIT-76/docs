import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Conv1D, AveragePooling1D, Concatenate, TimeDistributed, Reshape, GlobalAveragePooling1D
from tensorflow.keras.models import Model

class PredictionModel:
    def __init__(self, data_timesteps, data_features, holiday_timesteps, holiday_features):
        self.data_timesteps = data_timesteps
        self.data_features = data_features
        self.holiday_timesteps = holiday_timesteps
        self.holiday_features = holiday_features
        self.model = self._build_model()

    def _build_model(self):
        # Input layers
        input_data = Input(shape=(self.data_timesteps, self.data_features), name='input_data')
        input_holidays = Input(shape=(self.holiday_timesteps, self.holiday_features), name='input_holidays')

        # Downsample input data immediately to reduce computation
        norm_layer = AveragePooling1D(pool_size=4)(input_data)
        norm_layer = tf.keras.layers.BatchNormalization()(norm_layer)

        # Simplified holiday processing
        layer_holiday = tf.keras.layers.BatchNormalization()(input_holidays)

        # Simplified Data Processing Branch - reduced units and layers
        encoder_layer = TimeDistributed(Dense(units=16))(norm_layer)
        encoder_layer = GlobalAveragePooling1D()(encoder_layer)

        # Simplified CNN Branch - single conv layer with fewer filters
        encoder_cnn_layer = Conv1D(filters=16, kernel_size=3, activation="relu", padding='same')(norm_layer)
        encoder_cnn_layer = GlobalAveragePooling1D()(encoder_cnn_layer)

        # Simplified Holiday Processing
        layer_holiday = TimeDistributed(Dense(units=16))(layer_holiday)
        layer_holiday = GlobalAveragePooling1D()(layer_holiday)

        # Combine Features
        layer_combined = Concatenate()([
            encoder_layer,
            encoder_cnn_layer,
            layer_holiday
        ])

        # Simplified Dense layers
        layer = Dense(32, activation='relu')(layer_combined)

        # Reshape to match the required output timesteps
        layer = Dense(self.holiday_timesteps * 25)(layer)
        layer = Reshape((self.holiday_timesteps, 25))(layer)

        # Output Layer
        out_class = Dense(25, activation='softmax', name='output')(layer)

        # Define Model
        model = Model(inputs=[input_data, input_holidays], outputs=out_class)
        return model

    def compile(self, optimizer=None, loss='categorical_crossentropy', metrics=['accuracy']):
        """Compile the model with the specified optimizer, loss, and metrics."""
        if optimizer is None:
            # Use a simpler optimizer with an increased learning rate
            optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)

        self.model.compile(
            optimizer=optimizer,
            loss=loss,
            metrics=metrics,
            # Enable mixed precision for faster computation
            jit_compile=True
        )

    def summary(self):
        """Print the model summary."""
        return self.model.summary()

    def fit(self, x_train, y_train, **kwargs):
        """Train the model using the given data."""
        # Optimize training parameters for speed
        default_kwargs = {
            'batch_size': 64,      # Increased batch size
            'epochs': 5,           # Reduced epochs
            'verbose': 1,
            'validation_split': 0.1, # Reduced validation split
            'shuffle': True
        }
        default_kwargs.update(kwargs)

        return self.model.fit(x_train, y_train, **default_kwargs)

    def predict(self, x, **kwargs):
        """Make predictions using the model."""
        default_kwargs = {
            'batch_size': 64  # Increased batch size for prediction
        }
        default_kwargs.update(kwargs)
        return self.model.predict(x, **default_kwargs)