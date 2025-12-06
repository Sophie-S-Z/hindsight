"""
iMessage API Client for Hindsight
Handles all communication with the Series iMessage API
"""

import requests
from typing import Optional
import time

from .config import Config


class IMessageClient:
    """Client for the Series iMessage API"""
    
    def __init__(self):
        self.base_url = Config.IMESSAGE_API_BASE_URL
        self.api_key = Config.IMESSAGE_API_KEY
        self.sender_phone = Config.SENDER_PHONE
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make an API request with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            print(f"Response: {e.response.text if e.response else 'No response'}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            raise
    
    def check_imessage_availability(self, phone_number: str) -> bool:
        """Check if a phone number is available for iMessage"""
        try:
            result = self._make_request(
                "POST",
                "/api/i_message_availability/check",
                json={"phone_number": phone_number}
            )
            return result.get("available", False)
        except Exception as e:
            print(f"Error checking iMessage availability: {e}")
            return False
    
    def create_chat(self, recipient_phone: str, initial_message: str) -> Optional[dict]:
        """Create a new chat with an initial message"""
        payload = {
            "chat": {
                "phone_numbers": [recipient_phone],
                "display_name": "Future You ✨"
            },
            "message": {
                "text": initial_message
            },
            "send_from": self.sender_phone
        }
        
        try:
            return self._make_request("POST", "/api/chats", json=payload)
        except Exception as e:
            print(f"Error creating chat: {e}")
            return None
    
    def send_message(self, chat_id: str, text: str) -> Optional[dict]:
        """Send a message to an existing chat"""
        payload = {
            "message": {
                "text": text
            }
        }
        
        try:
            return self._make_request(
                "POST",
                f"/api/chats/{chat_id}/chat_messages",
                json=payload
            )
        except Exception as e:
            print(f"Error sending message: {e}")
            return None
    
    def get_chat(self, chat_id: str) -> Optional[dict]:
        """Get chat details"""
        try:
            return self._make_request("GET", f"/api/chats/{chat_id}")
        except Exception as e:
            print(f"Error getting chat: {e}")
            return None
    
    def list_chats(self) -> list:
        """List all chats"""
        try:
            result = self._make_request("GET", "/api/chats")
            return result.get("chats", [])
        except Exception as e:
            print(f"Error listing chats: {e}")
            return []
    
    def get_messages(self, chat_id: str) -> list:
        """Get messages from a chat"""
        try:
            result = self._make_request("GET", f"/api/chats/{chat_id}/chat_messages")
            return result.get("messages", [])
        except Exception as e:
            print(f"Error getting messages: {e}")
            return []
    
    def start_typing(self, chat_id: str) -> bool:
        """Start typing indicator"""
        try:
            self._make_request("POST", f"/api/chats/{chat_id}/start_typing")
            return True
        except Exception as e:
            print(f"Error starting typing indicator: {e}")
            return False
    
    def stop_typing(self, chat_id: str) -> bool:
        """Stop typing indicator"""
        try:
            self._make_request("DELETE", f"/api/chats/{chat_id}/stop_typing")
            return True
        except Exception as e:
            print(f"Error stopping typing indicator: {e}")
            return False
    
    def send_with_typing_indicator(self, chat_id: str, text: str, typing_duration: float = 2.0) -> Optional[dict]:
        """Send a message with a realistic typing indicator delay"""
        # Start typing
        self.start_typing(chat_id)
        
        # Calculate typing time based on message length (roughly 50 chars/sec)
        chars = len(text)
        calculated_duration = min(max(chars / 50, 1.0), 5.0)  # Between 1-5 seconds
        actual_duration = max(typing_duration, calculated_duration)
        
        time.sleep(actual_duration)
        
        # Stop typing and send
        self.stop_typing(chat_id)
        return self.send_message(chat_id, text)
    
    def react_to_message(self, message_id: str, reaction_type: str = "love") -> bool:
        """React to a message"""
        valid_reactions = ["love", "like", "dislike", "laugh", "emphasize", "question"]
        if reaction_type not in valid_reactions:
            print(f"Invalid reaction type: {reaction_type}")
            return False
        
        payload = {
            "operation": "add",
            "type": reaction_type
        }
        
        try:
            self._make_request("POST", f"/api/chat_messages/{message_id}/reactions", json=payload)
            return True
        except Exception as e:
            print(f"Error adding reaction: {e}")
            return False
    
    def mark_as_read(self, chat_id: str) -> bool:
        """Mark a chat as read"""
        try:
            self._make_request("PUT", f"/api/chats/{chat_id}/mark_as_read")
            return True
        except Exception as e:
            print(f"Error marking chat as read: {e}")
            return False


# Singleton instance
_client_instance: Optional[IMessageClient] = None

def get_client() -> IMessageClient:
    """Get the singleton client instance"""
    global _client_instance
    if _client_instance is None:
        _client_instance = IMessageClient()
    return _client_instance
