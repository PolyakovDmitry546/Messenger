import json
import datetime
from dataclasses import dataclass


@dataclass
class Message:
    author_id: int
    author_username: str
    text: str
    update_at: datetime

    class MessageJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, datetime.datetime):
                return o.isoformat()
            else:
                return super().default(o)

    def to_json(self):
        return json.dumps(self.__dict__, cls=self.MessageJSONEncoder)