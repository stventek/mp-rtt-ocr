import mss.tools

def get_displays():
    with mss.mss() as sct:
        return sct.monitors
