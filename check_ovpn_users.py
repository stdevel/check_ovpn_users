#!/usr/bin/python

# check_ovpn_users.py - a script for checking the
# amount of OpenVPN users
#
# 2016 By Christian Stankowic
# <info at stankowic hyphen development dot net>
# https://github.com/stdevel
#

from optparse import OptionParser, OptionGroup
import logging
import re

#set logger
LOGGER = logging.getLogger("check_ovpn_users")

#some script-wide variables
log=[]
matches=[]
state=0

def set_code(int):
	#set result code
	global state
	if int > state: state = int

def get_return_str():
	#get return string
	if state == 3: return "UNKNOWN"
	elif state == 2: return "CRITICAL"
	elif state == 1: return "WARNING"
	else: return "OK"

def check_users():
	#get _all_ the users
	for line in log:
		#find IP at the beginning of line (other IPs are crap)
		ips = re.findall("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
		#add if IP found
		if len(ips) > 0: matches.append(ips[0])
	LOGGER.debug("Found the following clients: {0}".format(",".join(matches)))
	
	#set result
	if len(ips) > options.users_crit:
		#critical
		set_code(2)
		snip_users = "OpenVPN users CRITICAL ({0})".format(len(matches))
	elif len(ips) > options.users_warn:
		#warning
		set_code(1)
		snip_users = "OpenVPN users WARNING ({0})".format(len(matches))
	else:
		#ok
		snip_users = "OpenVPN users OK ({0})".format(len(matches))
	
	#retrieve performance data
	perfdata=" | "
	if options.show_perfdata:
		perfdata = "{0}'ovpn_users'={1};{2};{3}".format(perfdata,len(matches),options.users_warn,options.users_crit)
	
	#return result
	print "{0}: {1}{2}".format(get_return_str(), snip_users, perfdata)
	exit(state)


def get_log():
	#get log file
	global log
	
	#read logfile into list
	with open(options.log_file, 'r') as my_log:
		log=my_log.read().splitlines()
	
	#die in a fire if we're empty
	if len(log) == 0:
		print "UNKNOWN: Log file seems to be invalid!"
		exit(3)



if __name__ == "__main__":
	#define description, version and load parser
	desc='''%prog is used to check the amount of logged in OpenVPN users.
	
	Checkout the GitHub page for updates: https://github.com/stdevel/check_ovpn_users'''
	parser = OptionParser(description=desc,version="%prog version 0.5.0")
	
	gen_opts = OptionGroup(parser, "Generic options")
	usr_opts = OptionGroup(parser, "User options")
	parser.add_option_group(gen_opts)
	parser.add_option_group(usr_opts)
	
	#-d / --debug
	gen_opts.add_option("-d", "--debug", dest="debug", default=False, action="store_true", help="enable debugging outputs")
	
	#-P / --show-perfdata
	gen_opts.add_option("-P", "--show-perfdata", dest="show_perfdata", default=False, action="store_true", help="enables performance data, requires -i (default: no)")
	
	#-f / --log-file
	gen_opts.add_option("-f", "--log-file", dest="log_file", default="/var/run/ovpnserver.log", action="store", help="defines the OpenVPN server log file (default: /var/run/ovpnserver.log)")
	
	#-w / --users-warning
	usr_opts.add_option("-w", "--users-warning", dest="users_warn", default=5, action="store", metavar="NUMBER", help="defines the user warning threshold (default: 5)")
	
	#-c / --users-critical
	usr_opts.add_option("-c", "--users-critical", dest="users_crit", default=10, action="store", metavar="NUMBER", help="defines the user critical threshold (default: 10)")
	
	#parse arguments
	(options, args) = parser.parse_args()

	#set logger level
	if options.debug:
		logging.basicConfig(level=logging.DEBUG)
		LOGGER.setLevel(logging.DEBUG)
	else:
		logging.basicConfig()
		LOGGER.setLevel(logging.INFO)
	
	#debug outputs
	LOGGER.debug("OPTIONS: {0}".format(options))
	
	#check users
	get_log()
	check_users()
