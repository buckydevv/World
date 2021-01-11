from .misc import Misc
from .wealth import Wealth
from .guild import Guild
from .paginator import Paginator
from .decorators import *

def initiate(client):
    setattr(client, "misc", Misc)
    setattr(client, "wealth", Wealth)
    setattr(client, "guild", Guild)
    setattr(client, "Paginator", Paginator)