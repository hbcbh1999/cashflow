from __future__ import division
import numpy as np
from copy import copy
from scipy.optimize import newton
from cashflow import CashFlow


class Curve(object):
    def __init__(self, formula):
        self.__call = formula

    def __call__(self, *args, **kwargs):
        return self.__call(*args, **kwargs)

    @staticmethod
    def calibrate(cashflow, price):
        n = newton(func=lambda y: cashflow.price(
            Curve.SingleRateCurve(y))-price,
               x0=0.001, tol=1.48e-9, maxiter=80)
        return n

    @classmethod
    def SingleRateCurve(cls, y, n=2):
        def d(t):
            return 1/(1+y/n)**(n*t)
        return Curve(d)


if __name__ == '__main__':
    c = Curve.SingleRateCurve(0.007368)
    #print(c(1), c(2))
    #print(type(c) is Curve)
    cf = CashFlow.CouponBond(100,(4+3/4)/100,0,2,2)
    print(cf)
    p = Curve.calibrate(cf, 107.9531)
    print(p)
    cf1 = CashFlow.CouponBond(100, 0.04, 0, 1)
    cf2 = CashFlow.CouponBond(100, 0.12, 0, 1)
    y1 = Curve.calibrate(cf1, 96.265)
    y12 = Curve.calibrate(cf1, 99.962)
    y2 = Curve.calibrate(cf2, 103.885)
    y22 = Curve.calibrate(cf2, 107.653)

    print(cf.price(c))
    print(y1, y12, y2, y22)