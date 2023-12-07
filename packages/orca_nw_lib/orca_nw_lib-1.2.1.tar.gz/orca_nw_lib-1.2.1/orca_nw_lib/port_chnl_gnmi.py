from orca_nw_lib.gnmi_pb2 import PathElem
from orca_nw_lib.gnmi_util import (
    create_gnmi_update,
    create_req_for_update,
    send_gnmi_get,
    send_gnmi_set,
)
from orca_nw_lib.portgroup_gnmi import get_port_chnl_mem_base_path
from .gnmi_pb2 import Path, PathElem
from .gnmi_util import (
    create_gnmi_update,
    create_req_for_update,
    get_gnmi_del_req,
    send_gnmi_get,
    send_gnmi_set,
)


def get_port_chnl_root_path() -> Path:
    """
    Get the root path of the port channel configuration in the OpenConfig model.

    Returns:
        A Path object representing the root path of the port channel configuration.
    """
    return Path(
        target="openconfig",
        origin="sonic-portchannel",
        elem=[
            PathElem(name="sonic-portchannel"),
        ],
    )


def get_port_chnl_base_path() -> Path:
    """
    Return the base path for the port channel.

    Returns:
        Path: The base path for the port channel.
    """
    path = get_port_chnl_root_path()
    path.elem.append(PathElem(name="PORTCHANNEL"))
    return path


def get_port_chnl_list_path() -> Path:
    """
    Return the path to the port channel list.

    Returns:
        Path: The path to the port channel list.
    """
    path = get_port_chnl_base_path()
    path.elem.append(PathElem(name="PORTCHANNEL_LIST"))
    return path


def get_port_chnl_path(chnl_name: str = None):
    """
    Retrieves the path for a specific channel or the entire port channel list.

    Args:
        chnl_name (str, optional): The name of the channel. Defaults to None.

    Returns:
        Path: The path object representing the channel or the entire port channel list.
    """
    path = get_port_chnl_base_path()
    if chnl_name:
        path.elem.append(PathElem(name="PORTCHANNEL_LIST", key={"name": chnl_name}))
    else:
        path.elem.append(PathElem(name="PORTCHANNEL_LIST"))
    return path


def get_lag_member_table_list_path() -> Path:
    """
    Returns the path to the list of LAG member tables.

    Returns:
        Path: The path to the list of LAG member tables.
    """

    path = get_port_chnl_root_path()
    path.elem.append(PathElem(name="LAG_MEMBER_TABLE"))
    path.elem.append(PathElem(name="LAG_MEMBER_TABLE_LIST"))
    return path


def get_lag_table_list_path(chnl_name: str = None) -> Path:
    """
    Generates the path to the LAG table list based on the given channel name.

    Parameters:
        chnl_name (str, optional): The name of the channel. Defaults to None.

    Returns:
        Path: The path to the LAG table list.
    """
    path = get_port_chnl_root_path()
    path.elem.append(PathElem(name="LAG_TABLE"))

    if chnl_name:
        path.elem.append(PathElem(name="LAG_TABLE_LIST", key={"lagname": chnl_name}))
    else:
        path.elem.append(PathElem(name="LAG_TABLE_LIST"))

    return path


def del_all_port_chnl(device_ip: str):
    """
    Deletes all port channels on the specified device.

    Args:
        device_ip (str): The IP address of the device.

    Returns:
        The result of sending the GNMI delete request to remove all port channels on the device.
    """
    return send_gnmi_set(get_gnmi_del_req(get_port_chnl_list_path()), device_ip)


def get_port_chnl_from_device(device_ip: str, chnl_name: str):
    """
    Retrieves the port channel from the specified device using the device's IP address and the channel's name.

    Args:
        device_ip (str): The IP address of the device.
        chnl_name (str): The name of the channel.

    Returns:
        str: The port channel retrieved from the device.

    """
    return send_gnmi_get(device_ip, [get_port_chnl_path(chnl_name)])


def get_port_chnls_info_from_device(device_ip: str, chnl_name: str = None):
    """
    Retrieves port channel information from a device.

    Args:
        device_ip (str): The IP address of the device.
        chnl_name (str, optional): The name of the channel. Defaults to None.

    Returns:
        The port channel information retrieved from the device.
    """
    return send_gnmi_get(
        device_ip,
        [get_lag_member_table_list_path(), get_lag_table_list_path(chnl_name)],
    )


def get_lag_member_table_list(device_ip: str):
    """
    Retrieves the list of LAG (Link Aggregation Group) member table entries for a given device IP.

    Args:
        device_ip (str): The IP address of the device to retrieve the LAG member table from.

    Returns:
        The list of LAG member table entries retrieved from the device.

    Raises:
        Any exceptions that may occur during the retrieval process.
    """
    return send_gnmi_get(device_ip, [get_lag_member_table_list_path()])


