#!/usr/bin/python
# -*- coding: utf-8 -*-

# pm_logconv : Pacemaker and Corosync log converter
#
#
# Copyright (C) 2011 NIPPON TELEGRAPH AND TELEPHONE CORPORATION
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os, sys, signal, time, datetime, syslog, types, glob, pickle
import ConfigParser, re, commands, operator, string
from optparse import OptionParser
from stat import ST_INO, ST_NLINK, ST_SIZE, S_IRUSR, S_IWUSR
from socket import gethostname
from errno import ESRCH

#
# version number of pm_logconv.
#
VERSION = "1.0"

#
# system's host name.
#
try:
	HOSTNAME = gethostname()
except Exception, strerror:
	print >> sys.stderr, "Error: gethostname() error occurred.", strerror
	sys.exit(1)

#
# default settings.
# (when not specified with configuration file or command line option.)
#
CONFIGFILE = "/etc/pm_logconv.conf"
HA_LOGFILE = "/var/log/ha-log"
OUTPUTFILE = "/var/log/pm_logconv.out"
SYSLOGFORMAT = True

#
# Timeout(ms) for reset log convert status.
#
RESET_INTERVAL = 60

# A flag of failer status
# resource failer 1(resource error)
# score    failer 2(pingd rsclocation)
# node     failer 3(split brain)
FAIL_RSC	= "1"
FAIL_SCORE	= "2"
FAIL_NODE	= "3"

# A flag of resource status(for failer)
# resource start   1
# resource move    2
# resource stop    3
# resource stopped 4
FAIL_STR	= "1"
FAIL_MOVE	= "2"
FAIL_STP	= "3"
FAIL_STPD	= "4"

#
# A list of [attribute_name, operation, attribute_value],
# The setting is described in CONFIGFILE.
# These are to decide whether some failure occur or not
# when cluster status changes to S_POLICY_ENGINE.
#
attrRuleList = list()
attrRules = list()

# A list of resource-id.
# If the all of specified resources are active,
# it means "F/O succeeded."
# If not, "F/O failed."
# The setting is described in CONFIGFILE.
actRscList = list()

#
# A list of patterns.
# The setting is described in CONFIGFILE.
#
lconvRuleList = list()

#
# shutdown flag, when SIGINT or SIGTERM signal is received, set it True.
#
do_shutdown = False

#
# command name for getting DC node status.
#
CMD_CRMADMIN = "crmadmin"

#
# output version number of pm_logconv and exit.
#
def print_version(option, opt, value, parser):
	sys.stdout.write("%s\n" % VERSION)
	sys.exit(0)

#
# signal handler method. only set True to the shutdown flag.
#
def shutdown_logconv(signum, frame):
	global do_shutdown
	pm_log.info("shutdown_logconv: received signal [%d], " \
		"scheduling shutdown.." % signum)
	do_shutdown = True

#
# set the signal handler.
#
signal.signal(signal.SIGINT, shutdown_logconv)
signal.signal(signal.SIGTERM, shutdown_logconv)


class LogconvLog:
	LOG_EMERG		= 0
	LOG_ALERT		= 1
	LOG_CRIT		= 2
	LOG_ERR			= 3
	LOG_WARNING		= 4
	LOG_NOTICE		= 5
	LOG_INFO		= 6
	LOG_DEBUG		= 7

	syspriority = [ syslog.LOG_EMERG, syslog.LOG_ALERT, syslog.LOG_CRIT,
					syslog.LOG_ERR, syslog.LOG_WARNING, syslog.LOG_NOTICE,
					syslog.LOG_INFO, syslog.LOG_DEBUG ]

	prioritystr = [ "emerg", "alert", "crit", "error", "warning", "notice", "info", "debug" ]

	DEFAULT_LOGOPT = syslog.LOG_CONS
	DEFAULT_FACILITY = syslog.LOG_DAEMON

	facility_map = {
		"kern":		syslog.LOG_KERN,
		"user":		syslog.LOG_USER,
		"mail":		syslog.LOG_MAIL,
		"daemon":	syslog.LOG_DAEMON,
		"auth":		syslog.LOG_AUTH,
		"syslog":	syslog.LOG_SYSLOG,
		"lpr":		syslog.LOG_LPR,
		"news":		syslog.LOG_NEWS,
		"uucp":		syslog.LOG_UUCP,
		"cron":		syslog.LOG_CRON,
		"authpriv":	10<<3,
		"ftp":		11<<3,
		"local0":	syslog.LOG_LOCAL0,
		"local1":	syslog.LOG_LOCAL1,
		"local2":	syslog.LOG_LOCAL2,
		"local3":	syslog.LOG_LOCAL3,
		"local4":	syslog.LOG_LOCAL4,
		"local5":	syslog.LOG_LOCAL5,
		"local6":	syslog.LOG_LOCAL6,
		"local7":	syslog.LOG_LOCAL7,
	}

	facilitystr_map = {
		syslog.LOG_KERN:	"kern",
		syslog.LOG_USER:	"user",
		syslog.LOG_MAIL:	"mail",
		syslog.LOG_DAEMON:	"daemon",
		syslog.LOG_AUTH:	"auth",
		syslog.LOG_SYSLOG:	"syslog",
		syslog.LOG_LPR:		"lpr",
		syslog.LOG_NEWS:	"news",
		syslog.LOG_UUCP:	"uucp",
		syslog.LOG_CRON:	"cron",
		10<<3:				"authpriv",
		11<<3:				"ftp",
		syslog.LOG_LOCAL0:	"local0",
		syslog.LOG_LOCAL1:	"local1",
		syslog.LOG_LOCAL2:	"local2",
		syslog.LOG_LOCAL3:	"local3",
		syslog.LOG_LOCAL4:	"local4",
		syslog.LOG_LOCAL5:	"local5",
		syslog.LOG_LOCAL6:	"local6",
		syslog.LOG_LOCAL7:	"local7",
	}

	facilitystr = facilitystr_map[DEFAULT_FACILITY]

	def __init__(self, priority, path):
		self.pid = os.getpid()

		if not isinstance(priority, int) and not isinstance(priority, long):
			self.priority = self.LOG_INFO
		else:
			self.priority = priority

		if not isinstance(path, types.StringTypes):
			self.output = None
		else:
			self.output = path

		self.facility = self.DEFAULT_FACILITY
		syslog.openlog("pm_logconv", self.DEFAULT_LOGOPT, self.facility)

	def __setattr__(self, name, val):
		if name != "LOG_EMERG" and name != "LOG_ALERT" and \
			name != "LOG_CRIT" and name != "LOG_ERR" and \
			name != "LOG_WARNING" and name != "LOG_NOTICE" and \
			name != "LOG_INFO" and name != "LOG_DEBUG" and \
			name != "DEFAULT_LOGOPT" and name != "DEFAULT_FACILITY":
			self.__dict__[name] = val

	def set_priority(self, priority):
		if not isinstance(priority, int) and not isinstance(priority, long):
			return False
		if self.LOG_EMERG < priority and self.DEBUG > priority:
			return False
		self.priority = priority
		return True

	def set_output(self, path):
		if not isinstance(path, types.StringTypes):
			return False
		self.output = path
		return True

	def set_facility(self, facility):
		# FYI: LOG_AUTHPRIV : 10<<3
		#      LOG_FTP      : 11<<3
		if self.facility == facility:
			return True
		if self.facilitystr_map.has_key(facility):
			pm_log.notice("syslog facility changed [%s] to [%s]"
				% (self.facilitystr, self.facilitystr_map[facility]))
			syslog.closelog()
			self.facility = facility
			syslog.openlog("pm_logconv", self.DEFAULT_LOGOPT, self.facility)
			self.facilitystr = self.facilitystr_map[facility]
			return True
		return False

	def emerg(self, message):
		if self.output == None or self.priority >= self.LOG_EMERG:
			return self.logging(self.LOG_EMERG, message)
		return True

	def alert(self, message):
		if self.output == None or self.priority >= self.LOG_ALERT:
			return self.logging(self.LOG_ALERT, message)
		return True

	def crit(self, message):
		if self.output == None or self.priority >= self.LOG_CRIT:
			return self.logging(self.LOG_CRIT, message)
		return True

	def error(self, message):
		if self.output == None or self.priority >= self.LOG_ERR:
			return self.logging(self.LOG_ERR, message)
		return True

	def warn(self, message):
		if self.output == None or self.priority >= self.LOG_WARNING:
			return self.logging(self.LOG_WARNING, message)
		return True

	def notice(self, message):
		if self.output == None or self.priority >= self.LOG_NOTICE:
			return self.logging(self.LOG_NOTICE, message)
		return True

	def info(self, message):
		if self.output == None or self.priority >= self.LOG_INFO:
			return self.logging(self.LOG_INFO, message)
		return True

	def debug(self, message):
		if self.output == None or self.priority >= self.LOG_DEBUG:
			return self.logging(self.LOG_DEBUG, message)
		return True

	def logging(self, priority, message):
		try:
			if not isinstance(priority, int) and not isinstance(priority, long):
				return False
			if not isinstance(message, types.StringTypes):
				return False

			if self.output == None:
				syslog.syslog(self.syspriority[priority], "[%d]: %8s %s" %
					(self.pid, self.prioritystr[priority] + ':', message.rstrip()))
			else:
				t = datetime.datetime.today()
				tfmt = "%s %2d %s" % \
					(t.strftime('%b'), int(t.strftime('%d')), t.strftime('%X'))
				f = open(self.output, 'a')
				f.write("%s %s [%d]: %8s %s\n" % (tfmt, HOSTNAME, self.pid,
					self.prioritystr[priority] + ':', message.rstrip()))
				f.close()
			return True
		except Exception, strerror:
			print >> sys.stderr, "Error: logging() error occurred.", strerror
			sys.exit(1)

class PIDFile:
	'''
	   status of the PID file operation.
	'''
	SYSTEM_ERROR	= -1
	FILE_NOTEXIST	= -2
	FILE_INVALID	= -3
	NOTRUNNING		= -4

	def __init__(self, path):
		self.path = path

	'''
	   status is set as read-only.
	'''
	def __setattr__(self, name, val):
		if name != "SYSTEM_ERROR" and name != "FILE_NOTEXIST" and \
			name != "FILE_INVALID" and name != "NOTRUNNING":
			self.__dict__[name] = val

	'''
	   check whether the process of the PID file has running.
	   return 0 >			: process is running.
	          SYSTEM_ERROR	: system error occurred.
	          NOTRUNNING	: process is NOT running.
	'''
	def is_running(self, pid, cmdline):
		try:
			os.kill(pid, 0)
		except Exception, (errNo, strerror):
			if errNo == ESRCH:
				pm_log.debug("is_running: pm_logconv isn't running.")
				return self.NOTRUNNING
			else:
				pm_log.error("is_running: kill(%d, 0) error occurred." % pid)
				pm_log.debug("is_running: kill(%d, 0) error occurred. [%s]"
					% (pid, strerror))
				return self.SYSTEM_ERROR

		# check to make sure pid hasn't been reused by another process.
		try:
			proc_path = "/proc/%d/cmdline" % pid
			f = open(proc_path, 'r')
			cmdline_now = f.readline().replace('\0', ' ').strip()
			f.close()

			pm_log.debug("is_running: tracked[%s], /proc/%d/cmdline[%s]"
				% (cmdline, pid, cmdline_now))
			if cmdline != cmdline_now:
				return self.NOTRUNNING
		except Exception, strerror:
			pm_log.error("is_running: couldn't read from '%s'." % proc_path)
			pm_log.debug("is_running: couldn't read from '%s'. %s"
				% (proc_path, strerror))
			return self.SYSTEM_ERROR
		return pid

	'''
	   read PID file.
	   return 0 >			: process is running. return running process's PID.
	          SYSTEM_ERROR	: system error occurred.
	          FILE_NOTEXIST	: PID file doesn't exist.
	          FILE_INVALID	: PID file is broken...
	          NOTRUNNING	: succeeded. process is NOT running.
	'''
	def read(self):
		try:
			if os.path.exists(self.path):
				f = open(self.path, 'r')
				pid = f.readline().strip()
				cmdline = f.readline().strip('\n')
				f.close()

				if pid.isdigit() and int(pid) != os.getpid():
					return self.is_running(int(pid), cmdline)
				else:
					pm_log.info("PIDFile.read: PID file is screwed up.")
					return self.FILE_INVALID
			else:
				pm_log.info("PIDFile.read: PID file doesn't exist.")
				return self.FILE_NOTEXIST
		except Exception, strerror:
			pm_log.error("PIDFile.read: I/O error occurred.")
			pm_log.debug("PIDFile.read: I/O error occurred. [%s]" % strerror)
			return self.SYSTEM_ERROR

	'''
	   lock PID file.
	   return 0				: succeeded.
	          0 >			: return already running process's PID.
	          SYSTEM_ERROR	: system error occurred.
	'''
	def lock(self):
		try:
			ret = self.read()
			if ret > 0 or ret == self.SYSTEM_ERROR:
				return ret
			elif ret == self.FILE_NOTEXIST:
				pass
			elif ret == self.FILE_INVALID or ret == self.NOTRUNNING:
				os.remove(self.path)
			else:
				return self.SYSTEM_ERROR
		except Exception, strerror:
			pm_log.error("PIDFile.lock: I/O error occurred.")
			pm_log.debug("PIDFile.lock: I/O error occurred. [%s]" % strerror)
			return self.SYSTEM_ERROR

		try:
			pid = os.getpid()
			f = open("/proc/%d/cmdline" % pid, 'r')
			cmdline = f.readline().replace('\0', ' ').strip()
			f.close()

			tfile = ("%s.%d" % (self.path, pid))
			f = open(tfile, 'w')
			f.write("%d\n%s\n" % (pid, cmdline))
			f.close()

			os.link(tfile, self.path)
			nlink = os.stat(tfile)[ST_NLINK]
			os.remove(tfile)
		except Exception, strerror:
			pm_log.error("PIDFile.lock: I/O error occurred.")
			pm_log.debug("PIDFile.lock: I/O error occurred. [%s]" % strerror)

			try:
				f.close()
				os.remove(tfile)
			except:
				pass
			return self.SYSTEM_ERROR

		if nlink < 2:
			# somehow, it didn't get through - NFS trouble?
			return self.SYSTEM_ERROR
		return 0

class ConvertStatus:
	def __init__(self):
		self.ino = 0
		self.offset = 0
		self.FAILURE_OCCURRED = False
		self.IN_CALC = False
		self.ACTRSC_MOVE = False
		self.IN_FO_PROCESS = False
		self.attrDict = dict()
		self.nodeDict = dict()

