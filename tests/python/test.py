import numpy as np
import pyriccaticpp as ric
import scipy.special as sp
import mpmath
import warnings
import pytest


def test_denseoutput():
    w = lambda x: np.sqrt(x)
    g = lambda x: np.zeros_like(x)
    info = ric.Init(w, g, 16, 32, 32, 32)
    xi = 1e0
    xf = 1e6
    eps = 1e-12
    epsh = 1e-13
    yi = complex(sp.airy(-xi)[0] + 1j * sp.airy(-xi)[2])
    dyi = complex(-sp.airy(-xi)[1] - 1j * sp.airy(-xi)[3])
    Neval = int(1e2)
    xeval = np.linspace(xi, xf, Neval)
    xs, ys, dys, ss, ps, stypes, yeval, dyeval = ric.evolve(
        info, xi, xf, yi, dyi, eps, epsh, init_stepsize=0.01, x_eval=xeval
    )
    ytrue = np.array([mpmath.airyai(-x) + 1j * mpmath.airybi(-x) for x in xeval])
    dytrue = np.array(
        [
            -mpmath.airyai(-x, derivative=1) - 1j * mpmath.airybi(-x, derivative=1)
            for x in xeval
        ]
    )
    yerr = np.abs((ytrue - yeval) / ytrue)
    dyerr = np.abs((dytrue - dyeval) / dytrue)
    print("Dense output", yeval, ytrue)
    print("Dense output derivative", dyeval, dytrue)
    maxerr = max(yerr)
    maxderr = max(dyerr)
    assert maxerr < 1e-6 and maxderr < 1e-6


def test_denseoutput_xbac():
    w = lambda x: np.sqrt(x)
    g = lambda x: np.zeros_like(x)
    info = ric.Init(w, g, 16, 32, 32, 32)
    xi = 1e0
    xf = 1e6
    eps = 1e-12
    epsh = 1e-13
    yi = complex(sp.airy(-xi)[0] + 1j * sp.airy(-xi)[2])
    dyi = complex(-sp.airy(-xi)[1] - 1j * sp.airy(-xi)[3])
    Neval = int(1e2)
    xeval = np.linspace(xf, xi, Neval)
    xs, ys, dys, ss, ps, stypes, yeval, dyeval = ric.evolve(
        info, xi, xf, yi, dyi, eps, epsh, init_stepsize=0.01, x_eval=xeval
    )
    ytrue = np.array([mpmath.airyai(-x) + 1j * mpmath.airybi(-x) for x in xeval])
    dytrue = np.array(
        [
            -mpmath.airyai(-x, derivative=1) - 1j * mpmath.airybi(-x, derivative=1)
            for x in xeval
        ]
    )
    yerr = np.abs((ytrue - yeval) / ytrue)
    dyerr = np.abs((dytrue - dyeval) / dytrue)
    maxerr = max(yerr)
    maxderr = max(dyerr)
    assert maxerr < 1e-6 and maxderr < 1e-6


def test_denseoutput_err():
    w = lambda x: np.sqrt(x)
    g = lambda x: np.zeros_like(x)
    info = ric.Init(w, g, 16, 32, 32, 32)
    xi = 1e0
    xf = 1e6
    eps = 1e-12
    epsh = 1e-13
    yi = complex(sp.airy(-xi)[0] + 1j * sp.airy(-xi)[2])
    dyi = complex(-sp.airy(-xi)[1] - 1j * sp.airy(-xi)[3])
    Neval = int(1e2)
    xeval = np.linspace(xi - 10.0, xi, Neval)
    # Turn on warnings
    warnings.simplefilter("always")
    with pytest.raises(Exception):
        xs, ys, dys, ss, ps, stypes, yeval, dyeval = ric.evolve(
            info, xi, xf, yi, dyi, eps, epsh, init_stepsize=0.01, x_eval=xeval
        )


