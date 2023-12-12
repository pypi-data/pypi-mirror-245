import numpy as np
from scipy import stats
from typing import NamedTuple
from glidergun.core import focal, Grid


class DescribeResult(NamedTuple):
    nobs: Grid
    min: Grid
    max: Grid
    mean: Grid
    variance: Grid
    skewness: Grid
    kurtosis: Grid


def _describe(data):
    try:
        result = stats.describe(data[0].ravel())
        return (
            result[0],
            result[1][0],
            result[1][1],
            result[2],
            result[3],
            result[4],
            result[5],
        )
    except Exception:
        return (np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan)


def focal_describe(grid: Grid, buffer: int = 1) -> DescribeResult:
    result = focal(_describe, buffer, 2, grid)
    return DescribeResult(*result)


def _pearson(data):
    try:
        return np.corrcoef(data[0].ravel(), data[1].ravel())[0, 1]
    except Exception:
        return np.nan


def focal_pearson(grid1: Grid, grid2: Grid, buffer: int = 1) -> Grid:
    return focal(_pearson, buffer, 1, grid1, grid2)[0]


class TtestResult(NamedTuple):
    statistic: Grid
    pvalue: Grid


def _ttest(data):
    try:
        result = stats.ttest_ind(data[0].ravel(), data[1].ravel())
        return (result[0], result[1])
    except Exception:
        return (np.nan, np.nan)


def focal_ttest(grid1: Grid, grid2: Grid, buffer: int = 1) -> TtestResult:
    result = focal(_ttest, buffer, 1, grid1, grid2)
    return TtestResult(*result)
