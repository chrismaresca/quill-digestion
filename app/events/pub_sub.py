import asyncio
from typing import Callable, Dict, List, Any

class PubSubManager:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}

    def subscribe(self, event_type: str, callback: Callable[[Dict[str, Any]], None]) -> None:
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def publish(self, event_type: str, data: Dict[str, Any]) -> None:
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                asyncio.create_task(callback(data))


pubsub_manager = PubSubManager()
