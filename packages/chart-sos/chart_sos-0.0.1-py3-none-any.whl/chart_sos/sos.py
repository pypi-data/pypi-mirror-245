"""Determine speed of sound by pressure, temperature, and gas specific gravity."""
# pylint: disable=disallowed-name
# pylint: disable=invalid-name
import math
import typing as typ
from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pkg_resources
from scipy.interpolate import Akima1DInterpolator
from scipy.interpolate import barycentric_interpolate
from scipy.interpolate import BarycentricInterpolator
from scipy.interpolate import CubicSpline
from scipy.interpolate import interp1d
from scipy.interpolate import KroghInterpolator
from scipy.interpolate import pchip_interpolate

fahrenheit_dict = {
    0.6: [19, 37, 55, 73, 108, 144, 215, 250, 321, 390],
    0.8: [40, 60, 81, 102, 123, 144, 165, 206, 248, 331, 373, 456],
    1.0: [66, 90, 113, 137, 161, 185, 209, 233, 257, 305, 352, 448],
    1.2: [134, 161, 188, 242, 269, 296, 323, 350, 404],
}

gas_sg_list: typ.List[float] = [0.6, 0.8, 1.0, 1.2]

# Eager load the dataframe in to memory all at once.
# Example: fahrenheit_pressure_df_dict[0.6][19]
fahrenheit_pressure_df_dict = {}
for _gas_sg_, _value_ in fahrenheit_dict.items():
    tmp_dict = {}
    for _temp_fahrenheit_ in _value_:
        try:
            csv_file = pkg_resources.resource_filename(
                "chart_sos", f"gas_sg_{_gas_sg_}_{_temp_fahrenheit_}F.csv"
            )
        except ModuleNotFoundError:
            csv_file = f"gas_sg_{_gas_sg_}_{_temp_fahrenheit_}F.csv"
        _dataframe_ = pd.read_csv(csv_file, header=None)
        _dataframe_.columns = ["psi", "ft/s"]
        _dataframe_ = _dataframe_.sort_values(by=["psi"])
        tmp_dict[_temp_fahrenheit_] = _dataframe_
    fahrenheit_pressure_df_dict[_gas_sg_] = tmp_dict


class OutChartException(Exception):
    """An exception class."""


@dataclass
class GasSGDataframe:
    """Dataclass."""

    gas_sg: float
    temp_f: float
    dataframe: pd.DataFrame
    interp_func: typ.Callable[[float], float]


def get_sos(
    pressure_psi: float, temperature_fahrenheit: float, gas_sg: float
) -> float:
    """Get speed of sound ft/sec by pressure, temperature, and gas_sg. By direct lookup."""
    if gas_sg not in gas_sg_list:
        raise OutChartException("gas_sg accepts only [0.6, 0.8, 1.0, 1.2]")
    if pressure_psi < 0 or pressure_psi > 3000:
        raise OutChartException("pressure accepts in range [0, 3000] psi")
    if temperature_fahrenheit not in fahrenheit_dict[gas_sg]:
        raise OutChartException(
            f"gas_sg {gas_sg} has fahrenheit temperature in range {fahrenheit_dict[gas_sg]}"
        )
    dataframe = pd.read_csv(
        f"gas_sg_{gas_sg}_{temperature_fahrenheit}F.csv", header=None
    )
    dataframe.columns = ["psi", "ft/s"]
    return float(
        dataframe.iloc[(dataframe["psi"] - pressure_psi).abs().argsort()[:1]][
            "ft/s"
        ]
    )


def return_interpolated_result(
    x: typ.List[float], y: typ.List[float], kind: typ.Union[str, int]
) -> Iterable:
    """Return wrapper."""
    # Define new x-values for interpolation
    f = interp1d(x, y, kind=kind)
    return f(x)


