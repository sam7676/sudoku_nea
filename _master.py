from time import perf_counter
start_time=perf_counter()

from converter import *
from front import *
from solver import *
from training import *
from imports import *
from database import *

print(f"Start time: {round(perf_counter()-start_time,3)}s")
front_end()