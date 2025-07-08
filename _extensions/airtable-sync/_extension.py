from pyairtable import Api
import yaml
import os
import sys
from pathlib import Path
import requests
from dotenv import load_dotenv
import json


def sanitize_filename(name):
    """Create a safe filename from a game name."""
    name = name.lower().replace(' ', '-').replace("'", '').replace('"', '')
    return ''.join(c for c in name if c.isalnum() or c in '-_')

def create_game_file(game_dir, fields, record_id):
    """Create a QMD file for a single game."""
    game_name = fields.get('Game Name', '').strip()
    if not game_name:
        return
    
    filename = sanitize_filename(game_name)
    qmd_path = game_dir / f"{filename}.qmd"
    
    # Get field values
    game_format = fields.get('Format', '').strip()
    complexity = fields.get('Complexity', '').strip()
    complexity = '★' * (1 + ['Primary', 'Middle', 'High'].index(complexity))
    players = fields.get('Number of Players', '').strip()
    external_links = fields.get('External Links', '').strip()
    rules_video = fields.get('Rules Video', '').strip()
    walkthrough_video = fields.get('Walkthrough Video', '').strip()
    summary = fields.get('Summary', '').strip()
    game_type = fields.get('Type', '').strip()
    time = fields.get('Time', '').strip()
    manual_links = fields.get('Manual Links', '').strip()
    board_links = fields.get('Board Links', '').strip()
    
    # Create basic frontmatter
    frontmatter = {
        'title': game_name,
        'game_format': game_format,
        'players': players,
        'external_links': external_links,
        'manual_links': manual_links,
        'board_links': board_links,
        'rules_video': rules_video,
        'walkthrough_video': walkthrough_video,
        'summary': summary,
        'type': game_type,
        'time': time,
        'complexity': complexity,
        'airtable_id': record_id,
        'filename': filename,
        'format': {
            'html': {
                'css': '../styles.css',
                'page-layout': 'full'
            }
        }
    }
    
    # Create the game page content
    with open(qmd_path, 'w', encoding="utf-8") as f:
        print(f"Creating game file: {qmd_path}")

        
        f.write('---\n')
        yaml.dump(frontmatter, f, default_flow_style=False, allow_unicode=True)
        f.write('---\n\n')
        
        # Write the HTML structure directly
        f.write(f"# {game_name}\n\n")
        
        # Game info box
        f.write(":::{.game-info-box}\n")
        f.write(":::{.game-stats}\n")
        f.write('```{=html}\n')
        f.write(f'<span class="tooltip-gamestats" data-tooltip="{time} minutes"><i class="fas fa-clock"></i></span>\n')
        f.write(f'<span class="tooltip-gamestats" data-tooltip="{players} players"><i class="fas fa-users"></i></span>\n')
        f.write(f'<span class="tooltip-gamestats" data-tooltip="{game_format} required"><i class="fas fa-clone"></i></span>\n')
        f.write(f'<span class="tooltip-gamestats" data-tooltip="{complexity}"><i class="fas fa-star"></i></span>\n')
        f.write('```\n')
        f.write(":::\n")
        f.write(":::\n\n")

        # Summary - add a placeholder if empty
        f.write(':::{.game-summary}\n')
        if summary:
            f.write(f"{summary}\n")
        else:
            f.write("Game summary not available yet.\n\n")
        f.write(":::\n\n")

        # Always add action buttons section with at least placeholders
        f.write(":::{.game-actions}\n```{=html}\n")
        if external_links:
            f.write(f'<a href="{external_links}" target="_blank" class="btn coloured-button"><i class="fa fa-gamepad"></i> Play the game</a>\n')
        elif game_type == 'SEL':
            pass
        else:
            f.write(f'<a href="#" target="_blank" class="btn disabled-button"><i class="fa fa-gamepad"></i> Play the game</a>\n')
            
        if rules_video:
            f.write(f'<a href="{rules_video}" target="_blank" class="btn coloured-button"><i class="fa fa-video"></i> Rules video</a>\n')
        else:
            f.write(f'<a href="#" target="_blank" class="btn disabled-button"><i class="fa fa-video"></i> Rules video</a>\n')

        if walkthrough_video:
            f.write(f'<a href="{walkthrough_video}" target="_blank" class="btn coloured-button"><i class="fa fa-video"></i> Watch us play</a>\n')
        else:
            f.write(f'<a href="#" target="_blank" class="btn disabled-button"><i class="fa fa-video"></i> Watch us play</a>\n')

        if manual_links:
            f.write(f'<a href="{manual_links}" target="_blank" class="btn coloured-button"><i class="fa fa-book"></i> Read the manual</a>\n')
        else:
            f.write(f'<a href="#" target="_blank" class="btn disabled-button"><i class="fa fa-book"></i> Read the manual</a>\n')

        if board_links:
            f.write(f'<a href="{board_links}" target="_blank" class="btn coloured-button"><i class="fa fa-file-pdf"></i> Printable PDF</a>\n')
        else:
            # f.write(f'<a href="#" target="_blank" class="btn disabled-button"><i class="fa fa-file-pdf"></i> Board PDF</a>\n')
            pass

        f.write('```\n')
        f.write(":::\n\n")

        with open('reactions.html', 'r') as reactions_file:
            reactions_html = reactions_file.read()
            f.write("```{=html}\n")
            f.write(reactions_html)
            f.write("```\n\n")

#         # Add Giscus comments
#         f.write(""" \n\n
# <script src="https://giscus.app/client.js"
# data-repo="gamesweplay-ccl/gamesweplay-ccl.github.io"
# data-repo-id="R_kgDOOLGMiQ"
# data-category="Announcements"
# data-category-id="DIC_kwDOOLGMic4CoVQN"
# data-mapping="title"
# data-strict="0"
# data-reactions-enabled="1"
# data-emit-metadata="0"
# data-input-position="bottom"
# data-theme="light"
# data-lang="en"
# crossorigin="anonymous"
# async>
# </script>
#         """
#         )
    
    return qmd_path, frontmatter

def main():
    try:
        # Airtable configuration
        load_dotenv()
        api_key = os.getenv("AIRTABLE_API_KEY")
        base_id = os.getenv("AIRTABLE_BASE_ID")  # Base ID for CCL Games We Play
        table_name = "Games"

        # Initialize Airtable API
        api = Api(api_key)
        table = api.table(base_id, table_name)
        print(f"Successfully connected to Airtable table '{table_name}'")
        
        # Create games directory if it doesn't exist
        games_dir = Path("../../games")
        games_dir.mkdir(exist_ok=True)
        print(f"Game files will be saved in: {games_dir.resolve()}")
        
        # Fetch all records
        records = table.all()
        print(f"Found {len(records)} games in Airtable")
        
        # Process each record
        created_files = []
        all_metadata = []
        for record in records:
            try:
                qmd_path, frontmatter = create_game_file(games_dir, record['fields'], record['id'])
                if qmd_path:
                    created_files.append(qmd_path)
                    all_metadata.append(frontmatter)
            except Exception as e:
                print(f"Error processing game {record.get('fields', {}).get('Game Name', 'Unknown')}: {str(e)}")
        
        print(f"Successfully created {len(created_files)} game files")

        # Dump all frontmatter as all_metadata.json
        json_output_path = Path("../../static/all_metadata.json")
        with open(json_output_path, "w", encoding="utf-8") as jf:
            json.dump(all_metadata, jf, ensure_ascii=False, indent=2)
        print(f"Dumped metadata to: {json_output_path.resolve()}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