cstat = ConvertStatus()

class StatusFile:
	def __init__(self, path):
		self.path = path
		self.w_ino = 0
		self.w_offset = 0
		self.in_calc = False

	'''
	   read from status(read position of ha-log and status of convert) file.
	'''
	def read(self):
		try:
			if os.path.exists(self.path):
				f = os.open(self.path, os.O_RDONLY)
				c = pickle.loads(os.read(f, os.stat(self.path)[ST_SIZE]))
				os.close(f)
				cstat.ino = self.w_ino = c.ino
				cstat.offset = self.w_offset = c.offset
				cstat.FAILURE_OCCURRED = c.FAILURE_OCCURRED
				cstat.IN_CALC = self.in_calc = c.IN_CALC
				cstat.ACTRSC_MOVE = c.ACTRSC_MOVE
				cstat.IN_FO_PROCESS = c.IN_FO_PROCESS
				cstat.attrDict = c.attrDict
				cstat.nodeDict = c.nodeDict
			else:
				pm_log.info("StatusFile.read: status file doesn't exist.")
				self.clear_cstat()
			pm_log.debug("StatusFile.read: [%d:%d], FAIL[%s], IN_CALC[%s], "\
				"RSC_MOVE[%s], IN_FO[%s], attrDict%s, nodeDict%s" %
				(cstat.ino, cstat.offset, cstat.FAILURE_OCCURRED,
				cstat.IN_CALC, cstat.ACTRSC_MOVE, cstat.IN_FO_PROCESS,
				dict(cstat.attrDict), dict(cstat.nodeDict)))
			return True
		except Exception, strerror:
			pm_log.error("StatusFile.read: I/O error occurred.")
			pm_log.debug("StatusFile.read: I/O error occurred. [%s]" % strerror)
			self.clear_cstat()
			return False

	'''
	   write to status(reading ha-log's position and status of convert) file.
	'''
	def write(self):
		if cstat.IN_CALC:
			if self.in_calc:
				return True
			self.in_calc = True
		else:
			self.in_calc = False
			self.w_ino = cstat.ino
			self.w_offset = cstat.offset

		try:
			# current implementation writes to the statfile with os.write().
			# since between built-in function write() and close(), file becomes empty.
			f = os.open(self.path, os.O_WRONLY | os.O_CREAT, S_IRUSR | S_IWUSR)
			l = os.write(f, pickle.dumps(cstat, pickle.HIGHEST_PROTOCOL))
			os.ftruncate(f, l)
			os.close(f)
			pm_log.debug("StatusFile.write: [%d:%d], FAIL[%s], IN_CALC[%s], "\
				"RSC_MOVE[%s], IN_FO[%s], attrDict%s, nodeDict%s" %
				(cstat.ino, cstat.offset, cstat.FAILURE_OCCURRED,
				cstat.IN_CALC, cstat.ACTRSC_MOVE, cstat.IN_FO_PROCESS,
				dict(cstat.attrDict), dict(cstat.nodeDict)))
			return True
		except Exception, strerror:
			pm_log.error("StatusFile.write: I/O error occurred.")
			pm_log.debug("StatusFile.write: I/O error occurred. [%s]" % strerror)
			return False

	def clear_cstat(self):
		global cstat
		pm_log.debug("clear_cstat: called.")
		cstat = ConvertStatus()
		self.w_ino = cstat.ino
		self.w_offset = cstat.offset
		self.in_calc = cstat.IN_CALC
		return

statfile = None

class ParseConfigFile:
	'''
		Initialization to parse config file.
		Open the config file. Its fd should be close in __del__().
	'''
	def __init__(self, config_file):
		self.SEC_SETTINGS = "Settings"
		self.OPT_HA_LOG_PATH = "ha_log_path"
		self.OPT_OUTPUT_PATH = "output_path"
		self.OPT_DATEFORMAT = "syslogformat"
		self.OPT_MANAGE_ATTR = "attribute"
		self.OPT_PATTERN = "pattern"
		self.OPT_RESET_INTERVAL = "reset_interval"
		self.OPT_FUNCNAME = "func"
		self.OPT_LOGLEVEL = "loglevel"
		self.OPT_FOTRIGGER = "fotrigger"
		self.OPT_IGNOREMSG = "ignoremsg"

		self.OPT_LOGFACILITY = "logconv_logfacility"
		self.logfacility = None

		self.OPT_ACTRSC = "act_rsc"

		self.fp = None
		self.cf = ConfigParser.RawConfigParser()
		# open the config file to read.
		if not os.path.exists(config_file):
			pm_log.error("ParseConfigFile.__init__(): " +
				"config file [%s] does not exist." % (config_file))
			#__init__ should return None...
			sys.exit(1)
		try:
			self.fp = open(config_file)
			self.cf.readfp(self.fp)
		except Exception, strerror:
			pm_log.error("ParseConfigFile.__init__(): " +
				"failed to read config file [%s]." % (config_file))
			pm_log.debug("ParseConfigFile.__init__(): %s" % (strerror))
			#__init__ should return None...
			sys.exit(1)

	def __del__(self):
		if self.fp is not None:
			self.fp.close()

	def get_optval(self, secname, optname):
		optval = None
		try:
			optval = self.cf.get(secname, optname)
		except Exception, strerror:
			pm_log.warn("get_optval(): " +
				"failed to get value of \"%s\" in [%s] section. " %
				(optname, secname))
			pm_log.debug("get_optval(): %s" % (strerror))
			return None

		if optval == "":
			pm_log.warn("get_optval(): " +
				"the value of \"%s\" in [%s] section is empty. " %
				(optname, secname))
			return None
		return optval

	'''
		Parse [Settings] section.
		return 0   : succeeded.
		       0 > : error occurs.
	'''
	def parse_basic_settings(self):
		global HA_LOGFILE
		global OUTPUTFILE
		global SYSLOGFORMAT
		global RESET_INTERVAL
		global attrRuleList
		global attrRules
		global actRscList

		# Get all options in the section.
		try:
			setting_opts = self.cf.options(self.SEC_SETTINGS)
		except:
			pm_log.warn("parse_basic_settings(): " +
				"[%s] section does not exist. " % (self.SEC_SETTINGS))
			return (-1)

		for optname in setting_opts:
			optval = self.get_optval(self.SEC_SETTINGS, optname)
			if not optval:
				pm_log.warn("parse_basic_settings(): " +
					"Ignore the setting of \"%s\"." % (optname))
				continue # To the next option in [Settings].

			if optname == self.OPT_HA_LOG_PATH:
				HA_LOGFILE = optval
			elif optname == self.OPT_OUTPUT_PATH:
				OUTPUTFILE = optval
			elif optname == self.OPT_DATEFORMAT:
				if optval.lower() == "true":
					SYSLOGFORMAT = True
				elif optval.lower() == "false":
					SYSLOGFORMAT = False
				else:
					pm_log.warn("parse_basic_settings(): " +
						"the value of \"%s\" is invalid. " % (optname) +
						"Ignore the setting.")
			elif optname == self.OPT_RESET_INTERVAL:
				try:
					tmpval = int(optval)
					# 1 to 32bit integer max value
					if tmpval > 0 and tmpval <= 2147483647:
						RESET_INTERVAL = tmpval
					else:
						raise
				except:
					pm_log.warn("parse_basic_settings(): " +
						"the value of \"%s\" is invalid. " % (optname) +
						"set an default value(60).")
			elif optname.startswith(self.OPT_MANAGE_ATTR) and optval.count(','):
				attrRule = optval.split(',')
				if len(attrRule) != 3:
					pm_log.warn("parse_basic_settings(): " +
						"the format of \"%s\" is invalid. " % (optname) +
						"Ignore the setting.")
					continue # To the next option in [Settings].
				(attrname, op, attrval) = tuple(attrRule)
				attrname = attrname.strip()
				op = op.strip()
				attrval = attrval.strip()
				if attrname == "" or op == "" or attrval == "":
					pm_log.warn("parse_basic_settings(): " +
						"the value of \"%s\" is invalid. " % (optname) +
						"Ignore the setting.")
					continue # To the next option in [Settings].

				'''
					op string should be [lt|gt|lte|gte|eq|ne] in cib.xml.
					However, with operator module of Python,
					"lte" is expressed "le", and "gte" is "ge".
					Here, replace op string to use it as function name.
				'''
				opList = ["lt", "gt", "le", "ge", "eq", "ne"]
				opmatch = False
				for opstr in opList:
					if op == opstr:
						opmatch = True
				if not opmatch:
					if op == "lte":
						op = "le"
					elif op == "gte":
						op = "ge"
					else:
						pm_log.warn("parse_basic_settings(): " +
							"operation \"%s\" (in \"%s\") is invalid. " %
							(op, optname) +
							"Ignore the setting.")
						continue # To the next option in [Settings].

				attrRule = [attrname, op, attrval]
				attrRuleList.append(attrRule)
				pm_log.debug("parse_basic_settings(): attrRuleList%s"%(attrRuleList))
			elif optname.startswith(self.OPT_MANAGE_ATTR) and not optval.count(','):
				optvals = []; rule = []
				for x in [x for x in optval.split(' ') if x]:
					if x.lower() in ['defined','not_defined']:
						optvals.append(None)
					optvals.append(x)
				if len(optvals) % 4 != 3:
					pm_log.warn("parse_basic_settings(): "
						"the format of \"%s\" is invalid."
						%(optname) + " Ignore the setting.")
					continue # To the next option in [Settings].

				binops = ['lt','gt','le','ge','eq','ne','defined','not_defined']
				for i,x in enumerate(optvals):
					if i % 4 == 0:
						name = x
					elif i % 4 == 1:
						y = x.lower().replace('lte','le').replace('gte','ge')
						if y in binops:
							op = y
						else:
							pm_log.warn("parse_basic_settings(): "
								"binary_op \"%s\" (in \"%s\") is invalid."
								%(x,optname) + " Ignore the setting.")
							break
					elif i % 4 == 2:
						rule.append([name, op, x])
					elif i % 4 == 3:
						if x.lower() in ['and','or']:
							rule.append(x.lower())
						else:
							pm_log.warn("parse_basic_settings(): "
								"bool_op \"%s\" (in \"%s\") is invalid."
								%(x,optname) + " Ignore the setting.")
							break
				else:
					attrRules.append(rule)
					pm_log.debug("parse_basic_settings(): attrRules%s"%(attrRules))
				continue # To the next option in [Settings].
			elif optname == self.OPT_LOGFACILITY:
				if LogconvLog.facility_map.has_key(optval.lower()):
					self.logfacility = LogconvLog.facility_map[optval.lower()]
				else:
					pm_log.warn("parse_basic_settings(): " +
						"the value of \"%s\" is invalid. " % (optname) +
						"Ignore the setting.")
			elif optname == self.OPT_ACTRSC:
				for rstr in optval.split(','):
					rstr = rstr.strip()
					if rstr != "":
						if rstr in actRscList:
							pm_log.warn("parse_basic_settings(): " +
								"resource id \"%s\" is written redundantly. " %
								(rstr) +
								"Ignore the redundancy.")
						else:
							actRscList.append(rstr)
			# __if optname == xxx:
		# __for optname in setting_opts:

		return 0

	'''
		Parse sections for log-convertion.
		return 0   : succeeded.
		       0 > : error occurs.
	'''
	def parse_logconv_settings(self):
		logconv_sections = self.cf.sections()
		try:
			logconv_sections.remove(self.SEC_SETTINGS)
		except:
			pm_log.warn("parse_logconv_settings(): " +
				"[%s] section does not exist. " % (self.SEC_SETTINGS))

		#
		# Parse each section.
		#
		for secname in logconv_sections:
			# Get all options in the section.
			try:
				logconv_opts = self.cf.options(secname)
			except:
				pm_log.warn("parse_logconv_settings(): " +
					"[%s] section does not exist. " % (secname) +
					"Ignore this section.")
				continue #To the next section.

			lconvfrm = LogconvFrame()
			lconvfrm.rulename = secname
			for optname in logconv_opts:
				optval = self.get_optval(secname, optname)
				if not optval:
					pm_log.warn("parse_logconv_settings(): " +
						"Ignore the setting of \"%s\"." % (optname))
					continue # To the next option.

				if optname == self.OPT_FUNCNAME:
					defined = hasattr(LogConvertFuncs, optval)
					if defined == False:
						pm_log.error("parse_logconv_settings(): " +
							"function %s() specified in " % (optval) +
							"[%s] section is not defined." % (secname))
						break # Break off parsing this section.
					lconvfrm.func = optval
				elif optname == self.OPT_LOGLEVEL:
					lconvfrm.loglevel = optval
				elif optname == self.OPT_FOTRIGGER:
						lconvfrm.fotrigger = optval
				elif optname == self.OPT_IGNOREMSG:
					if optval.lower() == "true":
						lconvfrm.ignoremsg = True
					elif optval.lower() == "false":
						lconvfrm.ignoremsg = False
					else:
						pm_log.warn("parse_logconv_settings(): " +
							"the value of \"%s\" is invalid. " % (optname) +
							"Ignore the setting.")
				elif optname.startswith(self.OPT_PATTERN):
					pstrList = list()
					tmpList = list()
					pstrList = self.parse_ptn_strings(optval)
					if len(pstrList) <= 0:
						pm_log.error("parse_logconv_settings(): " +
							"match pattern string of \"%s\" is empty." %
							(optname))
						break # Break off parsing this section.
					tmpList = self.compile_ptn_strings(pstrList)
					if tmpList is None:
						pm_log.error("parse_logconv_settings(): " +
							"failed to compile the pattern string in \"%s\"." %
							(optname))
						break # Break off parsing this section.
					lconvfrm.ptnList.append(tmpList)
				else:
					pm_log.debug("parse_logconv_settings(): " +
						"\"%s\" is not valid option string." % (optname) +
						"Ignore the setting.")
			# __for optname in logconv_opts:

			if len(lconvfrm.ptnList) == 0  or lconvfrm.func == None:
				pm_log.warn("parse_logconv_settings(): " +
					"\"%s\" and \"%s*\" setting is required in section [%s]. " %
					(self.OPT_FUNCNAME, self.OPT_PATTERN, secname) +
					"Ignore the section.")
				del lconvfrm
			else:
				lconvRuleList.append(lconvfrm)
			#To the next section.
		#__for secname in logconv_sections:
		return 0

	'''
		Parse match pattern strings (written in a line) and
		make a list of them.
		Strings are set apart by ','.
		arg1  : match pattern strings.
		return: a list of pattern strings.
	'''
	def parse_ptn_strings(self, pstrings):
		pstrList = list()
		for pstr in pstrings.split(','):
			pstr = pstr.strip()
			if pstr != "":
				pstrList.append(pstr)
		return pstrList

	'''
		Compile each pattern string.
		arg1  : a list of pattern strings (made with parse_ptn_strings()).
		return: a list of compiled objects.
	'''
	def compile_ptn_strings(self, pstrList):
		compiledList = list()
		for pstr in pstrList:
			#If it is a negative pattern, compile is as so.
			if pstr.startswith('!'):
				pstr = ur"^(?!.*" + pstr.lstrip('!') + ur").*$"
			compiledList.append(re.compile(pstr))
		return compiledList

