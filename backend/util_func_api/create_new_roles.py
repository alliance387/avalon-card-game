import requests

payload_create_role = {
    "publishParams": {
        "allowed": [
            "audio",
            "video",
            "screen"
        ],
        "audio": {
            "bitRate": 32,
            "codec": "opus"
        },
        "video": {
            "bitRate": 310,
            "codec": "vp8",
            "frameRate": 30,
            "width": 480,
            "height": 360
        },
        "screen": {
            "codec": "vp8",
            "frameRate": 10,
            "width": 1920,
            "height": 1080
        },
        "videoSimulcastLayers": {},
        "screenSimulcastLayers": {}
    },
    "subscribeParams": {
        "subscribeToRoles": [
            "guest",
            "host"
        ],
        "maxSubsBitRate": 3200,
        "subscribeDegradation": {
            "packetLossThreshold": 25,
            "degradeGracePeriodSeconds": 1,
            "recoverGracePeriodSeconds": 4
        }
    },
    "permissions": {
        "endRoom": True,
        "removeOthers": True,
        "mute": True,
        "unmute": True,
        "changeRole": True,
        "sendRoomState": False
    },
    "priority": 1,
    "maxPeerCount": 0
}

def create_new_role(headers: dict,
                    role: str):
    url = f'https://api.100ms.live/v2/templates/66127c9fbc5c70a0ac158bbc/roles/{role}'
    status = requests.request("POST", url, headers=headers, json=payload_create_role)
    print(status)