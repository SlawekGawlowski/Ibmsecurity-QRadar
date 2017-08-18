import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(qradarAppliance, server_ID, check_mode=False, force=False):
    """
    Retrieves a list of ethernet interfaces based on the supplied server ID
    """
    uri = "/system/servers/" + str(server_ID) + "/network_interfaces/ethernet"
    return qradarAppliance.invoke_get("Get ethernet network interfaces",
                                    uri)


def set(qradarAppliance, server_ID, device_name, role, ipversion, ip, mask, is_auto_ip, is_moving_config_with_active_ha, check_mode=False, force=False):
    """
    Updates an ethernet interface on the supplied server ID
    """
    if force is True or _check(qradarAppliance, server_ID, device_name, role, ipversion, ip, mask, is_auto_ip, is_moving_config_with_active_ha) is False:
        if check_mode is True:
            return qradarAppliance.create_return_object(changed=True)
        else:
            # update the supplied interface
            config = {
                    "ip": ip,
                    "ipversion": ipversion,
                    "role": role,
                    "mask": mask,
                    "is_auto_ip": is_auto_ip,
                    "is_moving_config_with_active_ha": is_moving_config_with_active_ha
                }

            uri = "/system/servers/" + str(server_ID) + "/network_interfaces/ethernet/" + str(device_name)

            return qradarAppliance.invoke_post(
                "Updating ethernet interace " + str(device_name) + " for host ID " + str(server_ID),
                uri,
                config
            )

    return qradarAppliance.create_return_object()


def _check(qradarAppliance, server_ID, device_name, role, ipversion, ip, mask, is_auto_ip, is_moving_config_with_active_ha):
    """
    Checks that the supplied ethernet interface on the supplied server ID does not already have the supplied configuration
    """
    config = get(qradarAppliance, server_ID)['data']

    for interface in config:
        if interface['device_name'] == device_name:
            if not interface['role'] == role \
                    or not interface['ipversion'] == ipversion \
                    or not interface['ip'] == ip \
                    or not interface['mask'] == mask \
                    or not interface['is_auto_ip'] is is_auto_ip \
                    or not interface['is_moving_config_with_active_ha'] is is_moving_config_with_active_ha:
                logger.info("Ethernet interface configuration does not match")
                return False
            break

    return True


def compare(qradarAppliance1, serverID1, qradarAppliance2, serverID2):
    """
    Compare ethernet interfaces on two QRadar hosts
    """
    ret_obj1 = get(qradarAppliance1, serverID1)
    ret_obj2 = get(qradarAppliance2, serverID2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