def show_error_interpolation_function(
    gas_sg: float, temp_fahrenheit: float
) -> None:
    """Return interpolation function of given dataframe."""
    dataframe = pd.read_csv(
        f"gas_sg_{gas_sg}_{temp_fahrenheit}F.csv", header=None
    )
    dataframe.columns = ["psi", "ft/s"]
    dataframe = dataframe.sort_values(by=["psi"])
    x: typ.List[float] = dataframe["psi"].tolist()
    y: typ.List[float] = dataframe["ft/s"].tolist()

    # Interpolate the data
    new_y_linear = return_interpolated_result(x, y, kind="linear")
    new_y_nearest = return_interpolated_result(x, y, kind="nearest")
    new_y_nearest_up = return_interpolated_result(x, y, kind="nearest-up")
    new_y_zero = return_interpolated_result(x, y, kind="zero")
    new_y_slinear = return_interpolated_result(x, y, kind="slinear")
    new_y_quadratic = return_interpolated_result(x, y, kind="quadratic")
    new_y_cubic = return_interpolated_result(x, y, kind="cubic")
    new_y_previous = return_interpolated_result(x, y, kind="previous")
    new_y_next = return_interpolated_result(x, y, kind="next")
    new_y_3 = return_interpolated_result(x, y, kind=3)
    new_y_5 = return_interpolated_result(x, y, kind=5)
    new_y_7 = return_interpolated_result(x, y, kind=7)
    new_y_9 = return_interpolated_result(x, y, kind=9)

    f_BarycentricInterpolator = BarycentricInterpolator(x, y, axis=0)
    new_y_BarycentricInterpolator = f_BarycentricInterpolator(x)

    f_krogh = KroghInterpolator(x, y)
    new_y_krogh = f_krogh(x)  # Runtime overflow

    f_barycentric_interpolate = barycentric_interpolate(x, y, x)
    new_y_pchip = pchip_interpolate(x, y, x)
    f_akima = Akima1DInterpolator(x, y)
    new_y_akima = f_akima(x)

    f_cubic_spline = CubicSpline(x, y)
    new_y_cubic_spline = f_cubic_spline(x)

    df = pd.DataFrame.from_dict(
        {
            "psi": x,
            "ft/s": y,
            "delta_cubic_spline": [
                round(abs(a - b), 3) for a, b in zip(y, new_y_cubic_spline)
            ],
            "delta_BarycentricInterpolator": [
                round(abs(a - b), 3)
                for a, b in zip(y, new_y_BarycentricInterpolator)
            ],
            "delta_krogh": [
                round(abs(a - b), 3) for a, b in zip(y, new_y_krogh)
            ],
            "new_y_barycentric_interpolate": [
                round(abs(a - b), 3)
                for a, b in zip(y, f_barycentric_interpolate)
            ],
            "delta_pchip": [abs(a - b) for a, b in zip(y, new_y_pchip)],
            "delta_akima": [abs(a - b) for a, b in zip(y, new_y_akima)],
            "delta_linear": [abs(a - b) for a, b in zip(y, new_y_linear)],
            "delta_nearest": [
                round(abs(a - b), 3) for a, b in zip(y, new_y_nearest)
            ],
            "delta_nearest_up": [
                round(abs(a - b), 3) for a, b in zip(y, new_y_nearest_up)
            ],
            "delta_zero": [round(abs(a - b), 3) for a, b in zip(y, new_y_zero)],
            "delta_slinear": [
                round(abs(a - b), 3) for a, b in zip(y, new_y_slinear)
            ],
            "delta_quadratic": [
                round(abs(a - b), 3) for a, b in zip(y, new_y_quadratic)
            ],
            "delta_cubic": [
                round(abs(a - b), 3) for a, b in zip(y, new_y_cubic)
            ],
            "delta_previous": [
                round(abs(a - b), 3) for a, b in zip(y, new_y_previous)
            ],
            "delta_next": [round(abs(a - b), 3) for a, b in zip(y, new_y_next)],
            "delta_3": [round(abs(a - b), 3) for a, b in zip(y, new_y_3)],
            "delta_5": [round(abs(a - b), 3) for a, b in zip(y, new_y_5)],
            "delta_7": [round(abs(a - b), 3) for a, b in zip(y, new_y_7)],
            "delta_9": [round(abs(a - b), 3) for a, b in zip(y, new_y_9)],
        }
    )
    df.to_csv(f"show_err_interp_{gas_sg}_{temp_fahrenheit}.csv", index=False)


