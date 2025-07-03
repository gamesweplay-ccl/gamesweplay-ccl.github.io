const difficultyMap = {
	easy: "★",
	medium: "★★",
	hard: "★★★",
};

const typeColors = {
	"Mathematics/Probability": "#ff9658",
	"SEL": "#94daff",
	"Strategy": "#fdd559",
	"Science/Deduction": "#bdd866",
};

let gameData = [];
let lastFilteredGames = [];

// Track selected values manually from toggle buttons
const formState = {
	time: "",
	players: "",
	difficulty: "",
};

// Setup toggle button behavior
document.querySelectorAll(".button-group").forEach((group) => {
	const name = group.dataset.name;
	const buttons = group.querySelectorAll("button");

	buttons.forEach((btn) => {
		btn.addEventListener("click", () => {
			buttons.forEach((b) => b.classList.remove("selected"));
			btn.classList.add("selected");
			formState[name] = btn.value;
		});
	});
});

// Load JSON if not already loaded
async function loadGames() {
	if (gameData.length === 0) {
		const res = await fetch("static/all_metadata.json");
		gameData = await res.json();
	}
	return gameData;
}

function isPlayerCountInRange(selected, rangeStr) {
	const selectedNum = parseInt(selected);
	if (!rangeStr) return false;

	if (rangeStr.includes("-")) {
		const [min, max] = rangeStr.split("-").map((s) => parseInt(s.trim()));
		return selectedNum >= min && selectedNum <= max;
	}

	return parseInt(rangeStr) === selectedNum;
}

function filterGames(games, { difficulty, time, players }) {
	return games.filter((game) => {
		const matchesDifficulty =
			!difficulty || game.complexity === difficultyMap[difficulty];
		const matchesTime = !time || parseInt(game.time) === parseInt(time);
		const matchesPlayers =
			!players || isPlayerCountInRange(players, game.players);
		return matchesDifficulty && matchesTime && matchesPlayers;
	});
}

// Form submit handler
document
	.getElementById("game-filter")
	.addEventListener("submit", async function (e) {
		e.preventDefault();

		const filters = { ...formState };
		const games = await loadGames();
		const matchingGames = filterGames(games, filters);
		lastFilteredGames = matchingGames;

		const resultsEl = document.getElementById("results-content");

		if (matchingGames.length > 0) {
			const typeOrder = [
				"Mathematics/Probability",
				"Strategy",
				"Science/Deduction",
				"SEL",
			];

			matchingGames.sort((a, b) => {
				return typeOrder.indexOf(a.type) - typeOrder.indexOf(b.type);
			});

			resultsEl.innerHTML = `<ul class="game-suggestions" style="list-style: none; padding: 0;">${matchingGames
				.map((g) => {
					const bgColor = typeColors[g.type] || "#ffffff";
					return `
					<li style="background-color: #fffdf0; padding: 1rem; margin-bottom: 0.5rem; border-top: 3rem solid ${bgColor}; border-left: 3px solid ${bgColor}; border-right: 3px solid ${bgColor}; border-bottom: 3px solid ${bgColor}; border-radius: 10px; position: relative;">
  					<a href="/games/${g.filename}.html" style="position: absolute; top: -2.2rem; left: 1rem; color: #fffdf0; font-weight: bold; text-decoration: none; background: transparent; padding: 0;">${g.title}</a>
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
				</li>`;
				})
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

// Lucky link handler
document.addEventListener("DOMContentLoaded", () => {
	const luckyLink = document.getElementById("lucky-link");
	if (luckyLink) {
		luckyLink.addEventListener("click", async function (e) {
			e.preventDefault();
			const games = await loadGames();
			const randomGame = games[Math.floor(Math.random() * games.length)];
			window.location.href = `/games/${randomGame.filename}.html`;
		});
	}
});

// Random from filtered results
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
