# Survive and Suffer

A grim but entertaining web-based game where you must outwit death itself through creative thinking and problem-solving.

## Overview

Survive and Suffer challenges players with deadly scenarios and asks them to devise escape plans. An AI judge evaluates these plans to determine if the player lives or dies. The game features a persistent leaderboard to track the most successful survivors.

## Features

- **Death Scenarios**: Face randomly generated life-threatening situations
- **AI Judgment**: Your escape plans are evaluated by an AI to determine your fate
- **Leaderboard**: Compete with others to see who can survive the most scenarios
- **Progressive Difficulty**: Challenges become increasingly difficult as you survive longer

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript
- **AI Integration**: OpenAI API
- **Icons**: Font Awesome

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/survive-and-suffer.git
   cd survive-and-suffer
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

5. Run the application:
   ```
   python main.py
   ```

6. Open your browser and navigate to `http://localhost:5000`

## How to Play

1. Enter your name to begin
2. Read the death scenario presented to you
3. Type your escape plan in the text area
4. Submit your plan and await judgment
5. If you survive, you'll face increasingly difficult scenarios
6. Your highest survival score will be recorded on the leaderboard

## Project Structure

- `main.py`: Flask application with route handlers and game logic
- `templates/`: HTML templates for the web interface
  - `index.html`: Landing page
  - `game.html`: Main game interface
  - `main.html`: Base template with common elements

## License

© 2025 AaravAtGit
