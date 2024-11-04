class BoggleGame {
  constructor(boardId, formId, timerId, scoreId, messageId) {
      this.boardId = boardId;
      this.formId = formId;
      this.timerId = timerId;
      this.scoreId = scoreId;
      this.messageId = messageId;
      this.score = 0;
      this.words = new Set();
      this.timeLeft = 60;
      this.timer = null;

      this.initialize();
  }

  initialize() {
      document.querySelector(`#${this.formId}`).onsubmit = (evt) => this.handleSubmit(evt);
      this.startTimer();
  }

  async handleSubmit(evt) {
      evt.preventDefault();
      const word = document.querySelector(`#${this.formId} input`).value;
      if (this.words.has(word)) {
          this.showMessage(`You've already found "${word}".`);
          return;
      }

      try {
          const response = await axios.post("/check-word", { word });
          const result = response.data.result;
          this.showMessage(result);
          if (result === "ok") {
              this.score += word.length;
              this.words.add(word);
              this.updateScore();
          }
      } catch (error) {
          console.error("Error checking word:", error);
      }
  }

  startTimer() {
      this.timer = setInterval(() => {
          this.timeLeft -= 1;
          document.querySelector(`#${this.timerId}`).innerText = this.timeLeft;
          if (this.timeLeft <= 0) {
              clearInterval(this.timer);
              document.querySelector(`#${this.formId}`).style.display = "none";
              this.showMessage("Time's up!");
              axios.post('/submit-score', { score: this.score })
                  .then(response => console.log("Stats updated:", response.data))
                  .catch(error => console.error("Error updating stats:", error));
          }
      }, 1000);
  }

  updateScore() {
      document.querySelector(`#${this.scoreId}`).innerText = this.score;
  }

  showMessage(msg) {
      document.querySelector(`#${this.messageId}`).innerText = msg;
  }
}

// Instantiate the game class when the DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  const game = new BoggleGame("board", "guess-form", "timer", "score", "message");
});

document.querySelector("#board-size-form").onsubmit = async function(evt) {
    evt.preventDefault();
    let size = document.querySelector("#board-size").value;
    try {
        const response = await axios.post("/set-board-size", { size: size });
        // Display the new board
        // Your code to update the board display goes here
    } catch (error) {
        console.error("Error setting board size:", error);
    }
};
