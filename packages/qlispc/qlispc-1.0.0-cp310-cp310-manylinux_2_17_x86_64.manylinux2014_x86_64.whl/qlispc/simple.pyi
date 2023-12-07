from typing import Callable

import numpy as np


def regesterGateMatrix(gate: str,
                       mat: Callable | np.ndarray,
                       N: int | None = ...,
                       docs: str = ...):
    ...


def applySeq(seq: list[tuple], psi0=None) -> np.ndarray:
    ...


def seq2mat(seq: list[tuple], U=None) -> np.ndarray:
    ...
