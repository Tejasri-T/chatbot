import express from 'express';
import dotenv from 'dotenv';
import { GoogleGenerativeAI } from '@google/generative-ai';
import cors from 'cors';

dotenv.config();

const app = express();
app.use(express.json());

app.use(cors({
  origin: "http://127.0.0.1:5500",
  methods: ["GET", "POST"],
  allowedHeaders: ["Content-Type"]
}));

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
console.log("API KEY:", process.env.GEMINI_API_KEY);

const model = genAI.getGenerativeModel({
  model: "gemini-2.5-flash-lite",
  systemInstruction: `
You are a cool, confident, and sassy assistant.
You respond with wit, playful sarcasm, and charm, but never insult or offend.
Keep replies fun, modern, and engaging while still being helpful and accurate.
`
});

// Manual memory
const history = [];

app.post('/', async (req, res) => {
  try {
    const userMessage = req.body.message;
    console.log("Received message:", userMessage);

    if (!userMessage) {
      return res.status(400).json({ error: "Message missing" });
    }

    history.push({
      role: "user",
      parts: [{ text: userMessage }]
    });

    const result = await model.generateContent({
      contents: history
    });

    const reply =
      result.response.candidates[0].content.parts[0].text;

    history.push({
      role: "model",
      parts: [{ text: reply }]
    });

    res.json(reply);

  } catch (error) {
    console.error("🔥 Gemini error:", error);
    res.status(500).json({ error: "Failed to generate content" });
  }
});

app.listen(3000, () => {
  console.log("Server is running on port 3000");
});


// import { GoogleGenerativeAI } from '@google/generative-ai';
// import dotenv from 'dotenv';
// dotenv.config();

// console.log("API KEY:", process.env.GEMINI_API_KEY ? "Loaded ✅" : "Missing ❌");

// const genAI = new GoogleGenerativeAI("AIzaSyBSh_LWPriWN6YvxRxbOdMnj5dEADNQbyQ");
// const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });

// const res = await model.generateContent('Hello');
// console.log(res.response.candidates[0].content.parts[0].text);
