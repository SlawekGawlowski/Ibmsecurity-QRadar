import logging
import ibmsecurity.utilities.tools

logger = logging.getLogger(__name__)


def get(qradarAppliance, check_mode=False, force=False):
    """
    Retrieves a list of all server hosts in the deployment
    """
    return qradarAppliance.invoke_get("Get server hosts",
                                    "/system/servers")


def compare(qradarAppliance1, qradarAppliance2):
    """
    Compare hosts managed by two QRadar appliances
    """
    ret_obj1 = get(qradarAppliance1)
    ret_obj2 = get(qradarAppliance2)

    return ibmsecurity.utilities.tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
