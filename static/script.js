//const API = "http://localhost:5000";

    async function setName() {
      const name = document.getElementById("playerName").value;
      const res = await fetch('/', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
      });
      const data = await res.json();
      console.log(data);
      message = data.message || data.error;
      document.getElementById("output").innerText = message;
      document.getElementById("difficulty-section").style.display = "block";
    }

    async function setDifficulty() {
      const difficulty = document.getElementById("difficulty").value;
      const res = await fetch('/diff_lvl', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ difficulty })
      });
      const data = await res.json();
      console.log(data);
      max_attempts = data.max_attempts || data.error;
      min = data.min;
      max = data.max;
      console.log("Min Number:", min);
      console.log("Max Number:", max);
      console.log("Max Attempts:", max_attempts);
      document.getElementById("output").innerText = "Guess a number between " + min + " and " + max + ". You have " + max_attempts + " attempts.";
      document.getElementById("game-section").style.display = "block";
      // document.getElementById("exit-section").style.display = "block";
    }

    async function makeGuess() {
      const guess = document.getElementById("guess").value;
      const res = await fetch('/game', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ guess })
      });
      const data = await res.json();
      console.log(data);
      document.getElementById("output").innerText = data.message + " You have " + data.attempts_left + " attempts left.";
      console.log(data.message)
      if (data.message === "Correct!" || data.attempts_left === 0) {
        document.getElementById("exit-section").style.display = "block";
      }
      
    }

    async function exitGame() {
      const res = await fetch('/exit', { method: "POST" });
      const data = await res.json();
      console.log(data);
      message = data.message || data.error;
      player = data.player || "Player";
      document.getElementById("output").innerText = " Goodbye "
      + player+"! Hope to See you again soon.";
      document.getElementById("name-section").style.display = "none";
      document.getElementById("difficulty-section").style.display = "none";
      document.getElementById("game-section").style.display = "none";
      document.getElementById("exit-section").style.display = "none";
    }

    async function showLeaderboard() {
      document.getElementById("container").style.display = "none";
      document.getElementById("exit-section").style.display = "block";
      const res = await fetch('/leaderboard');
      const data = await res.json();
      console.log(data);
//.     New
      document.getElementById("leaderboard").style.display = "flex";
      const container = document.getElementById("score-list");
      for (const level in data) {
  const section = document.createElement("div");

  let rows = data[level]
    .map(item => `<tr><td>${item.name}</td><td>${item.score}</td></tr>`)
    .join('');

  section.innerHTML = `
    <h2>${level}</h2>
    <table border="1" cellpadding="5">
      <tr><th>Name</th><th>Score</th></tr>
      ${rows}
    </table>
  `;

  container.appendChild(section);
}


      // document.getElementById("output").innerText = JSON.stringify(data, null, 2);
    }

    function resetGame() {
      window.location.reload('/');
      
    }