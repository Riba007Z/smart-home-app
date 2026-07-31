import requests
import urllib3

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


BASE = "https://1home.local/api"

USERNAME = "admin"
PASSWORD = "VqNmE9sy"


def login():

    r = requests.post(
        f"{BASE}/auth",
        json={
            "username": USERNAME,
            "password": PASSWORD,
        },
        verify=False,
    )

    r.raise_for_status()

    auth = r.json()

    return {
        "Authorization": f"{auth['tokenType']} {auth['token']}",
        "X-1H-Client-Type": "web",
    }



def get_devices():

    headers = login()


    #
    # Get KNX group address information
    #
    gateways = requests.get(
        f"{BASE}/knx/gateways",
        headers=headers,
        verify=False,
    ).json()


    group_addresses = {}


    for gateway in gateways:

        gateway_id = gateway["id"]


        ga_list = requests.get(
            f"{BASE}/knx/gateway/{gateway_id}/group-addresses",
            headers=headers,
            verify=False,
        ).json()


        for ga in ga_list:

            name = ga.get(
                "name",
                ""
            )


            # Ignore status helper addresses
            if "status" in name.lower():
                continue


            group_addresses[ga["groupAddress"]] = {
                "name": name,
                "dptType": ga.get(
                    "dptType",
                    "unknown"
                )
            }



    #
    # Get devices from 1Home
    #
    onehome_devices = requests.get(
        f"{BASE}/devices?extendedMetadata=true",
        headers=headers,
        verify=False,
    ).json()


    result = []


    for device in onehome_devices.get("devices", []):


        addresses = device.get(
            "metadata",
            {}
        ).get(
            "knxUsedGroupAddresses",
            []
        )


        if not addresses:
            continue



        command_address = addresses[0]


        status_address = (
            addresses[1]
            if len(addresses) > 1
            else addresses[0]
        )



        if command_address not in group_addresses:
            continue



        #
        # Device type from 1Home
        #
        device_type = "unknown"

        if device.get("types"):

            device_type = device["types"][0].get(
                "name",
                "unknown"
            )



        result.append({

            "id": device.get(
                "id"
            ),

            "name": device.get(
                "name",
                "unknown"
            ),


            "room": device.get(
                "roomName",
                "unknown"
            ),


            "type": device_type,


            "icon": device.get(
                "icon",
                ""
            ),


            "groupAddress": command_address,


            "statusAddress": status_address,


            "dptType": group_addresses[command_address]["dptType"]

        })


    print("DEVICES FOR KNX:")
    print(result)


    return result