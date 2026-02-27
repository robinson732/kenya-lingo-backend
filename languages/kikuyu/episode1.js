export const kikuyuEpisode1 = {
  id: 1,
  language: "Kikuyu",
  episodeTitle: "Greetings – Meeting Gikuyu and Mumbi",
  difficulty: "beginner",

  storyIntro: `The Kikuyu people traditionally live in the central highlands of Kenya near Mount Kenya.
Gikuyu and Mumbi are believed to be the ancestors of the Kikuyu people.
In this first lesson, you will learn common greetings used in daily conversation.`,

  dialogue: [
    { speaker: "Gikuyu", text: "Ũhoro waku?" },
    { speaker: "Mumbi", text: "Ndĩ mwega. Na we wĩ atĩa?" },
    { speaker: "Gikuyu", text: "Ndĩ mwega muno." }
  ],

  exercises: [
    {
      id: 1,
      type: "translation",
      prompt: "How are you?",
      answer: "Ũhoro waku?"
    },
    {
      id: 2,
      type: "translation",
      prompt: "I am fine",
      answer: "Ndĩ mwega"
    },
    {
      id: 3,
      type: "translation",
      prompt: "And you, how are you?",
      answer: "Na we wĩ atĩa?"
    },
    {
      id: 4,
      type: "translation",
      prompt: "I am very fine",
      answer: "Ndĩ mwega muno"
    },
    {
      id: 5,
      type: "translation",
      prompt: "Thank you",
      answer: "Nĩ ngatho"
    },
    {
      id: 6,
      type: "translation",
      prompt: "Goodbye",
      answer: "Thie na wega"
    }
  ],

  xpReward: 20
};