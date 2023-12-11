"""Definition of a Course Progress member."""

import logging

from .api import CourseProgressSession
from .classes import Class

_LOGGER = logging.getLogger(__name__)


class Member:
    """Represents a member."""

    def __init__(self, api: CourseProgressSession, member_id: int) -> None:
        """Initialize a new member."""
        self._api = api
        self.member_id = member_id
        self.card_id = None
        self.first_name = ""
        self.last_name = ""
        self.email_address = ""
        self.classes: list[Class] = []
        self.discovered_classes: list[int] = []
        self.raw = {}

    def get_class(self, class_id: int = -1, class_name: str = "") -> Class:
        """Return a single class by its name or ID."""
        data = [x for x in self.classes if x.class_id == class_id or x.class_name == class_name]
        if len(data) == 1:
            return data[0]
        raise ValueError("Unable to find class with given query.")

    async def update(self):
        """Update instance data."""
        _LOGGER.debug("Updating member %s", self.member_id)
        response = await self._api.send_http_request(endpoint="get_member", MEMBER_ID=str(self.member_id))
        response = response["response"]["content"]
        self.first_name = response["first_name"]
        self.last_name = response["last_name"]
        self.card_id = response["card_id"]
        self.email_address = response["email_address"]
        self.raw = response
        # now do the classes
        response = await self._api.send_http_request(endpoint="get_classes_history", MEMBER_ID=str(self.member_id))
        response = response["response"]["content"]
        for member_class in response:
            if member_class["class_id"] not in self.discovered_classes:
                _LOGGER.debug("Discovered new class %s for member %s", member_class["class_id"], self.member_id)
                self.classes.append(
                    await Class.create(
                        api=self._api,
                        class_id=member_class["class_id"],
                        member_id=self.member_id,
                        class_history_data=member_class,
                    )
                )
                self.discovered_classes.append(member_class["class_id"])
            else:
                await self.get_class(member_class["class_id"]).update(class_history_data=member_class)

    @classmethod
    async def create(cls, member_id: int, api: CourseProgressSession) -> 'Member':
        """Create a new instance of member for a given ID."""
        new_member = cls(api, member_id)
        await new_member.update()
        return new_member
