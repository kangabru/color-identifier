from argparse import ArgumentParser
from os.path import dirname, basename, exists
from PyQt5.QtGui import QColor
from src.util import LoadColorDescriptions, GetClosestColor, ColorDescription, COLOR_DESCRIPTIONS_TYPE
from typing import Dict, List, Tuple

def clean_colors_file(color_file: str, groups_file: str = None, force_remove=False):
    """Copies and cleans a given color description file.
    The cleaning process does the following:
        - Detects duplicates and prompts the user to remove them (if force remove is off).
        - Groups colors by their shade.
        - Sorts groups by their hue.
        - Sorts colors by their grayscale value.

    --color_file: The file to clean. The new file will be saved with a new suffix at the same location.
    --groups_file: An optional groups file to group colors by. If unset then the colors will remain in their original order.
    --force_remove: If set to True, the user will not be prompted to choose which duplicates to remove and the first HEX code occurrence will be kept.
    """
    colors = LoadColorDescriptions(color_file)
    colors = _remove_duplicates(colors, force_remove)

    if groups_file:
        colors_groups = LoadColorDescriptions(groups_file)
        groups = _group_and_sort(colors, colors_groups)
        lines = _get_lines_from_groups(groups)
    else:
        lines = _get_lines_from_colors(colors)

    color_file_new = _get_new_file_name(color_file)
    _save_lines(color_file_new, lines)


def _remove_duplicates(colors: COLOR_DESCRIPTIONS_TYPE, force_remove: bool) -> COLOR_DESCRIPTIONS_TYPE:
    """Removes duplicate colors in a given color description file and returns the result.
    - Duplicate lines are removed entirely.
    - Duplicate hex codes with different description are presented to the user unless force_remove is True.
    """
    hex_index = dict() # We're using dict because the insert order is maintained since Python 3.6.
    for color in colors:
        if color.hex in hex_index:
            color_orig = hex_index[color.hex]

            if force_remove:
                print("Removed duplicate color description:", color)
                continue
            else:
                remove_duplicate = _prompt_to_remove_duplicate(color_orig, color)
                if remove_duplicate: continue
        hex_index[color.hex] = color
    return hex_index.values()


def _prompt_to_remove_duplicate(color_orig: ColorDescription, color_new: ColorDescription) -> bool:
    """Returns True to indicate to remove the duplicate, and False to overwrite the original."""
    print("\nDuplicate lines found:")
    print("\t 1:", color_orig)
    print("\t 2:", color_new)

    attempt = ""
    for i in range(3):
        result = input("Keep '1' or '2'? %s" % attempt)
        if result == "1": return True
        if result == "2": return False
        attempt = "(Attempt %s/3) " % (i + 2)
    print("-> Kept '1'")
    return True


def _group_and_sort(colors: COLOR_DESCRIPTIONS_TYPE, colors_groups: COLOR_DESCRIPTIONS_TYPE) -> Dict[str, COLOR_DESCRIPTIONS_TYPE]:
    """Groups colors by their 'group' which is defined as the description of the closest color in the 'colors_groups' file."""
    groups = dict()
    for color in colors:
        shade = GetClosestColor(color.color, colors_groups)
        group = shade.description
        if group not in groups:
            groups[group] = []
        groups[group].append(color)

    # Sort colors by their grayscale values (light to dark) within their groups
    for group, colors in groups.items():
        colors.sort(key=lambda x: _gray(x.color), reverse=True)

    # Sort groups by their minimum hue
    def get_group_hue(groups_item: Tuple[str, COLOR_DESCRIPTIONS_TYPE]):
        group, colors = groups_item
        return min([c.color.hue() for c in colors])

    groups_list = list(groups.items())
    groups_list.sort(key=get_group_hue)

    groups = { group: colors for group, colors in groups_list }
    return groups


def _gray(color: QColor):
    """Returns the grayscale value of a color between 0 and 255."""
    r, g, b, _ = color.getRgb()
    return int((r * 11 + g * 16 + b * 5) / 32)


def _get_lines_from_colors(colors: COLOR_DESCRIPTIONS_TYPE):
    return [str(color) + "\n" for color in colors]


def _get_lines_from_groups(groups: Dict[str, COLOR_DESCRIPTIONS_TYPE]):
    lines = []
    for group, colors in groups.items():
        group_lines = [str(color) + "\n" for color in colors]
        group_lines.insert(0, "\n// %s\n" % group)
        lines += group_lines
    return lines


def _get_new_file_name(color_file: str) -> str:
    file_name = basename(color_file).split('.')[0]
    file_name_new = "%s-clean" % file_name
    color_file_new = color_file.replace(file_name, file_name_new)
    return color_file_new


def _save_lines(file_name: str, lines: List[str]):
    with open(file_name, 'w') as f:
        f.writelines(lines)


if __name__ == '__main__':
    parser = ArgumentParser("Copies and cleans a given color descriptoin file.")
    parser.add_argument('file_path', help='The path of the color description file to copy and clean.')
    parser.add_argument('-g', '--group-path', help='(Optional) The path of a color description file path used to group colors. If unset then colors will remain in their original order.')
    parser.add_argument('-f', '--force-remove-duplicates', action='store_true', help='If provided then the user will not be prompted to choose which duplicates to remove and the first HEX code occurrence will be kept.')
    args = parser.parse_args()

    # clean_colors_file("colors.txt", "colors-shades.txt")
    clean_colors_file(args.file_path, args.group_path, args.force_remove_duplicates)