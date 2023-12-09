"""Define a class for Course Progress."""

import logging

from contextlib import suppress
from datetime import datetime

from .api import CourseProgressSession

_LOGGER = logging.getLogger(__name__)


class Class:
    """A single class for Course Progress."""

    def __init__(self, api: CourseProgressSession, class_id: int, member_id: int) -> None:
        """Init a new class, you should generally call the create method."""
        self._api: CourseProgressSession = api
        self.class_id: int = class_id
        self.class_member_id: int = None
        self.member_id: int = member_id
        self.level_id: int = None
        self.plan_id: int = None
        self.option_id: int = None
        self.discount_id: int = None
        self.active: bool = None
        self.progress: int = None
        self.last_assessment: datetime = None
        self.sessions: int = None
        self.membership_id: int = None
        self.member_membership_id: int = None
        self.move: int = None
        self.move_date: datetime = None
        self.portal_move: int = None
        self.class_name: str = None
        self.class_date: str = None
        self.started: datetime = None
        self.finished: datetime = None
        self.course_name: str = None
        self.sessions: dict = {}
        self.competencies: dict = {}

    async def update(self, class_history_data: dict):
        """Update the local data."""
        _LOGGER.debug("Updating data for class %s", self.class_id)
        response = await self._api.send_http_request(
            endpoint="get_class", MEMBER_ID=str(self.member_id), CLASS_ID=str(self.class_id)
        )
        response = response["response"]["content"]
        self.class_id = response["class_id"]
        self.class_member_id = response["class_member_id"]
        self.active = response["active"] == 1
        self.member_id = response["member_id"]
        self.level_id = response["level_id"]
        self.plan_id = response["plan_id"]
        self.option_id = response["option_id"]
        self.discount_id = response["discount_id"]
        self.progress = response["assessment"]
        with suppress(TypeError):
            self.last_assessment = datetime.strptime(response["last_assessment"], "%Y-%m-%d %H:%M:%S")
        self.sessions = response["sessions"]
        self.membership_id = response["membership_id"]
        self.member_membership_id = response["member_membership_id"]
        self.move = response["move"]
        with suppress(TypeError):
            self.move_date = datetime.strptime(response["move_date"], "%Y-%m-%d %H:%M:%S")
        self.portal_move = response["portal_move"]
        self.class_name = response["class_name"]
        self.class_date = response["class_date"]
        self.course_name = class_history_data["course_name"]
        with suppress(TypeError):
            self.started = datetime.strptime(class_history_data["started"], "%Y-%m-%d %H:%M:%S")
        with suppress(TypeError):
            self.finished = datetime.strptime(class_history_data["finished"], "%Y-%m-%d %H:%M:%S")

        # retrieve sessions.
        response = await self._api.send_http_request(
            endpoint="get_sessions", MEMBER_ID=str(self.member_id), CLASS_ID=str(self.class_id)
        )
        self.sessions = response["response"]["content"]

        # retrieve competencies
        response = await self._api.send_http_request(
            endpoint="get_competencies", MEMBER_ID=str(self.member_id), CLASS_ID=str(self.class_id)
        )
        self.competencies = response["response"]["content"]

    @classmethod
    async def create(cls, api, class_id, member_id, class_history_data) -> 'Class':
        """Create a new instance of a class."""
        self = cls(api, class_id, member_id)
        await self.update(class_history_data)
        return self