'''
	Class to hold rules to convert log message.
'''
class LogconvFrame:
	'''
		rulename : convert rule name. set section name.
		ptnList  : list of compiled object list of match patterns
		           (list of lists).
		func     : function name to convert log message which matches the rule.
		loglevel : log level of converted log.
		fotrigger: the log message is trigger of F/O or not. [True|False]
		ignoremsg: wheter set the time of output log message for auto reset
		           function. [True|False]
	'''
	def __init__(self, rulename=None, ptnList=None, func=None, loglevel=None,
		fotrigger=False, ignoremsg=False):
		self.rulename = rulename
		self.ptnList = ptnList
		self.ptnList = list()
		self.func = func
		self.loglevel = loglevel
		self.fotrigger = fotrigger
		self.ignoremsg = ignoremsg

	'''
		Only for debug.
	'''
	def print_frmval(self):
		print self.rulename
		print self.ptnList
		print self.func
		print self.loglevel
		print self.fotrigger
		print self.ignoremsg

class LogConvert:
	PIDFILE = "/var/run/pm_logconv.pid"
	STATFILE = "/var/run/pm_logconv.stat"

	def __init__(self):
		self.daemonize = False
		self.stop_logconv = False
		self.ask_status = False
		self.is_continue = False
		self.is_present = False
		self.is_oneshot = False
		self.configfile = CONFIGFILE
		now = datetime.datetime.now()
		self.last_logoutput_t = now
		self.last_reset_t = now

		# Get obj of functions to convert log.
		self.funcs = LogConvertFuncs()
		signal.signal(signal.SIGUSR1, self.check_dc_and_reset)

		if not self.parse_args():
			sys.exit(1)

		pm_log.debug("option: daemon[%d], stop[%d], status[%d], continue[%d], " \
			"present[%d], oneshot[%d], config[%s], facility[%s]" % (self.daemonize, self.stop_logconv,
			self.ask_status, self.is_continue, self.is_present, self.is_oneshot, self.configfile, pm_log.facilitystr))
		if not self.stop_logconv and not self.ask_status:
			pm_log.debug("option: target[%s], output[%s], syslogfmt[%s], reset_interval[%d], actrsc%s" % (HA_LOGFILE, OUTPUTFILE, SYSLOGFORMAT, RESET_INTERVAL, actRscList))

	'''
	   PID and status(read position of ha-log and status of convert) file path
	   is set as read-only.
	'''
	def __setattr__(self, name, val):
		if name != "PIDFILE" and name != "STATFILE":
			self.__dict__[name] = val

	'''
	   parse options - command line option and configure file.
	'''
	def parse_args(self):
		myusage = "\n%prog [options]"
		psr = OptionParser(usage=myusage)

		psr.add_option("-d", action="store_true", dest="daemonize",
			default=False, help="make the program a daemon")
		psr.add_option("-k", action="store_true", dest="stop_logconv",
			default=False, help="stop the pm_logconv if it is already running")
		psr.add_option("-s", action="store_true", dest="ask_status",
			default=False, help="return pm_logconv status")
		psr.add_option("-c", action="store_true", dest="is_continue",
			default=False, help="start with a continuous mode (\"-p\" or \"-o\" option is mutually exclusive)")
		psr.add_option("-p", action="store_true", dest="is_present",
			default=False, help="start with a present mode    (\"-c\" or \"-o\" option is mutually exclusive)")
		psr.add_option("-o", action="store_true", dest="is_oneshot",
			default=False, help="start with a oneshot mode    (\"-c\" or \"-p\" option is mutually exclusive)")
		psr.add_option("-f", dest="config_file", default=CONFIGFILE,
			help="the specified configuration file is used")
		psr.add_option("-v", "--version", action="callback", callback=print_version,
			help="print out this program's version and exit")

		opts = psr.parse_args(sys.argv)[0]

		args = ''
		for arg in sys.argv:
			args = args + arg + ' '
		pm_log.info("starting... [%s]" % args[:len(args)-1])

		self.daemonize = opts.daemonize
		self.stop_logconv = opts.stop_logconv
		self.ask_status = opts.ask_status
		self.is_continue = opts.is_continue
		self.is_present = opts.is_present
		self.is_oneshot = opts.is_oneshot
		self.configfile = opts.config_file

		'''
			Parse config file.
		'''
		pcfobj = ParseConfigFile(self.configfile)
		# Parse pm_logconv's basic settings.
		pcfobj.parse_basic_settings()

		if pcfobj.logfacility != None:
			pm_log.set_facility(pcfobj.logfacility)
			pm_log.info("starting... [%s]" % args[:len(args)-1])

		# check command line option.
		true_opts = 0
		for opt in (self.daemonize, self.stop_logconv, self.ask_status):
			if opt:
				true_opts = true_opts + 1
				if true_opts > 1:
					pm_log.error("parse_args: option -d, -k, " \
						"and -s cannot be specified at the same time.")
					return False

		if (self.stop_logconv or self.ask_status) and self.is_continue:
			pm_log.error("parse_args: option -k and -s cannot be specified with -c.")
			return False

		if (self.stop_logconv or self.ask_status) and self.is_present:
			pm_log.error("parse_args: option -k and -s cannot be specified with -p.")
			return False

		if (self.stop_logconv or self.ask_status) and self.is_oneshot:
			pm_log.error("parse_args: option -k and -s cannot be specified with -o.")
			return False

		if \
			(self.is_continue and self.is_present) or \
			(self.is_continue and self.is_oneshot) or \
			(self.is_present  and self.is_oneshot):
			pm_log.error("parse_args: options -c ,-p and -o are mutually exclusive.")
			return False

		if not self.is_continue and not self.is_present and not self.is_oneshot:
			# check Corosync active or dead.
			ret = self.funcs.is_corosync()
			if ret == None:
				return False
			elif ret:
				self.is_continue = True
			else:
				self.is_present = True

		# check file path. isn't the same path specified?
		try:
			fileList = list()
			if not self.stop_logconv and not self.ask_status:
				fileList.append((OUTPUTFILE, "output file for converted message"))
				fileList.append((HA_LOGFILE, "Pacemaker and Corosync log file"))
				fileList.append((self.STATFILE,
					"pm_logconv's status file (can't specify by user)"))
			fileList.append((self.configfile, "pm_logconv's configuration file"))
			fileList.append((self.PIDFILE,
				"pm_logconv's PID file (can't specify by user)"))

			for i in range(0, len(fileList) - 1):
				for j in range(i + 1, len(fileList)):
					pathi, desci = tuple(fileList[i])
					pathj, descj = tuple(fileList[j])
					pm_log.debug("path check: [%s] [%s]"
						% (os.path.realpath(pathi), os.path.realpath(pathj)))
					if os.path.realpath(pathi) == os.path.realpath(pathj):
						pm_log.error("parse_args: specified same path [%s] " \
							"as \"%s\" and \"%s\"." % (pathi, desci, descj))
						return False
		except Exception, strerror:
			pm_log.error("checking path: error occurred.")
			pm_log.debug("checking path: error occurred. [%s]" % strerror)
			return False

		if not self.stop_logconv and not self.ask_status:
			# Parse settings for log convertion.
			pcfobj.parse_logconv_settings()
		return True

	'''
	   run in the background as a daemon, if option -d is specified.
	   and create PID file.
	'''
	def make_daemon(self, pidfile):
		if self.daemonize:
			try:
				pid = os.fork()
				if pid > 0:
					sys.exit(0)
				pm_log.debug("make_daemon: fork() #1 succeeded. pid[%d]" % os.getpid())
				pm_log.pid = os.getpid()
			except OSError, strerror:
				pm_log.error("make_daemon: fork() #1 error occurred.")
				pm_log.debug("make_daemon: fork() #1 error occurred. [%s]" % strerror)
				sys.exit(1)

			try:
				os.setsid()
			except OSError, strerror:
				pm_log.error("make_daemon: setsid() error occurred.")
				pm_log.debug("make_daemon: setsid() error occurred. [%s]" % strerror)
				sys.exit(1)

			try:
				pid = os.fork()
				if pid > 0:
					sys.exit(0)
				pm_log.debug("make_daemon: fork() #2 succeeded. pid[%d]" % os.getpid())
				pm_log.pid = os.getpid()
			except OSError, strerror:
				pm_log.error("make_daemon: fork() #2 error occurred.")
				pm_log.debug("make_daemon: fork() #2 error occurred. [%s]" % strerror)
				sys.exit(1)

		ret = pidfile.lock()
		if ret > 0:
			print >> sys.stderr, "pm_logconv: already running [pid %d]" % ret
			pm_log.info("make_daemon: pm_logconv is already running [pid %d]" % ret)
			sys.exit(0)
		elif ret == pidfile.SYSTEM_ERROR:
			pm_log.info("make_daemon: couldn't start pm_logconv.")
			sys.exit(1)

		if self.daemonize:
			try:
				os.chdir("/")
				os.umask(0)
				sys.stdin.close(); sys.stdin = None
				sys.stdout.close(); sys.stdout = None
				sys.stderr.close(); sys.stderr = None
				os.close(0)
				os.close(1)
				os.close(2)
			except:
				pass
		return True

	'''
	   stop running pm_logconv.
	   return 0	: succeeded. or already stopped.
	          1 : error occurred. it may not have stopped...
	'''
	def logconv_stop(self, pidfile):
		logconv_pid = pidfile.read()
		if logconv_pid <= 0:
			if logconv_pid == pidfile.SYSTEM_ERROR:
				pm_log.info("logconv_stop: couldn't try to stop pm_logconv.")
				return 1
			elif logconv_pid == pidfile.FILE_NOTEXIST:
				pm_log.info("logconv_stop: couldn't try to stop pm_logconv.")
				return 0
			elif logconv_pid == pidfile.FILE_INVALID:
				pm_log.info("logconv_stop: couldn't try to stop pm_logconv.")
				return 1
			elif logconv_pid == pidfile.NOTRUNNING:
				pm_log.info("logconv_stop: pm_logconv already stopped.")
				return 0
			return 1

		pm_log.info("logconv_stop: stopping pm_logconv with pid [%d]." % logconv_pid)
		try:
			os.kill(logconv_pid, signal.SIGTERM)

			# wait for the running pm_logconv to die.
			pm_log.info("logconv_stop: waiting for pid [%d] to exit." % logconv_pid)

			while 1:
				os.kill(logconv_pid, 0)
				time.sleep(1)
		except Exception, (errNo, strerror):
			if errNo != ESRCH:
				pm_log.warn("logconv_stop: pid %d not killed." % logconv_pid)
				pm_log.debug("logconv_stop: pid %d not killed. [%s]"
					% (logconv_pid, strerror))
				return 1
			else:
				pm_log.info("logconv_stop: pid %ld exited." % logconv_pid)
				return 0

	'''
	   get file descriptor which matched the contents of the status file
	   (read position of ha-log).
	'''
	def get_fd(self, statfile):
		try:
			if self.is_continue:
				if statfile.read() and cstat.ino == 0:
					pm_log.error("get_fd: status file doesn't exist.")

				if cstat.ino > 0:
					if os.path.exists(HA_LOGFILE) and \
						cstat.ino == os.stat(HA_LOGFILE)[ST_INO]:
						log = HA_LOGFILE
					else:
						# ha-log's inode didn't match, logrotate?
						# look for the file which inode matches.
						for log in glob.glob(HA_LOGFILE + "?*"):
							if cstat.ino == os.stat(log)[ST_INO]:
								break
						else:
							pm_log.warn("get_fd: Pacemaker and Corosync log" \
								"(inode:%d) doesn't exist." % cstat.ino)
							log = None
							statfile.clear_cstat()

					if log != None:
						f = open(log, 'r')
						if os.fstat(f.fileno()).st_size >= cstat.offset:
							f.seek(cstat.offset)
						else:
							pm_log.warn("get_fd: there is possibility that " \
								"Pacemaker and Corosync log was clear.")
							pm_log.debug("get_fd: reset offset, since " \
								"offset[%d] > file size[%d]"
								% (cstat.offset, os.fstat(f.fileno()).st_size))
							cstat.offset = 0
							self.funcs.clear_status()
						pm_log.info("get_fd: target to convert [%s(inode:%d)]"
							% (log, cstat.ino))
						return f

			if os.path.exists(HA_LOGFILE):
				f = open(HA_LOGFILE, 'r')
				if self.is_present:
					f.seek(os.fstat(f.fileno()).st_size)
			else:
				while not os.path.exists(HA_LOGFILE):
					if do_shutdown:
						return None
					elif self.is_oneshot:
						pm_log.warn("get_fd: Pacemaker and Corosync log(%s) doesn't exist." % HA_LOGFILE)
						return None
					time.sleep(1)
				f = open(HA_LOGFILE, 'r')
			pm_log.info("get_fd: target to convert [%s(inode:%d)]"
				% (HA_LOGFILE, os.fstat(f.fileno()).st_ino))
			return f
		except Exception, strerror:
			pm_log.error("get_fd: I/O error occurred.")
			pm_log.debug("get_fd: I/O error occurred. [%s]" % strerror)
			statfile.clear_cstat()
			return None

	'''
	   get the Pacemaker and Corosync log path, when `logrotate` occurs.
	'''
	def get_nextlog(self, ino, statfile):
		try:
			for log in glob.glob(HA_LOGFILE + "?*"):
				pm_log.debug("get_nextlog: searching previous target[%s(inode:%d)]"
					% (log, os.stat(log)[ST_INO]))
				if ino == os.stat(log)[ST_INO]:
					pm_log.debug("get_nextlog: searching.. found it[%s].size[%d]"
						% (log, os.stat(log)[ST_SIZE]))
					break
			else:
				pm_log.warn("get_nextlog: target(inode:%d) was lost. " \
					"there is possibility that file was remove." % ino)
				statfile.clear_cstat()
				return None

		except Exception, strerror:
			pm_log.warn("get_nextlog: error occurred.")
			pm_log.debug("get_nextlog: error occurred. [%s]" % strerror)
			statfile.clear_cstat()
		return None

	'''
		Check DC node is idle or not with crmadmin command.
		When DC is idle, crmadmin returns "S_IDLE" status.
		return: True  -> local is idle.
		        False -> local is not idle or not DC.
		        None  -> error occurs.
		                 cannot execute command or maybe during DC election.
	'''
	def is_idle(self):
		# Connection timeout (ms).
		# crmadmin command's default value is 30sec.
		TIMEOUT = 30 * 1000

		# Get DC status.
		options = ("-S %s -t %s" % (HOSTNAME, TIMEOUT))
		(status, output) = \
			self.funcs.exec_outside_cmd(CMD_CRMADMIN, options, False)
		if status == None:
			# Failed to exec command.
			pm_log.warn("is_idle(): failed to get local node status.")
			return None
		if status != 0:
			# Maybe during DC election.
			return False
		try:
			dcstat = output.split()[-2]
		except:
			# Failed to parse output strings.
			pm_log.warn("is_idle(): failed to parse output strings." +
				"local node status")
			return None
		if dcstat == "S_IDLE" or dcstat == "S_NOT_DC":
			return True
		return False

	'''
		Reset log convert status when Pacemaker doesn't output any log message
		over RESET_INTERVAL sec.
		Before reset process, check whether DC node is idle or not.
		arg1 : signal number. for use this func as signal handler.
		arg2 : stac frame. for use this func as signal handler.
		return nothing.
	'''
	def check_dc_and_reset(self, signum, frame):
		if signum == None:
			now = datetime.datetime.now()
			if ((self.last_logoutput_t +
					datetime.timedelta(seconds=RESET_INTERVAL)) > now) or \
				((self.last_reset_t +
					datetime.timedelta(seconds=RESET_INTERVAL)) > now):
				return
		if signum == None:
			self.last_reset_t = datetime.datetime.now()
		pm_log.debug("check_dc_and_reset(): try to reset log convert status.")
		self.funcs.debug_status()
		if self.funcs.is_init_status() == True:
			pm_log.debug("check_dc_and_reset(): log convert status is initial value. " +
				"Avoid to reset log convert status.")
			return
		ret = self.is_idle()
		if ret == True:
			self.funcs.clear_status()
			pm_log.debug("check_dc_and_reset(): " +
					"reset log convert status complete.")
			if statfile: statfile.write()
		elif ret == False:
			pm_log.debug("check_dc_and_reset(): DC node is not idle. " +
				"Avoid to reset log convert status.")
		elif ret == None:
			pm_log.error("check_dc_and_reset(): failed to check DC status. " +
				"Avoid to reset log convert status.")
		return

	'''
		Check a line of log message matched or not matched with each re-objects.
		NOTE: pattern strings which are written in a line (in a option which is
		      named "pattern*") are treated as "AND condition".
		      If one section has two or more options named "pattern*",
		      these are treated as "OR condition".
		      ex.)
		      pattern1 = aa, bb
		      pattern2 = cc, dd
		      means
		      "if (($0 ~ /aa/) && ($0 ~ /bb/) || ($0 ~ /cc/) && ($0 ~ /dd/))"
		True  : matched
		False : not matched
		None  : error occurs.
	'''
	def is_matched(self, logline, lconvfrm):
		matched = False
		for ptnobjList in lconvfrm.ptnList:
			# Matching with each re-object which came from strings
			# written in a option "pattern*"
			matchcnt = 0
			for ptnobj in ptnobjList:
				try:
					if ptnobj.search(logline) != None:
						matchcnt += 1
				except Exception, strerror:
					# Error occurs.
					pm_log.debug("is_matched(): %s" % (strerror))
					return None
			if matchcnt == len(ptnobjList):
				# If the log message matched with all object in a pattern line,
				# it is a target log message to convert.
				matched = True
				break
			# If not matched with objects in a pattern line,
			# continue to check with the next line.
		return matched

	'''
		Check the log message is a target to convert or not
		with all rules which are specified in config file.
		and call specified function when a target log message appears.
		return nothing
	'''
	def do_ptn_matching(self, logline):
		setdate = True
		for lconvfrm in lconvRuleList:
			matched = self.is_matched(logline, lconvfrm)
			if matched == True:
				logelm = LogElements()
				if logelm.parse_logmsg(logline, self.funcs) != 0:
					pm_log.error("do_ptn_matching(): " +
						"failed to parse log message. [%s]" % (logline))
					# Set the time of output log message for auto reset.
					self.last_logoutput_t = datetime.datetime.now()
					return # Break off converting this log message.
				# Set original date string and log level.
				outputobj = OutputConvertedLog()
				outputobj.set_datestr(logelm.datestr)
				outputobj.set_orgloglevel(logelm.haloglevel)
				outputobj.set_orglogmsg(logelm.halogmsg)

				# Call specified function.
				try:
					pm_log.debug("do_ptn_matching(): execute %s()." %
						(lconvfrm.func))
					ret = getattr(self.funcs, lconvfrm.func)(\
						outputobj, logelm, lconvfrm)
				except Exception, strerror:
					pm_log.error("do_ptn_matching(): " +
						"failed to execute %s()." % (lconvfrm.func))
					pm_log.debug("do_ptn_matching(): %s" % (strerror))
					continue # To check next rule.

				if ret == CONV_OK:
					# convertion succeeded.
					# If the log is a trigger of FailOver, tell to funcs.
					if lconvfrm.fotrigger:
						cstat.FAILURE_OCCURRED = lconvfrm.fotrigger
						# FailOver pattern
						#	resource failer  + resource move
						#	score failer     + resource move
						#	node failer      + resource move
						#	node failer      + resource start
						#	resource failer  + resource stop
						#	score failer     + resource stop
						#	node failer      + resource stop
						#	node failer      + resource stopped
						if \
							(cstat.FAILURE_OCCURRED == FAIL_RSC   and cstat.ACTRSC_MOVE == FAIL_MOVE) or \
							(cstat.FAILURE_OCCURRED == FAIL_SCORE and cstat.ACTRSC_MOVE == FAIL_MOVE) or \
							(cstat.FAILURE_OCCURRED == FAIL_NODE  and cstat.ACTRSC_MOVE == FAIL_MOVE) or \
							(cstat.FAILURE_OCCURRED == FAIL_NODE  and cstat.ACTRSC_MOVE == FAIL_STR)  or \
							(cstat.FAILURE_OCCURRED == FAIL_RSC   and cstat.ACTRSC_MOVE == FAIL_STP)  or \
							(cstat.FAILURE_OCCURRED == FAIL_SCORE and cstat.ACTRSC_MOVE == FAIL_STP)  or \
							(cstat.FAILURE_OCCURRED == FAIL_NODE  and cstat.ACTRSC_MOVE == FAIL_STP)  or \
							(cstat.FAILURE_OCCURRED == FAIL_NODE  and cstat.ACTRSC_MOVE == FAIL_STPD):
							self.funcs.detect_fo_start(outputobj)
					if lconvfrm.ignoremsg:
						setdate = False
				else:
					if ret == CONV_PARSE_ERROR:
						errmsg = ("%s(): " % (lconvfrm.func) +
							"failed to parse log message. [%s]" %
							(logelm.halogmsg))
					elif ret == CONV_ITEM_EMPTY:
						errmsg = ("%s(): " % (lconvfrm.func) +
							"invalid log message format. [%s]" %
						(logelm.halogmsg))
					elif ret == CONV_GETINFO_ERROR:
						errmsg = ("%s(): " % (lconvfrm.func) +
							"failed to get some information to output log. " +
							"[%s]" % (logelm.halogmsg))
					else:
						errmsg = ("%s(): " % (lconvfrm.func) +
							"unknown error occurred. " +
							"[%s]" % (logelm.halogmsg))
					# When log convertion failed, output original message.
					pm_log.error(errmsg)
					outputobj.output_log(lconvfrm.loglevel, None)
			elif matched == None:
				pm_log.error("do_ptn_matching(): " +
					"pattern matching about [%s] failed." %
					(lconvfrm.rulename))
			else:
				# Not matched.
				pass
		#__for lconvfrm in lconvRuleList: (check next rule)

		# Set the time of output log message for auto reset.
		if setdate:
			self.last_logoutput_t = datetime.datetime.now()
		return

	'''
	   read the Pacemaker and Corosync log and convert it.
	'''
	def convert(self):
		global statfile
		try:
			statfile = StatusFile(self.STATFILE)
			logfile = self.get_fd(statfile)
			if logfile == None:
				if do_shutdown:
					return 0
				return 1
			cstat.ino = os.fstat(logfile.fileno()).st_ino

			while 1:
				logline = logfile.readline()
				cstat.offset = logfile.tell()

				if not logline:
					if self.is_oneshot:
						logfile.close()
						return 0

					self.check_dc_and_reset(None, None)

					if cstat.ino != statfile.w_ino or \
						cstat.offset != statfile.w_offset:
						statfile.write()

					if os.fstat(logfile.fileno()).st_size < cstat.offset:
						pm_log.warn("convert: there is possibility that " \
							"Pacemaker and Corosync log was clear.")
						pm_log.debug("convert: reset offset, since " \
							"offset[%d] > file size[%d]" % (cstat.offset,
							os.fstat(logfile.fileno()).st_size))
						logfile.seek(0)
						cstat.offset = 0
						self.funcs.clear_status()
						statfile.write()

					if os.path.exists(HA_LOGFILE) and \
						cstat.ino == os.stat(HA_LOGFILE)[ST_INO]:
						if do_shutdown:
							logfile.close()
							return 0
						time.sleep(1)
						continue
					logfile.close()

					path = self.get_nextlog(cstat.ino, statfile)
					if path == None:
						path = HA_LOGFILE
						while not os.path.exists(path):
							if do_shutdown:
								return 0
							time.sleep(1)
					pm_log.info("convert: change target[%s(inode:%d)]"
						% (path, os.stat(path)[ST_INO]))
					logfile = open(path, 'r')
					cstat.ino = os.fstat(logfile.fileno()).st_ino
				else:
					self.do_ptn_matching(logline.replace('#011', ' '))
					statfile.write()
		except Exception, strerror:
			pm_log.error("convert: error occurred.")
			pm_log.debug("convert: error occurred. [%s]" % strerror)
			return 1

	'''
		main method.
	'''
	def main(self):
		signal.alarm(0)
		pidfile = PIDFile(self.PIDFILE)

		if self.ask_status:
			ret = pidfile.read()
			if ret > 0:
				pm_log.info("status: pm_logconv is running [pid = %d]" % ret)
				return 0
			elif ret == pidfile.FILE_NOTEXIST or ret == pidfile.NOTRUNNING:
				pm_log.info("status: pm_logconv is stopped.")
				return 1
			else:
				pm_log.info("status: couldn't check status of pm_logconv.")
				return 2

		if self.stop_logconv:
			return self.logconv_stop(pidfile)

		self.make_daemon(pidfile)
		time.sleep(1)
		pm_log.info("started: pid[%d], ppid[%d], pgid[%d]"
			% (os.getpid(), os.getppid(), os.getpgrp()))
		return self.convert()

