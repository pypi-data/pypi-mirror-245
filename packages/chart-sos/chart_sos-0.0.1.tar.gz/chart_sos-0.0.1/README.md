# Speed of Sound from 1970 chart
This project follow the echometer company [article](https://hamdon.net/wp-content/uploads/2015/04/Acoustic-Velocity-for-Natural-Gas.pdf).

# Data Extraction technique
Make use of [WebPlotDigitizer](https://automeris.io/WebPlotDigitizer/).
It saves data in Tar files.

# Usage
`gas_sg` has no unit<br>
`pressure` is psi<br>
`temp` in Fahrenheit
```python
import sos
gas_sg = 0.62
pressure = 0
temp_f = 40
sos.get_interpolate_sos(gas_sg, temp_f, pressure)
```

# Show plot
`gas_sg = 0.62` is not in the chart.<br>
![test.png](test.png)
