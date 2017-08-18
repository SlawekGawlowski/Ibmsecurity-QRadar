import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(qradarAppliance, server_id, check_mode=False, force=False):
    """
    Retrieves the server host with the supplied server ID
    """
    return qradarAppliance.invoke_get("Get server host " + str(server_id),
                                      "/system/servers/" + str(server_id))


def get_all(qradarAppliance, check_mode=False, force=False):
    """
    Retrieves a list of all server hosts in the deployment
    """
    return qradarAppliance.invoke_get("Get server hosts",
                                    "/system/servers")


def set(qradarAppliance, server_id, email_server_address, check_mode=False, force=False):
    """
    Updates the server host with the supplied server ID
    """
    if force is True or _check(qradarAppliance, server_id, email_server_address) is False:
        if check_mode is True:
            return qradarAppliance.create_return_object(changed=True)
        else:
            # update the supplied interface
            config = {
                    "email_server_address": email_server_address
                }

            uri = "/system/servers/" + str(server_id)

            return qradarAppliance.invoke_post(
                "Updating server host for server ID " + str(server_id),
                uri,
                config
            )

    return qradarAppliance.create_return_object()


def _check(qradarAppliance, server_id, email_server_address):
    """
    Checks that the host with the supplied server ID does not already have the supplied configuration
    """
    config = get(qradarAppliance, server_id)['data']

    if not config['email_server_address'] == email_server_address:
        logger.info("Server host configuration does not match")
        return False

    return True


def compare(qradarAppliance1, qradarAppliance2):
    """
    Compare hosts managed by two QRadar appliances
    """
    ret_obj1 = get_all(qradarAppliance1)
    ret_obj2 = get_all(qradarAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
