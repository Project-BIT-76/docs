import os
from tensorflow.keras.callbacks import Callback

class SaveModelWithAccuracy(Callback):
    def __init__(self, save_dir, monitor='val_accuracy', mode='max'):
        super().__init__()
        self.save_dir = save_dir
        self.monitor = monitor
        self.mode = mode
        self.best_accuracy = float('-inf')

    def on_epoch_end(self, epoch, logs=None):
        current_accuracy = logs.get(self.monitor)
        if current_accuracy is None:
            return

        if (self.mode == 'max' and current_accuracy > self.best_accuracy) or \
           (self.mode == 'min' and current_accuracy < self.best_accuracy):
            # Remove previously saved models with lower accuracy
            for filename in os.listdir(self.save_dir):
                if filename.startswith("model_epoch_") and filename.endswith(".keras"):
                    filepath = os.path.join(self.save_dir, filename)
                    os.remove(filepath)

            self.best_accuracy = current_accuracy
            model_filename = f"model_epoch_{epoch:02d}_accuracy_{current_accuracy:.4f}.keras"
            model_path = os.path.join(self.save_dir, model_filename)
            self.model.save(model_path)
            print(f"Saved model at epoch {epoch} with accuracy {current_accuracy:.4f} to {model_path}")