#!/bin/python

# REMEMBER: install i3ipc on system interpreter, make sure it's
# not being installed to just a pyenv installation, beacuse it
# won't use that.

import sys

try:
    from i3ipc import Connection, Event, ModeEvent
except ImportError:
    if "workspaces" in sys.argv:
        print(f"""(box :class "workspace" :orientation "h" :space-evenly false :spacing 10 "'i3pc' not installed")""", flush=True)
    elif "mode" in sys.argv:
        print("default", flush=True)
    sys.exit(0)

i3 = Connection()

workspaces = ["", "", "󰨞", "", "", "", "", "", "", "󰙯"]

def on_workspace(wm: Connection, e):

    open_workspaces = {wrk.num: wrk for wrk in wm.get_workspaces()}

    widgets = ""

    for i, workspace in enumerate(workspaces):
        classes = ["workspace"]

        if (wrk := open_workspaces.get(i+1)):
            
            classes.append("open")

            if wrk.focused:
                classes.append("focused")
            elif wrk.visible:
                classes.append("visible")
            elif wrk.urgent:
                classes.append("urgent")
            

        widgets += f""" (button :onclick "i3-msg workspace {i+1}" :class "{' '.join(classes)}" (label :text "{workspace}"))"""
    

    print(f"""(box :orientation "h" :space-evenly false :spacing 1 {widgets})""", flush=True)

def on_mode(wm: Connection, e: ModeEvent):
    print(e.change, flush=True)

if "workspaces" in sys.argv:
    i3.on(Event.WORKSPACE, on_workspace)
    on_workspace(i3, None)

if "mode" in sys.argv:
    i3.on(Event.MODE, on_mode)
    print("default", flush=True)

i3.main()
