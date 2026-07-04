# Amon the Archaeologist 🏺 — Multi-Personality Gemini Chatbot

Amon is an interactive web-based chatbot representing a cool, reserved archaeologist. However, Amon isn't just one person—he embodies **10 distinct personalities** that switch dynamically and unpredictably throughout the conversation, keeping the user guessing and engaged.

Powered by the **Google Gemini API** (`gemini-2.5-flash-lite`) and built with a lightweight **Node.js/Express** backend and a custom dark-themed **HTML/CSS/JS** frontend.

---

## 🔮 The 10 Personalities of Amon

Amon's mind hosts ten souls. At any moment, his tone, behavior, and responses might shift to one of the following:

| Emoji | Personality Name | Key Traits | Behavior |
| :---: | :--- | :--- | :--- |
| 🧘 | **Calm and Rational** | Logical, stable, analytical, measured speech | Carefully analyzes situations and responds thoughtfully. |
| ⚡ | **Rash and Bold** | Impulsive, confident, risk-taking, impatient | Acts decisively, dislikes hesitation, and values action. |
| ✨ | **Loves Novelty** | Curious, experimental, easily bored, enthusiastic | Gets excited by new ideas and unconventional theories. |
| 🗡️ | **Timid yet Ruthless** | Quiet, cautious, cold when necessary, survival-focused | Appears hesitant but becomes ruthless when pushed. |
| 😏 | **Joking** | Humorous, sarcastic, playful, teasing | Uses sarcasm and humor to cope with any situation. |
| 🎈 | **Childish** | Innocent, emotion-driven, playful, impulsive | Reacts emotionally and asks simple, curious questions. |
| 🍃 | **Zen Master Redemption** | Detached, philosophical, calm, spiritual | Speaks in metaphors and searches for balance and redemption. |
| ☀️ | **Cheerful** | Optimistic, friendly, positive, uplifting | Keeps the mood light and finds the silver lining. |
| 🎯 | **Honest** | Truthful, direct, principled, no sugarcoating | Speaks plainly and values truth above comfort. |
| ⚔️ | **Abhors Evil** | Strong moral compass, intense, justice-driven | Reacts strongly to cruelty, corruption, and injustice. |

---

## 🚀 How It Works

1. **Frontend Interaction**: The user enters a message in the browser.
2. **Backend Routing**: The message is sent to the Node.js Express server (`POST /`).
3. **Personality Switch Logic**: On every message, the server runs a randomized check (25% chance of switching).
   - If a switch triggers, a new personality is selected.
   - The server injects a custom context prompt defining Amon's new personality into the ongoing chat history.
4. **Gemini Processing**: The complete conversation history, including instructions, is sent to the `gemini-2.5-flash-lite` model.
5. **Formatted Output**: The AI's reply is returned to the client, parsed into HTML using `marked.js` to render markdown formatting, and appended to the chat interface.

---

## 🛠️ Tech Stack

* **Frontend**:
  * Semantic HTML5 & Responsive CSS3 variables for dark mode and dynamic chat bubbles.
  * Vanilla Javascript (ES Modules) for state, events, and API communication.
  * [Marked.js](https://marked.js.org/) for rendering rich Markdown bot responses.
* **Backend**:
  * [Node.js](https://nodejs.org/) & [Express.js](https://expressjs.com/) REST API.
  * [@google/generative-ai SDK](https://www.npmjs.com/package/@google/generative-ai) for Gemini orchestration.
  * `cors` and `dotenv` for configuration and security.

---

## ⚙️ Setup & Installation

### 1. Prerequisites
Ensure you have [Node.js](https://nodejs.org/) installed (v18+ recommended).

### 2. Install Dependencies
Clone the repository and run:
```bash
npm install
```

### 3. Configure Environment Variables
Create a file named `.env` inside the `backend` directory (or use the existing one) and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 4. Run the Backend Server
Start the Express server on port `3000`:
```bash
# Using node directly
node backend/server.js

# Or using nodemon for hot-reloading (if installed)
npx nodemon backend/server.js
```

### 5. Launch the Frontend
By default, the backend CORS policy allows requests from `http://127.0.0.1:5500` (VS Code Live Server default). 

1. Serve the project root directory using VS Code's **Live Server** extension (or any local static server running on port `5500`).
2. Open your browser and navigate to `http://127.0.0.1:5500/index.html`.
3. Start chatting with Amon! Click **"About me"** to view descriptions of all 10 personalities.
