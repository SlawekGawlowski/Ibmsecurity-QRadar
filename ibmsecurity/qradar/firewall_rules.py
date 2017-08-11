import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(qradarAppliance, server_ID, check_mode=False, force=False):
    """
    Retrieves a list of access control firewall rules based on the supplied server ID
    """
    uri = "/system/servers/" + str(server_ID) + "/firewall_rules"
    return qradarAppliance.invoke_get("Get firewall rules",
                                    uri)


def set(qradarAppliance, server_ID, is_any_source_ip, port_range, port_type, protocol, single_port, source_ip, check_mode=False, force=False):
    """
    Sets the access control firewall rules for the supplied server ID
    """
    if force is True or _check(qradarAppliance, server_ID, is_any_source_ip, port_range, port_type, protocol, single_port, source_ip) is False:
        if check_mode is True:
            return qradarAppliance.create_return_object(changed=True)
        else:
            # get the existing list of firewall rules and append the new rule to the end
            rules = get(qradarAppliance, server_ID)['data']
            rules.append({
                    "is_any_source_ip": is_any_source_ip,
                    "port_range": port_range,
                    "port_type": port_type,
                    "protocol": protocol,
                    "single_port": single_port,
                    "source_ip": source_ip
                })

            uri = "/system/servers/" + str(server_ID) + "/firewall_rules"

            return qradarAppliance.invoke_put(
                "Updating firewall rules for host ID " + str(server_ID),
                uri,
                rules
            )

    return qradarAppliance.create_return_object()


def _check(qradarAppliance, server_ID, is_any_source_ip, port_range, port_type, protocol, single_port, source_ip):
    """
    Checks that an equivalent firewall rule does not already exist on the supplied server ID
    """
    currentRules = get(qradarAppliance, server_ID)['data']
    for rule in currentRules:
        if not rule['port_type'] == port_type \
                or not rule['protocol'] == protocol \
                or not rule['is_any_source_ip'] == is_any_source_ip \
                or not rule['port_type'] == port_type:
            continue

        if is_any_source_ip is False:
            if not rule['source_ip'] == source_ip:
                continue

        if port_type is "SINGLE":
            if not rule['single_port'] == single_port:
                continue
        elif port_type is "RANGE":
            if not rule['port_range'] == port_range:
                continue
        else:
            if not rule['port_range'] == port_range or not rule['single_port'] == single_port:
                continue

        return True

    logger.info("Firewall rule does not exist")
    return False


def compare(qradarAppliance1, serverID1, qradarAppliance2, serverID2):
    """
    Compare firewall rules on two QRadar hosts
    """
    ret_obj1 = get(qradarAppliance1, serverID1)
    ret_obj2 = get(qradarAppliance2, serverID2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
