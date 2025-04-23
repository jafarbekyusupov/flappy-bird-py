# **🐦 Flappy Bird Clone**

#### A Python implementation of the classic Flappy Bird game **using Pygame**

## **🚀 Features**

_• Smooth animations and physics (Bird wing movements using sprites)_

_• Score tracking with high score system_

_• Pause/resume functionality_

_• Responsive UI with buttons_

_• Size selection menu (Small, Medium, Large)_

## **🕹️ How to Play**
_• Press Space to make the bird flap and avoid pipes_

_• Try to fly through the gaps between pipes to score points_

_• To Pause the Game - **Press P key or double-click the left mouse button**_

_• The game ends when you hit a pipe or the ground_

_• After game over, click "Play Again" to restart_

## 📜 Gameplay Showcase

> ### [Click here to view the Gameplay showcase](gameplay.md)

## ⚙️ Installation

1. 📥 **Clone the repository:**
   ```bash
   git clone https://github.com/jafarbekyusupov/flappy-bird-py.git
   cd flappy-bird-py

2. **🐍 Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. **📦 Install dependencies:**
   ```bash
   pip install -r requirements.txt # On Windows if pip is not recognized:  try py -m pip install -r requirements.txt
4. **🕹️ Run the game:**
   ```bash
   python main.py

## **🏗️ Project Structure**
  ```
flappy-bird/
├── game/  
│ ├── main.py ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  # Entry point that initializes and runs the game                                            
│ ├── settings.py‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  # Game settings and configuration                                                            
│ ├── game.py‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  # Main game logic and loop controller                                                        
│ ├── bird.py‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  # Bird class handling player character behavior                                                    
│ ├── pipes.py‎‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎   # Manages pipe creation, movement and collision                                                
│ ├── interface.py‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎   # Handles UI elements including buttons and overlays                                                            
│ ├── score_system.py‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎    # Manages score tracking and display                                                                       
│ ├── leaderboard.py‎‎             # LeaderboardButton button for Main Menu Screen to view leaderboard stored in .json file
│ 
├── testing/                 
│ ├── unit-tst.py                # Unit testing
│‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎                                                
├── assets/‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  # Game assets folder                                                        
│ ├── fonts/‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎# Font files                                                                                            
│ ├── img/‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎     # Image assets                                                                                                          
│ └── sounds/‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  # Sound effects                                                                
│
├── screenshots/
│ ├── game-Start-Screen.png          # Game Start Screen
| ├── game-getReady-screen.png       # Get ready Screen with 3 second countdown 
| ├── game-Pause-screen.png          # Game Pause Screen
| ├── gameOver-screen.png            # Game Over Screen
│
├── requirements.txt
├── gameplay.md                  # Screenshots and video showcasing the Gameplay
└── README.md‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  # This file                                          
```