def test_solve_airy():
    w = lambda x: np.sqrt(x)
    g = lambda x: np.zeros_like(x)
    info = ric.Init(w, g, 16, 32, 32, 32)
    xi = 1e0
    xf = 1e6
    eps = 1e-12
    epsh = 1e-13
    yi = complex(sp.airy(-xi)[0] + 1j * sp.airy(-xi)[2])
    dyi = complex(-sp.airy(-xi)[1] - 1j * sp.airy(-xi)[3])
    xs, ys, dys, ss, ps, stypes, yeval, dyeval = ric.evolve(
        info, xi, xf, yi, dyi, eps=eps, epsilon_h=epsh, init_stepsize=0.01
    )
    xs = np.array(xs)
    ys = np.array(ys)
    ytrue = np.array([mpmath.airyai(-x) + 1j * mpmath.airybi(-x) for x in xs])
    yerr = np.abs((ytrue - ys) / ytrue)
    maxerr = max(yerr)
    print(maxerr)
    assert maxerr < 1e-6


def test_solve_airy_backwards():
    w = lambda x: np.sqrt(x)
    g = lambda x: np.zeros_like(x)
    info = ric.Init(w, g, 16, 32, 32, 32)
    xi = 1e6
    xf = 1e0
    eps = 1e-12
    epsh = 1e-13
    yi = complex(sp.airy(-xi)[0] + 1j * sp.airy(-xi)[2])
    dyi = complex(-sp.airy(-xi)[1] - 1j * sp.airy(-xi)[3])
    xs, ys, dys, ss, ps, stypes, yeval, dyeval = ric.evolve(
        info,
        xi,
        xf,
        yi,
        dyi,
        eps=eps,
        epsilon_h=epsh,
        init_stepsize=-0.01,
        hard_stop=True,
    )
    xs = np.array(xs)
    ys = np.array(ys)
    ytrue = np.array([mpmath.airyai(-x) + 1j * mpmath.airybi(-x) for x in xs])
    yerr = np.abs((ytrue - ys) / ytrue)
    maxerr = max(yerr)
    print(maxerr, stypes)
    assert maxerr < 1e-6


def test_denseoutput_backwards_xfor():
    w = lambda x: np.sqrt(x)
    g = lambda x: np.zeros_like(x)
    info = ric.Init(w, g, 16, 32, 32, 32)
    xi = 1e6
    xf = 1e0
    eps = 1e-12
    epsh = 1e-13
    yi = complex(sp.airy(-xi)[0] + 1j * sp.airy(-xi)[2])
    dyi = complex(-sp.airy(-xi)[1] - 1j * sp.airy(-xi)[3])
    Neval = int(1e2)
    xeval = np.linspace(xi, xf, Neval)
    xs, ys, dys, ss, ps, stypes, yeval, dyeval = ric.evolve(
        info,
        xi,
        xf,
        yi,
        dyi,
        eps=eps,
        epsilon_h=epsh,
        x_eval=xeval,
        init_stepsize=-0.01,
        hard_stop=True,
    )
    ytrue = np.array([mpmath.airyai(-x) + 1j * mpmath.airybi(-x) for x in xeval])
    yerr = np.abs((ytrue - yeval) / ytrue)
    maxerr = max(yerr)
    print(maxerr)
    assert maxerr < 1e-6


def test_denseoutput_backwards_xback():
    w = lambda x: np.sqrt(x)
    g = lambda x: np.zeros_like(x)
    info = ric.Init(w, g, 16, 32, 32, 32)
    xi = 1e6
    xf = 1e0
    eps = 1e-12
    epsh = 1e-13
    yi = complex(sp.airy(-xi)[0] + 1j * sp.airy(-xi)[2])
    dyi = complex(-sp.airy(-xi)[1] - 1j * sp.airy(-xi)[3])
    Neval = int(1e2)
    xeval = np.flip(np.linspace(xf, xi, Neval))
    xs, ys, dys, ss, ps, stypes, yeval, dyeval = ric.evolve(
        info,
        xi,
        xf,
        yi,
        dyi,
        eps=eps,
        epsilon_h=epsh,
        init_stepsize=-0.01,
        x_eval=xeval,
        hard_stop=True,
    )
    ytrue = np.array([mpmath.airyai(-x) + 1j * mpmath.airybi(-x) for x in xeval])
    dytrue = np.array(
        [
            -mpmath.airyai(-x, derivative=1) - 1j * mpmath.airybi(-x, derivative=1)
            for x in xeval
        ]
    )
    yerr = np.abs((ytrue - yeval) / ytrue)
    dyerr = np.abs((dytrue - dyeval) / dytrue)
    maxerr = max(yerr)
    maxderr = max(dyerr)
    assert maxerr < 1e-6 and maxderr < 1e-6


