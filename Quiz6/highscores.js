const highScoresList = document.getElementById("highScoresList");
const highScores = JSON.parse(localStorage.getItem("highScores")) || [];

highScoresList.innerHTML = highScores
  .map(score => {
    return `<li class="high-score">${score.name} - ${score.score}</li>`;
  })
  .join("");


//   // Clear high scores function
// function clearHighScores() {
//   localStorage.removeItem('highScores');
//   // You might also want to update your UI to reflect the cleared scores
//   // For example, update a high score leaderboard on your webpage
// }

// // Example usage
// // You might call this function when a user clicks a "Clear High Scores" button
// clearHighScores();

  // Function to check and reset high scores
function checkAndResetHighScores() {
  // Get the timestamp of the last high score update from localStorage
  const lastUpdateTimestamp = localStorage.getItem('lastUpdateTimestamp');

  // Check if the last update timestamp exists and meets the reset condition (e.g., 24 hours)
  if (lastUpdateTimestamp && Date.now() - lastUpdateTimestamp > 24 * 60 * 60 * 1000) {
      // Reset high scores
      localStorage.removeItem('highScores');
      console.log('High scores reset.');

      // Update the last update timestamp
      localStorage.setItem('lastUpdateTimestamp', Date.now());
  }
}

// Call the function when the game starts or when the user accesses a relevant page
checkAndResetHighScores();

