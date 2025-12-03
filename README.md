# 🤖 Jarvis AI Assistant

A powerful AI-powered virtual assistant with voice recognition, natural language processing, and intelligent automation.

## ✨ Features

- 🎙️ **Voice Control** - Speech recognition and text-to-speech
- 🧠 **AI Intelligence** - Powered by Groq LLaMA models
- 🔍 **Real-time Search** - Google search integration
- 🎨 **Image Generation** - AI-generated images from text
- ✍️ **Content Writing** - Letters, essays, applications, and code
- 🚀 **Automation** - App control, web browsing, media playback
- 💻 **Modern GUI** - Beautiful PyQt5 interface

## 🔄 Live Demo

![Assistant Demo](Frontend/Graphics/DEMO.gif)

## 🚀 Quick Start

1. **Clone and setup**
```bash
git clone https://github.com/mannat-07/Jarvis-AI.git
cd Jarvis-AI
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure API keys** - Create `.env` file:
```env
Username=YourName
Assistantname=Jarvis
GroqAPIKey=your_groq_api_key
HuggingFaceAPIKey=your_huggingface_key
SerpAPIKey=your_serpapi_key
AssistantVoice=en-US-GuyNeural
```

3. **Run**
```bash
python Main.py
```

## 🎯 Example Commands

- "Hello Jarvis, how are you?"
- "What's the weather today?"
- "Open Chrome"
- "Play music on YouTube"
- "Write an application for sick leave"
- "Generate an image of a sunset"

## 🔑 Get API Keys

- [Groq](https://console.groq.com) - LLM inference
- [HuggingFace](https://huggingface.co/settings/tokens) - Image generation
- [SerpAPI](https://serpapi.com) - Google search

## 🛠️ Tech Stack

Python 3.11+ • PyQt5 • Groq LLaMA • Edge TTS • BeautifulSoup • Selenium

## 📝 License

MIT License - Feel free to use and modify!

---

**Made with ❤️ using Python**

