"""User credentials service module."""

from globals import KAFKA_BOOTSTRAP_SERVERS, KAFKA_USER_CREDS_CREATE_TOPIC, KAFKA_USER_CREDS_DELETE_TOPIC
from models.kafka_dtos import UserCredsCreateKafkaDto, UserCredsDeleteKafkaDto
from log.loggers import KAFKA_SERVICE_LOGGER, APP_LOGGER
from log.wrappers import log_entrance_debug
from aiokafka import AIOKafkaProducer
from typing import Optional
import json


class KafkaProducer:
    _instance: Optional['KafkaProducer'] = None
    _producer: Optional[AIOKafkaProducer] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    async def start(self):
        """Initialize the producer (call during app startup)"""

        APP_LOGGER.info("Starting Kafka producer...")

        if self._producer is None or self._producer._closed:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
            )
            await self._producer.start()

        APP_LOGGER.info("Kafka producer started.")


    async def stop(self):
        """Close connections (call during app shutdown)"""

        APP_LOGGER.info("Stopping Kafka producer...")

        if self._producer and not self._producer._closed:
            await self._producer.stop()


    @log_entrance_debug(KAFKA_SERVICE_LOGGER)
    async def publish_user_creds_create_event(self, user_dto: UserCredsCreateKafkaDto):
        """Publishes user credentials create event to Kafka."""

        if not self._producer:
            raise RuntimeError("Producer not initialized")
        
        try:
            await self._producer.send(
                KAFKA_USER_CREDS_CREATE_TOPIC,
                value=json.dumps(user_dto).encode('utf-8')
            )
        except Exception as e:
            KAFKA_SERVICE_LOGGER.exception(f"Cannot send message in topic {KAFKA_USER_CREDS_CREATE_TOPIC}: ", e)


    @log_entrance_debug(KAFKA_SERVICE_LOGGER)
    async def publish_user_creds_delete_event(self, user_dto: UserCredsDeleteKafkaDto):
        """Publishes user credentials delete event to Kafka."""
        
        if not self._producer:
            raise RuntimeError("Producer not initialized")
        
        try:
            await self._producer.send(
                KAFKA_USER_CREDS_DELETE_TOPIC,
                value=json.dumps(user_dto).encode('utf-8')
            )
        except Exception as e:
            KAFKA_SERVICE_LOGGER.exception(f"Cannot send message in topic {KAFKA_USER_CREDS_DELETE_TOPIC}: ", e)