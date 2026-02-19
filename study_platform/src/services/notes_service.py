import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from config import Config

class NotesService:
    def __init__(self):
        self.notes_file = Config.DATA_DIR / 'user_notes.json'
        # Ensure data dir exists
        self.notes_file.parent.mkdir(parents=True, exist_ok=True)
        
    def get_notes(self) -> List[Dict]:
        """Loads notes sorted by date (newest first)"""
        if not self.notes_file.exists():
            return []
            
        try:
            with open(self.notes_file, 'r', encoding='utf-8') as f:
                notes = json.load(f)
            # Sort by timestamp descending
            notes.sort(key=lambda x: x['timestamp'], reverse=True)
            return notes
        except Exception as e:
            print(f"Error loading notes: {e}")
            return []
            
    def add_note(self, content: str):
        """Adds a new note with current timestamp"""
        notes = self.get_notes()
        
        new_note = {
            'timestamp': datetime.now().isoformat(),
            'display_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'content': content
        }
        
        notes.append(new_note)
        
        try:
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump(notes, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving note: {e}")
            
    def clear_notes(self):
        try:
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
        except:
            pass
