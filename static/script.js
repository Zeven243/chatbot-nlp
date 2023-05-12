document.addEventListener("DOMContentLoaded", function () {
  const chatDisplay = document.getElementById("chat-display");
  const chatBot = document.getElementById("chat-bot");
  const userMsgInput = document.getElementById("user-msg");
  const sendBtn = document.getElementById("send-btn");

  // Function to display a user message in the chat display
  function displayUserMessage(message) {
    const userDiv = document.createElement("div");
    userDiv.className = "chat-msg";
    userDiv.innerHTML = `<span class="user">You:</span><span class="message">${message}</span>`;
    chatDisplay.insertBefore(userDiv, chatBot);
  }

  // Function to display a chatbot response in the chat display
  function displayBotResponse(response) {
    const botDiv = document.createElement("div");
    botDiv.className = "chat-msg";
    botDiv.innerHTML = `<span class="user">ChatBot:</span><span class="message">${response}</span>`;
    chatDisplay.insertBefore(botDiv, chatBot);
  }

  // Function to handle user input and get response from the chatbot
  function handleUserInput() {
    const userMsg = userMsgInput.value.trim();
    if (userMsg !== "") {
      displayUserMessage(userMsg);
      userMsgInput.value = "";
      getBotResponse(userMsg);
    }
  }

  // Function to get response from the chatbot via AJAX request
  function getBotResponse(userMsg) {
    const xhr = new XMLHttpRequest();
    const url = `/get?msg=${userMsg}`;

    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          const response = xhr.responseText;
          displayBotResponse(response);
          scrollToBottom();
        } else {
          console.log("Error:", xhr.status);
        }
      }
    };

    xhr.open("GET", url, true);
    xhr.send();
  }

  // Function to scroll to the bottom of the chat display
  function scrollToBottom() {
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
  }

  // Event listeners
  sendBtn.addEventListener("click", handleUserInput);
  userMsgInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      handleUserInput();
      event.preventDefault();
    }
  });

  // Initial focus on the input field
  userMsgInput.focus();
});
