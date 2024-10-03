from enum import Enum

# Embed Limits
MAX_MESSAGE_LENGTH = 100
EMBED_COLOR = 0xf482c1

# COOLDOWNS
GENERAL_COOLDOWN = 5
ADMIN_COOLDOWN = 10

# Role IDs
class Roles(Enum):
    ADMIN = None
    MODERATOR = None
    VIP = None

# Channel IDs
class Channels(Enum):
    GENERAL = None
    ANNOUNCEMENTS = None
    BOT_COMMANDS = None


# Emoji Reactions
THUMBS_UP = None
THUMBS_DOWN = None
MIDDLE_FINGER = None

# Error Messages
ERROR_PERMISSIONS = None
ERROR_COOLDOWN = None

# Success Messages
SUCCESS_COMMANDS = None

