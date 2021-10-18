from enum import Enum

class COG_ID(Enum):
    IMAGES = (1, 'Images')
    FUN = (2, 'Fun')
    INFO = (3, 'Information')
    ADMIN = (4, 'Admin only')
    TOOLS = (5, 'Tools')
    UNKNOWN = (6, 'No category')