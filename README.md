``check_ovpn_users`` is a Nagios/Icinga plugin for checking the amount of logged in OpenVPN users.

# Requirements
The plugin requires an installed OpenVPN server and the ``logging`` Python module.

# Usage
By default, the script checks the current amount of connected OpenVPN users by reading the log file. It is possible to control this behaviour by specifying additional parameters (*see below*).
The script also support performance data for data visualization.

The following parameters can be specified:

| Parameter | Description |
|:----------|:------------|
| `-d` / `--debug` | enable debugging outputs (*default: no*) |
| `-h` / `--help` | shows help and quits |
| `-P` / `--show-perfdata` | enables performance data (*default: no*) |
| `-f` / `--log-file` | defines the OpenVPN server log file (*default: /var/run/ovpnserver.log*) |
| `-w` / `--users-warning` | defines the user warning threshold (*default: 5*) |
| `-c` / `--users-critical` | defines the user critical threshold (*default: 10*) |
| `--version` | prints programm version and quits |

## Examples
Check with default thresholds and parameters:
```
$ ./check_ovpn_users.py
OK: OpenVPN users OK (2) |
```

Check with customized thresholds:
```
$ ./check_ovpn_users.py -w 1 -c 3
OK: OpenVPN users WARNING (2) |
```

Check also reporting performance data:
```
$ ./check_ovpn_users.py -P
OK: OpenVPN users OK (2) | 'ovpn_users'=2;5;10
```

# Installation
To install the plugin, move the Python script into the appropriate directory and create an appropriate **NRPE** or **Icinga2** configuration - check-out the examples in this repository. There is also a spec file for creating a RPM file.

# Configuration
Inside Nagios / Icinga you will need to configure a check, e.g. for Icinga2:
```
#check_nrpe_apcaccess
define command{
    command_name        check_nrpe_apcaccess
    command_line        $USER1$/check_nrpe -H $HOSTADDRESS$ -c check_apcaccess -a $ARG1$
}
```

For agentless systems (*e.g. IPFire/IPCop*), utilize the ``check_by_ssh`` command:
```
apply Service "DIAG: Updates" {
  import "generic-service"
  check_command = "by_ssh"
  vars.by_ssh_command = [ "/opt/check_pakfire.py", "-P" ]
  vars.by_ssh_port = host.vars.ssh_port
  vars.by_ssh_logname = "icinga"
  assign where host.vars.os == "Linux" && host.vars.app == "router"
}
```
