import logging
import os
from . import config
from .plotter import timeplot
import atexit

dirs = [config.LOG_DIR, config.PLOT_DIR]
for dir in dirs:
    if not os.path.exists(dir):
        os.makedirs(dir)

logging.basicConfig(
    filename=config.LOG_FILEPATH,
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(name)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

atexit.register(timeplot)