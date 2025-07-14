# **🐦 Flappy Bird Clone**

#### A Python implementation of the classic Flappy Bird game **using Pygame**

> [!TIP]
> #### [View the full project overview with UML Diagrams and detailed explanations by Cognition here](https://deepwiki.com/jafarbekyusupov/flappy-bird-py)

---

## 🎥 [Gameplay Video](https://youtube.com/shorts/bFRbRM-ebN0)

[![Flappy Bird Demo](https://i.ytimg.com/vi/bFRbRM-ebN0/sddefault.jpg)](https://youtube.com/shorts/bFRbRM-ebN0)

### [→ Watch the full demo on YouTube](https://youtube.com/shorts/bFRbRM-ebN0)

---

## **🚀 Features**

_• Smooth animations and physics (Bird wing movements using sprites)_

_• **Score tracking system** and **Leaderboard** implementation for Top Scores, storing data in .json format_

_• Pause/resume functionality_

_• Responsive UI with buttons_

_• Size selection menu (Small, Medium, Large)_

## **🕹️ How to Play**
_• Press Space to make the bird flap and avoid pipes_

_• Try to fly through the gaps between pipes to score points_

_• To Pause the Game - **Press P key or double-click the left mouse button**_

_• The game ends when you hit a pipe or the ground_

_• After game over, click "Play Again" to restart_

_• If your score is high enough, an input box will appear — enter your name to be featured on the leaderboard_

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
   source venv/bin/activate  # On Windows use `venv/Scripts/activate`
3. **📦 Install dependencies:**
   ```bash
   pip install -r requirements.txt # On Windows if pip is not recognized:  try py -m pip install -r requirements.txt
4. **🕹️ Run the game:**
   ```bash
   python code/main.py

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
│ ├── leaderboard.py‎‎             # LeaderboardButton button for Main Menu Screen to view leaderboard
│ 
├── testing/                 
│ ├── bird-test.py               # Unit testing for Bird object from code/Bird.py
│‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎                                                
├── assets/‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  # Game assets folder                                                                                                                                                
│ ├── img/‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎     # Image assets                                                              
│
├── gameplay/
│ ├── gameplay.mp4                   # Gameplay Demo in Video Format
│ ├── game-Start-Screen.png          # Game Start Screen
| ├── game-getReady-screen.png       # Get ready Screen with 3 second countdown 
| ├── game-Pause-screen.png          # Game Pause Screen
| ├── gameOver-screen.png            # Game Over Screen
│ ├── game-Leaderboard.png           # Leaderboard
│
├── requirements.txt
├── gameplay.md                  # Screenshots and video showcasing the Gameplay
└── README.md‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  # This file                                          
```