@lru_cache(maxsize=None)
def charts(gas_sg: float) -> typ.List[GasSGDataframe]:
    """Return list of GasSDDataframe and interpolation function."""
    array_list: typ.List[GasSGDataframe] = []
    for temp in fahrenheit_dict[gas_sg]:
        # try:
        #     csv_file = pkg_resources.resource_filename(
        #         "chart_sos", f"gas_sg_{gas_sg}_{temp}F.csv"
        #     )
        # except ModuleNotFoundError:
        #     csv_file = f"gas_sg_{gas_sg}_{temp}F.csv"
        # dataframe = pd.read_csv(csv_file, header=None)
        # dataframe.columns = ["psi", "ft/s"]
        # dataframe = dataframe.sort_values(by=["psi"])
        dataframe = fahrenheit_pressure_df_dict[gas_sg][temp]
        x = dataframe["psi"].tolist()
        y = dataframe["ft/s"].tolist()
        f_cubic_spline = CubicSpline(x, y)
        array_list.append(
            GasSGDataframe(gas_sg, temp, dataframe, f_cubic_spline)
        )
    return array_list


@lru_cache(maxsize=None)
def pressure_temperature_interpolation(
    gas_sg: float, temp_f: float, pressure: float
) -> float:
    """Experiment of gas_sg in range [0.6, 1.2], temp_f in range [19, 448]."""
    # Try to approximate the SOS when given gas_sg=0.6, temp_f=100, pressure=500
    array_list = charts(gas_sg)
    return round(
        float(local_interpolation(array_list, gas_sg, temp_f, pressure)), 3
    )


def return_pair_charts(
    gas_sg: float,
) -> typ.Tuple[
    typ.List[GasSGDataframe], typ.List[GasSGDataframe], float, float
]:
    """Return pair of charts."""
    if 0.6 <= gas_sg <= 0.8:
        low_sg_chart = charts(0.6)
        hi_sg_chart = charts(0.8)
        low_bound = 0.6
        hi_bound = 0.8
    elif 0.8 < gas_sg <= 1.0:
        low_sg_chart = charts(0.8)
        hi_sg_chart = charts(1.0)
        low_bound = 0.8
        hi_bound = 1.0
    elif 1.0 < gas_sg <= 1.2:
        low_sg_chart = charts(1.0)
        hi_sg_chart = charts(1.2)
        low_bound = 1.0
        hi_bound = 1.2
    else:
        raise OutChartException("Beyond reference")
    return low_sg_chart, hi_sg_chart, low_bound, hi_bound


def local_interpolation(
    _charts: typ.List[GasSGDataframe],
    _gas_sg: float,
    _temp_f: float,
    _pressure: float,
) -> float:
    """Return sos interpolation."""
    v = [
        instance.interp_func(_pressure) for instance in _charts
    ]  # ft/s at different temperature
    y = v
    x = fahrenheit_dict[_gas_sg]
    ff_cubic_spline = CubicSpline(x, y)
    return float(ff_cubic_spline(_temp_f))


