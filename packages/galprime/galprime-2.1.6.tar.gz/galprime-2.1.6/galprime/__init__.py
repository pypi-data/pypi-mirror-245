
__version__ = "2.1.6"

from .backgrounds import *
from .binning import *
from .config import *
from .data import *
from .extraction import *
from .GalPrimeContainer import *
from .koe import *
from .masking import *
from .medians import *
from .modelling import *
from .profiles import *
from .sims import *

# from .densities import *

from . import plotting

def __main__():
    pass


class GalPrimeError(Exception):
    pass


