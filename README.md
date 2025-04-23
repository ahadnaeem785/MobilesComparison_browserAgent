# 📱 AI-Powered Phone Comparison App

An intelligent, browser-automated comparison tool for mobile phones built using **LangChain**, **Chainlit**, **Playwright**, **Openai Agents SDK**, and **Google Gemini API**. This app performs live searches for phone specifications, compares them intelligently, and presents results in clean, markdown-formatted responses with streaming output in an interactive UI.

---

## 🚀 Features

- 🔍 **Live web search** using a browser automation agent
- 🤖 **Multi-agent orchestration** using LangChain’s + Openai Agents SDK
- 📋 **Structured Markdown output** comparing phone specs
- 🌐 **Browser automation** via `browser-use` and Playwright
- 💬 **Interactive UI with Chainlit** (streaming markdown in real time)
- 🔐 **Gemini model usage** (no OpenAI key required)

---


## 🔧 Quick Setup Instructions

1. **Clone the repository**:

```bash
git clone https://github.com/ahadnaeem785/MobilesComparison_browserAgent.git
```

2. **Sync and create virtual environment using `uv`**:

```bash
uv sync
```

> This will install all dependencies and set up your environment automatically.

3. **Run the Chainlit app**:

```bash
uv run chainlit run main.py
```

4. **Visit your app**:

Open your browser and go to: [http://localhost:8000](http://localhost:8000)

> ✅ Make sure you have `uv` installed on your system.

---

## 📁 Project Structure

```
.
├── .chainlit/              # Chainlit UI config and sessions
├── main.py                 # Chainlit entrypoint and agent runner
├── README.md               # Project documentation
├── chainlit.md             # Optional display markdown for Chainlit
├── pyproject.toml          # Project metadata and dependencies
├── uv.lock                 # uv-generated lockfile for reproducible env
├── .gitignore              # Git ignored files
├── .python-version         # Python version pin
└── __pycache__/            # Compiled Python cache
```

---

## 🔑 Environment Setup

Create a `.env` file in the root with the following:

```env
GEMINI_API_KEY=your-gemini-api-key-here
```

---

## 🧩 Dependencies

- [Chainlit](https://www.chainlit.io/)
- [LangChain](https://www.langchain.com/) 
- [Playwright](https://playwright.dev/) 
- [Google Generative AI](https://ai.google.dev/) 
- [uv](https://github.com/astral-sh/uv) 
- [OpenAI Agents SDK ](https://openai.github.io/openai-agents-python/)


---


## ✨ Demo Output Sample

```markdown
### Samsung A16
- 📱 Display: 6.7", Super AMOLED, 90Hz
- ⚙️ Processor: Mediatek Helio G99
- 🔋 Battery: 5000mAh, 25W

### iPhone 7 Plus
- 📱 Display: 5.5", Retina IPS LCD
- ⚙️ Processor: Apple A10 Fusion
- 🔋 Battery: 2900mAh
```

---

## 📜 License
MIT License. See [LICENSE](./LICENSE) for details.

---

## 👨‍💻 Author
Made with ❤️ by **Muhammad Ahad**


