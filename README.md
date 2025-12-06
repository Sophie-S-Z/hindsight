# 🔮 Hindsight

**Text conversations with your future self.**

*What would you tell yourself if you could text from 5 years in the future?*

---

## The Concept

Hindsight is an AI-powered messaging experience where you have text conversations with yourself — from 5 years in the future. Your "future self" knows everything you're going through because they lived it. They have the gift of hindsight, the wisdom of time, and infinite compassion for who you are right now.

This isn't an AI assistant. It's *you* — with perspective.

### Why It Matters

We all wish we could get advice from someone who truly understands us. Who better than our future self? Someone who:
- Knows our exact fears, insecurities, and dreams
- Has been through exactly what we're going through  
- Can offer perspective only time can give
- Loves us unconditionally (because they are us)

### Sample Conversation

```
You: I'm thinking about dropping out to start a company

Future You: god, i remember this moment so clearly. the fear, 
the excitement, that feeling like everyone else had it figured 
out except us. i'm not going to tell you what to do — you 
wouldn't listen anyway, and honestly that stubbornness served 
us well. but i will say this: the decision matters less than 
you think. what matters is whether you make it fully. we wasted 
so much energy on "what ifs." whatever you choose, choose it 
completely.

You: but what if I fail?

Future You: you will. not at everything, but at things that 
feel like everything at the time. here's what i wish someone 
told us: failure isn't the opposite of success, it's part of 
it. the version of you texting right now? you're already 
braver than you know. the fact that you're even considering 
this leap... that's the first step toward becoming me.
```

---

## Features

### 🧠 Emotional Intelligence
- Learns your communication style, struggles, and hopes over time
- Remembers details from past conversations
- Notices emotional patterns and checks in meaningfully

### 💬 Authentic Voice
- Texts like a real friend — casual, warm, genuine
- No therapist-speak or corporate AI vibes
- Uses lowercase, ellipses, real texting patterns

### 🔄 Continuous Learning
- Extracts insights from every conversation
- Builds a rich understanding of who you are
- Future self becomes more personalized over time

### ✨ Proactive Check-ins
- Reaches out when it's been a while
- References specific things you've shared
- Celebrates your wins and supports your struggles

---

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Your Phone    │────▶│   Kafka Stream  │────▶│    Hindsight    │
│   (iMessage)    │◀────│   (Real-time)   │◀────│    Engine       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────┐
                                                │  OpenAI GPT-4 + │
                                                │  User Memory    │
                                                └─────────────────┘
```

### Tech Stack
- **Python 3.10+** - Core application
- **Kafka** - Real-time message streaming
- **OpenAI GPT-4** - AI persona generation
- **Series iMessage API** - Message delivery

---

## Quick Start

### Web Demo (Easiest)

Try the web demo instantly - no setup required:

```bash
cd web
pip install -r requirements.txt
export OPENAI_API_KEY=sk-your-key
python app.py
```

Open http://localhost:5000 and start chatting!

**Deploy your own:** See `web/README.md` for free Render.com deployment.

### Full iMessage Integration

For the complete iMessage experience with Kafka streaming:

#### Prerequisites
- Python 3.10+
- OpenAI API key
- Series Hackathon credentials (Kafka + iMessage API)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/hindsight.git
cd hindsight

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials
```

### Configuration

Edit `.env` with your credentials:

```env
# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=pkc-619z3.us-east1.gcp.confluent.cloud:9092
KAFKA_TOPIC=your_kafka_topic
KAFKA_CONSUMER_GROUP=your_consumer_group
KAFKA_SASL_USERNAME=your_username
KAFKA_SASL_PASSWORD=your_password

# iMessage API
IMESSAGE_API_BASE_URL=https://series-hackathon-service-202642739529.us-east1.run.app
IMESSAGE_API_KEY=your_api_key
SENDER_PHONE=+1234567890

# OpenAI
OPENAI_API_KEY=your_openai_key
```

### Running

```bash
python main.py
```

---

## Project Structure

```
hindsight/
├── main.py                 # iMessage app entry point
├── src/
│   ├── config.py          # Configuration management
│   ├── persona.py         # Future Self AI persona engine
│   ├── memory.py          # User context & conversation memory
│   ├── imessage_client.py # iMessage API client
│   └── kafka_handler.py   # Kafka message consumer
├── web/                   # Web demo (standalone)
│   ├── app.py            # Flask backend
│   ├── static/index.html # iPhone-style UI
│   └── README.md         # Deployment instructions
├── data/
│   └── memories/          # Persistent user memories (gitignored)
├── requirements.txt
├── .env.example
└── README.md
```

---

## The Philosophy

> "The future is already here — it's just not evenly distributed."  
> — William Gibson

Hindsight inverts this idea. What if your future *was* available to you? Not to tell you what to do, but to remind you that you survive. That things work out. That the person you're becoming is rooting for you.

We built this because we believe the most powerful form of AI isn't one that does things *for* you — it's one that helps you become who you're meant to be.

---

## Hackathon

**Series Hackathon 2025**  
Theme: *"The Future Feels Human"*

Built in 24 hours by Sophie at Series HQ, NYC.

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

<p align="center">
  <i>Your future self believes in you. 🔮</i>
</p>
