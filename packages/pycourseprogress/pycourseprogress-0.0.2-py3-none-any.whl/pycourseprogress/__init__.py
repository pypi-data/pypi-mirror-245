"""Course Progress entry point."""

import logging

from .api import CourseProgressSession
from .member import Member

_LOGGER = logging.getLogger(__name__)


class CourseProgress:
    """The main Course Progress API."""

    def __init__(self, instance: str):
        """Super init, should only be used for advanced purposes.
        Use the class create method for standard usage."""
        self._api: CourseProgressSession = CourseProgressSession(instance)
        self.members: list[Member] = []
        self.discovered_members: list[int] = []

    def get_member(self, member_id):
        """Return an individual member."""
        member = [x for x in self.members if x.member_id == member_id]
        if len(member) == 1:
            return member[0]
        raise ValueError("Member not found or not yet discovered.")

    async def update(self):
        """Request update of cached data."""
        for member_id in self._api.get_available_member_ids:
            if member_id not in self.discovered_members:
                _LOGGER.debug("Discovered new member %s", member_id)
                member = await Member.create(member_id, self._api)
                self.members.append(member)
                self.discovered_members.append(member_id)
            else:
                await self.get_member(member_id).update()

    @classmethod
    async def create(cls, instance: str, username: str, password: str):
        """Creates an instance of Course Progress."""
        self = cls(instance)
        await self._api.login(username=username, password=password)
        await self.update()
        return self