def test_solve_burst():
    m = int(1e6)  # Frequency parameter
    w = lambda x: np.sqrt(m**2 - 1) / (1 + x**2)
    g = lambda x: np.zeros_like(x)
    bursty = (
        lambda x: np.sqrt(1 + x**2)
        / m
        * (np.cos(m * np.arctan(x)) + 1j * np.sin(m * np.arctan(x)))
    )
    burstdy = (
        lambda x: 1
        / np.sqrt(1 + x**2)
        / m
        * (
            (x + 1j * m) * np.cos(m * np.arctan(x))
            + (-m + 1j * x) * np.sin(m * np.arctan(x))
        )
    )
    xi = -m
    xf = m
    yi = bursty(xi)
    dyi = burstdy(xi)
    eps = 1e-10
    epsh = 1e-12
    info = ric.Init(w, g, 16, 32, 32, 32)
    xs, ys, dys, ss, ps, types, yeval, dyeval = ric.evolve(
        info, xi, xf, yi, dyi, eps=eps, epsilon_h=epsh
    )
    xs = np.array(xs)
    ys = np.array(ys)
    ytrue = bursty(xs)
    yerr = np.abs((ytrue - ys)) / np.abs(ytrue)
    maxerr = max(yerr)
    assert maxerr < 2e-7


def test_osc_evolve():
    w = lambda x: np.sqrt(x)
    g = lambda x: np.zeros_like(x)
    info = ric.Init(w, g, 16, 32, 32, 32)
    xi = 1e2
    xf = 1e6
    eps = 1e-12
    epsh = 1e-13
    yi = complex(sp.airy(-xi)[0] + 1j * sp.airy(-xi)[2])
    dyi = complex(-sp.airy(-xi)[1] - 1j * sp.airy(-xi)[3])
    # Store things
    xs, ys, dys = [], [], []
    # Always necessary for setting info.y
    # Always necessary for setting info.wn, info.gn, and for getting an initial stepsize
    hi = 2 * xi
    hi, _, _ = ric.choose_osc_stepsize(info, xi, hi, epsilon_h=epsh)
    # Not necessary here because info.x is already xi, but in general it might be:
    while xi < xf:
        status, x_next, h_next, osc_ret, yeval, dyeval, dense_start, dense_size = (
            ric.osc_evolve(
                info, xi, xf, yi, dyi, eps=eps, epsilon_h=epsh, init_stepsize=hi
            )
        )
        if status is False:
            break
        xs.append(x_next)
        ys.append(osc_ret[1])
        xi = x_next
        yi = osc_ret[1]
        dyi = osc_ret[2]
        hi = h_next
    xs = np.array(xs)
    ys = np.array(ys)
    ytrue = np.array([mpmath.airyai(-x) + 1j * mpmath.airybi(-x) for x in xs])
    yerr = np.abs((ytrue - ys) / ytrue)
    maxerr = max(yerr)
    print("Forward osc evolve max error:", maxerr)
    assert maxerr < 1e-4


def test_nonosc_evolve():
    w = lambda x: np.sqrt(x)
    g = lambda x: np.zeros_like(x)
    info = ric.Init(w, g, 16, 32, 32, 32)
    xi = 1e0
    xf = 4e1
    eps = 1e-12
    epsh = 2e-1  # Note different definition of epsh for Chebyshev steps!
    yi = complex(sp.airy(-xi)[0] + 1j * sp.airy(-xi)[2])
    dyi = complex(-sp.airy(-xi)[1] - 1j * sp.airy(-xi)[3])
    # Store things
    xs, ys, dys = [], [], []
    # Always necessary for setting info.y
    # Necessary for getting an initial stepsize
    hi = 1 / w(xi)
    hi = ric.choose_nonosc_stepsize(info, xi, hi, epsilon_h=epsh)
    # Not necessary here because info.x is already xi, but in general it might be:
    while xi < xf:
        status, x_next, h_next, nonosc_ret, yeval, dyeval, dense_start, dense_size = (
            ric.nonosc_evolve(
                info, xi, xf, yi, dyi, eps=eps, epsilon_h=epsh, init_stepsize=hi
            )
        )
        if status is False:
            break
        xs.append(x_next)
        ys.append(nonosc_ret[1])
        xi = x_next
        yi = nonosc_ret[1]
        dyi = nonosc_ret[2]
        hi = h_next
    xs = np.array(xs)
    ys = np.array(ys)
    ytrue = np.array([mpmath.airyai(-x) + 1j * mpmath.airybi(-x) for x in xs])
    yerr = np.abs((ytrue - ys) / ytrue)
    maxerr = max(yerr)
    print("Forward nonosc evolve max error:", maxerr)
    assert maxerr < 1e-4


