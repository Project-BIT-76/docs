import os
from functools import reduce

import numpy as np


def pred_accuracy(prediction, test_y_cl):
    acc = []
    # check_lbls = []#[val_y]
    # for x in val_y_cl:
    #     check_lbls.append(x)

    for i in range(0, len(prediction)):
        acc.append(classification_accuracy(prediction[i], test_y_cl[i]))  #
    lst_len = len(acc)

    accuracy = reduce(lambda x, y: x + y, acc) / lst_len

    return accuracy

def classification_accuracy(classification_scores, true_labels):
    return np.mean(np.argmax(classification_scores, axis=1) == true_labels)

def prepare_inputs_and_outputs(data, data_temperature, data_ppeak_hours, data_holiday, data_classes, n_input, n_out,
                               n_delay):
    inputs, inputs_temperature, inputs_ppeak_hours, inputs_holiday, outputs, output_classes = [], [], [], [], [], []
    for in_start in range(0, len(data), 24):
        in_end = in_start + n_input
        out_start = in_end + n_delay
        out_end = out_start + n_out
        out_classes_start = int(out_start / 24)
        out_classes_end = int(out_end / 24)
        if out_end > len(data) or out_classes_end > len(data_classes) or out_classes_end > len(data_holiday):
            break

        inputs.append(data[in_start:in_end])
        inputs_temperature.append(data_temperature[in_start:out_start])
        inputs_ppeak_hours.append(data_ppeak_hours[out_start:out_end])
        inputs_holiday.append(data_holiday[out_classes_start:out_classes_end])
        outputs.append(data[out_start:out_end, 0])
        output_classes.append(data_classes[out_classes_start:out_classes_end])

    return np.array(inputs), np.array(inputs_temperature), np.array(inputs_ppeak_hours), np.array(
        inputs_holiday), np.array(outputs), np.array(output_classes)

def find_best_model(save_dir):
    best_model = None
    best_accuracy = float('-inf')

    for filename in os.listdir(save_dir):
        if filename.startswith("model_epoch_") and filename.endswith(".keras"):
            accuracy = float(filename.split('_accuracy_')[1].replace('.keras', ''))
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_model = filename

    return os.path.join(save_dir, best_model) if best_model else None
