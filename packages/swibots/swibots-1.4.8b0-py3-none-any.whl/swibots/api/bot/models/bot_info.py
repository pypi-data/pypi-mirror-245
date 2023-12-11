from typing import TYPE_CHECKING, List, Optional
from swibots.api.common.models import User
from swibots.utils.types import JSONDict
from .bot_command import BotCommand


class BotInfo(User):
    def __init__(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
        username: Optional[str] = None,
        image_url: Optional[str] = None,
        active: Optional[bool] = None,
        deleted: Optional[bool] = None,
        role_info: Optional[str] = None,
        admin: Optional[bool] = None,
        is_bot: Optional[bool] = None,
        commands: Optional[List[BotCommand]] = None,
        description: Optional[str] = None,
        welcome_button: Optional[str] = None,
        welcome_command: Optional[str] = None,
        welcome_text: Optional[str] = None,
        welcome_thumb: Optional[str] = None,
        source_code: Optional[str] = None
    ):
        super().__init__(
            id=id,
            name=name,
            username=username,
            image_url=image_url,
            active=active,
            deleted=deleted,
            role_info=role_info,
            admin=admin,
            is_bot=is_bot,
        )
        self.commands: List[BotCommand] = commands or []
        self.description: Optional[str] = description
        self.welcome_text = welcome_text
        self.welcome_button = welcome_button
        self.welcome_thumb = welcome_thumb
        self.welcome_command = welcome_command
        self.source_code = source_code

    def to_json_request(self) -> JSONDict:
        return {
            "commands": [command.to_json() for command in self.commands],
            "description": self.description,
            "sourceCode": self.source_code
        }

    def from_json(self, data: Optional[JSONDict] = None) -> "BotInfo":
        super().from_json(data)
        if data is not None:
            self.commands = [
                BotCommand().from_json(x) for x in data.get("commands", [])
            ]
            self.description = data.get("description")
            self.welcome_command = data.get("buttonCommand")
            self.welcome_button = data.get("buttonName")
            self.welcome_thumb = data.get("welcomeImage")
            self.source_code = data.get("sourceCode")
            self.welcome_text = data.get("buttonText")
        return self

    def to_json(self) -> JSONDict:
        data = super().to_json()
        if not data.get("commands"):
            data["commands"] = [x.to_json() for x in self.commands]
        if not data.get("description"):
            data["description"] = self.description
        data.update({
            "welcomeImage": self.welcome_thumb,
            "welcomeText": self.welcome_text,
            "buttonName": self.welcome_button,
            "buttonCommand": self.welcome_command,
        })
        return data
