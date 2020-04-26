import re
import subprocess
import sys
from termcolor import cprint
from typing import List, Optional, Dict

DEVICE_RE = re.compile(r"(?P<device_name>.*?)\s+id:\s*(?P<device_id>\d+)\s+type:\s*(?P<device_type>.*)")


class XSetWacom:

    # Dict from device name to device id
    devices: Dict[str, int]

    def __init__(self):
        self._load_devices()

    def set_area(self, device_name: str, area: List[int]) -> None:
        device_id = self._get_device(device_name)

        old_value = XSetWacom._execute_xsetwacom("get {:d} Area".format(device_id), print_command=False)
        XSetWacom._execute_xsetwacom("set {:d} Area {} {} {} {}".format(device_id, *area))
        print("# Previous value: {}".format(old_value[0]))

    def set_presets(self, device_name: str, params: Dict[str, str]) -> None:
        device_id = self._get_device(device_name)

        for param, new_value in params.items():
            old_value = XSetWacom._execute_xsetwacom("get {:d} {}".format(device_id, param), print_command=False)
            XSetWacom._execute_xsetwacom("set {:d} {} '{}'".format(device_id, param, new_value))
            print("# Previous value: {}".format(old_value[0]))

    def _get_device(self, device_name: str) -> int:
        if device_id := self.devices.get(device_name):
            return device_id

        cprint("Couldn't find device: {}".format(device_name), 'red', file=sys.stderr)
        sys.exit(1)

    # Obtains the list of devices according to xsetwacom and assigns it to "devices"
    def _load_devices(self) -> None:
        devices_raw = XSetWacom._execute_xsetwacom("--list devices")
        if devices_raw is None:
            cprint("Couldn't find any device. Is the tablet connected?", 'red', file=sys.stderr)
            sys.exit(1)

        # Print all devices to stdout
        for line in devices_raw:
            print(line)
        print()

        devices = {}
        for device in devices_raw:
            if match := DEVICE_RE.fullmatch(device):
                devices[match.group("device_name")] = int(match.group("device_id"))
            else:
                cprint("Expecting a device specification, found: {}".format(device), 'red', file=sys.stderr)

        self.devices = devices

    # xsetwacom returns 0 even on error, so this function assumes that any output to stderr means the command failed.
    # Returns a list with each line returned by xsetwacom
    @staticmethod
    def _execute_xsetwacom(cmd: str, print_command=True) -> Optional[List[str]]:
        full_command = "xsetwacom " + cmd

        if print_command:
            cprint("$ {}".format(full_command), 'green')

        result = subprocess.run(full_command, shell=True, capture_output=True, encoding="utf")

        if result.stderr or result.returncode:
            cprint("Command '{}' failed with error {}:".format(full_command, result.returncode), 'red')
            cprint(result.stderr, 'red')
            sys.exit(1)

        return result.stdout.splitlines() if result.stdout else None
