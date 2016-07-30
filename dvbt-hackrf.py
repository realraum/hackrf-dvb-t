#!/usr/bin/env /usr/bin/python

# Copyright 2014 Ron Economos (w6rz@comcast.net)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gnuradio import blocks
from gnuradio import digital
from gnuradio import fft
from gnuradio import gr
from gnuradio import filter
from gnuradio.fft import window
import dvbt
import osmosdr
import sys
from dvbtconfig import DVBTConfig

def main(args):
    nargs = len(args)
    if nargs == 1:
        infile  = args[0]
        outfile = None
    elif nargs == 2:
        infile   = args[0]
        outfile  = args[1]
    else:
        sys.stderr.write("Usage: dvbt-hackrf.py infile [output_file]\n");
        sys.exit(1)

    ## Config Options
    config = DVBTConfig('dvbt.conf')

    # DVB-T Parameters
    channel_mhz = config.get_channel_mhz()
    mode = config.get_mode()
    code_rate = config.get_code_rate()
    constellation = config.get_constellation()
    guard_interval = config.get_guard_interval()

    # Hack-RF Parameters
    center_freq = config.get_center_freq()
    rf_gain = config.get_hackrf_rf_gain()
    if_gain = config.get_hackrf_if_gain()
    bb_gain = config.get_hackrf_bb_gain()

    ##

    samp_rate = 10000000.0

    if mode == dvbt.T2k:
        factor = 1
        carriers = 2048
    elif mode == dvbt.T8k:
        factor = 4
        carriers = 8192

    if guard_interval == dvbt.G1_32:
        gi = carriers / 32
    elif guard_interval == dvbt.G1_16:
        gi = carriers / 16
    elif guard_interval == dvbt.G1_8:
        gi = carriers / 8
    elif guard_interval == dvbt.G1_4:
        gi = carriers / 4

    if channel_mhz == 8:
        bandwidth = 8750000
    elif channel_mhz == 7:
        bandwidth = 7000000
    elif channel_mhz == 6:
        bandwidth = 6000000
    elif channel_mhz == 5:
        bandwidth = 5000000
    else:
        bandwidth = 8750000

    log=gr.logger("dvbt-hackrf")
    log.set_level("DEBUG");
    log.debug("logger initilized")

    tb = gr.top_block()
    log.debug("top block initialized")

    src = blocks.file_source(gr.sizeof_char, infile, True)
    log.debug("source block initialized")

    dvbt_energy_dispersal = dvbt.energy_dispersal(1 * factor)
    dvbt_reed_solomon_enc = dvbt.reed_solomon_enc(2, 8, 0x11d, 255, 239, 8, 51, (8 * factor))
    dvbt_convolutional_interleaver = dvbt.convolutional_interleaver((136 * factor), 12, 17)
    dvbt_inner_coder = dvbt.inner_coder(1, (1512 * factor), constellation, dvbt.NH, code_rate)
    dvbt_bit_inner_interleaver = dvbt.bit_inner_interleaver((1512 * factor), constellation, dvbt.NH, mode)
    dvbt_symbol_inner_interleaver = dvbt.symbol_inner_interleaver((1512 * factor), mode, 1)
    dvbt_dvbt_map = dvbt.dvbt_map((1512 * factor), constellation, dvbt.NH, mode, 1)
    dvbt_reference_signals = dvbt.reference_signals(gr.sizeof_gr_complex, (1512 * factor), carriers, constellation, dvbt.NH, code_rate, code_rate, dvbt.G1_32, mode, 0, 0)
    fft_vxx = fft.fft_vcc(carriers, False, (window.rectangular(carriers)), True, 10)
    digital_ofdm_cyclic_prefixer = digital.ofdm_cyclic_prefixer(carriers, carriers+(gi), 0, "")
    rational_resampler_xxx = filter.rational_resampler_ccc(interpolation=70, decimation=64, taps=None, fractional_bw=None)
    blocks_multiply_const_vxx = blocks.multiply_const_vcc((0.0022097087, ))
    log.debug("DVB-T blocks initialized")

    out = osmosdr.sink(args="numchan=1")
    out.set_sample_rate(samp_rate)
    out.set_center_freq(center_freq, 0)
    out.set_freq_corr(0, 0)
    out.set_gain(rf_gain, 0)
    out.set_if_gain(if_gain, 0)
    out.set_bb_gain(bb_gain, 0)
    out.set_antenna("", 0)
    out.set_bandwidth(0, 0)
    log.debug("Output block initialized")

    tb.connect(src, dvbt_energy_dispersal)
    tb.connect(dvbt_energy_dispersal, dvbt_reed_solomon_enc)
    tb.connect(dvbt_reed_solomon_enc, dvbt_convolutional_interleaver)
    tb.connect(dvbt_convolutional_interleaver, dvbt_inner_coder)
    tb.connect(dvbt_inner_coder, dvbt_bit_inner_interleaver)
    tb.connect(dvbt_bit_inner_interleaver, dvbt_symbol_inner_interleaver)
    tb.connect(dvbt_symbol_inner_interleaver, dvbt_dvbt_map)
    tb.connect(dvbt_dvbt_map, dvbt_reference_signals)
    tb.connect(dvbt_reference_signals, fft_vxx)
    tb.connect(fft_vxx, digital_ofdm_cyclic_prefixer)
    tb.connect(digital_ofdm_cyclic_prefixer, blocks_multiply_const_vxx)
    tb.connect(blocks_multiply_const_vxx, rational_resampler_xxx)
    tb.connect(rational_resampler_xxx, out)
    log.debug("all blocks connected")

    if outfile:
        dst = blocks.file_sink(gr.sizeof_gr_complex, outfile)
        tb.connect(blocks_multiply_const_vxx, dst)

    log.debug("running gnuradio")
    tb.run()


if __name__ == '__main__':
    main(sys.argv[1:])
