# Rock–Paper–Scissors (Pygame Edition) — Portfolio Project

A polished, animated Rock–Paper–Scissors game built with Python and Pygame.  
Features animated icons, sound effects, difficulty selection, persistent statistics & graphs, AI-vs-AI visualization, and instructions to build a Windows executable.

## Features
- Sprite-based icons for Rock, Paper, Scissors
- Smooth scale/bounce animation on moves
- Sound effects: click, win, lose
- Difficulty levels: Easy / Adaptive / Hard
- Cumulative statistics persisted to `stats_store.json`
- Statistics graph (Matplotlib) — press `G` or click "Show Graph"
- AI-vs-AI simulation mode — press `V` or click "AI vs AI"
- Packable to single-file `.exe` using PyInstaller

## Controls
- Click a move button to play
- `G` key or "Show Graph" button → show statistics chart
- `V` key or "AI vs AI" button → toggle AI-vs-AI mode
- `Esc` → quit
- `Reset Stats` → clear saved statistics

## Setup & Run
1. Clone repository.
2. Add assets:
   - `assets/images/rock.png`
   - `assets/images/paper.png`
   - `assets/images/scissors.png`
   - `assets/sounds/click.wav`
   - `assets/sounds/win.wav`
   - `assets/sounds/lose.wav`
3. Install dependencies:
```bash
pip install -r requirements.txt
python main.py