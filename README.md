# 🤖 AI Chatbot

A simple chatbot application powered by Gemini AI with multi-language support (Japanese/English).

**🔗 [Try the Live Demo!](https://vercel.com/taihei-sones-projects/bridge-to-practice-course)**

![Made with Love](https://img.shields.io/badge/Made%20with-Love-red)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)

## ✨ Features

- 🚀 **Simple & Fast** - High-speed responses using FastAPI and Gemini 2.0 Flash
- 💬 **Conversation History** - Natural dialogue with context understanding
- 🌐 **Multi-language** - Switch between Japanese and English interface
- 📱 **Responsive Design** - Works seamlessly on both mobile and desktop
- 🎨 **Modern UI** - Beautiful gradients and smooth animations
- 🆓 **Completely Free** - Deploy for free on Vercel

## 🏗️ Project Structure

```
BridgetoPracticeCourse/
├── public/              # Frontend
│   ├── index.html      # Main HTML
│   ├── style.css       # Stylesheet
│   ├── script.js       # Chat functionality
│   └── i18n.js        # Internationalization
├── api/                # Backend
│   └── index.py        # FastAPI + Gemini integration
├── requirements.txt    # Python packages
├── vercel.json        # Vercel configuration
├── .env.example       # Environment variables template
└── README.md          # This file
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/taso5789/bridge_to_practice_course.git
cd bridge_to_practice_course
```

### 2. Get Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/api-keys)
2. Click "Create new key"
3. Copy the API key

### 3. Set Up Environment Variables

```bash
# Create .env file
cp .env.example .env

# Edit .env and set your API key
# GEMINI_API_KEY=your_actual_api_key_here
```

### 4. Local Testing (Optional)

```bash
# Install Python packages
pip install -r requirements.txt

# Start FastAPI server
uvicorn api.index:app --reload --port 8000

# Open http://localhost:8000 in your browser
```

### 5. Deploy to Vercel

#### Method 1: Using Vercel CLI

```bash
# Install Vercel CLI (first time only)
npm i -g vercel

# Deploy
vercel

# Set environment variable
vercel env add GEMINI_API_KEY
```

#### Method 2: Using Vercel Web Dashboard

1. Log in to [Vercel](https://vercel.com/)
2. Click "New Project"
3. Connect your GitHub repository
4. Click "Import"
5. Set environment variables:
   - `GEMINI_API_KEY`: Your Gemini API key
6. Click "Deploy"

## 📝 Usage

1. Access the deployed URL
2. Type a message in the text box
3. Click send button or press Enter
4. Wait for AI response
5. Click the language button (EN/JP) to switch languages

### Keyboard Shortcuts

- **Enter**: Send message
- **Shift + Enter**: New line

## 🔧 Customization

### Change Design

Edit [public/style.css](public/style.css) to customize colors and layout.

### Change AI Model

Edit the following in [api/index.py](api/index.py):

```python
model = genai.GenerativeModel('gemini-2.0-flash-exp')
# Other models: 'gemini-pro', 'gemini-1.5-pro', etc.
```

### Add System Prompt

Set the chatbot's personality or role:

```python
# Add to api/index.py
system_instruction = "You are a helpful assistant."
model = genai.GenerativeModel(
    'gemini-2.0-flash-exp',
    system_instruction=system_instruction
)
```

### Add More Languages

Edit [public/i18n.js](public/i18n.js) to add translations:

```javascript
const translations = {
    ja: { /* Japanese translations */ },
    en: { /* English translations */ },
    es: { /* Spanish translations */ },
    // Add more languages...
};
```

## 🛠️ Troubleshooting

### API Errors

- Verify your Gemini API Key is correctly set
- Check API usage limits at [Google AI Studio](https://aistudio.google.com/usage)

### Vercel Deployment Errors

- Verify `vercel.json` configuration
- Check build logs for detailed error messages

## 🌐 Multi-language Support

The interface supports Japanese and English. The language preference is saved in the browser's localStorage and persists across sessions.

To add more languages:
1. Edit `public/i18n.js` to add translations
2. Update the language switching logic if needed

## 📚 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Gemini API](https://ai.google.dev/)
- [Vercel Documentation](https://vercel.com/docs)

## 📄 License

MIT License

## 🙏 Acknowledgments

Created based on knowledge learned from the "Bridge to Practice Course" by the University of Tokyo Matsuo-Iwasawa Lab LLM Community.

---

Created: January 2026
