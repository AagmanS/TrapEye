const express = require('express');
const cors = require('cors');
const fs = require('fs-extra');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Path to our JSON database
const dbPath = path.join(__dirname, 'db.json');

// Initialize db.json with sample data if it doesn't exist
async function initializeDB() {
  const dbExists = await fs.pathExists(dbPath);
  if (!dbExists) {
    const initialData = {
      lessons: [
        {
          id: 1,
          title: "Password Security",
          description: "Learn how to create strong passwords and keep them secure.",
          content: "Passwords are the first line of defense against cyber attacks. A strong password should be at least 12 characters long and include a mix of uppercase and lowercase letters, numbers, and special characters. Avoid using easily guessable information like birthdays or pet names. Use a unique password for each account and consider using a password manager to keep track of them all.",
          quiz: [
            {
              question: "What is the minimum recommended length for a strong password?",
              options: ["6 characters", "8 characters", "12 characters", "16 characters"],
              correctAnswer: 2
            },
            {
              question: "Which of the following is NOT a good practice for password security?",
              options: ["Using a password manager", "Reusing passwords across multiple sites", "Enabling two-factor authentication", "Changing passwords regularly"],
              correctAnswer: 1
            },
            {
              question: "What should you avoid when creating passwords?",
              options: ["Special characters", "Numbers", "Personal information like birthdays", "Uppercase letters"],
              correctAnswer: 2
            }
          ]
        },
        {
          id: 2,
          title: "Phishing Awareness",
          description: "Identify and avoid phishing attempts that try to steal your information.",
          content: "Phishing is a type of cyber attack where criminals try to trick you into revealing sensitive information like passwords or credit card numbers. They often use fake emails, texts, or websites that look legitimate. Warning signs of phishing include: urgent language, requests for personal information, suspicious links or attachments, and poor grammar or spelling. Always verify the sender's identity and never click on suspicious links.",
          quiz: [
            {
              question: "What is phishing?",
              options: ["A type of fish", "A cyber attack that tricks people into revealing sensitive information", "A software update", "A computer virus"],
              correctAnswer: 1
            },
            {
              question: "Which of the following is a warning sign of phishing?",
              options: ["Professional email signature", "Perfect grammar and spelling", "Urgent language requesting immediate action", "Personalized greeting with your name"],
              correctAnswer: 2
            },
            {
              question: "What should you do if you receive a suspicious email?",
              options: ["Click all links to verify", "Forward it to friends", "Delete it immediately", "Verify the sender through another channel"],
              correctAnswer: 3
            }
          ]
        },
        {
          id: 3,
          title: "Social Media Safety",
          description: "Protect your privacy and personal information on social media platforms.",
          content: "Social media platforms can reveal a lot of personal information that cybercriminals can use. Protect yourself by reviewing your privacy settings regularly, limiting who can see your posts, avoiding oversharing personal details like your address or phone number, and being cautious about accepting friend requests from strangers. Think twice before posting photos that reveal your location or daily routines.",
          quiz: [
            {
              question: "What should you avoid sharing on social media?",
              options: ["Your favorite movies", "Your vacation photos", "Your home address", "Your hobbies"],
              correctAnswer: 2
            },
            {
              question: "How often should you review your social media privacy settings?",
              options: ["Once a year", "Regularly", "Never", "Only when you first create your account"],
              correctAnswer: 1
            },
            {
              question: "What is a good practice for social media safety?",
              options: ["Accepting all friend requests", "Posting your location in real-time", "Using the same password for all accounts", "Being cautious about accepting friend requests from strangers"],
              correctAnswer: 3
            }
          ]
        }
      ],
      progress: {}
    };
    await fs.writeJson(dbPath, initialData);
    console.log('Database initialized with sample data');
  }
}

// Helper function to read the database
async function readDB() {
  await initializeDB();
  return await fs.readJson(dbPath);
}

// Helper function to write to the database
async function writeDB(data) {
  return await fs.writeJson(dbPath, data);
}

// Routes

// Get all lessons
app.get('/api/lessons', async (req, res) => {
  try {
    const db = await readDB();
    res.json(db.lessons);
  } catch (error) {
    console.error('Error fetching lessons:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get user progress
app.get('/api/progress/:userId', async (req, res) => {
  try {
    const { userId } = req.params;
    const db = await readDB();
    const userProgress = db.progress[userId] || {};
    res.json(userProgress);
  } catch (error) {
    console.error('Error fetching progress:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Update user progress
app.post('/api/progress', async (req, res) => {
  try {
    const { userId, lessonId, completed, quizScore } = req.body;
    const db = await readDB();
    
    if (!db.progress[userId]) {
      db.progress[userId] = {};
    }
    
    db.progress[userId][lessonId] = {
      completed: completed || false,
      quizScore: quizScore || 0,
      completedAt: completed ? new Date().toISOString() : null
    };
    
    await writeDB(db);
    res.json({ success: true, progress: db.progress[userId][lessonId] });
  } catch (error) {
    console.error('Error updating progress:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Learning backend server running on port ${PORT}`);
  console.log(`API endpoints available at http://localhost:${PORT}/api`);
});