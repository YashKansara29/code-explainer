# Code Explainer

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135.1-00a67e.svg)
![Gemini API](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-orange.svg)
![Vanilla JS](https://img.shields.io/badge/Vanilla-JavaScript-f7df1e.svg)

An intelligent, full-stack web application that leverages Google's Gemini 2.5 Flash model to instantly analyze, break down, and explain Python code snippets.

This tool is designed to act as an automated expert engineering tutor, providing structured Markdown responses complete with line-by-line breakdowns and optimization suggestions.

## Key Features

- **Lightning-Fast AI Analysis:** Integrates the state-of-the-art `gemini-2.5-flash` model for rapid, highly accurate code comprehension.
- **Structured Output Generation:** Utilizes strict system prompting to force deterministic, perfectly formatted Markdown responses.
- **Professional Syntax Highlighting:** Renders Python code intuitively using `highlight.js`, mirroring the developer experience of modern IDEs.
- **Modern UI/UX:** Features a responsive, glass-morphism dark mode interface with asynchronous loading states and a one-click "Copy to Clipboard" utility.

## Architecture

The application is cleanly separated into a decoupled client-server architecture:

1. **Frontend:** Lightweight vanilla HTML/CSS/JS client that handles user input and renders Markdown dynamically.
2. **Backend:** Asynchronous FastAPI server that processes requests, validates payloads using Pydantic, and securely communicates with the Google Generative AI endpoints.

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn, Pydantic
- **AI Integration:** Google Generative AI SDK (`google-generativeai`)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+), Fetch API
- **Libraries:** Marked.js (Markdown parsing), Highlight.js (Syntax highlighting)

## Local Setup & Installation

### Prerequisites

- Python 3.8 or higher
- A valid Google Gemini API Key (Generate one at [Google AI Studio](https://aistudio.google.com/))

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/code-explainer.git](https://github.com/yourusername/code-explainer.git)
   cd code-explainer
   ```


2. **Create and activate a virtual environment:**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

```

3. **Install dependencies:**

```bash
pip install -r requirements.txt

```

4. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your API key securely:

```env
GEMINI_API_KEY=your_actual_api_key_here

```

5. **Run the FastAPI Server:**

```bash
uvicorn main:app --reload

```

_The API will be available at `http://127.0.0.1:8000_`6. **Launch the Client:**
Open`frontend/index.html` directly in your web browser. No local frontend development server is required.

## API Reference

### `POST /explain`

Analyzes a provided Python code string and returns an AI-generated explanation.

**Request Body:**

```json
{
  "code": "def example():\n    return 'Hello World'"
}
```

**Response (200 OK):**

```json
{
  "result": "### Explanation\nThis is a simple function...\n### Step-by-step breakdown\n..."
}
```

## Roadmap / Future Enhancements

- [ ] Add support for multiple programming languages (JavaScript, C++, Go).
- [ ] Implement an OCR feature utilizing the OpenCV library to extract and explain code directly from uploaded screenshots.
- [ ] Integrate a PostgreSQL/Supabase database to allow users to save their explanation history.
