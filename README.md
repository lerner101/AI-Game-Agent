# Colosseum Survival!
This project features an AI agent utilizing the Minimax algorithm to make optimal decisions in a game setting. The Minimax algorithm is a classic approach in artificial intelligence for decision-making in two-player games. In this implementation, the student agent player is empowered with Minimax to strategically navigate the game space and make optimal moves. Feel free to explore the code, understand the Minimax algorithm's mechanics, and adapt it for your own game scenarios. Whether you're a student diving into AI or an enthusiast exploring game-playing agents, this repository serves as a valuable resource for learning and experimentation. Enjoy gaming with intelligence!

### Final Report
The final report/Analysis of my agent can be found in the **Final_Report.pdf**

### View MiniMax Algorithm
Code used for Agent in competition can be found in Agenta/student_agent

## Setup

To setup the game, clone this repository and install the dependencies:

```bash
pip install -r requirements.txt
```

## Playing a game vs my Agent

To start playing a game, we will run the simulator and specify which agents should complete against eachother. To start, several agents are given to you, and you will add your own following the same game interface. For example, to play the game using two copies of the provided random agent (which takes a random action every turn), run the following:

```bash
python simulator.py --player_1 student_agent --player_2 random_agent
```

This will spawn a random game board of size NxN, and run the two agents of class [RandomAgent](agents/random_agent.py). You will be able to see their moves in the console.

## Visualizing a game vs my Agent

To visualize the moves within a game, use the `--display` flag. You can set the delay (in seconds) using `--display_delay` argument to better visualize the steps the agents take to win a game.

```bash
python simulator.py --player_1 student_agent --player_2 random_agent --display
```

## Play on your own!

To take control of one side of the game and compete against the random agent yourself, use a [`human_agent`](agents/human_agent.py) to play the game.

```bash
python simulator.py --player_1 human_agent --player_2 random_agent --display
```

## Autoplaying multiple games

There is some randomness (coming from the initial game setup and potentially agent logic), so go fairly evaluate agents, we will run them against eachother multiple times, alternating their roles as player_1 and player_2, and on boards are drawn randomly (between size 6 and 12). The aggregate win % will determine a fair winner. Use the `--autoplay` flag to run $n$ games sequentially, where $n$ can be set using `--autoplay_runs`.

```bash
python simulator.py --player_1 student_agent --player_2 random_agent --autoplay
```

During autoplay, boards are drawn randomly between size `--board_size_min` and `--board_size_max` for each iteration. You may try various ranges for your own information and development by providing these variables on the command-line. However, the defaults (to be used during grading) are 6 and 12, so ensure the timing limits are satisfied for every board in this size range. 


## Full API

```bash
python simulator.py -h       
usage: simulator.py [-h] [--player_1 PLAYER_1] [--player_2 PLAYER_2]
                    [--board_size BOARD_SIZE] [--display]
                    [--display_delay DISPLAY_DELAY]

optional arguments:
  -h, --help            show this help message and exit
  --player_1 PLAYER_1
  --player_2 PLAYER_2
  --board_size BOARD_SIZE
  --display
  --display_delay DISPLAY_DELAY
  --autoplay
  --autoplay_runs AUTOPLAY_RUNS
```

