# pyhiir
use hiir (https://github.com/unevens/hiir) library in python 

HIIR is a DSP (digital signal processing) library in C++ which allows:
 - Changing the sampling rate of a signal by a factor of 2
 - Obtaining two signals with a pi/2 phase difference (Hilbert Transform)

 Pyhiir offers wrappers for the hiir methods in python. 

usage example:

```python
from pyhiir.hiir import hiir
from pyhiir.allpass import LowPass
import matplotlib.pyplot as plt
import numpy as np
from scypi import signal

if __name__=='__main__':
    h = hiir()

    # compute filter coeficients, order 5 and 0.01 passband ripple
    c = h.compute_coefs_order_tbw(5, .01)

    # create an half-band low pass filter with allpass chains
    f = LowPass(c)

    # Now get the filter transfer function for plotting
    ff = f.get_transfer_function()
    w, h = signal.freqz(ff.b, ff.a)
    plt.plot(w / np.pi, 20 * np.log10(abs(h)), 'b')
    plt.show()

```