def cal_interpolate_gas_sg(
    gas_sg: float, temp_f: float
) -> typ.Tuple[
    typ.List[float],
    typ.List[float],
    typ.List[float],
    typ.List[float],
    float,
    float,
]:
    """Calculate gas_sg by interpolation."""
    sos_06_list: typ.List[float] = []
    sos_08_list: typ.List[float] = []
    sos_geo_list: typ.List[float] = []
    pressures: typ.List[float] = list(range(0, 3000))

    charts_low_sg, charts_hi_sg, low_bound, hi_bound = return_pair_charts(
        gas_sg
    )
    # Find the in between hi-lo gas_sg.
    # m+n = 0.2
    m = gas_sg - low_bound
    n = hi_bound - gas_sg
    # Average the SOS from geometry analysis.
    for press in pressures:
        p = local_interpolation(charts_low_sg, low_bound, temp_f, press)
        sos_06_list.append(p)
        q = local_interpolation(charts_hi_sg, hi_bound, temp_f, press)
        sos_08_list.append(q)
        avg_sos = (m * q + n * p) / (m + n)
        sos_geo_list.append(avg_sos)
    return (
        sos_06_list,
        sos_08_list,
        sos_geo_list,
        pressures,
        low_bound,
        hi_bound,
    )


def show_interpolate_gas_sg(gas_sg: float, temp_f: float) -> None:
    """Experiment find the SOS by interpolate the gas_sg."""
    (
        sos_06_list,
        sos_08_list,
        sos_geo_list,
        pressures,
        low_bound,
        hi_bound,
    ) = cal_interpolate_gas_sg(gas_sg, temp_f)
    plt.plot(pressures, sos_06_list, color="black", label=f"gas_sg={low_bound}")
    plt.plot(pressures, sos_08_list, color="blue", label=f"gas_sg={hi_bound}")
    plt.plot(pressures, sos_geo_list, color="green", label=f"gas_sg={gas_sg}")
    plt.title(f"Dual plot of gas_sg {low_bound} and {hi_bound}. Temp={temp_f}")
    plt.xlabel("psi")
    plt.ylabel("ft/s")
    plt.legend()
    plt.savefig("test.png")


def get_interpolate_sos(gas_sg: float, temp_f: float, pressure: float) -> float:
    """
    Get the interpolated SOS from interpolation of temperature and gas_sg.

    Valid range of gas_sg is [0.6, 1.2] psi
    Valid range of pressure is [0, 2999] ft/s
    Valid range of temperature is [40, 390] F
    https://hamdon.net/wp-content/uploads/2015/04/Acoustic-Velocity-for-Natural-Gas.pdf
    """
    gas_sg_err_msg: str = ""
    pressure_err_msg: str = ""
    temperature_err_msg: str = ""
    low_gas_sg, hi_gas_sg = 0.6, 1.2
    low_press, hi_press = 0, 2999
    low_temp, hi_temp = 40, 390
    if gas_sg < low_gas_sg or gas_sg > hi_gas_sg:
        gas_sg_err_msg = f"gas_sg must in range [{low_gas_sg}, {hi_gas_sg}]"
    if pressure < low_press or pressure > hi_press:
        pressure_err_msg = f"pressure must in range [{low_press}, {hi_press}]"
    if temp_f < low_temp or temp_f > hi_temp:
        temperature_err_msg = f"pressure must in range [{low_temp}, {hi_temp}]"
    errors = {
        "gas_sg": gas_sg_err_msg,
        "pressure": pressure_err_msg,
        "temperature": temperature_err_msg,
    }
    for _, value in errors.items():
        if value:
            raise OutChartException(errors)

    _, __, sos_geo_list, pressures, ___, ____ = cal_interpolate_gas_sg(
        gas_sg, temp_f
    )
    bounded_pressure = math.floor(pressure)
    index = pressures.index(bounded_pressure)
    return round(float(sos_geo_list[index]), 3)


def calculate_liquid_level_from_sos(
    sos_array: typ.List[float], rttt: float
) -> float:
    """Calculate liquid level from SOS array(ft/s) and rttt(Return Trip Travel Time)(seconds)."""
    # Since rttt is whole go down and go up. It has to be divided by 2.
    go_down_time: float = rttt * 0.5
    dx_magnitude: float = go_down_time / len(sos_array)
    dx_list: typ.List[float] = []
    moving_dx: float = 0
    for _ in sos_array:
        dx_list.append(moving_dx)
        moving_dx += dx_magnitude
    ll = round(np.trapz(sos_array, dx_list), 3)
    return ll
