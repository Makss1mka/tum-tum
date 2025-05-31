from enum import Enum

class VideoStatus(Enum):
    """Enum for video statuses.

    This enum represents the various statuses a video can have in the system.

    Values:
        WAIT_FOR_VIDEO_FILE (1): Video is waiting for the file to be uploaded.
        ON_PRIMARY_MODERATION (2): Video is under primary moderation.
        ON_CHECKING_MODERATION (3): Video is under checking moderation.
        BANNED (4): Video is banned.
        ONLY_FOR_SUBS (5): Video is only available for subscribers.
        ONLY_FOR_VIP_SUBS (6): Video is only available for VIP subscribers.
        ONLY_FOR_PAID_SUBS (7): Video is only available for paid subscribers.
        ONLY_BY_LINK (8): Video can only be accessed via a link.
        HIDDEN (9): Video is hidden from public view.
        PUBLIC (10): Video is publicly accessible.
        WITHOUT_STATUS (11): Video has no specific status assigned.

    Methods:
        from_str(str_value): Returns the status corresponding to the given string value.
        from_num(num_value): Returns the status corresponding to the given numeric value.
        get_str_value(): Returns the string representation of the status.
        get_num_value(): Returns the numeric representation of the status.
    """

    WAIT_FOR_VIDEO_FILE = (1, 'WAIT_FOR_VIDEO_FILE')
    ON_PRIMARY_MODERATION = (2, 'ON_PRIMARY_MODERATION')
    ON_CHECKING_MODERATION = (3, 'ON_CHECKING_MODERATION')
    BANNED = (4, 'BANNED')
    ONLY_FOR_SUBS = (5, 'ONLY_FOR_SUBS')
    ONLY_FOR_VIP_SUBS = (6, 'ONLY_FOR_VIP_SUBS')
    ONLY_FOR_PAID_SUBS = (7, 'ONLY_FOR_PAID_SUBS')
    ONLY_BY_LINK = (8, 'ONLY_BY_LINK')
    HIDDEN = (9, 'HIDDEN')
    PUBLIC = (10, 'PUBLIC')
    WITHOUT_STATUS = (11, 'WITHOUT_STATUS')

    def __init__(self, num_value, str_value):
        self.num_value = num_value
        self.str_value = str_value

    @classmethod
    def from_str(cls, str_value):
        """Получение статуса по строковому значению."""
        return next((status for status in cls if status.str_value == str_value), None)

    @classmethod
    def from_num(cls, num_value):
        """Получение статуса по числовому значению."""
        return next((status for status in cls if status.num_value == num_value), None)

    def get_str_value(self):
        """Получение строкового значения статуса."""
        return self.str_value

    def get_num_value(self):
        """Получение числового значения статуса."""
        return self.num_value
    
    def __str__(self):
        """Строковое представление статуса."""
        return self.str_value


