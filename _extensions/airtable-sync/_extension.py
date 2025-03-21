from pyairtable import Api
import yaml
import os
import sys
from pathlib import Path
import requests
from dotenv import load_dotenv


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
    players = fields.get('Number of Players', '').strip()
    external_links = fields.get('External Links', '').strip()
    video_docs = fields.get('Video Docs', '').strip()
    summary = fields.get('Summary', '').strip()
    game_type = fields.get('Type', '').strip()
    time = fields.get('Time', '').strip()
    
    # Create basic frontmatter
    frontmatter = {
        'title': game_name,
        'game_format': game_format,
        'players': players,
        'external_links': external_links,
        'video_docs': video_docs,
        'summary': summary,
        'type': game_type,
        'time': time,
        'complexity': complexity,
        'airtable_id': record_id,
        'format': {
            'html': {
                'css': '../styles.css',
                'page-layout': 'full'
            }
        }
    }
    
    # Create the game page content
    with open(qmd_path, 'w') as f:
        print(f"Creating game file: {qmd_path}")

        
        f.write('---\n')
        yaml.dump(frontmatter, f, default_flow_style=False, allow_unicode=True)
        f.write('---\n\n')
        
        # Write the HTML structure directly
        f.write(f"# {game_name}\n\n")
        
        # Game info box
        f.write(":::{.game-info-box}\n")
        f.write(":::{.game-stats}\n")
        f.write(":::{.left-stats}\n")
        f.write(f"Player Count: {players}  \n")
        f.write(f"Time: {time}\n")
        f.write(":::\n")
        f.write(":::{.right-stats}\n")
        f.write(f"Format: {game_format}  \n")
        f.write(f"Complexity: {complexity}\n")
        f.write(":::\n")
        f.write(":::\n")
        f.write(":::\n\n")
        
        # Summary - add a placeholder if empty
        if summary:
            f.write(f"{summary}\n\n")
        else:
            f.write("Game summary not available yet.\n\n")
        
        # Always add action buttons section with at least placeholders
        f.write(":::{.game-actions}\n")
        if external_links:
            f.write(f"<a href=\"{external_links}\" class=\"btn btn-play\"><i class=\"fa fa-gamepad\"></i> Play the game</a>\n")
        else:
            f.write(f"<a href=\"#\" class=\"btn btn-play\"><i class=\"fa fa-gamepad\"></i> Play the game</a>\n")
            
        if video_docs:
            f.write(f"<a href=\"{video_docs}\" class=\"btn btn-watch\"><i class=\"fa fa-video\"></i> Watch a video</a>\n")
        else:
            f.write(f"<a href=\"#\" class=\"btn btn-watch\"><i class=\"fa fa-video\"></i> Watch a video</a>\n")
        f.write(":::")
    
    return qmd_path

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
        for record in records:
            try:
                qmd_path = create_game_file(games_dir, record['fields'], record['id'])
                if qmd_path:
                    created_files.append(qmd_path)
            except Exception as e:
                print(f"Error processing game {record.get('fields', {}).get('Game Name', 'Unknown')}: {str(e)}")
        
        print(f"Successfully created {len(created_files)} game files")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
