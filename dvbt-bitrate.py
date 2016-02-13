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

import sys
import dvbt
from dvbtconfig import DVBTConfig

def main(args):
    ## Config Options
    config = DVBTConfig('dvbt-hackrf.conf')

    # DVB-T Parameters
    channel_mhz = config.get_channel_mhz()
    mode = config.get_mode()
    code_rate = config.get_code_rate()
    constellation = config.get_constellation()
    guard_interval = config.get_guard_interval()

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

    TBandwidth = channel_mhz * 1000000

    TCodeRate = 0.0
    if code_rate == dvbt.C1_2:
        TCodeRate = 1.0/2.0
    elif code_rate == dvbt.C2_3:
        TCodeRate = 2.0/3.0
    elif code_rate == dvbt.C3_4:
        TCodeRate = 3.0/4.0
    elif code_rate == dvbt.C5_6:
        TCodeRate = 5.0/6.0
    elif code_rate == dvbt.C7_8:
        TCodeRate = 7.0/8.0
    else:
        raise ValueError("invalid cod_rate")

    TConstellation = 0
    if constellation == dvbt.QPSK:
        TConstellation = 2
    elif constellation == dvbt.QAM16:
        TConstellation = 4
    elif constellation == dvbt.QAM64:
        TConstellation = 6
    else:
        raise ValueError("invalid constellation")

    TGuardInterval = 0.0
    if guard_interval == dvbt.G1_32:
        TGuardInterval = 32.0/33.0
    elif guard_interval == dvbt.G1_16:
        TGuardInterval = 16.0/17.0
    elif guard_interval == dvbt.G1_8:
        TGuardInterval = 8.0/9.0
    elif guard_interval == dvbt.G1_4:
        TGuardInterval = 4.0/5.0
    else:
        raise ValueError("invalid guard_interval")


    MaxBitrate = 423.0 / 544.0 * TBandwidth * TCodeRate * TConstellation * TGuardInterval

    print "Maximum Bitrate = %d bps (%9.3f kbps, %6.3f Mbps)" % (MaxBitrate, MaxBitrate/1000, MaxBitrate/(1000000))

if __name__ == '__main__':
    main(sys.argv[1:])
