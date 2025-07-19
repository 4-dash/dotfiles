#!/usr/bin/env python3

import subprocess
import json

def get_player_status():
    try:
        status = subprocess.check_output(["playerctl", "status"], stderr=subprocess.DEVNULL)
        return status.strip().decode()
    except subprocess.CalledProcessError:
        return "Inactive"

def is_muted():
    try:
        output = subprocess.check_output(
            ["wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@"], stderr=subprocess.DEVNULL
        ).decode()
        return "MUTED" in output
    except subprocess.CalledProcessError:
        return False

def get_metadata():
    try:
        artist = subprocess.check_output(["playerctl", "metadata", "artist"], stderr=subprocess.DEVNULL).strip().decode()
        title = subprocess.check_output(["playerctl", "metadata", "title"], stderr=subprocess.DEVNULL).strip().decode()
        return f"{artist} - {title}"
    except subprocess.CalledProcessError:
        return "Unknown track"

def main():
    status = get_player_status()
    muted = is_muted()

    output = {
        "text": "",
        "class": "inactive",
        "tooltip": ""
    }

    if status == "Playing":
        metadata = get_metadata()
        output["text"] = " playing" #f" {metadata}"
        output["class"] = "playing-muted" if muted else "playing"
        output["tooltip"] = f"{metadata}\n\nClick to pause\nRight click to mute\nScroll to adjust volume"

    elif status == "Paused":
        metadata = get_metadata()
        output["text"] = " paused" #f" {metadata}"
        output["class"] = "paused-muted" if muted else "paused"
        output["tooltip"] = f"{metadata}\n\nClick to resume\nRight click to mute\nScroll to adjust volume"

    elif status == "Stopped":
        output["text"] = "■ Stopped"
        output["class"] = "stopped-muted" if muted else "stopped"
        output["tooltip"] = "Media is stopped.\nClick to start."

    else:
        output["text"] = "" #"No media 󰎇"
        output["class"] = "inactive"
        output["tooltip"] = "" #"Nothing is playing."

    print(json.dumps(output))

if __name__ == "__main__":
    main()

