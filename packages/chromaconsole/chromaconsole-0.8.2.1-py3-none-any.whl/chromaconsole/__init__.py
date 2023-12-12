#https://en.wikipedia.org/wiki/ANSI_escape_code

from .styling import Styling
from .Color import Color
from .Console import Console
from .Style import Style
from .ColorBackground import Background as background
from .ColorText import Text as text
import argparse

__all__ = ['Styling', 'Color', 'Style', 'Console']

def setup():
    try:
        import sys, os, platform
        from pkg_resources import get_distribution
        
        try:
            import requests

            current_version = get_distribution("chromaconsole").version
            latest_version = requests.get(f'https://pypi.org/pypi/chromaconsole/json').json()['info']['version']

            if tuple(map(int, current_version.split('.'))) < tuple(map(int, latest_version.split('.'))):
                os.system("pip install chromaconsole -U")
        except:
            pass

        def FixWinConsoleColors():
            if platform.system() == "Windows" and sys.stdout and hasattr(sys.stdout, "fileno"):
                try:
                    import ctypes
                    ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
                except Exception:
                    pass

        FixWinConsoleColors()
    except:
        pass

setup()

def color_tuple(color_str):
    if not color_str:
        return ""

    if ',' in color_str:
        try:
            return tuple(map(int, color_str.replace(" ", "").lstrip('(').rstrip(')').split(',')))
        except ValueError:
            raise ValueError(f"Invalid RGB format: {color_str}")
    elif color_str.startswith('#'):
        color_str = color_str.lstrip("#")
        try:
            if len(color_str) == 3:
                r, g, b = (int(c * 2, 16) for c in color_str)
            elif len(color_str) == 6:
                r, g, b = (int(color_str[i:i+2], 16) for i in range(0, 6, 2))
            else:
                raise ValueError("Invalid color format")
        except ValueError:
            raise ValueError(f"Invalid hex color format: {color_str}")
        
        return (r, g, b)
    else:
        raise ValueError("Invalid color format")

def console_line(textcolor='', backgroundcolor=''):
    parser = argparse.ArgumentParser(description="Print colored text to the console.")
    parser.add_argument("-c", "--textcolor", default=textcolor, help="color code (e.g., #ff0000 or 255,0,0)")
    parser.add_argument("-b", "--backgroundcolor", default=backgroundcolor, help="color code (e.g., #ff0000 or 255,0,0)")
    parser.add_argument("-B", "--bold", action="store_true", help="Make the text bold")
    parser.add_argument("-I", "--italic", action="store_true", help="Make the text italic")
    parser.add_argument("-U", "--underline", action="store_true", help="Make the text underlined")
    parser.add_argument("-s", "--slowblink", action="store_true", help="Make the text slow blink")
    parser.add_argument("-r", "--rapidblink", action="store_true", help="Make the text rapid blink")
    parser.add_argument("-R", "--reverse", action="store_true", help="reverse bg and text color")
    parser.add_argument("-H", "--hidden", action="store_true", help="Make the text hidden")
    parser.add_argument("-S", "--strikethrough", action="store_true", help="Make the text strikethrough")
    parser.add_argument("-D", "--doublyunderlined", action="store_true", help="Make the text doubly underlined")
    parser.add_argument("-P", "--proportionalspacing", action="store_true", help="Make the text proportional spacing")
    parser.add_argument("-O", "--overlined", action="store_true", help="Make the text overlined")
    parser.add_argument("-X", "--reset", action="store_true", help="reset all to default")

    args = parser.parse_args()

    print(
        f"{Color.text(color_tuple(args.textcolor))}"
        f"{Color.background(color_tuple(args.backgroundcolor))}"
        f"{Style.bold() if args.bold else ''}"
        f"{Style.italic() if args.italic else ''}"
        f"{Style.underlined() if args.underline else ''}"
        f"{Style.slow_blink() if args.slowblink else ''}"
        f"{Style.rapid_blink() if args.rapidblink else ''}"
        f"{Style.reverse() if args.reverse else ''}"
        f"{Style.hidden() if args.hidden else ''}"
        f"{Style.strikethrough() if args.strikethrough else ''}"
        f"{Style.doubly_underlined() if args.doublyunderlined else ''}"
        f"{Style.proportional_spacing() if args.proportionalspacing else ''}"
        f"{Style.overlined() if args.overlined else ''}"
        f"{Style.reset() if args.reset else ''}")

def check_ver():
    try:
        from pkg_resources import get_distribution
        import requests
        print(f"current: {get_distribution('chromaconsole').version}\n latest: {requests.get(f'https://pypi.org/pypi/chromaconsole/json').json()['info']['version']}")
    except:
        print(f"Something went wrong")

if __name__ == "__main__":
    console_line()
    check_ver()
