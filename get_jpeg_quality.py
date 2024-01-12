#!/usr/bin/env python

"""Forensic analysis of the JPEG image compression quality"""
"JPEG compression quality analysis for image forensics"
import argparse
import numpy as np
import imageio as iio
import scipy as sp
import scipy.fftpack
from skimage.util import view_as_blocks

D = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
        ])

def get_jpeg_quality(img: np.ndarray):
    lum = np.round((img * np.array([.299, .587, .113])[None, None]).sum(axis=-1))
    Y, X = lum.shape
    Y -= Y%8
    X -= X%8
    blocks = view_as_blocks(lum[:Y, :X], (8, 8)).reshape(-1, 8, 8)
    coeffs = sp.fftpack.dctn(blocks, axes=(1, 2), norm='ortho')
    coeffs = coeffs.reshape(Y//8 * X//8, 64)
    quant_table = []
    quant_table_main_peak_range = []
    quant_table_other_possible_values = []
    epsilon = -10
    nfas = []
    possible_qs = np.arange(1, 256)
    for i_c in range(64):
        #print(i_c, end='\r')
        c = coeffs[:, i_c]
        div_quant = c[:, None] / possible_qs[None]
        rounded = np.round(div_quant)
        mask = np.abs(rounded)>1e-100
        error = 2 * np.abs(div_quant - rounded)
        error[~mask] = 0
        s = error.sum(axis=0)
        n = np.count_nonzero(mask, axis=0)
        iw_ln_pvalue = n*np.log(s.clip(1e-100, np.inf)) - 0.5*np.log(2*np.pi) - (n+0.5)*np.log(n.clip(1, np.inf)) + n * np.log(np.exp(1))
        hoeffding = -2*np.square(0.5 * n - s)/n.clip(1, np.inf)
        nfa = np.minimum(iw_ln_pvalue, hoeffding)
        nfa[0.5 * n - s<=0] = 0
        nfa += np.log10(63*64*255)
        q = np.argmin(nfa)
        quant_table.append(q+1)
        nfas.append(nfa[q])
        if nfa[q] >= epsilon:
            quant_table_main_peak_range.append([-1, -1])
            quant_table_other_possible_values.append([])
            continue
        qq = q
        while qq >= 1:
            qq -= 1
            if nfa[qq] >= epsilon:
                qq += 1
                break
        q_min = qq + 1
        qq = q
        while qq < 256:
            qq += 1
            if nfa[qq] >= epsilon:
                qq -= 1
                break
        q_max = qq + 1
        quant_table_main_peak_range.append((q_min, q_max))
        #excl = np.array(range(q_min, q_max))
        #for q in range(q_min, q_max+1):
        #    excl = np.union1d(excl, dividers[q])
        #excl = np.sort(excl)
        #quant_table_other_possible_values.append([q+1 for q in np.argwhere(nfa<0) if q+1 not in excl])
    quant_table = np.array(quant_table)
    quant_table_main_peak_range = np.array(quant_table_main_peak_range)
    nfas = np.array(nfas)
    return quant_table, quant_table_main_peak_range, nfas

def get_compression_quality(quant_table, nfas):
    Q = quant_table.reshape(8, 8)
    nfa = nfas.reshape(8, 8)
    epsilon = 0
    nfa[0, 0] = epsilon + 1  # for now avoid the DC coef
    kl = (100*(Q+0.5)) / D
    ku = (100*(Q-1.5)) / D
    min_Q = 100 - kl/2
    min_Q[kl>100] = 5000 / kl[kl>100]
    max_Q = 100 - ku/2
    max_Q[ku>100] = 5000 / ku[ku>100]
    if not np.any(nfa<0):
        return None, None
    return int(np.floor(min_Q[nfa<0].max())), int(np.ceil(max_Q[nfa<0].min()))

def get_extended_compression_quality(quant_range):
    Q = quant_range[1:] # avoid the DC coef for now
    Q_low = Q[:, 0]
    Q_high = Q[:, 1]
    kl = (100*(Q_high+0.5)) / D.ravel()[1:]
    ku = (100*(Q_low-1.5)) / D.ravel()[1:]
    min_Q = 100 - kl/2
    min_Q[kl>100] = 5000 / kl[kl>100]
    max_Q = 100 - ku/2
    max_Q[ku>100] = 5000 / ku[ku>100]
    min_Q[Q_low==-1] = 0
    max_Q[Q_high==-1] = 100
    return int(np.floor(min_Q.max())), int(np.ceil(max_Q.min()))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()
    path = args.input
    img = iio.imread(path)
    quant_table, quant_table_main_peak_range, nfas = get_jpeg_quality(img)
    min_qf, max_qf = get_compression_quality(quant_table, nfas)
    min_qf_extended, max_qf_extended = get_extended_compression_quality(quant_table_main_peak_range)
    if min_qf is None:
        print("No JPEG compression significantly detected")
    else:
        print(f"JPEG compression was detected at a quality factor between {min_qf} (lower bound) and {max_qf} (higher bound)")
        print(f"An extended confident range for the JPEG compression is between {min_qf_extended} (lower bound) and {max_qf_extended} (higher bound)")
        if max_qf < min_qf:
            print("The minimal quality is higher that the maximal quality. This suggests either the compression was done using a non-standard quantization table, or that the image was compressed multiple times")


