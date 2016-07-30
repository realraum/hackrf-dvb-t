#!/usr/bin/env /usr/bin/python

# Copyright 2015 Christian Pointner <equinox@spreadspace.org>
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

import os
import sys
import dvbt
from dvbtconfig import DVBTConfig

def main(args):
    nargs = len(args)
    if nargs == 1:
        infile  = args[0]
        device = '0'
    elif nargs == 2:
        infile   = args[0]
        device  = args[1]
    else:
        sys.stderr.write("Usage: dvbt-hackrf.py infile [device-index (default=0)]\n");
        sys.exit(1)

    gainDBm = '3'

    ## Config Options
    config = DVBTConfig('dvbt.conf')

    # DVB-T Parameters
    channel_mhz = config.get_channel_mhz()
    mode = config.get_mode()
    code_rate = config.get_code_rate()
    constellation = config.get_constellation()
    guard_interval = config.get_guard_interval()

    # HF Parameters
    center_freq = '%d' % (config.get_center_freq()/1000)
    gain = '%d' % config.get_tsrfsend_gain()
    cell_id = '%d' % config.get_tsrfsend_cell_id()


    ##

    # this is based on the formula found at:
    #  http://www.dveo.com/broadcast/bit-rate-calculation-for-COFDM-modulation.shtml
    #
    # DVB-T modulator maximum play rate depends on code rate, constellation, guard interval, bandwidth.
    # The maximum bit rate can be calculated as below.
    #
    # TBandwidth = {6,000,000, 7,000,000, 8,000,000} in Hz for 6MHz, 7MHz, 8MHz
    # TCodeRate = {1/2, 2/3, 3/4, 5/6, 7/8}
    # TConstellation = {2, 4, 6} <- QPSK = 2, 16QAM=4, 64QAM = 6
    # TGuardInterval = {4/5, 8/9, 16/17, 32/33}, 1/4 = 4/5, 1/8 = 8/9, 1/16 => 16/17, 1/32 => 32/33}
    # 2K/8K mode does not matter
    #
    # Maximum bit rate = 1512 / 2048 * 188 / 204 * 64 / 56 * TBandwidth * TcodeRate * TConstellation * TGuardInterval (bps)
    #                  =             423 / 544             * TBandwidth * TCodeRate * TConstellation * TGuardInterval (bps)
    #

    argBW = '%d' % (channel_mhz * 1000)

    argCR = '1/2'
    if code_rate == dvbt.C1_2:
        argCR = '1/2'
    elif code_rate == dvbt.C2_3:
        argCR = '2/3'
    elif code_rate == dvbt.C3_4:
        argCR = '3/4'
    elif code_rate == dvbt.C5_6:
        argCR = '5/6'
    elif code_rate == dvbt.C7_8:
        argCR = '7/8'
    else:
        raise ValueError("invalid cod_rate")

    argCO = '4'
    if constellation == dvbt.QPSK:
        argCO = '4'
    elif constellation == dvbt.QAM16:
        argCO = '16'
    elif constellation == dvbt.QAM64:
        argCO = '64'
    else:
        raise ValueError("invalid constellation")

    argGI = '1/4'
    if guard_interval == dvbt.G1_32:
        argGI = '1/32'
    elif guard_interval == dvbt.G1_16:
        argGI = '1/16'
    elif guard_interval == dvbt.G1_8:
        argGI = '1/8'
    elif guard_interval == dvbt.G1_4:
        argGI = '1/4'
    else:
        raise ValueError("invalid guard_interval")

    argMO = '2'
    if mode == dvbt.T2k:
        argMO = '2'
    elif mode == dvbt.T8k:
        argMO = '8'
    else:
        raise ValueError("invalid guard_interval")

    os.execl('./tsrfsend', 'tsrfsend', infile, device, center_freq, argBW, argCO, argCR, argGI, argMO, cell_id, gain)

if __name__ == '__main__':
    main(sys.argv[1:])
