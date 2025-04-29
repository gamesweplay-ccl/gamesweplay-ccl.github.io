const difficultyMap = {
	easy: "★",
	medium: "★★",
	hard: "★★★",
};

// Load JSON once and reuse
let gameData = [];
let lastFilteredGames = [];

async function loadGames() {
	if (gameData.length === 0) {
		const res = await fetch("static/all_metadata.json"); // adjust path as needed
		gameData = await res.json();
	}
	return gameData;
}

function getFilters() {
	return {
		difficulty: document.getElementById("difficulty").value,
		maxTime: document.getElementById("time").value,
		players: document.getElementById("players").value,
	};
}

function isPlayerCountInRange(selected, rangeStr) {
	const selectedNum = parseInt(selected);
	if (!rangeStr) return false;

	if (rangeStr.includes("-")) {
		const [min, max] = rangeStr.split("-").map((s) => parseInt(s.trim()));
		return selectedNum >= min && selectedNum <= max;
	}

	// Single number match
	return parseInt(rangeStr) === selectedNum;
}

function filterGames(games, { difficulty, maxTime, players }) {
	return games.filter((game) => {
		const matchesDifficulty =
			!difficulty || game.complexity === difficultyMap[difficulty];
		const matchesTime =
			!maxTime || parseInt(game.time) === parseInt(maxTime);
		const matchesPlayers =
			!players || isPlayerCountInRange(players, game.players);
		return matchesDifficulty && matchesTime && matchesPlayers;
	});
}

// "Find Games" Button
document
	.getElementById("game-filter")
	.addEventListener("submit", async function (e) {
		e.preventDefault();

		const filters = getFilters();
		const games = await loadGames();
		const matchingGames = filterGames(games, filters);
		lastFilteredGames = matchingGames;

		const resultsEl = document.getElementById("results-content");

		if (matchingGames.length > 0) {
			resultsEl.innerHTML = `<ul class="game-suggestions">${matchingGames
				.map(
					(g) => `
        <li style="margin-bottom: 2rem;">
          <a href="/games/${g.filename}.html"><strong>${
						g.title
					}</strong></a><br>

          <div class="game-info-box">
            <div class="game-stats">
              <span class="tooltip-gamestats" data-tooltip="${
					g.time
				} minutes"><i class="fas fa-clock"></i></span>
              <span class="tooltip-gamestats" data-tooltip="${
					g.players
				} players"><i class="fas fa-users"></i></span>
              <span class="tooltip-gamestats" data-tooltip="${
					g.game_format
				} required"><i class="fas fa-clone"></i></span>
              <span class="tooltip-gamestats" data-tooltip="Complexity: ${
					g.complexity
				}"><i class="fas fa-star"></i></span>
            </div>
          </div>

          <small>${g.summary || "No description available."}</small>
        </li>`
				)
				.join("")}
      </ul>`;

			document.getElementById(
				"random-from-filtered-container"
			).style.display = "block";
		} else {
			resultsEl.innerHTML =
				"<p>No games found matching your filters.</p>";
			document.getElementById(
				"random-from-filtered-container"
			).style.display = "none";
		}

		document.getElementById("results").style.display = "block";
	});

// Lucky link
document.addEventListener("DOMContentLoaded", () => {
	document
		.getElementById("lucky-link")
		.addEventListener("click", async function (e) {
			e.preventDefault(); // prevent jump

			const games = await loadGames(); // reuse existing function
			const randomGame = games[Math.floor(Math.random() * games.length)];
			window.location.href = `/games/${randomGame.filename}.html`;
		});
});

// Filtered random button
document
	.getElementById("filtered-random-btn")
	.addEventListener("click", function () {
		if (lastFilteredGames.length > 0) {
			const randomGame =
				lastFilteredGames[
					Math.floor(Math.random() * lastFilteredGames.length)
				];
			window.location.href = `/games/${randomGame.filename}.html`;
		} else {
			alert("No games available in the current filtered list.");
		}
	});
