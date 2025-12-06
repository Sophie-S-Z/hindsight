"""
Configuration module for Hindsight
Loads environment variables and provides config access
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration from environment variables"""
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
    KAFKA_CONSUMER_GROUP = os.getenv("KAFKA_CONSUMER_GROUP")
    KAFKA_CLIENT_ID = os.getenv("KAFKA_CLIENT_ID")
    KAFKA_SASL_USERNAME = os.getenv("KAFKA_SASL_USERNAME")
    KAFKA_SASL_PASSWORD = os.getenv("KAFKA_SASL_PASSWORD")
    
    # iMessage API
    IMESSAGE_API_BASE_URL = os.getenv("IMESSAGE_API_BASE_URL", "https://api.series.dev")
    IMESSAGE_API_KEY = os.getenv("IMESSAGE_API_KEY")
    SENDER_PHONE = os.getenv("SENDER_PHONE")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    @classmethod
    def validate(cls):
        """Validate that all required config values are present"""
        required = [
            "KAFKA_BOOTSTRAP_SERVERS",
            "KAFKA_TOPIC", 
            "KAFKA_CONSUMER_GROUP",
            "KAFKA_SASL_USERNAME",
            "KAFKA_SASL_PASSWORD",
            "IMESSAGE_API_KEY",
            "SENDER_PHONE",
            "OPENAI_API_KEY",
        ]
        
        missing = [key for key in required if not getattr(cls, key)]
        
        if missing:
            raise ValueError(f"Missing required config: {', '.join(missing)}")
        
        return True
