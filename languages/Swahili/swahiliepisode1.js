export const swahiliEpisode1 = {
  id: 1,
  language: "Swahili",
  episodeTitle: "Your First Day as a Trader",
  difficulty: "beginner",

  storyIntro: `You are a new trader at the Mombasa trading centre!
Your stall is set up with spices, gold, and other goods to sell.
Customers are arriving and you must greet them and negotiate prices in Swahili.
Learn the essential words to do business in the market.`,

  dialogue: [
    { speaker: "You (Trader)", text: "Karibu sokoni! Hujambo?" },
    { speaker: "Customer", text: "Sijambo. Unauza nini?" },
    { speaker: "You (Trader)", text: "Nauza dhahabu, bibi na pilipili." },
    { speaker: "Customer", text: "Bei gani?" },
    { speaker: "You (Trader)", text: "Dhahabu ni elfu moja. Pesa ngapi unayo?" },
    { speaker: "Customer", text: "Niko na elfu tano. Asante!" }
  ],

  exercises: [
    {
      id: 1,
      type: "multiple-choice",
      prompt: "Greet a customer",
      question: "How do you greet someone?",
      options: ["Hujambo", "Asante", "Kwaheri"],
      correctAnswer: "Hujambo"
    },
    {
      id: 2,
      type: "multiple-choice",
      prompt: "Thank you",
      question: "Thank you",
      options: ["Asante", "Ndiyo", "Maji"],
      correctAnswer: "Asante"
    },
    {
      id: 3,
      type: "multiple-choice",
      prompt: "Your stall",
      question: "Market stall",
      options: ["Sokoni", "Nyumba", "Gari"],
      correctAnswer: "Sokoni"
    },
    {
      id: 4,
      type: "multiple-choice",
      prompt: "Ask the price",
      question: "How much?",
      options: ["Bei gani", "Nini", "Karibu"],
      correctAnswer: "Bei gani"
    },
    {
      id: 5,
      type: "multiple-choice",
      prompt: "Currency",
      question: "Money",
      options: ["Pesa", "Chai", "Mkate"],
      correctAnswer: "Pesa"
    },
    {
      id: 6,
      type: "multiple-choice",
      prompt: "Offer water",
      question: "Water",
      options: ["Maji", "Mboga", "Ndizi"],
      correctAnswer: "Maji"
    },
    {
      id: 7,
      type: "multiple-choice",
      prompt: "What you sell",
      question: "Spices",
      options: ["Pilipili", "Samaki", "Wimbo"],
      correctAnswer: "Pilipili"
    },
    {
      id: 8,
      type: "multiple-choice",
      prompt: "Say goodbye",
      question: "Goodbye",
      options: ["Kwaheri", "Hujambo", "Asante"],
      correctAnswer: "Kwaheri"
    }
  ],

  xpReward: 20
};