class LogElements:
	def __init__(self, procname=None, datestr=None,
		haloglevel=None, halogmsg=None):
		self.procname = procname
		self.datestr = datestr
		self.haloglevel = haloglevel
		self.halogmsg = halogmsg

	'''
		Divide ha-log message into process-name, date-string, log-level, and
		log-message.
		arg1  : a line of log message.
		return: 0   -> succeeded.
		        0 > -> error occurrs.
	'''
	def parse_logmsg(self, logline, funcs):
		SYSFMT_PROC_POS = 4
		SYSFMT_DATE_START_POS = 0
		SYSFMT_DATE_END_POS = 2 + 1
		SYSFMT_LOGLV_POS = 5

		HBFMT_PROC_POS = 0
		HBFMT_DATE_POS = 1
		HBFMT_LOGLV_POS = 2

		try:
			elementList = logline.split()
			if elementList[0].isalpha():
				# Case of syslogmsgfmt = True (default)
				pm_log.debug("parse log message as syslog format.")
				self.datestr = ' '.join(\
					elementList[SYSFMT_DATE_START_POS:SYSFMT_DATE_END_POS])
				# The following are examples of parsing:
				#     Jan  1 00:00:00 node corosync[1000]:   [MAIN  ] message
				#                          *1~~~~~~          *3~~~~~~~~~~~~~~
				#     Jan  1 00:00:00 node pengine[1000]:    info: function: message
				#                          *1~~~~~           *2~~  *3~~~~~~~~~~~~~~~
				# *1: process  (self.procname)
				# *2: loglevel (self.haloglevel)
				# *3: message  (self.halogmsg)
				self.procname = elementList[SYSFMT_PROC_POS].split('[')[0]
				if elementList[SYSFMT_LOGLV_POS][0] == "[":
					# Corosync process (corosync)
					self.haloglevel = "info"
					msgpos = SYSFMT_PROC_POS + 1
				else:
					# Pacemaker processes (pacemakerd, crmd, pengine, etc.)
					self.haloglevel = funcs.trimmark(elementList[SYSFMT_LOGLV_POS])
					msgpos = SYSFMT_LOGLV_POS + 1
				self.halogmsg = ' '.join(elementList[msgpos:]).strip()
			else:
				# Case of syslogmsgfmt = False
				pm_log.debug("parse log message as ha-log format.")
				self.procname = elementList[HBFMT_PROC_POS].split('[')[0]
				self.datestr = elementList[HBFMT_DATE_POS]
				self.haloglevel = funcs.trimmark(elementList[HBFMT_LOGLV_POS])
				msgpos = HBFMT_LOGLV_POS + 1
				self.halogmsg = ' '.join(elementList[msgpos:])

			return 0
		except Exception, strerror:
			pm_log.debug("parse_logmsg(): %s" % (strerror))
			return -1

	'''
		Only for debug.
	'''
	def print_logelements(self):
		print self.procname
		print self.datestr
		print self.haloglevel
		print self.halogmsg

