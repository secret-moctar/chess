from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
from queue import Queue


class EventType(Enum):
    KeyDown = auto()
    MouseDown = auto()
    MouseUp = auto()
    MouseMove = auto()
    UiButtonClick = auto()
    QuitGame = auto()

@dataclass
class GameEvent:
    type: EventType
    src: str
    data: dict


class EventQueue:
    def __init__(self):
        self._queue = Queue()

    def display(self):
        temp = []
        while not self.is_empty():
            event = self._queue.get()
            temp.append(event)
            print(f"event: {event}")
        for event in temp:
            self.push(event)

    def push(self, event: GameEvent):
        self._queue.put(event)

    def pop(self) -> GameEvent:
        return self._queue.get() if not self.is_empty() else None

    def is_empty(self):
        return self._queue.empty()


class EventDispatcher:
    def __init__(self):
        self._handlers = defaultdict(set)

    def register(self, event_type: EventType, handler):
        self._handlers[event_type].add(handler)

    def display(self):
        for event_type in self._handlers:
            print(f"{event_type} size: {len(self._handlers[event_type])}")
            print(f"{event_type} :{self._handlers[event_type]}")

    def unregister(self, event_type: EventType, handler):
        if event_type in self._handlers:
            if handler in self._handlers[event_type]:
                print(f"handler: {handler} unregistered")
                self._handlers[event_type].remove(handler)
            else:
                print(f" handler: {handler} not registerd")
        else:
            print(f"event type: {EventType} not registered")

    def dispatch(self, event: GameEvent):
        print(f"dispatch: {event}")
        one_button = False
        if event.type not in self._handlers: return
        handlers = list(self._handlers.get(event.type, []))
        for handler in handlers:
            if one_button: break
            print(f"\t handler: {handler}")
            feed_back = handler(event)
            if event.type == EventType.MouseDown:
                one_button = feed_back

event_queue = EventQueue()
event_dispatcher = EventDispatcher()
