import os
import sys
import yaml
from termcolor import cprint

from xsetwacom import XSetWacom
from xsetwacom_area_mapping import get_area_bounds

STYLUS_DEVICE = "Tablet Monitor Pen stylus"


def main() -> None:
    xsetwacom = XSetWacom()

    # Set the area
    area = [int(f) for f in get_area_bounds()]
    xsetwacom.set_area(STYLUS_DEVICE, area)

    # Setup button shortcuts
    if len(sys.argv) != 2:
        cprint("Not setting any shortcuts", 'red')
        return

    # For now, only supporting 1 presets file
    entries = os.listdir("presets")
    with open("presets/" + entries[0]) as file:
        all_presets = yaml.safe_load(file)
        all_presets = {k.lower(): v for k, v in all_presets.items()}

    program = sys.argv[1].lower()
    presets = all_presets.get(program)
    if not presets:
        cprint("Couldn't find any presets for: {}".format(program), 'red', file=sys.stderr)
        sys.exit(1)

    print()
    cprint("Setting shortcuts for {}".format(program), 'blue')
    print()
    for k, v in presets.items():
        xsetwacom.set_presets(k, v)


if __name__ == "__main__":
    main()