'''
	Class for output converted log message.
'''
class OutputConvertedLog:
	def __init__(self, datestr=None, loglevel=None, logmsg=None):
		self.datestr = datestr
		self.loglevel = loglevel
		self.logmsg = logmsg
		self.monthnumDic = {
			'01':'Jan',
			'02':'Feb',
			'03':'Mar',
			'04':'Apr',
			'05':'May',
			'06':'Jun',
			'07':'Jul',
			'08':'Aug',
			'09':'Sep',
			'10':'Oct',
			'11':'Nov',
			'12':'Dec'
		}
		self.monthstrDic = {
			'Jan':'01',
			'Feb':'02',
			'Mar':'03',
			'Apr':'04',
			'May':'05',
			'Jun':'06',
			'Jul':'07',
			'Aug':'08',
			'Sep':'09',
			'Oct':'10',
			'Nov':'11',
			'Dec':'12'
		}

	def set_datestr(self, datestr):
		if SYSLOGFORMAT:
			tmp_datestr = self.to_syslog_dateformat(datestr)
		else:
			tmp_datestr = self.to_halog_dateformat(datestr)

		if tmp_datestr != None:
			self.datestr = tmp_datestr
		else:
			pm_log.error("set_datestr(): " +
				"invalid date format. [%s] " % (datestr) +
				"output in original format.")
			self.datestr = datestr

	def set_orgloglevel(self, loglevel):
		self.orgloglevel = loglevel

	def set_orglogmsg(self, logmsg):
		self.orglogmsg = logmsg

	'''
		Output log message.
		loglevel and log message is variable, but date is not
		(output original log's date).
		arg1  : loglevel string.
		arg2  : log message
		return: 0   -> succeeded.
		        0 > -> error occurrs.
	'''
	def output_log(self, convloglevel, convlogmsg):
		output_loglevel = self.orgloglevel
		if convloglevel != None:
			output_loglevel = convloglevel
		output_logmsg = self.orglogmsg
		if convlogmsg != None:
			output_logmsg = convlogmsg

		try:
			outputstr = ("%s %s %7s: %s" %
				(self.datestr, HOSTNAME, output_loglevel, output_logmsg))
			f = open(OUTPUTFILE, 'a')
			f.write("%s\n" % (outputstr))
			f.close()
		except Exception, strerror:
			pm_log.error("output_log(): " +
				"failed to output converted log message. [%s]" %
				(outputstr))
			pm_log.debug("output_log(): %s" % (strerror))
			return -1
		return 0

	'''
		Convert dateformat form ha-log format to syslog format.
		"2009/01/01_00:00:00" -> "Jan 1 00:00:00"
		arg1   : date string of ha-log format.
		return : date string which is converted to syslog format.
		         None -> error occurs.
	'''
	def to_syslog_dateformat(self, orgdatestr):
		DATE_POS = 0  #YYYY/MM/DD
		TIME_POS = 1  #hh:mm:ss
		MONTH_POS = 1 #MM
		DAY_POS = 2   #DD

		if orgdatestr.split()[0].isalpha():
			pm_log.debug("It seems already syslog date format.")
			return orgdatestr

		try:
			datestr = orgdatestr.split('_')[DATE_POS].strip()
			timestr = orgdatestr.split('_')[TIME_POS].strip()
			if datestr == "" or timestr == "":
				return None

			monthstr = datestr.split('/')[MONTH_POS].strip()
			daystr = datestr.split('/')[DAY_POS].strip().lstrip('0')
			if monthstr == "" or daystr == "":
				return None
			if monthstr in self.monthnumDic == False:
				return None
			monthstr = self.monthnumDic[monthstr]
			syslog_datestr = ("%s %s %s" % (monthstr, daystr, timestr))
			return syslog_datestr
		except Exception, strerror:
			pm_log.debug("to_syslog_dateformat(): %s" % (strerror))
			return None

	'''
		Convert dateformat form syslog format to ha-log format.
		"Jan 1 00:00:00" -> "2009/01/01_00:00:00"
		arg1   : date string of syslog format.
		return : date string which is converted to ha-log original format.
		         None -> error occurs.
	'''
	def to_halog_dateformat(self, orgdatestr):
		MONTH_POS = 0
		DAY_POS = 1
		TIME_POS = 2

		strList = orgdatestr.split()
		if strList[0].isalpha() == False:
			pm_log.debug("It seems already ha-log date format.")
			return orgdatestr
		try:
			monthstr = strList[MONTH_POS].strip()
			daystr = strList[DAY_POS].strip()
			timestr = strList[TIME_POS].strip()
			if monthstr == "" or daystr == "" or timestr == "":
				return None
			if monthstr in self.monthstrDic == False:
				return None
			monthstr = self.monthstrDic[monthstr]
			now = datetime.datetime.now()
			yearstr = str(now.timetuple().tm_year)
			hblog_datestr = ("%s/%s/%02d_%s" %
				(yearstr, monthstr, int(daystr), timestr))

			# If date string is future, minus year value.
			hblog_date = datetime.datetime(\
				*time.strptime(hblog_datestr, "%Y/%m/%d_%H:%M:%S")[0:6])
			if hblog_date > now:
				year = int(yearstr) - 1
				hblog_datestr = hblog_datestr.replace(yearstr, str(year), 1)

			return hblog_datestr
		except Exception, strerror:
			pm_log.debug("to_halog_dateformat(): %s" % (strerror))
			return None

'''
	Class to hold resource status in F/O process.
'''
class RscStat:
		'''
			rscid    : resource id.
			status   : [Started on node|Stopped|Move node -> node]
			unmanaged: True  -> resource is unmanaged.
			           False -> resource is managed.
			operated : True  -> resource is operated.
			           False -> resource isn't operated.
		'''
		def __init__(self, rscid=None, status=None, unmanaged=False, operated=False):
			self.rscid = rscid
			self.status = status
			self.unmanaged = unmanaged
			self.operated = operated

		'''	operator eq	'''
		def __eq__(self,other):
			return (self.rscid == other.rscid)

		'''	replace status and flags'''
		def replace(self,new):
			if new.status:
				self.status = new.status
			if new.unmanaged:
				self.unmanaged = new.unmanaged
			if new.operated:
				self.operated = new.operated

		'''
			Only for debug.
		'''
		def print_rscstat(self):
			print "rsc:%s\tstatus:%s\tunmanaged:%s\toperated:%s" % (self.rscid,self.status,self.unmanaged,self.operated)

