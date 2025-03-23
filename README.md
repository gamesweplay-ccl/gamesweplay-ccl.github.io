# Games We Play

A Quarto website showcasing our collection of games and puzzles, with data synchronized from Airtable.

## Features

- Automatically syncs game data from Airtable
- Individual game pages with detailed information
- Responsive design with modern UI
- Filterable and sortable game listings

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Airtable API key in the extension configuration
4. Run the sync command to fetch game data:
   ```bash
   cd _extentions/airtable-sync
   python _extension.py
   ```
5. Preview the website:
   ```bash
   quarto preview
   ```

## Technologies

- [Quarto](https://quarto.org/) for website generation
- [Airtable](https://airtable.com/) for game data management
- FontAwesome for icons
- Custom CSS for styling

## Typography

- Headings: Lato
- Body text: Droid Sans
