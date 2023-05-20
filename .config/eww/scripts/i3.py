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

def on_workspace(wm: Connection, e):

    workspaces = wm.get_workspaces()

    widgets = ""

    workspaces.sort(key = lambda x: int(x.name.split(":")[0]))

    for workspace in workspaces:
        classes = ["workspace"]
        if workspace.focused:
            classes.append("focused")
        elif workspace.visible:
            classes.append("visible")
        elif workspace.urgent:
            classes.append("urgent")

        name = workspace.name.split(":")[1]
        widgets += f""" (button :onclick "i3-msg workspace {workspace.name}" :class "{' '.join(classes)}" (label :text "{name}"))"""
    
    print(f"""(box :orientation "h" :space-evenly false :spacing 10 {widgets})""", flush=True)

def on_mode(wm: Connection, e: ModeEvent):
    print(e.change, flush=True)

if "workspaces" in sys.argv:
    i3.on(Event.WORKSPACE, on_workspace)
    on_workspace(i3, None)

if "mode" in sys.argv:
    i3.on(Event.MODE, on_mode)
    print("default", flush=True)

i3.main()