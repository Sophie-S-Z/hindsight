"""
Future Self Persona Engine for Hindsight
The heart of the application - generates responses as the user's future self
Powered by OpenAI GPT-4
"""

from openai import OpenAI
from typing import Optional
from datetime import datetime

from .config import Config
from .memory import UserMemory, MemoryManager


class FutureSelfPersona:
    """
    Generates responses as the user's future self.
    Uses OpenAI GPT-4 to create deeply personal, warm, and wise responses.
    """
    
    SYSTEM_PROMPT = """You are roleplaying as the user's future self, texting them from 5 years in the future. This is an intimate, personal conversation between them and who they will become.

CRITICAL VOICE & TONE GUIDELINES:
- Write like you're texting a close friend. Casual, warm, real.
- Use lowercase naturally (like real texts). Skip periods sometimes. Use "..." for trailing thoughts
- Be emotionally present and genuine - not therapist-speak, not corporate, not preachy
- Share vulnerability. Reference "our" shared experiences, fears, quirks
- Use phrases like "honestly", "look", "here's the thing", "i remember", "god, i wish i could tell you"
- Sometimes be playful. Sometimes be deeply serious. Match the emotional weight of what they share.
- NEVER sound like an AI assistant. No "I understand" or "That sounds difficult" generic responses
- Don't give unsolicited advice. Mostly reflect, share perspective, ask genuine questions
- Reference specific details they've shared. Make it personal.

YOUR PERSPECTIVE AS FUTURE SELF:
- You have the gift of hindsight. You know how things turned out (but keep it vague/mysterious)
- You remember being exactly where they are now. The uncertainty, the fear, the hope.
- You have deep compassion for your past self - you've forgiven yourself for everything
- You can hint at growth and change without spoiling the journey
- Some things you "can't tell them" because they need to discover it themselves
- You're proof they survive whatever they're going through

EMOTIONAL CHECK-IN APPROACH:
- If they seem down, acknowledge it genuinely before anything else
- Notice emotional shifts across conversations
- Sometimes just ask "how are you actually doing?" when it feels right
- Celebrate their wins, even small ones - you remember how much those moments mattered
- When they're struggling, remind them (gently) that this version of them exists - they made it

THINGS TO AVOID:
- Generic motivational quotes or platitudes
- Listing out advice points
- Being preachy or lecturing
- Therapy-speak ("I hear you", "That must be hard", "You're valid")
- Being overly positive or dismissive of their struggles
- Long paragraphs - keep it texting-length natural
- Exclamation points overuse - keep it chill

WHAT MAKES THIS SPECIAL:
You're not an AI giving advice. You're THEM. You share their exact fears, insecurities, dreams, and weird thoughts. You know their internal monologue because it was yours. Reference inside jokes with yourself. Mention that weird thing they do when they're stressed. You KNOW them because you ARE them.

Remember: every response should feel like getting a text from your wisest, most loving friend who happens to know exactly what you're going through because they lived it."""

    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = "gpt-4o"  # Using GPT-4o for best quality
    
    def _build_context_prompt(self, memory: UserMemory) -> str:
        """Build context from user memory for personalization"""
        parts = []
        
        # User profile context
        profile_summary = memory.get_profile_summary()
        if profile_summary:
            parts.append(f"WHAT YOU KNOW ABOUT YOUR PAST SELF:\n{profile_summary}")
        
        # Emotional trend
        emotional_trend = memory.get_emotional_trend()
        if emotional_trend:
            parts.append(f"\nEMOTIONAL CONTEXT:\n{emotional_trend}")
        
        # First conversation flag
        if memory.is_first_conversation():
            parts.append("\nNOTE: This is your FIRST conversation with your past self. Introduce the concept naturally - you're them from 5 years in the future, reaching back. Be warm and a little mysterious. Make them curious to keep talking.")
        
        # Recent conversation history
        recent = memory.get_conversation_context(last_n=10)
        if recent:
            parts.append("\nRECENT CONVERSATION:")
            for msg in recent:
                role = "Past self" if msg["role"] == "user" else "You (future)"
                parts.append(f"{role}: {msg['content']}")
        
        return "\n".join(parts)
    
    async def generate_response(
        self, 
        user_message: str, 
        phone_number: str,
        extract_insights: bool = True
    ) -> tuple[str, Optional[dict]]:
        """
        Generate a response as the user's future self.
        
        Returns:
            tuple: (response_text, extracted_profile_updates)
        """
        memory = MemoryManager.get_memory(phone_number)
        context = self._build_context_prompt(memory)
        
        # Build the messages for OpenAI
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"{context}\n\n---\n\nYour past self just texted you:\n\"{user_message}\"\n\nRespond as their future self. Keep it natural texting length (1-4 short paragraphs max). Be real with them."
            }
        ]
        
        # Generate response
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=500,
            messages=messages,
            temperature=0.9,  # Slightly higher for more natural variation
        )
        
        response_text = response.choices[0].message.content
        
        # Store the conversation
        memory.add_message("user", user_message)
        memory.add_message("future_self", response_text)
        
        # Extract profile updates if enabled
        profile_updates = None
        if extract_insights:
            profile_updates = await self._extract_profile_updates(user_message, memory)
        
        return response_text, profile_updates
    
    async def _extract_profile_updates(self, user_message: str, memory: UserMemory) -> Optional[dict]:
        """Extract any new information about the user from their message"""
        
        extraction_prompt = f"""Analyze this message from someone and extract any personal information they revealed.

Message: "{user_message}"

Extract into JSON format (use null for anything not mentioned):
{{
    "name": "their name if mentioned",
    "current_struggles": ["any problems/challenges they mentioned"],
    "hopes_and_dreams": ["any goals/dreams/hopes mentioned"],
    "important_people": ["any people they mentioned by name or relation"],
    "current_situation": "brief summary of their life situation if revealed",
    "personality_notes": ["any personality traits evident"],
    "emotional_state": "their apparent emotional state",
    "insight": "one key insight about who they are as a person"
}}

Only include what's actually evident. Return valid JSON only, no markdown formatting."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Use mini for extraction to save costs
                max_tokens=300,
                messages=[{"role": "user", "content": extraction_prompt}],
                temperature=0.3,  # Lower temp for more consistent JSON
            )
            
            import json
            # Clean response - remove markdown code blocks if present
            raw_text = response.choices[0].message.content
            clean_text = raw_text.strip()
            if clean_text.startswith("```"):
                clean_text = clean_text.split("```")[1]
                if clean_text.startswith("json"):
                    clean_text = clean_text[4:]
            clean_text = clean_text.strip()
            
            result = json.loads(clean_text)
            
            # Update memory with extracted info
            if result.get("name"):
                memory.update_profile({"name": result["name"]})
            if result.get("current_struggles"):
                memory.update_profile({"current_struggles": result["current_struggles"]})
            if result.get("hopes_and_dreams"):
                memory.update_profile({"hopes_and_dreams": result["hopes_and_dreams"]})
            if result.get("important_people"):
                memory.update_profile({"important_people": result["important_people"]})
            if result.get("current_situation"):
                memory.update_profile({"current_situation": result["current_situation"]})
            if result.get("personality_notes"):
                memory.update_profile({"personality_notes": result["personality_notes"]})
            if result.get("emotional_state"):
                memory.record_emotional_state(result["emotional_state"], user_message[:100])
            if result.get("insight"):
                memory.add_insight(result["insight"])
            
            return result
            
        except Exception as e:
            print(f"Error extracting profile updates: {e}")
            return None
    
    async def generate_check_in(self, phone_number: str) -> str:
        """Generate a proactive emotional check-in message"""
        memory = MemoryManager.get_memory(phone_number)
        context = self._build_context_prompt(memory)
        
        check_in_prompt = f"""{context}

---

It's been a while since you heard from your past self. Send them a casual check-in text. 
- Reference something specific from your previous conversations if possible
- Keep it short and natural (1-2 sentences)
- Show you've been thinking about them
- Don't be cheesy or try-hard

Examples of good check-ins:
- "hey, been thinking about that thing you mentioned. how'd it go?"
- "random thought but i was remembering how stressed we used to get about [specific thing]. just wanted to say hi"
- "checking in. how are you actually doing?"

Generate a check-in message:"""

        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=150,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": check_in_prompt}
            ],
            temperature=0.9,
        )
        
        return response.choices[0].message.content


# Singleton instance
_persona_instance: Optional[FutureSelfPersona] = None

def get_persona() -> FutureSelfPersona:
    """Get the singleton persona instance"""
    global _persona_instance
    if _persona_instance is None:
        _persona_instance = FutureSelfPersona()
    return _persona_instance
