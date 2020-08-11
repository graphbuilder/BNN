import numpy as np
from numpy.lib.stride_tricks import as_strided
import os
import argparse
from PIL import Image

def conv_np(input_fm, conv_filter, cond=(0, 0, 0)):
    input_fm = input_fm.squeeze()  
    # fm = np.pad(input_fm, ((0, 0), (1, 1), (1, 1)), 'constant', constant_values=(1, 1))
    fm = input_fm  # first input, (3, 30, 30)
    flt_size = conv_filter.shape[0]  # = 4, (4, 3, 3, 3)
    channel_size = conv_filter.shape[1]  # = 3, 
    kernal_size = conv_filter.shape[-1]  # =3,
    fm_size = fm.shape[-1]  # = 30, input_fm size

    def next_tile():
        new_shape = (fm_size - 2, fm_size - 2, channel_size, kernal_size, kernal_size)  # (28, 28, 3, 3, 3)

        strides = fm.itemsize * np.array([fm_size, 1, fm_size ** 2, fm_size, 1])  # (120,4,3600,120,4) = 4 * (30, 1, 30 ** 2, 30, 1)
        patches = as_strided(fm, shape=new_shape, strides=strides)  #new matrix, fm is old matrix, 

        for y in range(fm_size - 2):
            for x in range(fm_size - 2):
                yield patches[y, x, :, :, :], y, x,

    def fit_condition(cond, i, y, x):
        if cond is None:
            return False
        else:
            c_in, y_in, x_in = cond
            if c_in == i and y_in == y and x_in == x:
                return True
        return False

    def outside_of_calculation(cond, i, y, x):
        if cond is None:
            return False
        else:
            c_in, y_in, x_in = cond
            if c_in < i and y_in < y and x_in < x:
                return True
        return False

    output_fm = np.zeros((flt_size, fm_size - 2, fm_size - 2), dtype=np.int)  # (4, 28, 28)
    for tile, y, x in next_tile():
        for i in range(flt_size):
            flt = conv_filter[i, :, :, :]
            if fit_condition(cond, i, y, x):
                result_conv, result_log = sum_point_wise_one_by_one(tile, flt)
                output_fm[i, y, x] += result_conv
                print(result_log)
            else:
                continue

    return output_fm[np.newaxis, :]


def sum_point_wise_one_by_one(tile, flt):
    print(f"tile shape : {tile.shape}, flt shape : {flt.shape}")
    if tile.shape != flt.shape:
        raise ValueError(f"tile shape : {tile.shape} not fit with filter shape : {flt.shape}")

    cnt = 0

    def get_point_weight_one():
        for x in range(tile.size):
            yield tile.flat[x], flt.flat[x]

    result = 0
    result_log = ''
    for p1, w1 in get_point_weight_one():
        result_before = result
        result += p1 * w1
        cnt += 1
        result_log += 'MAC%02d : %s = %s + %s * %s\n' % (cnt, result, result_before, w1, p1)

    return result, result_log


if __name__ == '__main__':
    input_fm = np.load("fm/input.fm.npy") 
    weights = np.load("param/features0.0.weight.npy")

    print('input_fm.shape: ', input_fm.shape, '\n',
            'weights.shape: ', weights.shape, '\n')
    print("input_fm:", '\n', input_fm[0, :, :3, :3], '\n'*2, 
            "weights:", '\n', weights[0, :, :, :], '\n')

    conv_np(input_fm, weights, cond=(0, 0, 0))

