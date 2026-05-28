export const swahiliEpisode2 = {
  id: 2,
  language: "Swahili",
  episodeTitle: "A New Customer Arrives",
  difficulty: "beginner",

  storyIntro: `A new customer walks into your trading stall!
You greet them and they ask about your goods.
Learn more simple trading words to serve customers well.`,

  dialogue: [
    { speaker: "You (Trader)", text: "Karibu! Habari yako?" },
    { speaker: "Customer", text: "Nzuri. Unauza nini?" },
    { speaker: "You (Trader)", text: "Nauza dhahabu na pilipili." },
    { speaker: "Customer", text: "Ninataka dhahabu. Bei gani?" },
    { speaker: "You (Trader)", text: "Pesa elfu moja." }
  ],

  exercises: [
    {
      id: 1,
      type: "multiple-choice",
      prompt: "Welcome",
      question: "Welcome!",
      options: ["Karibu", "Kwaheri", "Asante"],
      correctAnswer: "Karibu"
    },
    {
      id: 2,
      type: "multiple-choice",
      prompt: "No problem",
      question: "No problem",
      options: ["hakuna matata", "Ubaya", "Karibu"],
      correctAnswer: "hakuna matata"
    },
    {
      id: 3,
      type: "multiple-choice",
      prompt: "How are you?",
      question: "How are you?",
      options: ["Habari yako", "Bei gani", "Unauza"],
      correctAnswer: "Habari yako"
    },
    {
      id: 4,
      type: "multiple-choice",
      prompt: "I sell",
      question: "I sell",
      options: ["Nauza", "Nita nunua", "Asante"],
      correctAnswer: "Nauza"
    },
    {
      id: 5,
      type: "multiple-choice",
      prompt: "Gold",
      question: "Gold",
      options: ["Dhahabu", "Pesa", "Maji"],
      correctAnswer: "Dhahabu"
    },
    {
      id: 6,
      type: "multiple-choice",
      prompt: "Price",
      question: "Price",
      options: ["Bei", "Pesa", "Sokoni"],
      correctAnswer: "Bei"
    },
    {
      id: 7,
      type: "multiple-choice",
      prompt: "I want",
      question: "I want",
      options: ["Ninataka", "Nauza", "Nita nunua"],
      correctAnswer: "Ninataka"
    },
    {
      id: 8,
      type: "multiple-choice",
      prompt: "Thank you",
      question: "Thank you",
      options: ["Asante", "Ndiyo", "Maji"],
      correctAnswer: "Asante"
    }
  ],

  xpReward: 20
};
