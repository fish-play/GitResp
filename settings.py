import os

BASE_DIR = os.getcwd()[:os.getcwd().find("framework\\") + len("framework\\")]
STATIC = os.path.join(BASE_DIR, r"mars\bin\static")


IMAGES = {
    "banner": os.path.join(STATIC, "images","banner.png"),
    "min_win": os.path.join(STATIC, "images","min_win.png"),
    "close": os.path.join(STATIC, "images","close.png"),
    "start_programs": os.path.join(STATIC, "images","start_programs.png"),
    "stop_programs": os.path.join(STATIC, "images","stop_programs.png"),
    "magnifier": os.path.join(STATIC, "images","magnifier.png"),
    "refresh": os.path.join(STATIC, "images","refresh.png"),
    "left": os.path.join(STATIC, "images","left.png"),
    "logo": os.path.join(STATIC, "images","logo.png"),
    "my_programs": os.path.join(STATIC, "images","my_programs.png"),
    "log": os.path.join(STATIC, "images","log.png"),
}