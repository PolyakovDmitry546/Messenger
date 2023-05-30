import json
import datetime
from typing import List
from dataclasses import dataclass


class MessageJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        else:
            return super().default(o)


@dataclass
class Message:
    author_id: int
    author_username: str
    text: str
    update_at: datetime

    def to_json(self):
        return json.dumps(self.__dict__, cls=MessageJSONEncoder)
    

@dataclass
class MessageList:
    messages: List[Message]

    def to_json(self):
        return json.dumps([mes.__dict__ for mes in self.messages], cls=MessageJSONEncoder)