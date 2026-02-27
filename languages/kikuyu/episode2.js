export const kikuyuEpisode2 = {
  id: 2,
  language: "Kikuyu",
  episodeTitle: "Introductions – What Is Your Name?",
  difficulty: "beginner",

  storyIntro: `After greeting each other, Gikuyu and Mumbi begin to introduce themselves.
In this lesson, you will learn how to ask for someone's name and introduce yourself.`,

  dialogue: [
    { speaker: "Mumbi", text: "Wĩĩ wĩ atĩa?" },
    { speaker: "Gikuyu", text: "Ngũĩtwa Gikuyu." },
    { speaker: "Gikuyu", text: "Na we?" },
    { speaker: "Mumbi", text: "Ngũĩtwa Mumbi." }
  ],

  exercises: [
    {
      id: 1,
      type: "translation",
      prompt: "What is your name?",
      answer: "Wĩĩ wĩ atĩa?"
    },
    {
      id: 2,
      type: "translation",
      prompt: "My name is Gikuyu",
      answer: "Ngũĩtwa Gikuyu"
    },
    {
      id: 3,
      type: "translation",
      prompt: "My name is Mumbi",
      answer: "Ngũĩtwa Mumbi"
    },
    {
      id: 4,
      type: "translation",
      prompt: "And you?",
      answer: "Na we?"
    },
    {
      id: 5,
      type: "translation",
      prompt: "Who are you?",
      answer: "We niwe u?"
    }
  ],

  xpReward: 25
};