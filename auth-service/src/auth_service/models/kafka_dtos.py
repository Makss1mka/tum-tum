"""Kafka DTOs module."""

from .entities import UserCredits
from datetime import datetime

class UserCredsCreateKafkaDto:
    """User credentials create Kafka DTO."""
    
    def __init__(self, user_entity: UserCredits):
        self.id: str = str(user_entity.id)
        self.username: str = user_entity.username
        self.email: str = user_entity.email
        self.created_at: datetime = user_entity.created_at

        self.indepotency_id = 'idempotency_' + str(user_entity.id)


class UserCredsDeleteKafkaDto:
    """User credentials delete Kafka DTO."""
    
    def __init__(self, user_entity: UserCredits):
        self.id: str = str(user_entity.id)

        self.indepotency_id = 'idempotency_' + str(user_entity.id)
