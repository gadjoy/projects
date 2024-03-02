<template>
  <div class="container">
    <h1>AI-Powered Quiz Generator</h1>

    <table>
      <tr>
        <td class="label">Enter Topic:</td>
        <td><input type="text" v-model="topic"></td>
      </tr>
      <tr>
        <td class="label">Choose Difficulty:</td>
        <td>
          <select v-model="difficulty">
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </td>
      </tr>
      <tr>
        <td class="label">Number of Questions:</td>
        <td><input type="number" v-model="num_questions" placeholder="2" /></td>
      </tr>
      <tr>
        <td colspan="2" style="text-align: center;">
          <button @click="generateQuiz" class="generate-button">Generate Quiz</button>
        </td>
      </tr>
    </table>

    <div>
    <div v-for="(question, index) in quiz" :key="index">
      <h3>Question {{ index + 1 }}</h3>
      <p>{{ question.query }}</p>
      <div v-for="(choice, i) in question.choices" :key="i">
        <input type="radio" :value="i" v-model="userAnswers[index]" :id="`choice-${index}-${i}`">
        <label :for="`choice-${index}-${i}`">{{ choice }}</label>
      </div>
      <div v-if="userAnswers[index] !== null">
        <p v-if="isAnswerCorrect[index]">Your answer is correct!</p>
        <div v-else>
          <button @click="showHint(index)">Hint</button>
          <p v-if="showHints[index]">{{ question.explanation }}</p>
        </div>
      </div>
    </div>

  </div>
</div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      num_questions: 2,
      topic: 'Python',
      difficulty: 'easy',
      quiz: [],
      userAnswers: [],
      showHints: [],
      questionType: 'multipleChoice',
    };
  },
  methods: {
    async generateQuiz() {
      try {
        const response = await this.fetchQuestions();
        this.quiz = response.questions || [];
        this.userAnswers = new Array(this.quiz.length).fill(null);
        this.showHints = new Array(this.quiz.length).fill(false);
      } catch (error) {
        console.error('Error fetching questions:', error);
      }
    },
    submitQuiz() {
      console.log('Quiz submitted:', this.quiz);
      // You can send the quiz data to your backend for scoring and analysis
    },
    async fetchQuestions() {
      const url = 'http://127.0.0.1:5000/generate';
      const requestData = {
        num_questions: this.num_questions,
        topic: this.topic,
        difficulty: this.difficulty,
      };

      try {
        const response = await axios.post(url, requestData);

        if (!response.data.questions) {
          console.error('Error response from server:', response);
          throw new Error('Invalid response from the server');
        }

        return response.data;
      } catch (error) {
        console.error('Error fetching questions:', error);
        throw error;
      }
    },
    showHint(index) {
      this.showHints[index] = true;
    },
  },

  computed: {
    isAnswerCorrect() {
      return this.userAnswers.map((answer, index) => {
        let correctAnswer = this.quiz[index].answer;
        correctAnswer = correctAnswer === 0 ? correctAnswer : correctAnswer - 1;
        return answer === correctAnswer;
      });
    }
  },
};
</script>

<style scoped>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }

  table {
    margin: 20px;
    border-collapse: collapse;
    width: 50%;
  }

  table, th, td {
    border: 1px solid #ddd;
  }

  th, td {
    padding: 10px;
    text-align: left;
  }

  textarea {
    width: 100%;
    height: 100px;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    resize: vertical;
  }

  .label {
    font-weight: bold;
  }

  .generate-button {
    background-color: #4CAF50;
    color: #fff;
    border: none;
    padding: 10px 15px;
    font-size: 16px;
    cursor: pointer;
    border-radius: 4px;
  }

  .generate-button:hover {
    background-color: #45a049;
  }

  .submit-button {
    background-color: #007BFF;
    color: #fff;
    border: none;
    padding: 10px 15px;
    font-size: 16px;
    cursor: pointer;
    border-radius: 4px;
    margin-top: 10px;
  }

  .submit-button:hover {
    background-color: #0056b3;
  }

  .quiz-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }

  .quiz-table th, .quiz-table td {
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
  }

  .quiz-table th {
    background-color: #f2f2f2;
  }
</style>