def test_osc_evolve_backwards():
    w = lambda x: np.sqrt(x)
    g = lambda x: np.zeros_like(x)
    info = ric.Init(w, g, 16, 32, 32, 32)
    xi = 1e6
    xf = 1e2
    eps = 1e-12
    epsh = 1e-13
    yi = complex(sp.airy(-xi)[0] + 1j * sp.airy(-xi)[2])
    dyi = complex(-sp.airy(-xi)[1] - 1j * sp.airy(-xi)[3])
    # Store things
    xs, ys, dys = [], [], []
    # Always necessary for setting info.y
    # Always necessary for setting info.wn, info.gn, and for getting an initial stepsize
    hi = -xi / 10
    hi, _, _ = ric.choose_osc_stepsize(info, xi, hi, epsilon_h=epsh)
    # Not necessary here because info.x is already xi, but in general it might be:
    while xi > xf:
        status, x_next, h_next, osc_ret, yeval, dyeval, dense_start, dense_size = (
            ric.osc_evolve(
                info, xi, xf, yi, dyi, eps=eps, epsilon_h=epsh, init_stepsize=hi
            )
        )
        if status is False:
            break
        xs.append(x_next)
        ys.append(osc_ret[1])
        xi = x_next
        yi = osc_ret[1]
        dyi = osc_ret[2]
        hi = h_next
    xs = np.array(xs)
    ys = np.array(ys)
    ytrue = np.array([mpmath.airyai(-x) + 1j * mpmath.airybi(-x) for x in xs])
    yerr = np.abs((ytrue - ys) / ytrue)
    maxerr = max(yerr)
    print("Backwards osc evolve max error:", maxerr)
    assert maxerr < 1e-4


def test_nonosc_evolve_backwards():
    w = lambda x: np.sqrt(x)
    g = lambda x: np.zeros_like(x)
    info = ric.Init(w, g, 16, 32, 32, 32)
    xi = 4e1
    xf = 1e0
    eps = 1e-12
    epsh = 2e-1  # Note different definition of epsh for Chebyshev steps!
    yi = complex(sp.airy(-xi)[0] + 1j * sp.airy(-xi)[2])
    dyi = complex(-sp.airy(-xi)[1] - 1j * sp.airy(-xi)[3])
    # Store things
    xs, ys, dys = [], [], []
    # Necessary for getting an initial stepsize
    hi = -1 / w(xi)
    hi = ric.choose_nonosc_stepsize(info, xi, hi, epsilon_h=epsh)
    # Not necessary here because info.x is already xi, but in general it might be:
    while xi > xf:
        status, x_next, h_next, nonosc_ret, yeval, dyeval, dense_start, dense_size = (
            ric.nonosc_evolve(
                info, xi, xf, yi, dyi, eps=eps, epsilon_h=epsh, init_stepsize=hi
            )
        )
        if status != 1:
            break
        xs.append(x_next)
        ys.append(nonosc_ret[1])
        xi = x_next
        yi = nonosc_ret[1]
        dyi = nonosc_ret[2]
        hi = h_next

    xs = np.array(xs)
    ys = np.array(ys)
    ytrue = np.array([mpmath.airyai(-x) + 1j * mpmath.airybi(-x) for x in xs])
    yerr = np.abs((ytrue - ys) / ytrue)
    maxerr = max(yerr)
    print("Backward nonosc evolve max error:", maxerr)
    assert maxerr < 1e-10