'''
	Return codes for functions to convert log.
'''
CONV_OK				=  0	#log conversion succeeded.
CONV_PARSE_ERROR	= -1	#failed to parse log message.
CONV_ITEM_EMPTY		= -2	#parsing succeeded, but some gotten items are empty.
CONV_GETINFO_ERROR	= -3	#failed to get info which is required to conversion.
'''
	Class for functions to convert log message.
	convert-functions' arguments are:
	  arg1: outputobj -> object for output converted log.
	  arg2: logelm    -> elements which constructs target log. date, msg etc.
	  arg3: lconvfrm  -> info for conversion. loglevel, F/Otrigger etc.
	return codes are:
	  [CONV_OK|CONV_PARSE_ERROR|CONV_ITEM_EMPTY|CONV_GETINFO_ERROR]
	  See the head of this file.
'''
class LogConvertFuncs:
	LOG_ERR_LV   = "error"
	LOG_WARN_LV  = "warning"
	LOG_INFO_LV  = "info"
	LOG_DEBUG_LV = "debug"

	def __init__(self, rscstatList=None):
		# This list is used only in F/O process.
		# If hg_logconv exits abnormally during parsing F/O process's log,
		# read from start of F/O, so it doesn't need to output status file.
		self.rscstatList = rscstatList
		self.rscstatList = list()

	'''
		Check Corosync service is active or dead.
		return: True  -> active
				False -> dead
				None  -> error occurs.
	'''
	def is_corosync(self):
		# Get DC node name.
		status = self.exec_outside_cmd("service", "corosync status", False)[0]
		if status == None:
			# Failed to exec command.
			pm_log.warn("is_corosync(): failed to get status.")
			return None
		if status != 0:
			# Maybe during DC election.
			return False
		return True

	'''
		triming mark from value.
	'''
	def trimmark(self, word, minus=None, plus=None):
		marklist = "(),.;:[]=<>'"
		if minus:
			markset = set(marklist) - set(minus)
			marklist = "".join(markset)
		if plus:
			marklist = marklist + plus
		trimword = word.translate(string.maketrans("",""),marklist)
		return trimword

	'''
		Check specified strings are empty or not.
		arg*   : target strings.
		return : True  -> there is at least an empty string
		                  in specified strings.
		         False -> there is no empty string in specified strings.
	'''
	def is_empty(self, *args):
		for arg in args:
			if arg == "":
				return True
		return False

	'''
		Parse operation id (resourceid_opname_interval)
		arg1   : operationid
		return : resourceid, opname, interval
	'''
	def parse_opid(self, opid):
		# please detect parse error in caller.
		tmp = opid.split('_')
		if tmp[-2] in ['to','from'] and tmp[-3] == 'migrate':
			rscid = '_'.join(tmp[:-3])
			op = '_'.join(tmp[-3:-1])
		else:
			rscid = '_'.join(tmp[:-2])
			op = tmp[-2]
		interval = tmp[-1]
		return rscid, op, interval

	'''
		Execute commandline command.
		arg1   : command name to execute.
		arg2   : command options.
		arg3   : check return code or not.
		return : [status, output]
		           status -> exit status.
		           output -> output strings of the command.
		         None -> error occurs.
	'''
	def exec_outside_cmd(self, cmdname, options, checkrc):
		# Get full path of specified command.
		try:
			status, cmdpath = \
				commands.getstatusoutput("which " + cmdname)
		except Exception, strerror:
			pm_log.error("exec_outside_cmd(): " +
				"failed to execute which command to get command path. " +
				"[%s]" % (cmdname))
			pm_log.debug("exec_outside_cmd(): %s" % (strerror))
			return None, None
		if (os.WIFEXITED(status) == False or os.WEXITSTATUS(status) != 0):
			pm_log.error("exec_outside_cmd(): " +
				"failed to get command path. [%s]" % (cmdname))
			return None, None

		# Check whether it is able to execute the command.
		if os.access(cmdpath, os.F_OK | os.X_OK) == False:
			return None, None

		# Execute command.
		exec_cmd = ("%s %s" % (cmdpath, options))
		pm_log.debug("exec_outside_cmd(): " +
			"execute command. [%s]" % (exec_cmd))
		try:
			status, output = commands.getstatusoutput(exec_cmd)
		except Exception, strerror:
			pm_log.error("exec_outside_cmd(): " +
				"failed to exec command. [%s]" % (exec_cmd))
			pm_log.debug("exec_outside_cmd(): %s" % (strerror))
			return None, None

		# Check return status.
		if os.WIFEXITED(status) == False:
			pm_log.error("exec_outside_cmd(): " +
				"command [%s] exited abnormally. (status=%s)" %
				(exec_cmd, status))
			return None, None
		rc = os.WEXITSTATUS(status)
		if checkrc == True and rc != 0:
			pm_log.warn("exec_outside_cmd(): " +
				"command [%s] returns error. (rc=%s, msg=\"%s\")" %
				(exec_cmd, rc, output))
			return None, None
		return rc, output

	'''
		Compare specified attribute's value with specified value.
		Operations to compare is [lt|gt|le|ge|eq|ne].
		arg1   : target attribute name.
		arg2   : operation to compare.
		arg3   : the value to compare with current attribute value.
		arg4   : node name which has the attribute.
		return : (result_of_comparision, current_attr_val)
		         result_of_comparision:
		           True  -> matched.
		           False -> not matched.
		           None  -> error occurs or attribute doesn't exist.
	'''
	def check_attribute(self, attrname, op, attrval, node):
		if not (node, attrname) in cstat.attrDict:
			return None, None
		# Get attribute value from log.
		currentval = cstat.attrDict[node, attrname]
		pm_log.debug("check_attribute(): log's node[%s] attr[%s] value[%s]" %
			(node, attrname, currentval))

		try:
			if currentval.isdigit() and attrval.isdigit():
				result = getattr(operator, op)(int(currentval),int(attrval))
			else:
				result = getattr(operator, op)(currentval,attrval)
		except:
			pm_log.error("check_attribute(): " +
				"failed to comparison %s's value. " % (attrname) +
				"(currentval=%s, op=%s, specifiedval=%s)" %
				(currentval, op, attrval))
			return None, None
		return result, currentval

	'''
		Compare attribute value with it that acquired from CIB or log message.
		Operations to compare is [lt|gt|le|ge|eq|ne].
		arg1   : list of target attributes ([[name, op, value], bool_op, [...] ...])
		arg2   : node name which has the attribute.
		return : result of comparision:
		           True  -> matched.
		           False -> not matched.
		           None  -> error occurs or attribute doesn't exist.
	'''
	def check_attributes(self, rules, node):
		def operate(rules, i, op):
			if rules[i-1] == None:
				pass
			elif rules[i+1] == None:
				rules[i+1] = rules[i-1]
			else:
				rules[i+1] = getattr(operator,op)(rules[i-1],rules[i+1])
			rules[i-1] = rules[i] = ''

		pm_log.debug("check_attributes(): node[%s] rules%s"%(node,rules))
		attrs = {} # current attribute values
		for i,rule in [(i,x) for (i,x) in enumerate(rules) if i % 2 == 0]:
			if not rule[0] or rule[0] in attrs:
				continue
			if (node, rule[0]) in cstat.attrDict:
				# Get attribute value from log.
				attrs[rule[0]] = cstat.attrDict[node, rule[0]]
				pm_log.debug("check_attributes(): log's node[%s] attr[%s] value[%s]" %
					(node, rule[0], attrs[rule[0]]))

		if len(attrs) < 1:
			return None
		pm_log.debug("check_attributes(): attrs%s"%(attrs))

		# phase1: Operate each condition of the attribute.
		#
		#     [[None, 'not_defined', 'attribute'], 'and', ['attribute', 'lt', '100']]
		#      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^         ~~~~~~~~~~~~~~~~~~~~~~~~~~
		#  -> [None,                               'and', True]
		#      ^^^^                                       ~~~~
		#     * 'defined' and 'not_defined' are made None unconditionally.
		#
		for i,rule in [(i,x) for (i,x) in enumerate(rules) if i % 2 == 0]:
			if not rule[0]: # unary_op
				rules[i] = None
				continue
			v = attrs[rule[0]] # current value
			try:
				if v.isdigit() and rule[2].isdigit():
					rules[i] = getattr(operator,rule[1])(int(v),int(rule[2]))
				else:
					rules[i] = getattr(operator,rule[1])(v,rule[2])
				pm_log.debug("check_attributes(): phase1(%d): (%s %s %s)=%s"
					%(i,v,rule[1],rule[2],rules[i]))
			except:
				pm_log.error("check_attributes(): "
					"failed to comparison %s's value. "%(rule[0]) +
					"(currentval=%s, op=%s, specifiedval=%s)"
					%(v,rule[1],rule[2]))
				return None
		pm_log.debug("check_attributes(): phase1: rules%s"%(rules))

		# phase2: Operate each 'and' condition.
		#
		#     [True, 'or', True, 'and', False, 'and', True]
		#                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
		#  -> [True, 'or', False]
		#                  ^^^^^
		#     * [None, 'and', True] is True, [None 'and', False] is False,
		#     * and [None, 'and', None] is None.
		#
		for i in [i for (i,x) in enumerate(rules) if i % 2 == 1 and x == 'and']:
			operate(rules, i, 'and_')
			pm_log.debug("check_attributes(): phase2(%d): rules%s"%(i,rules))
		l = rules[:]; rules = []
		for x in [x for x in l if x != '']:
			rules.append(x)
		pm_log.debug("check_attributes(): phase2: rules%s"%(rules))

		# phase3: Operate each 'or' condition.
		#
		#     [True, 'or', False]
		#      ^^^^^^^^^^^^^^^^^
		#  -> [True]
		#      ^^^^
		#     * [None, 'or', True] is True, [None 'or', False] is False,
		#     * and [None, 'or', None] is None.
		#
		for i in [i for (i,x) in enumerate(rules) if i % 2 == 1 and x == 'or']:
			operate(rules, i, 'or_')
			pm_log.debug("check_attributes(): phase3(%d): rules%s"%(i,rules))
		pm_log.debug("check_attributes(): phase3: rules[%s]"%(rules[-1]))
		return rules[-1]

	'''
		Check unmatched attribute exists or not.
		Compared with the attribute's rule of configure file.
		return : True  -> unmatched attribute exists.
		         False -> unmatched attribute not exists.
	'''
	def check_unmatch_attr_rule(self):
		if \
			(len(cstat.attrDict) == 0) or \
			(len(attrRuleList) == 0 and len(attrRules) == 0):
			return False

		for node, stat in cstat.nodeDict.iteritems():
			if stat != "online":
				continue
			# Check each attribute's value.
			for attrRule in attrRuleList:
				attrname, op, attrval = tuple(attrRule)
				# Check attribute's value for each node.
				# Now, the node seems to be active.
				result = self.check_attribute(attrname, op, attrval, node)[0]
				pm_log.debug("check_unmatch_attr_rule(): "
					"check_attribute returns [%s]"%(result))
				if result:
					# attribute's value means "failure(s) occurred"!
					return True
					# [COMMENT]
					# result == False:
					#   attribute did not change or
					#   it was updated to normal value.
					# result == None:
					#  some errors occurred in check_attribute() or
					#  the node is not running or
					#  specified attribute does not exist.
			for rules in attrRules:
				result = self.check_attributes(rules[:], node)
				pm_log.debug("check_unmatch_attr_rule(): "
					"check_attributes returns [%s]"%(result))
				if result:
					return True
		return False

	'''
		Set specified values to RscStat object list.
		If the same rscid is already in the list, update the elements' value.
		If not, append the new RscStat object to the list.
		When the arg's value is None, don't update the element's value.

		arg1 : resource id.
		arg2 : the rsc's status. [Started on node|Stopped|Move node -> node]
		arg3 : the rsc is managed or not.
		arg4 : the rsc is operated or not.
		return Nothing.
	'''
	def set_rscstat(self, rscid, statstr, unmanaged, operated):
		newrsc = RscStat(rscid, statstr, unmanaged, operated)
		if newrsc in self.rscstatList:
			idx = self.rscstatList.index(newrsc)
			self.rscstatList[idx].replace(newrsc)
		else:
			self.rscstatList.append(newrsc)

	'''
		Debug print for ConvertStatus (exclude ino and offset).
	'''
	def debug_status(self):
		pm_log.debug("debug_status(): FAIL[%s], IN_CALC[%s], "\
			"RSC_MOVE[%s], IN_FO[%s], attrDict%s, nodeDict%s" %
			(cstat.FAILURE_OCCURRED, cstat.IN_CALC,
			cstat.ACTRSC_MOVE, cstat.IN_FO_PROCESS,
			dict(cstat.attrDict), dict(cstat.nodeDict)))

	'''
		Clear ConvertStatus (exclude ino and offset).
	'''
	def clear_status(self):
		pm_log.debug("clear_status():" +
			"clear convert status (exclude ino and offset).")
		self.debug_status()
		cstat.FAILURE_OCCURRED = False
		cstat.IN_CALC = False
		cstat.ACTRSC_MOVE = False
		cstat.IN_FO_PROCESS = False
		cstat.attrDict = dict()
		cstat.nodeDict = dict()
		self.debug_status()

	'''
		Check ConvertStatus(exclude ino and offset) is initial value or not.
		return : True  -> initial value
		         False -> not initial value
	'''
	def is_init_status(self):
		if \
			cstat.FAILURE_OCCURRED      == False and \
			cstat.IN_CALC               == False and \
			cstat.ACTRSC_MOVE           == False and \
			cstat.IN_FO_PROCESS         == False and \
			len(cstat.attrDict)         == 0     and \
			len(cstat.nodeDict)         == 0:
			return True
		return False

	##########
	# General-purpose functions.
	##########
	'''
		Output original ha-log message.
	'''
	def output_original_log(self, outputobj, logelm, lconvfrm):
		# Output original log message
		outputobj.output_log(lconvfrm.loglevel, None)
		return CONV_OK

	'''
		Output static message.
		This function just outputs section name.
	'''
	def output_static_msg(self, outputobj, logelm, lconvfrm):
		# Output rulename (= section name).
		outputobj.output_log(lconvfrm.loglevel, lconvfrm.rulename)
		return CONV_OK

	'''
		No output message.
	'''
	def no_output_msg(self, outputobj, logelm, lconvfrm):
		return CONV_OK

	##########
	# For Resource event.
	##########
	'''
		Convert log message which means HB tries to operate.
		This function is common for OCF resource's start, stop, promote, demote
		and STONITH resource's start, stop.
		NOTE: monitor operation is not a target.

		MsgNo.1-1)
			Jan  1 00:00:00 node01 crmd[777]:     info: do_lrm_rsc_op: 
			Performing key=11:1:0:00000000-0000-0000-0000-000000000000
			op=prmRSC_start_0
		MsgNo.2-1)
			Jan  1 00:00:00 node01 crmd[777]:     info: do_lrm_rsc_op: 
			Performing key=11:1:0:00000000-0000-0000-0000-000000000000
			op=prmRSC_stop_0
		MsgNo.4-1)
			Jan  1 00:00:00 node01 crmd[777]:     info: do_lrm_rsc_op: 
			Performing key=11:1:0:00000000-0000-0000-0000-000000000000
			op=prmRSC_promote_0
		MsgNo.5-1)
			Jan  1 00:00:00 node01 crmd[777]:     info: do_lrm_rsc_op: 
			Performing key=11:1:0:00000000-0000-0000-0000-000000000000
			op=prmRSC_demote_0
		MsgNo.11-1)
			Jan  1 00:00:00 node01 crmd[777]:     info: do_lrm_rsc_op: 
			Performing key=11:1:0:00000000-0000-0000-0000-000000000000
			op=prmRSC_migrate_to_0
		MsgNo.12-1)
			Jan  1 00:00:00 node01 crmd[777]:     info: do_lrm_rsc_op: 
			Performing key=11:1:0:00000000-0000-0000-0000-000000000000
			op=prmRSC_migrate_from_0
		MsgNo.17-1)
			Jan  1 00:00:00 node01 crmd[777]:     info: do_lrm_rsc_op: 
			Performing key=11:1:0:00000000-0000-0000-0000-000000000000
			op=prmStonith1_start_0
		MsgNo.18-1)
			Jan  1 00:00:00 node01 crmd[777]:     info: do_lrm_rsc_op: 
			Performing key=11:1:0:00000000-0000-0000-0000-000000000000
			op=prmStonith1_stop_0
	'''
	def try_to_operate(self, outputobj, logelm, lconvfrm):
		try:
			# In the case of example above, tmp's value is
			# "op=master_slave_Stateful0:1_promote_0".
			tmp = logelm.halogmsg.split()[3]
			# remove "op=" at the head.
			opid = tmp[3:]
			rscid, op = self.parse_opid(opid)[:2]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(rscid, op):
			return CONV_ITEM_EMPTY

		convertedlog = ("Resource %s tries to %s." % (rscid, op))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	'''
		Convert log message which means HB succeeded in operation.
		This function is common for OCF resource's start, stop, promote, demote
		and STONITH resource's start, stop.
		NOTE: monitor operation is not a target.

		MsgNo.1-2)
			Jan  1 00:00:00 node01 crmd[777]:   notice: process_lrm_event: 
			LRM operation prmRSC_start_0 (call=168, rc=0, 
			cib-update=67, confirmed=true) ok
		MsgNo.2-2)
			Jan  1 00:00:00 node01 crmd[777]:   notice: process_lrm_event: 
			LRM operation prmRSC_stop_0 (call=168, rc=0, 
			cib-update=67, confirmed=true) ok
		MsgNo.4-2)
			Jan  1 00:00:00 node01 crmd[777]:   notice: process_lrm_event: 
			LRM operation prmRSC_promote_0 (call=132, rc=0, 
			cib-update=54, confirmed=true) ok
		MsgNo.5-2)
			Jan  1 00:00:00 node01 crmd[777]:   notice: process_lrm_event: 
			LRM operation prmRSC_demote_0 (call=132, rc=0, 
			cib-update=54, confirmed=true) ok
		MsgNo.11-2)
			Jan  1 00:00:00 node01 crmd[777]:   notice: process_lrm_event: 
			LRM operation prmRSC_migrate_to_0 (call=215, rc=0, 
			cib-update=100, confirmed=true) ok
		MsgNo.12-2)
			Jan  1 00:00:00 node01 crmd[777]:   notice: process_lrm_event: 
			LRM operation prmRSC_migrate_from_0 (call=215, rc=0, 
			cib-update=100, confirmed=true) ok
		MsgNo.17-2)
			Jan  1 00:00:00 node01 crmd[777]:   notice: process_lrm_event: 
			LRM operation prmStonith1_start_0 (call=168, rc=0, 
			cib-update=67, confirmed=true) ok
		MsgNo.18-2)
			Jan  1 00:00:00 node01 crmd[777]:   notice: process_lrm_event: 
			LRM operation prmStonith1_stop_0 (call=168, rc=0, 
			cib-update=67, confirmed=true) ok
	'''
	def operation_succeeded(self, outputobj, logelm, lconvfrm):
		completeopDic = {
			'start'  : 'started',
			'stop'   : 'stopped',
			'promote': 'promoted',
			'demote' : 'demoted',
			'migrate_to' : 'migrated_to',
			'migrate_from' : 'migrated_from'
		}
		try:
			wordlist = logelm.halogmsg.split()
			rscid, op = self.parse_opid(wordlist[2])[:2]
			rcstr = self.trimmark(wordlist[6],"=")
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(rscid, op, rcstr):
			return CONV_ITEM_EMPTY

		if op in completeopDic.keys():
			opstr = completeopDic[op]
		else:
			#Just in case. It shuoldn't occur unless cf file is modified.
			opstr = ("%s ok" % (op))
		convertedlog = ("Resource %s %s. (%s)" % (rscid, opstr, rcstr))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	'''
		Convert log message which means HB failed to do the operation.
		This function is common for OCF resource's start, stop,
		monitor (exclude rc=OCF_NOT_RUNNING), promote, demote,
		and STONITH resource's start, stop.
		MsgNo.1-3)
			Jan  1 00:00:00 node01 crmd[777]:   notice: process_lrm_event: 
			LRM operation prmRSC_start_0 (call=254, rc=1, 
			cib-update=107, confirmed=true) unknown error
		MsgNo.2-3)
			Jan  1 00:00:00 node01 crmd[777]:   notice: process_lrm_event: 
			LRM operation prmRSC_stop_0 (call=254, rc=1, 
			cib-update=107, confirmed=true) unknown error
		MsgNo.3-1)
			Jan  1 00:00:00 node01 crmd[777]:   notice: process_lrm_event: 
			LRM operation prmRSC_monitor_0 (call=254, rc=1, 
			cib-update=107, confirmed=true) unknown error
		MsgNo.4-3)
			Jan  1 00:00:00 node01 crmd[777]:   notice: process_lrm_event: 
			LRM operation prmRSC_promote_0 (call=254, rc=1, 
			cib-update=107, confirmed=true) unknown error
		MsgNo.5-3)
			Jan  1 00:00:00 node01 crmd[777]:   notice: process_lrm_event: 
			LRM operation prmRSC_demote_0 (call=254, rc=1, 
			cib-update=107, confirmed=true) unknown error
		MsgNo.11-3)
			Jan  1 00:00:00 node01 crmd[777]:   notice: process_lrm_event: 
			LRM operation prmRSC_mitrate_to_0 (call=254, rc=1, 
			cib-update=107, confirmed=true) unknown error
		MsgNo.12-3)
			Jan  1 00:00:00 node01 crmd[777]:   notice: process_lrm_event: 
			LRM operation prmRSC_mitrate_from_0 (call=254, rc=1, 
			cib-update=107, confirmed=true) unknown error
		MsgNo.17-3)
			Jan  1 00:00:00 node01 crmd[777]:    error: process_lrm_event: 
			LRM operation prmStonith1_start_0 (call=145, status=4, 
			cib-update=127, confirmed=true) Error
		MsgNo.19-1)
			Jan  1 00:00:00 node01 crmd[777]:    error: process_lrm_event: 
			LRM operation prmStonith1_monitor_10000 (call=130, status=4, 
			cib-update=79, confirmed=false) Error
	'''
	def operation_failed(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			rscid, op = self.parse_opid(wordlist[2])[:2]
			idx = logelm.halogmsg.find("rc=")
			if idx == -1:
				idx = logelm.halogmsg.find("status=")
			if idx == -1:
				return CONV_PARSE_ERROR
			rcstr = self.trimmark(logelm.halogmsg[idx:].split(',')[0],"=")
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(rscid, op, rcstr):
			return CONV_ITEM_EMPTY

		convertedlog = ("Resource %s failed to %s. (%s)" % (rscid, op, rcstr))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	'''
		Convert log message which means operation for OCF resource timed out.
		This function is common for start, stop, monitor, promote, demote.
		MsgNo.1-4)
			Jan  1 00:00:00 node01 crmd[777]:    error: process_lrm_event: 
			LRM operation prmRSC_start_0 (77) Timed Out (timeout=10000ms)
		MsgNo.2-4)
			Jan  1 00:00:00 node01 crmd[777]:    error: process_lrm_event: 
			LRM operation prmRSC_stop_0 (77) Timed Out (timeout=10000ms)
		MsgNo.3-3)
			Jan  1 00:00:00 node01 crmd[777]:    error: process_lrm_event: 
			LRM operation prmRSC_monitor_10000 (77) Timed Out (timeout=10000ms)
		MsgNo.4-4)
			Jan  1 00:00:00 node01 crmd[777]:    error: process_lrm_event: 
			LRM operation prmRSC_promote_0 (77) Timed Out (timeout=10000ms)
		MsgNo.5-4)
			Jan  1 00:00:00 node01 crmd[777]:    error: process_lrm_event: 
			LRM operation prmRSC_demote_0 (77) Timed Out (timeout=10000ms)
		MsgNo.11-4)
			Jan  1 00:00:00 node01 crmd[777]:    error: process_lrm_event: 
			LRM operation prmRSC_migrate_to_0 (77) Timed Out (timeout=10000ms)
		MsgNo.12-4)
			Jan  1 00:00:00 node01 crmd[777]:    error: process_lrm_event: 
			LRM operation prmRSC_migrate_from_0 (77) Timed Out (timeout=10000ms)
	'''
	def operation_timedout_ocf(self, outputobj, logelm, lconvfrm):
		try:
			opid = logelm.halogmsg.split()[2]
			rscid, op = self.parse_opid(opid)[:2]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(rscid, op):
			return CONV_ITEM_EMPTY

		# remove from timed out rscop list.
		# Because it became clear that the operation timed out.
		rscid_and_op = ("%s:%s" % (rscid, op))

		convertedlog = ("Resource %s failed to %s. (Timed Out)" % (rscid, op))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	'''
		Convert log message which means resource is not running.
		This function is only for OCF resource's monitor
		(rc=OCF_NOT_RUNNING).

		MsgNo.3-2)
			Jan  1 00:00:00 node01 crmd[777]:   notice: process_lrm_event: 
			LRM operation prmRSC_monitor_10000 (call=270, rc=7, 
			cib-update=118, confirmed=false) not running
	'''
	def detect_rsc_failure(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			rscid = self.parse_opid(wordlist[2])[0]
			rcstr = self.trimmark(wordlist[7],"=")
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(rscid, rcstr):
			return CONV_ITEM_EMPTY

		convertedlog = ("Resource %s does not work. (%s)" % (rscid, rcstr))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	#########
	# For Node status event.
	#########
	'''
		Convert log message which means Node status updated.

		MsgNo.6-1)
			Jan  1 00:00:00 node01 crmd[777]:     info: peer_update_callback: 
			node02 is now lost (was member)
		MsgNo.6-2)
			Jan  1 00:00:00 node01 crmd[777]:     info: peer_update_callback: 
			node02 is now member
	'''
	def node_status_updated(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			nodename = wordlist[1]
			status = wordlist[4]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(nodename, status):
			return CONV_ITEM_EMPTY

		# It's node status's change.
		output_loglevel = self.LOG_INFO_LV
		if status == "lost":
			output_loglevel = self.LOG_WARN_LV

		convertedlog = ("Node %s is %s" % (nodename, status))
		outputobj.output_log(output_loglevel, convertedlog)
		return CONV_OK

	'''
		Determine Node status.
		So it outputs nothing.

		MsgNo. 6-3)
			Jan  1 00:00:00 node01 crmd[777]:     info: 
			determine_online_status: Node node01 is online
	'''
	def node_status_determined(self, outputobj, logelm, lconvfrm):
		try:
			nodename = logelm.halogmsg.split()[2]
			nodestat = logelm.halogmsg.split()[4]
		except:
			return CONV_PARSE_ERROR

		if self.is_empty(nodename, nodestat):
			return CONV_ITEM_EMPTY

		if nodestat == "online":
			cstat.nodeDict[nodename] = "online"
		else:
			cstat.nodeDict[nodename] = None

		return CONV_OK

	##########
	# For Interconnect-LAN status event and
	# Network status event (detected by pingd).
	##########
	'''
		Convert log message which means Interconnect-LAN status changed to "dead"

		MsgNo.7-1)
			Jan  1 00:00:00 node01 corosync[777]:  [TOTEM ] Marking seqid 53645 
			ringid 0 interface 192.168.101.1 FAULTY
	'''
	def detect_iconnlan_dead(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			idx = wordlist.index("interface") + 1
			interface_ip = wordlist[idx]
			idx = wordlist.index("ringid") + 1
			ring_no = wordlist[idx]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(interface_ip, ring_no):
			return CONV_ITEM_EMPTY

		convertedlog = ("Ring number %s is FAULTY (interface %s)." % (ring_no, interface_ip))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	'''
		Convert log message which means Interconnect-LAN status changed to "recovered"

		MsgNo.7-2)
			Jan  1 00:00:00 node01 corosync[777]: [TOTEM ] Automatically recovered ring 0
	'''
	def detect_iconnlan_recover(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			idx = wordlist.index("ring") + 1
			ring_no = wordlist[idx]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(ring_no):
			return CONV_ITEM_EMPTY

		convertedlog = ("Ring number %s is recovered." % (ring_no))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	'''
		Convert log message which means Network to ping node status changed
		to "dead"
		See also the comment on detect_iconnlan_dead().

		MsgNo.8-1)
			Jan  1 00:00:00 node01 ping(prmPing)[777]: WARNING: 
			192.168.201.254 is inactive: PING 192.168.201.254 (192.168.201.254) 
			56(84) bytes of data.
	'''
	def detect_node_dead(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			idx = wordlist.index("is") - 1
			nodename = wordlist[idx]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(nodename):
			return CONV_ITEM_EMPTY

		convertedlog = ("Network to %s is unreachable." % (nodename))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	##########
	# For Disk status event (detected by diskd).
	##########
	'''
		Convert log message which means disk error.

		MsgNo.9-1)
			Jan  1 00:00:00 node01 diskd[777]:  warning: check_status: 
			disk status is changed, attr_name=diskcheck_status, 
			target=/dev/mapper/lun1, new_status=ERROR
	'''
	def detect_disk_error(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split(',')
			attrname = wordlist[1].split('=')[1]
			target = wordlist[2].split('=')[1]
			status = wordlist[3].split('=')[1]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(attrname, target, status):
			return CONV_ITEM_EMPTY

		convertedlog = ("Disk connection to %s is %s. (attr_name=%s)" % (target, status, attrname))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	#########
	# For respawn process event.
	#########
	'''
		Convert log message which means respawn process start.

		MsgNo.10-1)
			Jan  1 00:00:00 node01 pacemakerd[777]:     info: start_child: 
			Forked child 888 for process cib
	'''
	def respawn_start(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			procname = wordlist[-1]
			pid = wordlist[-4]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(procname, pid):
			return CONV_ITEM_EMPTY

		convertedlog = ("Start \"%s\" process. (pid=%s)" % (procname, pid))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	'''
		Convert log message which means respawn process exited with error.

		MsgNo.10-2)
			Jan  1 00:00:00 node01 pacemakerd[777]:    error: pcmk_child_exit: 
			Child process crmd (888) exited: Generic Pacemaker error (201)
	'''
	def respawn_exited_abnormally(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			procname = wordlist[wordlist.index("process") + 1]
			pid = self.trimmark(wordlist[wordlist.index("process") + 2])
			exitcode = self.trimmark(wordlist[-1])
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(procname, pid, exitcode):
			return CONV_ITEM_EMPTY

		convertedlog = ("Managed \"%s\" process exited. (pid=%s, rc=%s)" % (procname, pid, exitcode))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	'''
		Convert log message which means respawn process killed by signal.

		MsgNo.10-3)
			Jan  1 00:00:00 node01 pacemakerd[777]:   notice: pcmk_child_exit: 
			Child process cib terminated with signal 9 (pid=888, core=0)
	'''
	def respawn_killed(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			procname = wordlist[-7]
			signum = wordlist[-3]
			pid = self.trimmark(wordlist[-2],"=").split("=")[1]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(procname, pid, signum):
			return CONV_ITEM_EMPTY

		convertedlog = ("Managed \"%s\" process terminated with signal %s. (pid=%s)" % (procname, signum, pid))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	'''
		Convert log message which means respawn process exited normally in shutdown process.

		MsgNo.10-6)
			Jan  1 00:00:00 node01 pacemakerd[777]:     info: 
			pcmk_child_exit: Child process cib (888) exited: OK (0)
	'''
	def respawn_exited_normally(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			procname = wordlist[wordlist.index("process") + 1]
			pid = self.trimmark(wordlist[wordlist.index("process") + 2])
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(procname, pid):
			return CONV_ITEM_EMPTY

		convertedlog = ("Stop \"%s\" process normally. (pid=%s)" % (procname, pid))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	'''
		Convert log message which means do respawning too frequently in a short term.

		MsgNo.10-7)
			Jan  1 00:00:00 node01 pacemakerd[777]:    error: 
			pcmk_process_exit: Child respawn count exceeded by cib
	'''
	def respawn_too_fast(self, outputobj, logelm, lconvfrm):
		try:
			procname = logelm.halogmsg.split()[-1]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(procname):
			return CONV_ITEM_EMPTY

		convertedlog = ("Respawn count exceeded by \"%s\"." % (procname))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	##########
	# For Fail Over.
	##########
	'''
		Output the log which tells F/O starts.
	'''
	def detect_fo_start(self, outputobj):
		self.debug_status()
		if cstat.IN_FO_PROCESS == True:
			return
		cstat.IN_FO_PROCESS = True
		convertedlog = ("Start to fail-over.")
		outputobj.output_log(self.LOG_ERR_LV, convertedlog)
		self.debug_status()
		return

	'''
		Detect pengine starts the calculation for transition.
		This function is called when cluster status became "S_POLICY_ENGINE"
		and input data is not I_SHUTDOWN (do shutdown process).
		It considers a failure occurred when specified attributes are
		updated to abnormal value.
		When the failure occurred, this function outputs the log to tell it.
		If not or it is already in F/O process, it outputs nothing.

		MsgNo.F0-1, F9-1, F10-1)
			Jan  1 00:00:00 node01 crmd[777]:   notice: do_state_transition: 
				State transition S_IDLE -> S_POLICY_ENGINE 
				[ input=I_PE_CALC cause=C_TIMER_POPPED origin=crm_timer_popped ]
	'''
	def detect_pe_calc(self, outputobj, logelm, lconvfrm):
		cstat.IN_CALC = True

		# Initialize resource status list.
		# See the comment on detect_rsc_unmanaged().
		self.rscstatList = None
		self.rscstatList = list()

		return CONV_OK

	'''
		Output the log which tells F/O finished.
		In addition, output all resources' status.
		It considers that F/O succeeded when all of specified resources
		(with the parameter OPT_ACTRSC in config file) are running,
		and if any resource at all stops, it considers F/O failed.
		This function is called when cluster status became "S_IDLE" or "S_STOPPING".

		MsgNo.F0-2, F12-1, F12-2)
			Jan  1 00:00:00 node01 crmd[777]:   notice: do_state_transition: 
				State transition S_TRANSITION_ENGINE -> S_IDLE 
				[ input=I_TE_SUCCESS cause=C_FSA_INTERNAL origin=notify_crmd ]
	'''
	def detect_fo_complete(self, outputobj, logelm, lconvfrm):

		# Check specified resources exist in this cluster.
		if len(self.rscstatList) > 0:
			for actrsc in actRscList:
				newrsc = RscStat(actrsc)
				if newrsc not in self.rscstatList:
					pm_log.error("detect_fo_complete(): " +
						"resource [%s] is not in this cluster." % (actrsc))
					break

		if cstat.IN_FO_PROCESS == False:
			self.clear_status()
			return CONV_OK
		self.clear_status()

		# When one or more Unmanaged resource exists in the cluster,
		# (even if the resource is not set in act_rsc)
		# it is unusual state, so consider it "F/O failed".
		detect_fo_failed = False
		unmanaged_rsc_exists = False
		for rscstat in self.rscstatList:
			if rscstat.unmanaged:
				convertedlog = ("Unmanaged resource exists.")
				outputobj.output_log(self.LOG_ERR_LV, convertedlog)
				detect_fo_failed = True
				unmanaged_rsc_exists = True
				break

		if unmanaged_rsc_exists == False:
			# Confirm each resource's status.
			detect_fo_failed = False
			rsc_operated = False
			for rscstat in self.rscstatList:
				if rscstat.rscid in actRscList:
					if rscstat.status == "Stopped" :
						output_loglevel = self.LOG_ERR_LV
						output_status = ("Stopped")
						detect_fo_failed = True
					else:
						output_loglevel = self.LOG_INFO_LV
						output_status = rscstat.status
					if not (rscstat.status != "Stopped" and rscstat.operated != True):
						rsc_operated = True
						convertedlog = ("Resource %s : %s" % (rscstat.rscid, output_status))
						outputobj.output_log(output_loglevel, convertedlog)

			if not rsc_operated:
				detect_fo_failed = True

		if detect_fo_failed:
			outputobj.output_log(self.LOG_ERR_LV, "fail-over failed.")
		else:
			outputobj.output_log(self.LOG_INFO_LV, "fail-over succeeded.")

		return CONV_OK

	'''
		Detect resource start action added.
		This is to get resource status when F/O finished.
		So it outputs nothing.

		MsgNo. F11-1)
			Jan  1 00:00:00 node01 pengine[777]:   notice: LogActions: 
			Start   prmRSC (node01)
	'''
	def add_rsc_start(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			nodename = self.trimmark(wordlist[-1])
			rscid = wordlist[2]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(nodename, rscid):
			return CONV_ITEM_EMPTY

		# Set the resource's status to the list.
		statstr = ("Started on %s" % (nodename))
		self.set_rscstat(rscid, statstr, None, None)

		if rscid in actRscList:
			cstat.ACTRSC_MOVE = FAIL_STR
			if cstat.FAILURE_OCCURRED == FAIL_NODE:
				self.detect_fo_start(outputobj)
		return CONV_OK

	'''
		Detect resource stop action added.
		This is to get resource status when F/O finished.

		MsgNo. F11-2)
			Jan  1 00:00:00 node01 pengine[777]:   notice: LogActions: 
			Stop   prmRSC (node01)
			Jan  1 00:00:00 node01 pengine[777]:   notice: LogActions: 
			Stop   prmRSC (node01 - blocked)
	'''
	def add_rsc_stop(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			rscid = wordlist[2]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(rscid):
			return CONV_ITEM_EMPTY

		# Set the resource's status to the list.
		statstr = ("Stopped")
		self.set_rscstat(rscid, statstr, None, None)

		if rscid in actRscList:
			cstat.ACTRSC_MOVE = FAIL_STP
			if cstat.FAILURE_OCCURRED == False and self.check_unmatch_attr_rule() == True:
				cstat.FAILURE_OCCURRED = FAIL_SCORE
			if \
				cstat.FAILURE_OCCURRED == FAIL_RSC   or \
				cstat.FAILURE_OCCURRED == FAIL_SCORE or \
				cstat.FAILURE_OCCURRED == FAIL_NODE:
				self.detect_fo_start(outputobj)
		return CONV_OK

	'''
		Detect no action added for the resource.
		This is to get resource status when F/O finished.
		So it outputs nothing.

		MsgNo.F11-3)
			Jan  1 00:00:00 node01 pengine[777]:     info: LogActions: 
			Leave   prmRSC (Started node01)
		MsgNo.F11-5)
			Jan  1 00:00:00 node01 pengine[777]:     info: LogActions: 
			Leave   prmRSC (Started unmanaged)
		MsgNo.F11-8)
			Jan  1 00:00:00 node01 pengine[777]:   notice: LogActions: 
			Restart prmRSC (Started node01)
		MsgNo.F11-9)
			Jan  1 00:00:00 node01 pengine[777]:     info: LogActions: 
			Leave   prmRSC (Stopped)
		MsgNo.F11-11)
			Jan  1 00:00:00 node01 pengine[777]:   notice: LogActions: 
			Recover prmRSC (Started node01)
		MsgNo.F11-12)
			Jan  1 00:00:00 node01 pengine[777]:   notice: LogActions: 
			Reload prmRSC (Started node01)
	'''
	def add_no_action(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			rscid = wordlist[2]
			status = self.trimmark(wordlist[3])
			node = ""
			if len(wordlist) >= 5:
				node = self.trimmark(wordlist[4])
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(rscid, status):
			return CONV_ITEM_EMPTY

		# Set the resource's status flag to the list.
		unmanaged = None
		if node == "unmanaged":
			status = None
			unmanaged = True
		elif node != "":
			status = ("%s on %s" % (status, node))
		self.set_rscstat(rscid, status, unmanaged, None)

		if status == "Stopped":
			if rscid in actRscList:
				cstat.ACTRSC_MOVE = FAIL_STPD
				if cstat.FAILURE_OCCURRED == FAIL_NODE:
					self.detect_fo_start(outputobj)
		return CONV_OK

	'''
		Detect resource move action added.
		This is to get resource status when F/O started.

		MsgNo. F11-6)
			Jan  1 00:00:00 node01 pengine[777]:   notice: LogActions: 
			Move    prmRSC (Started node01 -> node02)
		MsgNo. F11-13)
			Jan  1 00:00:00 node01 pengine[777]:   notice: LogActions: 
			Recover prmRSC (Started node01 -> node02)
		MsgNo. F11-14)
			Jan  1 00:00:00 node01 pengine[777]:   notice: LogActions: 
			Migrate prmRSC (Started node01 -> node02)
	'''
	def add_rsc_move(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			a_nodename = self.trimmark(wordlist[-1])
			f_nodename = self.trimmark(wordlist[-3])
			rscid = wordlist[2]
		except:
			return CONV_PARSE_ERROR

		if self.is_empty(a_nodename, rscid):
			return CONV_ITEM_EMPTY

		# Set the resource's status to the list.
		statstr = ("Move %s -> %s" % (f_nodename,a_nodename))
		self.set_rscstat(rscid, statstr, None, None)

		if rscid in actRscList:
			cstat.ACTRSC_MOVE = FAIL_MOVE
			if cstat.FAILURE_OCCURRED == False and self.check_unmatch_attr_rule() == True:
				cstat.FAILURE_OCCURRED = FAIL_SCORE
			if \
				cstat.FAILURE_OCCURRED == FAIL_RSC   or \
				cstat.FAILURE_OCCURRED == FAIL_SCORE or \
				cstat.FAILURE_OCCURRED == FAIL_NODE:
				self.detect_fo_start(outputobj)
		return CONV_OK

	'''
		Resource initiating action.
		This is to get resource status when F/O finished.
		So it outputs nothing.

		MsgNo. F11-10)
			Jan  1 00:00:00 node01 crmd[777]:   notice: te_rsc_command: 
				Initiating action 26: start prmRSC_start_0 on node01 (local)
	'''
	def rsc_init_action(self, outputobj, logelm, lconvfrm):
		if cstat.IN_FO_PROCESS == False:
			return CONV_OK

		try:
			rscid, op = self.parse_opid(logelm.halogmsg.split()[5])[:2]
			if op == "monitor":
				return CONV_OK
		except:
			return CONV_PARSE_ERROR

		if self.is_empty(rscid):
			return CONV_ITEM_EMPTY

		if rscid in actRscList:
			self.set_rscstat(rscid, None, None, True)

		return CONV_OK

	##########
	# For DC election.
	##########
	'''
		Convert log message which means DC election is complete.

		MsgNo.13-2)
			Jan  1 00:00:00 node01 crmd[777]:     info: update_dc: 
			Set DC to node01 (3.0.7)
	'''
	def dc_election_complete(self, outputobj, logelm, lconvfrm):
		try:
			nodename = logelm.halogmsg.split()[-2]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(nodename):
			return CONV_ITEM_EMPTY

		convertedlog = ("Set DC node to %s." % (nodename))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	'''
		Convert log message which means unset DC node.

		MsgNo.13-5)
			Jan  1 00:00:00 node01 crmd[777]:     info: update_dc: 
			Unset DC. Was node02
	'''
	def detect_unset_dc(self, outputobj, logelm, lconvfrm):
		try:
			nodename = logelm.halogmsg.split()[-1]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(nodename):
			return CONV_ITEM_EMPTY

		convertedlog = ("Unset DC node %s." % (nodename))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	##########
	# For Pacemaker and Corosync service shutdown.
	##########
	'''
		Detect Corosync service on localhost shutdown complete.
		Output message is static, but to remove the node name from
		node list, detect the message with peculiar function.

		MsgNo.14-2)
			Jan  1 00:00:00 node01 corosync[777]:  [MAIN  ] 
			Corosync Cluster Engine exiting normally
	'''
	def detect_cs_shutdown(self, outputobj, logelm, lconvfrm):
		outputobj.output_log(lconvfrm.loglevel, lconvfrm.rulename)
		cstat.nodeDict.clear()
		return CONV_OK

	'''
		Convert log message which means Pacemaker service on the node
		in the cluster send shutdown request.

		MsgNo.14-5)
			Jan  1 00:00:00 node01 crmd[777]:     info: handle_shutdown_request: 
				Creating shutdown request for node02 (state=S_IDLE)
	'''
	def detect_shutdown_request(self, outputobj, logelm, lconvfrm):
		try:
			nodename = logelm.halogmsg.split()[-2]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(nodename):
			return CONV_ITEM_EMPTY

		convertedlog = ("Pacemaker on %s is shutting down." % (nodename))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	##########
	# For fence operation.
	##########
	'''
		Convert log message which means fence operation started.

		MsgNo.21-1)
			Jan  1 00:00:00 node01 crmd[777]:   notice: te_fence_node: 
				Executing reboot fencing operation (79) on node02 
				(timeout=60000)
	'''
	def fence_op_started(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			op = wordlist[2]
			target = wordlist[7]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(op, target):
			return CONV_ITEM_EMPTY

		convertedlog = ("Try to STONITH (%s) %s." % (op, target))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	'''
		Convert log message which means fence operation ended.

		MsgNo.21-2)
			Jan  1 00:00:00 node01 crmd[777]:   notice: tengine_stonith_notify: 
				Peer node02 was terminated (reboot) by node03 for node01: OK 
				(ref=00000000-0000-0000-0000-000000000000) by client crmd.777
			Jan  1 00:00:00 node01 crmd[777]:   notice: tengine_stonith_notify:
				Peer node02 was terminated (off) by a human for node01: OK
				(ref=00000000-0000-0000-0000-000000000000) by client stonith_admin.888
		MsgNo.21-3)
			Jan  1 00:00:00 node01 crmd[777]:   notice: tengine_stonith_notify: 
				Peer node02 was not terminated (reboot) by node03 for node01: 
				Timer expired (ref=00000000-0000-0000-0000-000000000000) 
				by client crmd.777
	'''
	def fence_op_ended(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			tgt_node = wordlist[wordlist.index("Peer") + 1]
			op = self.trimmark(wordlist[wordlist.index("terminated") + 1])
			by_node = " ".join(wordlist[wordlist.index("by") + 1 : wordlist.index("for")])
			for_node = self.trimmark(wordlist[wordlist.index("for") + 1])
			result = wordlist[wordlist.index("for") + 2]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(tgt_node, op, by_node, for_node, result):
			return CONV_ITEM_EMPTY

		if result == "OK":
			convertedlog = ("Succeeded to STONITH (%s) %s by %s." % (op, tgt_node, by_node))
		else:
			convertedlog = ("Failed to STONITH (%s) %s by %s."    % (op, tgt_node, by_node))

		outputobj.output_log(lconvfrm.loglevel, convertedlog)

		return CONV_OK

	'''
		Convert log message which means too many failuers to stonith.

		MsgNo.21-4)
			Jan  1 00:00:00 node01 crmd[777]:   notice: too_many_st_failures: 
				Too many failures to fence node02 (11), giving up
	'''
	def fence_too_many_failures(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			node = wordlist[wordlist.index("fence") + 1]
		except:
			return CONV_PARSE_ERROR

		if self.is_empty(node):
			return CONV_ITEM_EMPTY

		convertedlog = ("Too many failures to STONITH %s." % (node))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	'''
		Convert log message which means executing stonith device started.

		MsgNo.21-5)
			Jan  1 00:00:00 node01 stonith-ng[777]:     info: 
			call_remote_stonith: Requesting that node03 perform op 
			reboot node02 with prmStonith1 for crmd.888 (72s)
	'''
	def exec_st_device_started(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			by_node = wordlist[3]
			op = wordlist[6]
			for_node = wordlist[7]
			if wordlist[8] == "with":
				rsc = " " + wordlist[9]
			else:
				rsc = ""

		except:
			return CONV_PARSE_ERROR
		if self.is_empty(by_node, op, for_node):
			return CONV_ITEM_EMPTY

		convertedlog = ("Try to execute STONITH device%s on %s for %s %s." % (rsc, by_node, op, for_node))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	'''
		Convert log message which means executing stonith device ended.

		MsgNo.21-6)
			Jan  1 00:00:00 node01 stonith-ng[777]:   notice: 
			process_remote_stonith_exec: Call to prmStonith1 for node02 
			on behalf of crmd.888@node01: OK (0)
		MsgNo.21-7)
			Jan  1 00:00:00 node01 stonith-ng[777]:   notice: 
			process_remote_stonith_exec: Call to prmStonith1 for node02 
			on behalf of crmd.888@node01: Generic Pacemaker error (-201)
	'''
	def exec_st_device_ended(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			target = self.trimmark(wordlist[wordlist.index("for") + 1])
			rsc = self.trimmark(wordlist[wordlist.index("to") + 1])
			rtn = self.trimmark(wordlist[-1])
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(target, rsc, rtn):
			return CONV_ITEM_EMPTY

		if rtn == "0":
			convertedlog = ("Succeeded to execute STONITH device %s for %s." % (rsc, target))
		else:
			convertedlog = ("Failed to execute STONITH device %s for %s."    % (rsc, target))

		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	##########
	# For attribute event.
	##########
	'''
		Convert log message which means attribute value on own node updated.

		MsgNo.22-1)
			Jan  1 00:00:00 node01 attrd[777]:   notice: attrd_perform_update: 
				Sent update 7: diskcheck_status=normal
	'''
	def detect_attr_updated(self, outputobj, logelm, lconvfrm):
		try:
			attrval = None
			# attribute name can has empty char.
			wordlist = logelm.halogmsg.split()
			from_node = self.trimmark(wordlist[2].split("[")[1])
			attrname = wordlist[2].split("[")[0]
			attrval = logelm.halogmsg.split("->")[1].split("from")[0].strip()
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(attrname, attrval):
			return CONV_ITEM_EMPTY

		convertedlog = ("Attribute \"%s\" is updated to \"%s\" at \"%s\"." %
			(attrname, attrval, from_node))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		cstat.attrDict[from_node, attrname] = attrval
		return CONV_OK

	'''
		Convert log message which means attribute value on own node deleted.

		MsgNo.22-2)
			Jan  1 00:00:00 node01 attrd[777]:   notice: attrd_perform_update: 
				Sent delete 51: node=2657462464, attr=diskcheck_status, 
				id=<n/a>, set=(null), section=status
	'''
	def detect_attr_deleted(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			from_node = self.trimmark(wordlist[2].split("[")[1])
			attrname = wordlist[2].split("[")[0]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(attrname):
			return CONV_ITEM_EMPTY

		convertedlog = ("Attribute \"%s\" is deleted at \"%s\"." %
			(attrname, from_node))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	##########
	# For Corosync service starts.
	##########
	'''
		Convert log message which means Corosync service is starting.

		MsgNo.23-1)
			Jan  1 00:00:00 node01 corosync[777]:  [MAIN  ] Corosync Cluster 
			Engine ('2.3.0'): started and ready to provide service.
	'''
	def detect_cs_start(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			idx = wordlist.index("Engine") + 1
			version = self.trimmark(wordlist[idx],".")
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(version):
			return CONV_ITEM_EMPTY

		self.clear_status()
		convertedlog = ("Starting Corosync %s." % (version))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

	'''
		Convert log message which means Pacemaker is starting.

		MsgNo.23-4)
			Jan  1 00:00:00 node01 pacemakerd[777]:   notice: main: 
			Starting Pacemaker 1.1.10 (Build: 1af3c9b):  generated-manpages 
			agent-manpages ascii-docs publican-docs ncurses libqb-logging 
			libqb-ipc lha-fencing nagios  corosync-native
	'''
	def detect_pcmk_start(self, outputobj, logelm, lconvfrm):
		try:
			wordlist = logelm.halogmsg.split()
			version = wordlist[wordlist.index("Pacemaker") + 1].split("-")[0]
		except:
			return CONV_PARSE_ERROR
		if self.is_empty(version):
			return CONV_ITEM_EMPTY

		self.clear_status()
		convertedlog = ("Starting Pacemaker %s." % (version))
		outputobj.output_log(lconvfrm.loglevel, convertedlog)
		return CONV_OK

pm_log = LogconvLog(LogconvLog.LOG_INFO, None)

if __name__ == "__main__":
	sys.exit(LogConvert().main())
