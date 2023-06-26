"""Declares the Job object"""

from fabman.fabman_object import FabmanObject


class Job(FabmanObject):
    """Simple object for handling Jobs. No methods are currently available for Jobs"""

    def __str__(self):
        return f"Job #{self.id}"
