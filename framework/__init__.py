from .misc import Misc
from .wealth import Wealth
from .guild import Guild

def initiate(client):
    setattr(client, "misc", Misc)
    setattr(client, "wealth", Wealth)
    setattr(client, "guild", Guild)
