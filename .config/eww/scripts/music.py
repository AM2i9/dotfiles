#!/bin/python
import time
import json
from collections import namedtuple

import dbus

Player = namedtuple('Player', ('name', 'obj'))

session = dbus.SessionBus()

_status = 1

players = {
    "spotify": "",
    "vlc": "󰕼",
    "firefox": "",
    "other": "󰋋"
}


while True:

    if _status == 1:
        _status = 0
        print(json.dumps({"status":"none", "player":"none", "text":"󰋋 Not Playing", "position":0}), flush=True)

    running_players = [
        Player(service.split(".")[3], session.get_object(service, "/org/mpris/MediaPlayer2"))
        for service in session.list_names()
        if service.startswith("org.mpris.MediaPlayer2.")
    ]

    if running_players:
        _status = 1
        running_players.sort(key=lambda p: tuple(players.keys()).index(p.name) if p.name in players else 99)

        cur_player = running_players[0]

        c = 0

        while True:
            try:
                status = cur_player.obj.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus', dbus_interface='org.freedesktop.DBus.Properties')
                metadata = cur_player.obj.Get('org.mpris.MediaPlayer2.Player', 'Metadata', dbus_interface='org.freedesktop.DBus.Properties')

                text_str = f"{players.get(cur_player.name, '󰋋')} {metadata.get('xesam:title') or metadata.get('xesam:url')} - {', '.join(metadata.get('xesam:artist') or ['None'])}"

                data = {
                    "status": status,
                    "player": cur_player.name,
                    "text": text_str,
                    "position": 0.0
                }

                if cur_player.name in ('spotify', 'vlc'):
                    position = cur_player.obj.Get('org.mpris.MediaPlayer2.Player', 'Position', dbus_interface='org.freedesktop.DBus.Properties')
                    data["position"] = 100 * (position/metadata.get('mpris:length')) if metadata.get('mpris:length') != 0 else 0.0

                print(json.dumps(data), flush=True)

                time.sleep(0.5)
            except dbus.exceptions.DBusException as e:
                break
    