import numpy as np


def dtw(sample_1: np.ndarray, sample_2: np.ndarray):

    dist = abs(sample_1 - sample_2)
    window = np.full((int(sample_1.shape[0] * sample_2.shape[0]), 2), np.nan)

    cnt = 0
    for i in range(sample_1.shape[0]):
        for j in range(sample_2.shape[0]):
            window[cnt] = [sample_1[i], sample_2[j]]
            cnt += 1

    # for i, j in window:
    #     dt = abs(sample_1[i-1] - sample_2[j)-1])
    # #window = [(i, j) for i in range(len(sample_1)) for j in range(len(sample_2))]
    # #print(window)
    #print(sample_1.shape[0])


sample_1 = np.array([1, 2, 3, 4, 5, 6])
sample_2 = np.array([2, 1, 5, 10, 5, 6])

dtw(sample_1=sample_1, sample_2=sample_2)