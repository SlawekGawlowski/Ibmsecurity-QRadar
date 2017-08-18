import logging.config
import pprint
from ibmsecurity.appliance.qradarappliance import QRadarAppliance
from ibmsecurity.user.applianceuser import ApplianceUser
from ibmsecurity.user.qradaruser import QRadarUser
import pkgutil
import importlib
import yaml
import json


def import_submodules(package, recursive=True):
    """
    Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


import ibmsecurity

# Import all packages within ibmsecurity - recursively
# Note: Advisable to replace this code with specific imports for production code
import_submodules(ibmsecurity)

# Setup logging to send to stdout, format and set log level
# logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig()
# Valid values are 'DEBUG', 'INFO', 'ERROR', 'CRITICAL'
logLevel = 'INFO'
DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [PID:%(process)d TID:%(thread)d] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': logLevel,
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'level': logLevel,
            'handlers': ['default'],
            'propagate': True
        },
        'requests.packages.urllib3.connectionpool': {
            'level': 'ERROR',
            'handlers': ['default'],
            'propagate': True
        }
    }
}
logging.config.dictConfig(DEFAULT_LOGGING)


# Function to pretty print JSON data and in YAML format
def p(jdata):
    pp = pprint.PrettyPrinter(indent=2)
    #pp.pprint(jdata)
    print(yaml.safe_dump(jdata, encoding='utf-8', allow_unicode=True))


# Create a user credential for QRadar appliance
u = QRadarUser(username="admin", password="Object00")
# Create a QRadar appliance with above credential
qradar_server = QRadarAppliance(hostname="192.168.42.100", user=u, lmi_port=443)

# Retrieve the details of all hosts in the deployment
server_details = ibmsecurity.qradar.servers.get_all(qradarAppliance=qradar_server)
print("----------servers.get_all----------")
p(server_details)

# print("----------servers.compare----------")
# p(ibmsecurity.qradar.servers.compare(qradar_server, qradar_server))

serverID = server_details['data'][0]['server_id']

# Check ethernet interfaces on the first host in the deployment
print("----------ethernet.get_all----------")
p(ibmsecurity.qradar.ethernet.get_all(qradarAppliance=qradar_server, server_ID=serverID))

# Update an ethernet interfaces on the first host in the deployment
print("----------ethernet.set----------")
p(ibmsecurity.qradar.ethernet.set(qradarAppliance=qradar_server,
                                  server_ID=serverID,
                                  device_name="eth1",
                                  role="regular",
                                  ipversion="ipv4",
                                  ip="192.168.125.101",
                                  mask="255.255.255.0",
                                  is_auto_ip=False,
                                  is_moving_config_with_active_ha=True))

print("----------ethernet.get_all----------")
p(ibmsecurity.qradar.ethernet.get_all(qradarAppliance=qradar_server, server_ID=serverID))

# print("----------ethernet.compare----------")
# p(ibmsecurity.qradar.ethernet.compare(qradar_server, serverID, qradar_server, serverID))
#
# # Check firewall rules on the first host in the deployment
# print("----------firewall_rules.get----------")
# p(ibmsecurity.qradar.firewall_rules.get(qradarAppliance=qradar_server, server_ID=serverID))
# #
# # Add a firewall rule to the console appliance
# print("----------firewall_rules.set----------")
# p(ibmsecurity.qradar.firewall_rules.set(qradarAppliance=qradar_server,
#                                     server_ID=serverID,
#                                     is_any_source_ip=False,
#                                     port_range="",
#                                     port_type="SINGLE",
#                                     protocol="ANY",
#                                     single_port="22",
#                                     source_ip ="192.168.42.105",
#                                     check_mode=False,
#                                     force=False))
# print("----------firewall_rules.get----------")
# p(ibmsecurity.qradar.firewall_rules.get(qradarAppliance=qradar_server, server_ID=serverID))
#
# print("----------firewall_rules.compare----------")
# p(ibmsecurity.qradar.firewall_rules.compare(qradar_server, serverID, qradar_server, serverID))