from model.custom_ds import Event as DSEvent
from dataclasses import asdict


class Event(DSEvent):
    def __iter__(self):
        return iter(asdict(self).items())
