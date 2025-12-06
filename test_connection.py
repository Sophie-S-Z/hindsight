#!/usr/bin/env python3
"""
Test script for Hindsight
Run this to verify your configuration and connections
"""

import sys
import json

def test_config():
    """Test configuration loading"""
    print("\n1️⃣  Testing configuration...")
    try:
        from src.config import Config
        Config.validate()
        print("   ✅ Configuration loaded successfully")
        print(f"   📱 Sender phone: {Config.SENDER_PHONE}")
        print(f"   📡 Kafka topic: {Config.KAFKA_TOPIC}")
        return True
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return False

def test_openai():
    """Test OpenAI API connection"""
    print("\n2️⃣  Testing OpenAI API...")
    try:
        from openai import OpenAI
        from src.config import Config
        
        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=50,
            messages=[{"role": "user", "content": "Say 'Hindsight connection test successful!' in 5 words or less."}]
        )
        print(f"   ✅ OpenAI API working: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"   ❌ OpenAI API error: {e}")
        return False

def test_imessage_api():
    """Test iMessage API connection"""
    print("\n3️⃣  Testing iMessage API...")
    try:
        from src.imessage_client import get_client
        
        client = get_client()
        chats = client.list_chats()
        print(f"   ✅ iMessage API working - found {len(chats)} existing chats")
        return True
    except Exception as e:
        print(f"   ❌ iMessage API error: {e}")
        return False

def test_kafka_connection():
    """Test Kafka connection (quick check)"""
    print("\n4️⃣  Testing Kafka connection...")
    try:
        from kafka import KafkaConsumer
        from src.config import Config
        
        consumer = KafkaConsumer(
            Config.KAFKA_TOPIC,
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS.split(","),
            security_protocol="SASL_SSL",
            sasl_mechanism="PLAIN",
            sasl_plain_username=Config.KAFKA_SASL_USERNAME,
            sasl_plain_password=Config.KAFKA_SASL_PASSWORD,
            consumer_timeout_ms=5000,  # 5 second timeout
            group_id=Config.KAFKA_CONSUMER_GROUP,
        )
        
        # Just check if we can connect
        topics = consumer.topics()
        consumer.close()
        
        print(f"   ✅ Kafka connection working")
        return True
    except Exception as e:
        print(f"   ❌ Kafka connection error: {e}")
        return False

def test_memory_system():
    """Test memory persistence"""
    print("\n5️⃣  Testing memory system...")
    try:
        from src.memory import MemoryManager
        
        # Create test memory
        memory = MemoryManager.get_memory("+1234567890")
        memory.add_message("user", "Test message")
        memory.update_profile({"name": "Test User"})
        
        # Verify it persists
        memory2 = MemoryManager.get_memory("+1234567890")
        assert memory2.data["profile"]["name"] == "Test User"
        
        print("   ✅ Memory system working")
        return True
    except Exception as e:
        print(f"   ❌ Memory system error: {e}")
        return False

def test_send_message(phone_number: str):
    """Test sending an actual message (optional)"""
    print(f"\n6️⃣  Sending test message to {phone_number}...")
    try:
        from src.imessage_client import get_client
        
        client = get_client()
        
        test_message = "🔮 hey, it's your future self. just checking the connection works. ignore this if you're testing!"
        
        result = client.create_chat(phone_number, test_message)
        if result:
            print(f"   ✅ Test message sent successfully!")
            print(f"   Chat ID: {result.get('id', 'unknown')}")
            return True
        else:
            print("   ❌ Failed to send test message")
            return False
    except Exception as e:
        print(f"   ❌ Error sending message: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("🔮 HINDSIGHT - Connection Test Suite")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Configuration", test_config()))
    results.append(("OpenAI API", test_openai()))
    results.append(("iMessage API", test_imessage_api()))
    results.append(("Kafka", test_kafka_connection()))
    results.append(("Memory System", test_memory_system()))
    
    # Optional: Send test message
    if len(sys.argv) > 1 and sys.argv[1] == "--send-test":
        if len(sys.argv) > 2:
            phone = sys.argv[2]
            results.append(("Send Message", test_send_message(phone)))
        else:
            print("\n⚠️  To send a test message, provide phone number:")
            print("   python test_connection.py --send-test +1234567890")
    
    # Summary
    print("\n" + "="*60)
    print("📊 RESULTS SUMMARY")
    print("="*60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} - {name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 All tests passed! You're ready to run Hindsight.")
        print("   Run: python main.py")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
