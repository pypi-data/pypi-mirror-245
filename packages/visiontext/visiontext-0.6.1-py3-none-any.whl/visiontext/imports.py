"""
Collection of useful imports e.g. for jupyter notebooks. Usage:

>>> from visiontext.imports import *

"""

from collections import defaultdict, Counter

import base64
import hashlib
import io
import json
import numpy as np
import os
import random
import re
import shutil
import sys
import time
from IPython.display import Image, display, HTML
from PIL import Image
from copy import deepcopy
from enum import Enum
from loguru import logger
from matplotlib import pyplot as plt
from pathlib import Path
from pprint import pprint, pformat
from timeit import default_timer as timer
from tqdm import tqdm
from typing import (
    Dict,
    List,
    Optional,
    Any,
    Iterable,
    Mapping,
    Tuple,
    Union,
    Callable,
    BinaryIO,
    Sequence,
    Collection,
)

from packg import format_exception
from packg.iotools.jsonext import load_json, dump_json, loads_json, dumps_json
from packg.log import configure_logger
from packg.magic import reload_recursive
from ovqa.paths import get_annotations_dir, get_cache_dir, get_data_dir, get_library_root_dir
from ovqa.paths import get_output_dir
from packg.strings import b64_encode_from_bytes
from visiontext.images import PILImageScaler
from visiontext.htmltools import NotebookHTMLPrinter, display_html_table

# # the __all__ list below is used to stop pycharm or other tools from removing unused imports
# # to update it after changing the imports above, uncomment the code below and copypaste the output
# imported_modules = [m for m in globals().keys() if not m.startswith("_")]
#
# print(f"__all__ = {repr(sorted(imported_modules))}")

__all__ = [
    "Any",
    "BinaryIO",
    "Callable",
    "Collection",
    "Counter",
    "Dict",
    "Enum",
    "HTML",
    "Image",
    "Iterable",
    "List",
    "Mapping",
    "NotebookHTMLPrinter",
    "Optional",
    "PILImageScaler",
    "Path",
    "Sequence",
    "Tuple",
    "Union",
    "b64_encode_from_bytes",
    "base64",
    "configure_logger",
    "deepcopy",
    "defaultdict",
    "display",
    "display_html_table",
    "dump_json",
    "dumps_json",
    "format_exception",
    "get_annotations_dir",
    "get_cache_dir",
    "get_library_root_dir",
    "get_data_dir",
    "hashlib",
    "io",
    "json",
    "load_json",
    "loads_json",
    "logger",
    "np",
    "os",
    "pformat",
    "plt",
    "pprint",
    "random",
    "re",
    "reload_recursive",
    "shutil",
    "sys",
    "time",
    "timer",
    "tqdm",
]
