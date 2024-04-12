// script.js
const form = document.getElementById('test-case-form');
const input = document.getElementById('input');
const chatbotType = document.getElementById('chatbot-type');
const errorClassification = document.getElementById('error-classification');
const output = document.getElementById('output');

form.addEventListener('submit', (event) => {
  event.preventDefault();

  // Validate form data (optional)

  const testCaseData = {
    input: input.value,
    chatbotType: chatbotType.value,
    errorClassification: errorClassification.value,
    output: output.value,
  };

  // Submit test case data to your backend or data storage (replace with your implementation)
  console.log('Test case created:', testCaseData);

  // Clear form after submission
  form.reset();
});
