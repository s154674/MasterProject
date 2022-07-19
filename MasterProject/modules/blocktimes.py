from enum import Enum

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