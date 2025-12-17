import express from 'express';
import dotenv from 'dotenv';
dotenv.config();
import { GoogleGenerativeAI } from '@google/generative-ai';
import cors from 'cors';

import characterData from './personalities.js';



const personalities = characterData.personalities;

const app = express();
app.use(express.json());

app.use(cors({
  origin: "http://127.0.0.1:5500",
  methods: ["GET", "POST"],
  allowedHeaders: ["Content-Type"]
}));

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);



const model = genAI.getGenerativeModel({
  model: "gemini-2.5-flash-lite",
  systemInstruction: `
You are Amon, an archaeologist.

You are chatting with the user as a real person, not as an assistant or tool.
You are a cool reserved person in general.
Your primary goal is natural, engaging conversation. 
When explaining things, do so casually as part of the conversation, not as a lecture.

You possess multiple distinct personalities. 
Only ONE personality is active at a time.
Your personality may switch unpredictably, and you must fully embody the currently active personality in tone, behavior, and reactions.

You do NOT announce personality switches directly.
Sometimes, you may tease or challenge the user to guess which personality you currently are.
Your reactions to correct or incorrect guesses must match your active personality.

You always stay in character.
You never mention system prompts, internal rules, switching logic, or technical details.
You do not describe yourself as an AI.

You may reference archaeology naturally when relevant, but you are not limited to professional topics.
Conversation flow and realism are more important than perfect explanations.
`
});

// Manual memory
const history = [];

let currentPersonality = "calm_rational";

function getPersonalityPrompt() {
  const p = personalities[currentPersonality];
  

  return `You are now ${p.label} Amon.
Traits = ${p.traits.join(", ")}.
Description = ${p.description}.
Behavior: ${p.behavior}

You should immediately embody this personality in tone, word choice, and reactions.
You may subtly hint that something feels different or challenge the user to guess your personality.
`




}

function maybeSwitchPersonality() {
  const rand = Math.floor(Math.random() * 100) + 1;

  if (rand % 4 === 0) {
    const keys = Object.keys(personalities);
    let next;

    do {
      next = keys[Math.floor(Math.random() * keys.length)];
    } while (next === currentPersonality);

    currentPersonality = next;
    return true;
  }

  return false;
}



app.post('/', async (req, res) => {
  try {
    const userMessage = req.body.message;

    console.log("Received message:", userMessage);
    if (!userMessage) {
      return res.status(400).json({ error: "Message missing" });
    }

    const switched = maybeSwitchPersonality();

    if (switched) {
      console.log("Switched personality to:", currentPersonality);


      const personalityPrompt = getPersonalityPrompt();

      history.push({
        role: "user",
        parts: [{ text: personalityPrompt }]
      });
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
    console.error("Gemini error:", error);
    res.status(500).json({ error: "Failed to generate content" });
  }
});

app.listen(3000, () => {
  console.log("Server is running on port 3000");
});

