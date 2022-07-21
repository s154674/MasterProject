from enum import Enum
from events.models import Networks, BlockTimes
import numpy as np
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial as P

class MainBlocks(Enum):
    # All block between the 1st and 7th (inclusive) of july 2022
    FIRST_WEEK_JULY = (15053226, 15098519) 
    JUNE = (14881650, 15053225)
    ALL = (14881650, 15098519)

class OptiBlocks(Enum):
    # All block between the 1st and 7th (inclusive) of july 2022
    FIRST_WEEK_JULY = (86417, 89163) 
    JUNE = (63340, 86416)
    ALL = (63340, 89163)

class ArbiBlocks(Enum):
    # All block between the 1st and 7th (inclusive) of july 2022
    FIRST_WEEK_JULY = (16662000, 17220200) 
    JUNE = (13383500, 16661999)
    ALL = (13383500, 17220200)

class PolyBlocks(Enum):
    # All block between the 1st and 7th (inclusive) of july 2022
    FIRST_WEEK_JULY = (30194060, 30462400)
    JUNE = (29011700, 30194059)
    ALL = (29011700, 30462400)


class Blocktimes():
    def __init__(self, network):
        x = []
        y = []
        blocks = BlockTimes.objects.filter(network=network)
        for block in blocks:
            x.append(block.blockNumber)
            y.append(int(block.timestamp))
        # print(x,y)
        self.model = np.poly1d(np.polyfit(x,y,2))
        
    
        # print(r2_score(y, model(x)))

    def get_blocktime(self, x):
        return int(self.model(x))

    def expand_timestamp(self, ts):
        lower = ts - 30*60
        upper = ts + 30*60
        
            
    def get_range(self, block, minutes=30):
        ts = int(self.model(block))
        lower = ts - minutes*60
        upper = ts + minutes*60
        return (lower, upper)

    def test(self, number):
        p = P.fit(self.model)
        return (p - number).roots()