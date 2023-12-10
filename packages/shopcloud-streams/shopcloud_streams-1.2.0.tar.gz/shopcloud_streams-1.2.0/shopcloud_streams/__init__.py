import os
import uuid
from datetime import datetime
import json


import decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


class Event:
    def __init__(self, action: str, context = {}, **kwargs):
        self.action = action
        self.context = context
        self.pk = str(uuid.uuid4())
        self.env = os.environ.get('ENV', 'production')
        self.delay = kwargs.get('delay')

    def fire(self) -> dict:
        event = {
            'action': self.action,
            'pk': self.pk,
            'env': self.env,
            'created_at': datetime.utcnow().isoformat(),
            'context': self.context,
        }
        if self.delay is not None:
            event['delay'] = int(self.delay)
        print('streams-fire {}'.format(json.dumps(event, cls=DecimalEncoder)))
        return event