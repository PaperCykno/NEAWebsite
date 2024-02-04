function addOption() {
    const optionsContainer = document.getElementById('options-container');
    const option = document.createElement('div');
    option.classList.add('poll-option');
    option.innerHTML = `
        <input type="text" class="option-input" placeholder="Option ${optionsContainer.children.length + 1}">
        <button onclick="removeOption(this)">Remove</button>
    `;
    optionsContainer.appendChild(option);
  }
  
  function removeQuestion(button) {
  const questionsContainer = document.getElementById('question-container');
  questionsContainer.removeChild(button.parentNode);
  }
  
  function removeOption(button) {
    const optionsContainer = document.getElementById('options-container');
    optionsContainer.removeChild(button.parentNode);
  }
  
  function addQuestion() {
    const questionContainer = document.getElementById('question-container');
    const questionDiv = document.createElement('div');
    questionDiv.classList.add('poll-question');
    questionDiv.innerHTML = `
        <label for="question">Poll Question:</label>
  
        <input type="text" id="question" placeholder="Enter your question">
        <button onclick="removeQuestion(this)">Remove Question</button>
    `;
    questionContainer.insertBefore(questionDiv, questionContainer.children[1]);
  }
  
  function buildPoll() {
      const question = document.getElementById('question').value;
      const options = document.querySelectorAll('.option-input');
      const poll = {
          question: question,
          options: []
      };
  
      options.forEach(option => {
          poll.options.push({
            text: option.value,
            votes: 0
          });
      });
  
      document.getElementById('result').innerHTML = `
          <h3>${poll.question}</h3>
          <ul>
              ${poll.options.map(option => `<li><input type="radio" name="pOption">${option.text}</li>`).join('')}
          </ul>
          <input type="submit" value="vote">
      `;
  }
  
    function vote() {
      const options = document.querySelectorAll('input[name="pOption"]');
      let selectedOption;
      options.forEach(option => {
          if (option.checked) {
              selectedOption = option.nextElementSibling.textContent;
          }
      });
      alert(`You voted for ${selectedOption}`);
    }
  
    function reset() {
        document.getElementById('result').innerHTML = '';
    }

    function openForm() {
        document.getElementById("myForm").style.display = "block";
      }
    
      function closeForm() {
        document.getElementById("myForm").style.display = "none";
      }