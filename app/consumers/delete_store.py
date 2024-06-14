# app/consumers/delete_store_consumer.py
import logging
import redis.exceptions
from typing import Dict, Any

from app.consumers.callback_wrapper import callback_wrapper
from app.clients import RedisClient
from app.payloads import DeleteStorePayload
from app.interface import delete_store

# Event and consumer details
EVENT_NAME = 'DELETE_STORE_EVENT'
CONSUMER_GROUP = 'delete_store_group'
CONSUMER_NAME = 'delete_store_consumer_1'

@callback_wrapper
async def delete_store_callback(event: Dict[str, Any]):
    """
    Handling of the delete store process.
    """
    try:
        payload = DeleteStorePayload(**event)
        await delete_store(payload)
    except Exception as e:
        logging.error(f"Error in delete_store_callback: {e}")
        raise

async def consume_delete_store(redis_client: RedisClient):
    """
    Consumer functionality for DeleteStore. Uses the redis client for implementation.
    """
    try:
        redis_client.register_event(event_name=EVENT_NAME, group_name=CONSUMER_GROUP)
    except redis.exceptions.ResponseError:
        logging.warning('Consumer group already exists, continuing with existing group.')
    except Exception as e:
        logging.error(f"Error registering event: {e}")
        return

    try:
        await redis_client.consume_events(event_name=EVENT_NAME, group_name=CONSUMER_GROUP, consumer_name=CONSUMER_NAME, callback=delete_store_callback)
    except Exception as e:
        logging.error(f"Error consuming events: {e}")
