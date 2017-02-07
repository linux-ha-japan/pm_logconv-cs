# -*- coding: utf-8 -*-

# sosreport plugin for pm_logconv-cs : Pacemaker and Corosync log converter
#
# Copyright (C) 2016 NIPPON TELEGRAPH AND TELEPHONE CORPORATION

### This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from sos.plugins import Plugin, RedHatPlugin
import ConfigParser

# the class name determines the plugin name
# if you want to override it simply provide a @classmethod name()
# that returns the name you want
class pm_logconv_cs(Plugin, RedHatPlugin):
    """Pacemaker and Corosync log message converter
    """

#    packages = [ "pm_logconv-cs", ]
    plugin_name = "pm_logconv_cs"
    profiles = [ "cluster", ]

    option_list = [
        ("single-file", "enable single file collection", "", False),
    ]

    def setup(self):

        self.add_copy_spec("/etc/pm_logconv.conf")

        # obtain output path if customized
        config = ConfigParser.RawConfigParser()
        config.read("/etc/pm_logconv.conf")

        try:
            output_path = config.get("Settings", "output_path")
        except:
            output_path = "/var/log/pm_logconv.out"
            self._log_info(
                "output_path not exist, uses the default %s"
                % output_path)

        output_path = output_path + "*"

        try:
            halog_path = config.get("Settings", "ha_log_path")
        except:
            halog_path = "/var/log/ha-log"
            self._log_info(
                "halog_path not exist, uses the default %s"
                % halog_path)

        halog_path = halog_path + "*"

        if self.get_option("single-file"):
            self._log_info("enable single-file options")
            output_path = output_path.rstrip("*")
            halog_path = halog_path.rstrip("*")

        self.add_copy_spec([
            output_path,
            halog_path
        ])

