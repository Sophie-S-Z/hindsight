"""
Kafka Message Handler for Hindsight
Processes incoming messages from the Kafka stream and orchestrates responses
"""

import json
import asyncio
from typing import Optional, Callable
from kafka import KafkaConsumer
from datetime import datetime

from .config import Config
from .persona import get_persona
from .imessage_client import get_client
from .memory import MemoryManager


class MessageHandler:
    """Handles incoming messages and generates responses"""
    
    def __init__(self):
        self.persona = get_persona()
        self.imessage = get_client()
        self.chat_mapping = {}  # phone_number -> chat_id
    
    async def handle_message(self, event_data: dict) -> Optional[str]:
        """
        Process an incoming message event and generate a response.
        
        Args:
            event_data: The parsed Kafka message payload
            
        Returns:
            The response text if successful, None otherwise
        """
        event_type = event_data.get("event_type") or event_data.get("type")
        
        print(f"\n{'='*50}")
        print(f"Received event: {event_type}")
        print(f"Data: {json.dumps(event_data, indent=2)[:500]}...")
        
        # Handle different event types
        if event_type == "message.received":
            return await self._handle_incoming_message(event_data)
        elif event_type == "typing_indicator.received":
            return await self._handle_typing_indicator(event_data)
        elif event_type == "reaction.received":
            return await self._handle_reaction(event_data)
        else:
            print(f"Unhandled event type: {event_type}")
            return None
    
    async def _handle_incoming_message(self, event_data: dict) -> Optional[str]:
        """Handle an incoming text message"""
        
        # Extract message details - handle different payload structures
        message_data = event_data.get("data", event_data)
        message_text = (
            message_data.get("text") or 
            message_data.get("message", {}).get("text") or
            message_data.get("body")
        )
        
        if not message_text:
            print("No message text found in event")
            return None
        
        # Get sender info
        sender_phone = (
            message_data.get("sender_phone") or 
            message_data.get("from") or
            message_data.get("sender", {}).get("phone")
        )
        
        chat_id = (
            message_data.get("chat_id") or 
            message_data.get("conversation_id")
        )
        
        print(f"\nProcessing message from {sender_phone}: {message_text[:100]}...")
        
        # Store chat mapping for future responses
        if sender_phone and chat_id:
            self.chat_mapping[sender_phone] = chat_id
        
        # Generate response from future self
        try:
            response_text, profile_updates = await self.persona.generate_response(
                user_message=message_text,
                phone_number=sender_phone or "unknown"
            )
            
            print(f"\nGenerated response: {response_text[:200]}...")
            
            # Send the response
            if chat_id:
                # Use typing indicator for natural feel
                result = self.imessage.send_with_typing_indicator(
                    chat_id=chat_id,
                    text=response_text,
                    typing_duration=2.0
                )
                
                if result:
                    print(f"Response sent successfully!")
                    return response_text
                else:
                    print("Failed to send response")
                    return None
            else:
                print("No chat_id available, cannot send response")
                return response_text  # Return anyway for logging
                
        except Exception as e:
            print(f"Error generating/sending response: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def _handle_typing_indicator(self, event_data: dict) -> None:
        """Handle typing indicator (user is typing)"""
        # Could use this to prepare response or show "future self is thinking"
        print("User is typing...")
        return None
    
    async def _handle_reaction(self, event_data: dict) -> None:
        """Handle reaction to a message"""
        reaction_data = event_data.get("data", event_data)
        reaction_type = reaction_data.get("type") or reaction_data.get("reaction")
        print(f"Received reaction: {reaction_type}")
        
        # Could respond to reactions in fun ways
        # For now, just acknowledge
        return None
    
    def get_or_create_chat(self, phone_number: str, initial_message: str) -> Optional[str]:
        """Get existing chat or create new one"""
        if phone_number in self.chat_mapping:
            return self.chat_mapping[phone_number]
        
        # Create new chat
        result = self.imessage.create_chat(phone_number, initial_message)
        if result and "id" in result:
            self.chat_mapping[phone_number] = result["id"]
            return result["id"]
        
        return None


class KafkaMessageConsumer:
    """Consumes messages from Kafka and routes to handler"""
    
    def __init__(self, handler: Optional[MessageHandler] = None):
        self.handler = handler or MessageHandler()
        self.consumer = None
        self.running = False
    
    def _create_consumer(self) -> KafkaConsumer:
        """Create and configure the Kafka consumer"""
        return KafkaConsumer(
            Config.KAFKA_TOPIC,
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS.split(","),
            security_protocol="SASL_SSL",
            sasl_mechanism="PLAIN",
            sasl_plain_username=Config.KAFKA_SASL_USERNAME,
            sasl_plain_password=Config.KAFKA_SASL_PASSWORD,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="latest",  # Only get new messages
            enable_auto_commit=True,
            group_id=Config.KAFKA_CONSUMER_GROUP,
            consumer_timeout_ms=1000,  # Check for stop signal every second
        )
    
    async def start(self):
        """Start consuming messages"""
        print(f"\n{'='*60}")
        print("🔮 HINDSIGHT - Your Future Self Awaits")
        print(f"{'='*60}")
        print(f"\nConnecting to Kafka...")
        print(f"Topic: {Config.KAFKA_TOPIC}")
        print(f"Consumer Group: {Config.KAFKA_CONSUMER_GROUP}")
        
        self.consumer = self._create_consumer()
        self.running = True
        
        print("\n✅ Connected! Waiting for messages...")
        print("(Send a text to start a conversation with your future self)\n")
        
        try:
            while self.running:
                # Poll for messages
                try:
                    for message in self.consumer:
                        if not self.running:
                            break
                        
                        print(f"\n📨 New message received at {datetime.now()}")
                        
                        try:
                            await self.handler.handle_message(message.value)
                        except Exception as e:
                            print(f"Error handling message: {e}")
                            import traceback
                            traceback.print_exc()
                            
                except StopIteration:
                    # No messages, continue polling
                    await asyncio.sleep(0.1)
                    
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down gracefully...")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the consumer"""
        self.running = False
        if self.consumer:
            self.consumer.close()
            print("Consumer closed.")


# Factory function
def create_consumer() -> KafkaMessageConsumer:
    """Create a new Kafka message consumer"""
    return KafkaMessageConsumer()
