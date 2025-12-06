"""
Hindsight - Text Conversations with Your Future Self
Main application entry point

"The Future Feels Human" - Series Hackathon 2025
"""

import asyncio
import sys

from src.config import Config
from src.kafka_handler import create_consumer


ASCII_ART = """
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   ██╗  ██╗██╗███╗   ██╗██████╗ ███████╗██╗ ██████╗ ██╗  ██╗████████╗║
║   ██║  ██║██║████╗  ██║██╔══██╗██╔════╝██║██╔════╝ ██║  ██║╚══██╔══╝║
║   ███████║██║██╔██╗ ██║██║  ██║███████╗██║██║  ███╗███████║   ██║   ║
║   ██╔══██║██║██║╚██╗██║██║  ██║╚════██║██║██║   ██║██╔══██║   ██║   ║
║   ██║  ██║██║██║ ╚████║██████╔╝███████║██║╚██████╔╝██║  ██║   ██║   ║
║   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ║
║                                                                   ║
║              Text conversations with your future self             ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""


def print_startup_info():
    """Print startup information"""
    print(ASCII_ART)
    print("  🔮 What would you tell yourself if you could text from the future?")
    print("")
    print("  Series Hackathon 2025 - 'The Future Feels Human'")
    print("  ─" * 35)
    print("")


async def main():
    """Main application entry point"""
    print_startup_info()
    
    # Validate configuration
    try:
        Config.validate()
        print("  ✅ Configuration validated")
    except ValueError as e:
        print(f"  ❌ Configuration error: {e}")
        print("\n  Please check your .env file and ensure all required values are set.")
        sys.exit(1)
    
    print(f"  📱 Sender phone: {Config.SENDER_PHONE}")
    print(f"  📡 Kafka topic: {Config.KAFKA_TOPIC}")
    print("")
    
    # Create and start consumer
    consumer = create_consumer()
    
    try:
        await consumer.start()
    except Exception as e:
        print(f"\n  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
