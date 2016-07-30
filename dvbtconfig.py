#
#  Copyright (C) 2016 Christian Pointner <equinox@spreadspace.org>
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

import dvbt
import ConfigParser

class DVBTConfig:
    config = ConfigParser.RawConfigParser()

    # DVB-T Parameters
    dflt_channel_mhz = 6
    dflt_mode = dvbt.T2k
    dflt_code_rate = dvbt.C1_2
    dflt_constellation = dvbt.QPSK
    dflt_guard_interval = dvbt.G1_32

    # Channel Parameters
    dflt_center_freq = 498000000

    # Hack-RF Parameters
    dflt_hackrf_rf_gain = 14
    dflt_hackrf_if_gain = 20
    dflt_hackrf_bb_gain = 20

    # tsrfsend Parameters
    dflt_tsrfsend_gain = 0
    dflt_tsrfsend_cell_id = 0


    def __init__(self, configfile):
        self.config.readfp(open(configfile))

    def get_channel_mhz(self):
        try:
            c = self.config.getint('dvb-t', 'bandwith')
            if c < 5 or c > 8:
                raise ValueError("illegal value for bandwith: %d" % c)
            return c
        except ConfigParser.NoSectionError:
            return self.dflt_channel_mhz
        except ConfigParser.NoOptionError:
            return self.dflt_channel_mhz


    def get_mode(self):
        try:
            m = self.config.get('dvb-t', 'mode')
            if m.upper() == "2K":
                return dvbt.T2k
            if m.upper() == "8K":
                return dvbt.T8k
            raise ValueError("illegal value for mode: %s" % m)
        except ConfigParser.NoSectionError:
            return self.dflt_mode
        except ConfigParser.NoOptionError:
            return self.dflt_mode

    def get_code_rate(self):
        try:
            c = self.config.get('dvb-t', 'code-rate')
            if c == "1/2":
                return dvbt.C1_2
            if c == "2/3":
                return dvbt.C2_3
            if c == "3/4":
                return dvbt.C3_4
            if c == "5/6":
                return dvbt.C5_6
            if c == "7/8":
                return dvbt.C7_8
            raise ValueError("illegal value for code_rate: %s" % c)
        except ConfigParser.NoSectionError:
            return self.dflt_code_rate
        except ConfigParser.NoOptionError:
            return self.dflt_code_rate

    def get_constellation(self):
        try:
            c = self.config.get('dvb-t', 'constellation')
            if c.upper() == "QPSK":
                return dvbt.QPSK
            if c.upper() == "QAM16":
                return dvbt.QAM16
            if c.upper() == "QAM64":
                return dvbt.QAM64
            raise ValueError("illegal value for constellation: %s" % c)
        except ConfigParser.NoSectionError:
            return self.dflt_constellation
        except ConfigParser.NoOptionError:
            return self.dflt_constellation

    def get_guard_interval(self):
        try:
            g = self.config.get('dvb-t', 'guard-interval')
            if g == "1/32":
                return dvbt.G1_32
            if g == "1/16":
                return dvbt.G1_16
            if g == "1/8":
                return dvbt.G1_8
            if g == "1/4":
                return dvbt.G1_4
            raise ValueError("illegal value for guard_interval: %s" % g)
        except ConfigParser.NoSectionError:
            return self.dflt_guard_interval
        except ConfigParser.NoOptionError:
            return self.dflt_guard_interval


    def get_center_freq(self):
        try:
            f = self.config.getint('channel', 'frequency')
            if f < 474000000 or f > 858000000:
                raise ValueError("center frequency is out of allowed range: %d" % f)
            return f
        except ConfigParser.NoSectionError:
            return self.dflt_center_freq
        except ConfigParser.NoOptionError:
            return self.dflt_center_freq

    def get_hackrf_rf_gain(self):
        try:
            return self.config.getint('hackrf', 'rf-gain')
        except ConfigParser.NoSectionError:
            return self.dflt_hackrf_rf_gain
        except ConfigParser.NoOptionError:
            return self.dflt_hackrf_rf_gain

    def get_hackrf_if_gain(self):
        try:
            return self.config.getint('hackrf', 'if-gain')
        except ConfigParser.NoSectionError:
            return self.dflt_hackrf_if_gain
        except ConfigParser.NoOptionError:
            return self.dflt_hackrf_if_gain

    def get_hackrf_bb_gain(self):
        try:
            return self.config.getint('hackrf', 'bb-gain')
        except ConfigParser.NoSectionError:
            return self.dflt_hackrf_bb_gain
        except ConfigParser.NoOptionError:
            return self.dflt_hackrf_bb_gain

    def get_tsrfsend_cell_id(self):
        try:
            return self.config.getint('tsrfsend', 'cell-id')
        except ConfigParser.NoSectionError:
            return self.dflt_tsrfsend_cell_id
        except ConfigParser.NoOptionError:
            return self.dflt_tsrfsend_cell_id

    def get_tsrfsend_gain(self):
        try:
            return self.config.getint('tsrfsend', 'gain')
        except ConfigParser.NoSectionError:
            return self.dflt_tsrfsend_gain
        except ConfigParser.NoOptionError:
            return self.dflt_tsrfsend_gain
