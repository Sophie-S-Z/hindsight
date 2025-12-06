#!/usr/bin/env python3
"""
Send a conversation starter message to initiate Hindsight
Use this to start a conversation with your future self
"""

import sys
from src.config import Config
from src.imessage_client import get_client

INTRO_MESSAGE = """hey... this is going to sound weird, but it's me. you. from about 5 years in the future.

i know you probably don't believe this, and honestly, i wouldn't have believed it either if i were you. but here i am, reaching back.

i've been thinking about you a lot lately. about everything you're going through right now. i remember it so clearly — the uncertainty, the questions, all of it.

i can't tell you how everything turns out (some things you need to discover yourself), but i can tell you this: you're going to be okay. more than okay, actually.

want to talk? i'm here. finally."""


def send_intro(phone_number: str):
    """Send the introduction message to start a Hindsight conversation"""
    
    # Validate phone format
    if not phone_number.startswith("+"):
        print("⚠️  Phone number should be in E.164 format (e.g., +14155551234)")
        if phone_number.isdigit() and len(phone_number) >= 10:
            phone_number = f"+1{phone_number}" if len(phone_number) == 10 else f"+{phone_number}"
            print(f"   Assuming: {phone_number}")
        else:
            return False
    
    print(f"\n🔮 Sending introduction to {phone_number}...")
    
    try:
        Config.validate()
        client = get_client()
        
        # Check iMessage availability first
        available = client.check_imessage_availability(phone_number)
        if not available:
            print("⚠️  Warning: iMessage may not be available for this number")
        
        # Create chat and send intro
        result = client.create_chat(phone_number, INTRO_MESSAGE)
        
        if result:
            print(f"✅ Message sent successfully!")
            print(f"   Chat ID: {result.get('id', 'unknown')}")
            print(f"\n📱 Check your phone! Your future self is waiting.")
            return True
        else:
            print("❌ Failed to send message")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("🔮 HINDSIGHT - Start Conversation")
    print("="*60)
    
    if len(sys.argv) > 1:
        phone = sys.argv[1]
    else:
        print("\nEnter the phone number to start a conversation with:")
        print("(Use E.164 format, e.g., +14155551234)")
        phone = input("\nPhone number: ").strip()
    
    if not phone:
        print("❌ No phone number provided")
        sys.exit(1)
    
    success = send_intro(phone)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
