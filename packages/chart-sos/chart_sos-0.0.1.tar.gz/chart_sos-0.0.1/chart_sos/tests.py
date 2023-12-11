"""Unit-test file."""
# pylint: disable=no-self-use
# pylint: disable=invalid-name
# pylint: disable=disallowed-name
import typing as typ
import unittest
from timeit import default_timer as timer
from unittest import skip

import sos


class TestStringMethods(unittest.TestCase):
    """Testing class."""

    @skip(reason="Output is files")
    def test_run(self) -> None:
        """Run to generate the files."""
        for gas_sg in sos.gas_sg_list:
            for temp_f in sos.fahrenheit_dict[gas_sg]:
                sos.show_error_interpolation_function(gas_sg, temp_f)

    def test_normal_speed(self) -> None:
        """Test normal speed."""
        self.assertEqual(
            1364.85, sos.pressure_temperature_interpolation(0.6, 90.5, 500)
        )

    def test_hispeed(self) -> None:
        """Test on hi-speed."""
        self.assertEqual(
            1819.753, sos.pressure_temperature_interpolation(0.6, 390, 2500)
        )

    def test_show_interpolate_gas_sg(self) -> None:
        """Test output as a file."""
        gas_sg = 0.62
        temp_f = 390
        sos.show_interpolate_gas_sg(gas_sg, temp_f)

    def test_get_interpolate_sos(self) -> None:
        """Test output as a file."""
        gas_sg = 0.62
        temp_f = 390
        pressure = 2000
        self.assertEqual(
            1745.025, sos.get_interpolate_sos(gas_sg, temp_f, pressure)
        )

    def test_low_bound(self) -> None:
        """Test low bound."""
        gas_sg = 0.62
        pressure = 0
        temp_f = 40
        self.assertEqual(
            1331.421, sos.get_interpolate_sos(gas_sg, temp_f, pressure)
        )

    def test_hi_bound(self) -> None:
        """Test hi bound."""
        gas_sg = 1.19
        pressure = 2999
        temp_f = 390
        self.assertEqual(
            1265.264,
            round(float(sos.get_interpolate_sos(gas_sg, temp_f, pressure)), 3),
        )

    def test_get_interpolate_sos_one_exception(self) -> None:
        """Test one exception."""
        gas_sg = 0.5
        pressure = 2999
        temp_f = 390
        with self.assertRaises(sos.OutChartException) as cm:
            sos.get_interpolate_sos(gas_sg, temp_f, pressure)
        self.assertEqual(
            str(cm.exception),
            str(
                {
                    "gas_sg": "gas_sg must in range [0.6, 1.2]",
                    "pressure": "",
                    "temperature": "",
                }
            ),
        )

    def test_get_interpolate_sos_two_exception(self) -> None:
        """Test 2 exceptions."""
        gas_sg = 0.5
        pressure = 4000
        temp_f = 390
        with self.assertRaises(sos.OutChartException) as cm:
            sos.get_interpolate_sos(gas_sg, temp_f, pressure)
        self.assertEqual(
            str(cm.exception),
            str(
                {
                    "gas_sg": "gas_sg must in range [0.6, 1.2]",
                    "pressure": "pressure must in range [0, 2999]",
                    "temperature": "",
                }
            ),
        )

    def test_get_interpolate_sos_three_exception(self) -> None:
        """Test 3 exceptions."""
        gas_sg = 0.5
        pressure = 4000
        temp_f = 500
        with self.assertRaises(sos.OutChartException) as cm:
            sos.get_interpolate_sos(gas_sg, temp_f, pressure)
        self.assertEqual(
            str(cm.exception),
            str(
                {
                    "gas_sg": "gas_sg must in range [0.6, 1.2]",
                    "pressure": "pressure must in range [0, 2999]",
                    "temperature": "pressure must in range [40, 390]",
                }
            ),
        )

    def test_find_liquid_level(self) -> None:
        """Find liquid level."""
        sos_list: typ.List[float] = [
            1256.261,
            1258.568,
            1260.903,
            1263.29,
            1265.61,
            1267.772,
            1269.866,
            1272.032,
            1274.312,
            1276.594,
            1278.829,
            1281.112,
            1281.112,
            1281.118,
            1281.125,
            1283.657,
            1286.241,
            1288.713,
            1290.985,
            1293.172,
            1295.676,
            1298.302,
            1300.832,
            1300.839,
            1300.845,
            1303.389,
            1305.742,
            1308.101,
            1310.369,
            1310.375,
            1310.38,
            1312.346,
            1314.232,
            1316.22,
            1318.257,
            1318.262,
            1318.267,
            1320.361,
            1322.229,
            1324.127,
            1324.132,
            1324.137,
            1325.757,
            1327.445,
            1329.168,
            1329.173,
            1329.178,
            1331.066,
            1332.91,
            1334.769,
            1336.633,
            1338.464,
            1340.316,
            1342.165,
            1343.985,
            1345.832,
            1347.673,
            1349.497,
            1351.393,
            1353.334,
            1355.315,
            1357.246,
            1359.019,
        ]
        self.assertEqual(
            3223.071, sos.calculate_liquid_level_from_sos(sos_list, 5)
        )

    def test_cache(self) -> None:
        """Test cache. Gain 20%."""
        gas_sg = 0.62
        pressure = 0
        temp_f = 40
        print("1st hit")
        start = timer()
        self.assertEqual(
            1331.421, sos.get_interpolate_sos(gas_sg, temp_f, pressure)
        )
        end = timer()
        print(end - start)
        print("2nd hit")
        start = timer()
        self.assertEqual(
            1331.421, sos.get_interpolate_sos(gas_sg, temp_f, pressure)
        )
        end = timer()
        print(end - start)


if __name__ == "__main__":
    unittest.main()
