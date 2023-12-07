"""A package for basic computational tools for LineVision specific physics and maths."""
from os import path
from pathlib import Path

from . import core, dlr, emf, lidar, utils


LVP_DATA_PATH = path.join(Path(__package__).parent, "data/")
del path, Path

__version__ = "0.2.2"
