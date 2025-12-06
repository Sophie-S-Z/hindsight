#!/usr/bin/env python3
"""
Hindsight Interactive Demo
Test the Future Self persona without the full Kafka setup
Perfect for demos and testing the AI responses
"""

import asyncio
import sys
from datetime import datetime


def print_header():
    print("\n" + "="*60)
    print("🔮 HINDSIGHT - Interactive Demo Mode")
    print("="*60)
    print("\nText with your future self. Type 'quit' to exit.")
    print("Type 'reset' to start a new conversation.")
    print("-"*60 + "\n")


async def demo_conversation():
    """Run an interactive demo conversation"""
    from src.config import Config
    from src.persona import FutureSelfPersona
    from src.memory import MemoryManager
    
    # Validate config (just needs OpenAI key for demo)
    if not Config.OPENAI_API_KEY:
        print("❌ Please set OPENAI_API_KEY in your .env file")
        return
    
    print_header()
    
    # Use a demo phone number
    demo_phone = "+1demo0000000"
    persona = FutureSelfPersona()
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'quit':
                print("\n👋 Take care. Your future self believes in you.\n")
                break
            
            if user_input.lower() == 'reset':
                # Clear memory for this demo user
                demo_phone = f"+1demo{datetime.now().strftime('%H%M%S')}"
                print("\n🔄 Started fresh conversation.\n")
                continue
            
            # Generate response
            print("\n💭 Future You is typing...\n")
            
            response, _ = await persona.generate_response(
                user_message=user_input,
                phone_number=demo_phone
            )
            
            # Display response with nice formatting
            print(f"Future You: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Take care. Your future self believes in you.\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


async def demo_single_message(message: str):
    """Generate a single response (for scripted demos)"""
    from src.config import Config
    from src.persona import FutureSelfPersona
    
    if not Config.OPENAI_API_KEY:
        print("❌ Please set OPENAI_API_KEY in your .env file")
        return
    
    persona = FutureSelfPersona()
    
    print(f"\nYou: {message}\n")
    print("💭 Future You is typing...\n")
    
    response, _ = await persona.generate_response(
        user_message=message,
        phone_number="+1demo0000000"
    )
    
    print(f"Future You: {response}\n")


def main():
    if len(sys.argv) > 1:
        # Single message mode
        message = " ".join(sys.argv[1:])
        asyncio.run(demo_single_message(message))
    else:
        # Interactive mode
        asyncio.run(demo_conversation())


if __name__ == "__main__":
    main()
