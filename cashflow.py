from __future__ import division
import numpy as np
from copy import copy


class CashFlow(object):
    def __init__(self, cashflow):
        if type(cashflow) is dict:
            self._cashflow = cashflow
        elif type(cashflow[0]) is tuple:
            self._cashflow = {t: Ct for t, Ct in cashflow}

    def __repr__(self):
        t, C = self.profile
        return '{}\n{}'.format(str(t), str(C))

    def __getitem__(self, t):
        if t not in self._cashflow:
            return 0
        else:
            return self._cashflow[t]

    def __mul__(self, scalar):
        __cashflow_copy = copy(self._cashflow)
        for t in __cashflow_copy:
            __cashflow_copy[t] *= scalar
        return CashFlow(__cashflow_copy)

    def __add__(self, cashflow):
        __cashflow_copy = copy(self._cashflow)
        for t in cashflow.cashflow_tuples:
            if t not in __cashflow_copy:
                __cashflow_copy[t] = cashflow[t]
            else:
                __cashflow_copy[t] += cashflow[t]
        return CashFlow(__cashflow_copy)

    @property
    def cashflow_tuples(self):
        return self._cashflow

    @property
    def profile(self):
        profile = [(t, Ct) for t, Ct in self._cashflow.items()]
        profile = sorted(profile, key=lambda a: a[0])
        t = map(lambda a: a[0], profile)
        C = map(lambda a: a[1], profile)
        return t, C

    @classmethod
    def CouponBond(cls, par, c, t0, T, n=2):
        cashflow, t, C = dict(), t0 + 1 / n, c * par / n
        while t <= T:
            cashflow[t] = C
            t += 1 / n
        if T in cashflow:
            cashflow[T] += par
        else:
            cashflow[T] = par
        return cls(cashflow)

    @classmethod
    def Annuity(cls, A, t0, T, n=2):
        cashflow, t = dict(), t0 + 1 / n
        while t <= T:
            cashflow[t] = A / n
            t += 1 / n
        return cls(cashflow)

    @staticmethod
    def replicate(target, securities):
        t, C = target.profile
        C = np.array(C).reshape(len(C), 1)
        cashflow_space = np.array([
            [security[tau] for tau in t]
            for security in securities
        ]).T
        w = np.linalg.solve(cashflow_space, C)
        return w, cashflow_space

    def price(self, disc):
        price = 0
        if type(disc) is dict:
            for t, Ct in self._cashflow.items():
                assert (t in disc)
                price += Ct * disc[t]
        elif hasattr(disc, '__call__'):
            for t, Ct in self._cashflow.items():
                price += Ct * disc(t)
        return price
