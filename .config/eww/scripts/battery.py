#!/bin/python
import time
import json
from pathlib import Path

base_path = Path("/sys/class/power_supply/BAT1")

discharge_total = 0
discharge_total_c = 0

if base_path.exists():
    charge_now_p = base_path / 'charge_now'
    current_now_p = base_path / 'current_now'
    charge_full_p = base_path / 'charge_full'
    status_p = base_path / 'status'

    while True:

        status = status_p.read_text().strip()
        charge_now = int(charge_now_p.read_text().strip())
        # current_now = int(current_now_p.read_text().strip())
        charge_full = int(charge_full_p.read_text().strip())

        capacity = int((charge_now / charge_full) * 100)

        extra_class = ""

        if status == "Discharging":

            # bat_time = charge_now / current_now

            if capacity < 20:
                extra_class = "battery-low"

        elif status == "Charging":
            
            # bat_time = (charge_full - charge_now) / current_now
            extra_class = "charging"

        else:
            bat_time = 0


        # hours = int(bat_time)
        # minutes = int((bat_time - hours) * 60)

        tip = f"{status} {capacity}%"

        print(json.dumps({"tip": tip, "status": extra_class, "capacity": capacity}), flush=True)

        time.sleep(5)
