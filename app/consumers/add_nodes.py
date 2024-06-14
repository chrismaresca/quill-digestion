import logging
import redis.exceptions
from typing import Dict, Any

from app.consumers.callback_wrapper import callback_wrapper
from app.clients import RedisClient
from app.payloads import AddNodesPayload
from app.interface import add_nodes

# Event and consumer details
EVENT_NAME = 'ADD_NODES_EVENT'
CONSUMER_GROUP = 'add_nodes_group'
CONSUMER_NAME = 'add_nodes_consumer_1'

@callback_wrapper
async def add_nodes_callback(event: Dict[str, Any]):
    """
    Handling of the add nodes process.
    """
    try:
        payload = AddNodesPayload(**event)
        await add_nodes(payload)
    except Exception as e:
        logging.error(f"Error in add_nodes_callback: {e}")
        raise

async def consume_add_nodes(redis_client: RedisClient):
    """
    Consumer functionality for AddNodes. Uses the redis client for implementation.
    """
    try:
        redis_client.register_event(event_name=EVENT_NAME, group_name=CONSUMER_GROUP)
    except redis.exceptions.ResponseError:
        logging.warning('Consumer group already exists, continuing with existing group.')
    except Exception as e:
        logging.error(f"Error registering event: {e}")
        return

    try:
        await redis_client.consume_events(event_name=EVENT_NAME, group_name=CONSUMER_GROUP, consumer_name=CONSUMER_NAME, callback=add_nodes_callback)
    except Exception as e:
        logging.error(f"Error consuming events: {e}")