def get_lag_table_list(device_ip: str, chnl_name: str = None):
    """
    Get the list of LAG tables for a given device IP and channel name.

    Args:
        device_ip (str): The IP address of the target device.
        chnl_name (str, optional): The name of the channel. Defaults to None.

    Returns:
        The list of LAG tables for the given device IP and channel name.
    """
    return send_gnmi_get(device_ip, [get_lag_table_list_path(chnl_name)])


def get_port_chnl_mem_list_path():
    """
    Generates the path for the 'PORTCHANNEL_MEMBER_LIST' element in the port channel
    channel memory list.

    Returns:
        The generated path for the 'PORTCHANNEL_MEMBER_LIST' element.
    """
    path = get_port_chnl_mem_base_path()
    path.elem.append(PathElem(name="PORTCHANNEL_MEMBER_LIST"))
    return path


def get_all_port_chnl_members(device_ip: str):
    """
    Retrieves all the members of a port channel on a given device.

    Args:
        device_ip (str): The IP address of the device.

    Returns:
        The list of members of the port channel.

    Raises:
        None.
    """
    return send_gnmi_get(device_ip, [get_port_chnl_mem_list_path()])


def get_port_chnl_mem_path(chnl_name: str, ifname: str):
    """
    Generate the path for a specific port channel member in the memory.

    Args:
        chnl_name (str): The name of the port channel.
        ifname (str): The name of the interface.

    Returns:
        Path: The generated path for the port channel member in the memory.
    """
    path = get_port_chnl_mem_base_path()
    path.elem.append(
        PathElem(
            name="PORTCHANNEL_MEMBER_LIST", key={"name": chnl_name, "ifname": ifname}
        )
    )
    return path


def remove_port_chnl_member(device_ip: str, chnl_name: str, ifname: str):
    """
    Remove a member from a port channel.

    Args:
        device_ip (str): The IP address of the target device.
        chnl_name (str): The name of the port channel.
        ifname (str): The interface name of the member to be removed.

    Returns:
        The result of sending a GNMI delete request to remove the member from the port channel.
    """
    return send_gnmi_set(
        get_gnmi_del_req(get_port_chnl_mem_path(chnl_name, ifname)), device_ip
    )


def del_port_chnl_from_device(device_ip: str, chnl_name: str = None):
    """
    Delete a port channel from a device.

    Args:
        device_ip (str): The IP address of the device.
        chnl_name (str, optional): The name of the channel to be deleted. Defaults to None.

    Returns:
        The response from the GNMI set request.

    """
    return send_gnmi_set(get_gnmi_del_req(get_port_chnl_path(chnl_name)), device_ip)


def add_port_chnl_member(device_ip: str, chnl_name: str, ifnames: list[str]):
    """
    Adds a member to a port channel on a device.

    Args:
        device_ip (str): The IP address of the device.
        chnl_name (str): The name of the port channel.
        ifnames (list[str]): A list of interface names to add to the port channel.

    Returns:
        str: The response from the send_gnmi_set function.
    """
    port_chnl_add = {"sonic-portchannel:PORTCHANNEL_MEMBER_LIST": []}
    for intf in ifnames:
        port_chnl_add.get("sonic-portchannel:PORTCHANNEL_MEMBER_LIST").append(
            {"name": chnl_name, "ifname": intf}
        )
    return send_gnmi_set(
        create_req_for_update(
            [create_gnmi_update(get_port_chnl_mem_list_path(), port_chnl_add)]
        ),
        device_ip,
    )


def add_port_chnl_on_device(
    device_ip: str, chnl_name: str, admin_status: str = None, mtu: int = None
):
    """
    Adds a port channel to a specific device.

    Args:
        device_ip (str): The IP address of the device.
        chnl_name (str): The name of the port channel.
        admin_status (str, optional): The administrative status of the port channel.
            Valid values are "up" and "down". Defaults to None.
        mtu (int, optional): The Maximum Transmission Unit (MTU) of the port channel.
            Defaults to None.

    Returns:
        str: The result of the GNMI set operation.

    """
    port_chnl_add = {"sonic-portchannel:PORTCHANNEL_LIST": []}
    port_chnl_item = {"name": chnl_name}
    if admin_status is not None and admin_status in ["up", "down"]:
        port_chnl_item["admin_status"] = admin_status
    if mtu is not None:
        port_chnl_item["mtu"] = mtu

    port_chnl_add.get("sonic-portchannel:PORTCHANNEL_LIST").append(port_chnl_item)
    return send_gnmi_set(
        create_req_for_update(
            [create_gnmi_update(get_port_chnl_list_path(), port_chnl_add)]
        ),
        device_ip,
    )
