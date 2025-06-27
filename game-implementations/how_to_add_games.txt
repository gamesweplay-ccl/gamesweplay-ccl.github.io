# How do i add games here?

1. Download the game files
2. Copy the game files into game-implementations
   cp -r your-game-folder/ game-implementations/
3. If the game folder has index.html, rename it to something else (like start.html)
   mv index.html start.html (inside the game folder)
4. Remove the .git directory if it is there
   rm -rf .git/ (inside the game folder)
5. Update the airtable and make the game link
   eg. for lines-of-action it will be https://gamesweplay-ccl.github.io/game-implementations/lines-of-action/start.html
