import numpy as np
import scipy.stats as stats
import scipy.special
import pandas as pd

def friedman_test(data):
    N, k = data.shape
    mr = np.mean(stats.rankdata(data, axis=0), axis=0)
    
    friedman_stat = 12 * N / (k * (k + 1)) * (np.sum(mr**2) - (k * (k + 1)**2) / 4)
    p_value = 1 - stats.chi2.cdf(friedman_stat, df=(k - 1))
    
    htest_result = {
        "statistic": friedman_stat,
        "parameter": (k - 1),
        "p_value": p_value,
        "method": "Friedman's rank sum test",
        "data_name": "data"
    }
    return htest_result

def friedman_post(data, control=None):
    k, N = data.shape
    control = process_control_column(data, control)
    pairs = generate_pairs(k, control)
    mean_rank = np.mean(stats.rankdata(data, axis=0), axis=0)
    sd = np.sqrt((k * (k + 1)) / (6 * N))

    def compute_pvalue(pair):
        stat = abs(mean_rank[pair[0]] - mean_rank[pair[1]]) / sd
        return 2 * (1 - stats.norm.cdf(stat))

    pvalues = np.apply_along_axis(compute_pvalue, 1, pairs)
    matrix_raw = build_pval_matrix(pvalues, k, pairs, data.columns, control)
    return matrix_raw

def build_pval_matrix(pvalues, k, pairs, cnames, control):
    if control is None:
        matrix_raw = np.full((k, k), np.nan)
        for pval, pair in zip(pvalues, pairs):
            matrix_raw[pair[0], pair[1]] = pval
            matrix_raw[pair[1], pair[0]] = pval
        return pd.DataFrame(matrix_raw, columns=cnames, index=cnames)
    else:
        matrix_raw = np.full(k, np.nan)
        for pval, pair in zip(pvalues, pairs):
            matrix_raw[pair[1]] = pval
        return pd.DataFrame([matrix_raw], columns=cnames)

def process_control_column(data, control):
    if control is not None:
        if isinstance(control, str):
            control = np.where(data.columns == control)[0]
            if len(control) == 0:
                raise ValueError("The name of the column to be used as control does not exist in the data matrix")
        else:
            if control > data.shape[1] or control < 1:
                raise ValueError(f"Non-valid value for the control parameter. It has to be either the name of a column or a number between 1 and {data.shape[1]}")
    return control

def generate_pairs(k, control):
    if control is None:
        pairs = [(i, j) for i in range(k) for j in range(i+1, k)]
    else:
        pairs = [(control, i) for i in range(k) if i != control]
    return np.array(pairs)

def adjust_shaffer(raw_matrix):
    if not (isinstance(raw_matrix, np.ndarray) or isinstance(raw_matrix, pd.DataFrame)):
        raise ValueError("This correction method requires a square matrix or data.frame with the p-values of all pairwise comparisons.")
    
    if raw_matrix.shape[0] != raw_matrix.shape[1]:
        raise ValueError("This correction method requires a square matrix or data.frame with the p-values of all pairwise comparisons.")
    
    k = raw_matrix.shape[0]
    pairs = generate_pairs(k, None)
    raw_pvalues = raw_matrix.values[pairs[:,0], pairs[:,1]]
    
    sk = count_recursively(k)[1:]
    t_i = np.concatenate([np.repeat(sk[:-1], np.diff(sk)), [sk[-1]]])
    t_i = t_i[::-1]
    
    o = np.argsort(raw_pvalues)
    adj_pvalues = raw_pvalues[o] * t_i
    adj_pvalues = np.minimum(adj_pvalues, 1)
    adj_pvalues = correct_for_monotonicity(adj_pvalues)
    
    adj_pvalues = adj_pvalues[np.argsort(o)]
    adj_matrix = raw_matrix.copy()
    for (pair, pval) in zip(pairs, adj_pvalues):
        adj_matrix.iat[pair[0], pair[1]] = pval
        adj_matrix.iat[pair[1], pair[0]] = pval

    return adj_matrix

def generate_pairs(k, control):
    if control is None:
        pairs = [(i, j) for i in range(k) for j in range(i+1, k)]
    else:
        pairs = [(control, i) for i in range(k) if i != control]
    return np.array(pairs)

def count_recursively(k):
    res = [0]
    if k > 1:
        res += count_recursively(k - 1)
        for j in range(2, k + 1):
            res += count_recursively(k - j) + [scipy.special.comb(j, 2)]
    return sorted(set(res))

def correct_for_monotonicity(pvalues):
    return np.maximum.accumulate(pvalues)

# Example usage
# raw_matrix = np.random.rand(5, 5)  # Replace with actual p-value matrix
# adjusted_matrix = adjust_shaffer(raw_matrix)

