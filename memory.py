"""
Memory module for Hindsight
Manages conversation history and user context for personalized interactions
"""

import json
import os
from datetime import datetime
from typing import Optional
from pathlib import Path


class UserMemory:
    """
    Stores and retrieves user context and conversation history.
    Each user gets their own memory file for persistence.
    """
    
    MEMORY_DIR = Path("data/memories")
    
    def __init__(self, phone_number: str):
        self.phone_number = self._normalize_phone(phone_number)
        self.memory_file = self.MEMORY_DIR / f"{self.phone_number}.json"
        self._ensure_memory_dir()
        self.data = self._load()
    
    def _normalize_phone(self, phone: str) -> str:
        """Normalize phone number to consistent format"""
        return phone.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    
    def _ensure_memory_dir(self):
        """Create memory directory if it doesn't exist"""
        self.MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    
    def _load(self) -> dict:
        """Load existing memory or create new"""
        if self.memory_file.exists():
            with open(self.memory_file, "r") as f:
                return json.load(f)
        return self._create_fresh_memory()
    
    def _create_fresh_memory(self) -> dict:
        """Initialize a new user memory structure"""
        return {
            "phone_number": self.phone_number,
            "created_at": datetime.now().isoformat(),
            "profile": {
                "name": None,
                "current_struggles": [],
                "hopes_and_dreams": [],
                "important_people": [],
                "current_situation": None,
                "personality_notes": [],
                "emotional_patterns": [],
            },
            "conversation_history": [],
            "insights": [],  # Things future self has "learned" about them
            "check_in_streak": 0,
            "last_interaction": None,
            "emotional_state_history": [],
        }
    
    def save(self):
        """Persist memory to disk"""
        with open(self.memory_file, "w") as f:
            json.dump(self.data, f, indent=2, default=str)
    
    def add_message(self, role: str, content: str, emotional_tone: Optional[str] = None):
        """Add a message to conversation history"""
        message = {
            "role": role,  # "user" or "future_self"
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "emotional_tone": emotional_tone,
        }
        self.data["conversation_history"].append(message)
        self.data["last_interaction"] = datetime.now().isoformat()
        
        # Keep last 50 messages for context
        if len(self.data["conversation_history"]) > 50:
            self.data["conversation_history"] = self.data["conversation_history"][-50:]
        
        self.save()
    
    def update_profile(self, updates: dict):
        """Update user profile with new information"""
        for key, value in updates.items():
            if key in self.data["profile"]:
                if isinstance(self.data["profile"][key], list):
                    if isinstance(value, list):
                        self.data["profile"][key].extend(value)
                    else:
                        self.data["profile"][key].append(value)
                    # Deduplicate
                    self.data["profile"][key] = list(set(self.data["profile"][key]))
                else:
                    self.data["profile"][key] = value
        self.save()
    
    def add_insight(self, insight: str):
        """Add an insight the future self has learned"""
        self.data["insights"].append({
            "insight": insight,
            "timestamp": datetime.now().isoformat()
        })
        self.save()
    
    def record_emotional_state(self, state: str, context: str = None):
        """Track emotional state over time"""
        self.data["emotional_state_history"].append({
            "state": state,
            "context": context,
            "timestamp": datetime.now().isoformat()
        })
        # Keep last 20 emotional states
        if len(self.data["emotional_state_history"]) > 20:
            self.data["emotional_state_history"] = self.data["emotional_state_history"][-20:]
        self.save()
    
    def get_conversation_context(self, last_n: int = 10) -> list:
        """Get recent conversation history for context"""
        return self.data["conversation_history"][-last_n:]
    
    def get_profile_summary(self) -> str:
        """Generate a summary of what we know about the user"""
        profile = self.data["profile"]
        parts = []
        
        if profile.get("name"):
            parts.append(f"Their name is {profile['name']}.")
        
        if profile.get("current_situation"):
            parts.append(f"Current situation: {profile['current_situation']}")
        
        if profile.get("current_struggles"):
            parts.append(f"They're dealing with: {', '.join(profile['current_struggles'][:3])}")
        
        if profile.get("hopes_and_dreams"):
            parts.append(f"They hope to: {', '.join(profile['hopes_and_dreams'][:3])}")
        
        if profile.get("important_people"):
            parts.append(f"Important people in their life: {', '.join(profile['important_people'][:3])}")
        
        if profile.get("personality_notes"):
            parts.append(f"Personality: {', '.join(profile['personality_notes'][:3])}")
        
        if self.data.get("insights"):
            recent_insights = [i["insight"] for i in self.data["insights"][-3:]]
            parts.append(f"Key insights: {'; '.join(recent_insights)}")
        
        return " ".join(parts) if parts else "This is a new conversation. We don't know much about them yet."
    
    def get_emotional_trend(self) -> Optional[str]:
        """Analyze recent emotional patterns"""
        history = self.data.get("emotional_state_history", [])
        if len(history) < 2:
            return None
        
        recent = [h["state"] for h in history[-5:]]
        return f"Recent emotional states: {', '.join(recent)}"
    
    def is_first_conversation(self) -> bool:
        """Check if this is the first interaction"""
        return len(self.data["conversation_history"]) == 0


class MemoryManager:
    """Manages memories for multiple users"""
    
    _instances: dict = {}
    
    @classmethod
    def get_memory(cls, phone_number: str) -> UserMemory:
        """Get or create memory for a user"""
        normalized = phone_number.replace("+", "").replace("-", "").replace(" ", "")
        if normalized not in cls._instances:
            cls._instances[normalized] = UserMemory(phone_number)
        return cls._instances[normalized]
