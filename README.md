# Santorini Game FIT3077 - Sprint 3
## Alvin Andrean - 33279071

An implementation of the board game Santorini using Python and Pygame with an object-oriented architecture. 

## Features

- **Santorini Core Mechanics**: Selecting workers, moving workers, building blocks and domes
- **Tutorial System**: Learn with guided tutorials (Basic, Win Condition, Lose Condition)
- **God Cards**: Special abilities including Artemis, Demeter, and Triton
- **Timer System**: Configurable turn timers

## Installation
1. Clone the repository
2. Navigate to `Sprint 3/prototype/`
3. Install dependencies: `pip install pygame`
4. Run the game: `python application.py`

### Creating an Executable
```bash
cd "Sprint 3/prototype"
pip install pyinstaller
pyinstaller --onefile --add-data "assets;assets" --noconsole --name "Santorini" application.py
```

## 📁 Project Structure

### Root Directory
```
Sprint 3/
├── prototype/          # Main game implementation
├── document/          # UML diagrams and documentation
└── README.md         # This file
```

### Class Diagrams and Documentation
```
document/
├── final/             # Final UML class diagram and CRC cards
├── crc_draft        # CRC cards draft (progress)
├── class_diagram_draft # UML class diagram draft (progress)
└── design_rationale/ # Design rationale
```

### Main Application
```
prototype/
├── application.py     # Main application entry point and game loop
└── .gitignore        # Git ignore configuration
```

## File Organization by Directory

### ui/
- **`base_screen.py`** - Abstract base class for all screens
- **`screen_enums.py`** - Screen type enumeration
- **`screen_manager.py`** - Manages screen transitions and lifecycle
- **`main_menu_screen.py`** - Main menu with title image and navigation
- **`tutorial_selection_screen.py`** - Tutorial type selection screen
- **`setup_screen.py`** - Game configuration and player setup
- **`game_screen.py`** - Main gameplay screen with board visualization
- **`game_over_screen.py`** - Victory/defeat screen with replay options

### core/
- **`game.py`** - Main game controller
- **`board.py`** - Game board representation and tile management
- **`tile.py`** - Individual tile properties
- **`player.py`** - Player data
- **`worker.py`** - Worker pieces and positioning
- **`position.py`** - 2D coordinates

### game_modes/
- **`game_mode.py`** - Abstract base class for game modes
- **`standard_game_mode.py`** - Traditional multiplayer gameplay
- **`tutorial_game_mode.py`** - Guided learning experience (tutorial mode)

### tutorial/
- **`tutorial_manager.py`** - Manages tutorial progression and state
- **`tutorial_step.py`** - Abstract base class for tutorial steps
- **`tutorial_observer.py`** - Observer pattern for tutorial events
- **`tutorial_ui_adapter.py`** - UI integration for tutorials

### tutorial/steps/
- **`introduction_step.py`** - Welcome and instructions
- **`select_worker_step.py`** - Learn worker selection
- **`move_worker_step.py`** - Learn movement mechanics
- **`build_step.py`** - Learn building construction
- **`move_to_level3_step.py`** - Win condition tutorial
- **`move_to_trap_step.py`** - Lose condition tutorial
- **`completion_step.py`** - Tutorial completion and celebration

### god_cards/
- **`god_card.py`** - Base god card functionality
- **`artemis.py`** - Move twice ability
- **`demeter.py`** - Build twice ability  
- **`triton.py`** - Perimeter movement ability
- **`god_card_deck.py`** - Deck of god cards
- **`god_card_factory.py`** - Create and register new god cards
- **`standard_god_card.py`** - God Card with no special ability (for tutorial mode)

### buildings/
- **`building.py`** - Building abstract class
- **`block.py`** - A building that can be at level 1, 2, or 3.
- **`dome.py`** - A type of building that blocks worker from moving onto the tile

### actions/
- **`move_action.py`** - Worker movement logic
- **`build_action.py`** - Building construction logic
- **`action_result.py`** - Result of action execution
- **`action.py`** - Abstract action class
- **`artemis_move_action.py`** - Artemis Worker movement logic
- **`demeter_build_action.py`** - Demeter Building construction logic
- **`triton_move_action.py`** - Triton Worker movement logic

### win_conditions/
- **`standard_win_condition.py`** - Level 3 win condition and both worker unable to move lose condition
- **`timer_win_condition.py`** - Timer runs out lose condition
- **`composite_win_condition.py`** - Combination of multiple win conditions
- **`win_condition_strategy.py`** - Abstract win condition class
- **`win_condition_checker.py`** - Determine win/lose

### game_management/
- **`turn_manager.py`** - Turn sequence and phase management
- **`game_input_handler.py`** - Handles game input interactions
- **`game_phase_manager.py`** - Manages game phases and action sequences
- **`seqeunce.py`** - A sequence of items that can be iterated over.

### assets/
- **`background.png`** - Main menu background
- **`setup.png`** - Setup screen background
- **`game.png`** - Game screen background
- **`tutor.png`** - Tutorial selection background
- **`title.png`** - Game title logo
- **`grass.png`** - Light tile texture
- **`grass_dark.png`** - Dark tile texture
- **`red_worker.png`** - Red player worker sprite
- **`blue_worker.png`** - Blue player worker sprite
- **`worker.png`** - Generic worker fallback
- **`artemis.png`** - Artemis god card image
- **`demeter.png`** - Demeter god card image
- **`triton.png`** - Triton god card image
- **`music.mp3`** - Background music track

### colors/
- **`color.py`** - Color enumeration

### utils/
- **`resource_manager.py`** - Asset loading and caching
- **`validator.py`** - Game rule validation
- **`timer_manager.py`** - Player timer functionality
- **`player_timer.py`** - Player's timer information

## How to Play

### Standard Mode
1. **Setup**: Configure player names, colors, and timer duration
2. **Gameplay**: Take turns moving workers and building structures
3. **Victory**: First player to move a worker to a level 3 building wins

### Tutorial Mode
Choose from three tutorials:
- **Basic Tutorial**: Learn fundamental game mechanics
- **Win Tutorial**: Practice achieving victory conditions
- **Lose Tutorial**: Understand defeat scenarios

### Controls
- **Mouse**: Click to interact with buttons and board
- **Keyboard Shortcuts**:
  - `ESC`: Return to main menu
  - `SPACE`: Play again (on game over screen)

## Game Rules

### Basic Rules
1. **Turn Structure**: Must Move → Build → End Turn
2. **Movement**: Adjacent tiles only, can't move up more than 1 level
3. **Building**: Adjacent to worker, builds levels 1-3 then dome
4. **Victory**: Move worker to level 3 building
5. **Defeat**: Can't move any worker

### God Card Abilities
- **Artemis**: May move one additional time (not back to start)
- **Demeter**: May build one additional time (not same space)
- **Triton**: May move unlimited times on perimeter

## Code Style
- Follow PEP 8 Python style guidelines and PEP257 for docstrings
- Use type hints for better code documentation
- Maintain clear separation of concerns


 
 