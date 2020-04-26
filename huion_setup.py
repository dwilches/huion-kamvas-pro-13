
import re
import subprocess
import sys
from termcolor import cprint
from typing import List, Optional

from xsetwacom_area_mapping import get_area_bounds

STYLUS_DEVICE = "Tablet Monitor Pen stylus"
PAD_DEVICE = "Tablet Monitor Pad pad"

DEVICE_RE = re.compile(r"(?P<device_name>.*?)\s+id:\s*(?P<device_id>\d+)\s+type:\s*(?P<device_type>.*)")


def main():
    # Set the area
    area = [int(f) for f in get_area_bounds()]
    _xsetwacom_set_area(area)

    # Setup button shortcuts
    if len(sys.argv) == 2:
        if not stylus_device_id:
            print("Couldn't find device", STYLUS_DEVICE, file=sys.stderr)
            sys.exit(1)

        program = sys.argv[1].lower()
        print()
        if program == "blender":
            cprint("Setting shortcuts for Blender", 'blue')
            print()
            _xsetwacom_set_button(1, "ctrl z")   # Undo
            _xsetwacom_set_button(2, "tab")      # Change to Edit modes
            _xsetwacom_set_button(3, "f")        # Change brush size
            _xsetwacom_set_button(8, "shift f")  # Change brush strength
            _xsetwacom_set_button(9, "q")        # Quick Favorites

        elif program == "krita":
            cprint("Setting shortcuts for Krita", 'blue')
            print()
            _xsetwacom_set_button(1, "ctrl z")   # Undo
            _xsetwacom_set_button(2, "e")        # Toggle eraser
            _xsetwacom_set_button(3, "shift")    # Change brush size
            _xsetwacom_set_button(8, "ctrl")     # Pick color
            _xsetwacom_set_button(9, "m")        # Mirror

        else:
            cprint("Not setting any shortcuts", 'red')


def _get_device(raw_devices: List[str], device_name: str) -> int:
    for device in raw_devices:
        match = DEVICE_RE.fullmatch(device)

        if match.group("device_name") == device_name:
            return int(match.group("device_id"))

    print("Couldn't find device", device_name, file=sys.stderr)
    sys.exit(1)


def _xsetwacom_set_area(area: List[int]) -> List[str]:
    return _execute_xsetwacom("set {:d} Area {} {} {} {}".format(stylus_device_id, *area))


def _xsetwacom_set_button(button: int, set_cmd: str) -> List[str]:
    return _execute_xsetwacom("set {:d} Button {:d} 'key {}'".format(pad_device_id, button, set_cmd))


# xsetwacom returns 0 even on error, so this function assumes that any output to stderr means the command failed.
def _execute_xsetwacom(cmd: str) -> Optional[List[str]]:
    full_command = "xsetwacom " + cmd

    cprint("$ {}".format(full_command), 'green')
    result = subprocess.run(full_command, shell=True, capture_output=True, encoding="utf")

    if result.stderr or result.returncode:
        cprint("Command failed with error {}:".format(result.returncode), 'red')
        cprint(result.stderr, 'red')
        sys.exit(1)

    if result.stdout:
        lines = result.stdout.splitlines()
        for line in lines:
            print(line)
        print()
        return lines

    return None


if __name__ == "__main__":
    devices = _execute_xsetwacom("--list devices")
    stylus_device_id = _get_device(devices, STYLUS_DEVICE)
    pad_device_id = _get_device(devices, PAD_DEVICE)
    main()
