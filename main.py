from openai import OpenAI
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, render_template
import random
import json

# Load environment variables
load_dotenv()
app = Flask(__name__)

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY, base_url="https://api.studio.nebius.com/v1/")



def judgement(player_name, scenario, user_response):
    """Evaluates a player's response to a death scenario using AI."""
    try:
        response = openai.chat.completions.create(
            messages=[
                {"role": "system", "content": 'You are a judgement AI. You will be presented with a death scenario and the users answer to escape it. Judge and determine the outcome in the third person. respond in json format with values response and survived. for eg {"response": "the actual response", "survived": true}. Let the user be creative but be harsh on the user and find other ways for them to die. for example if user responses with "I would teleport out of the situation" create a sinario like "the teleporter breaks and they get teleported elsewhere and dies."'},
                {"role": "user", "content": f"Player: {player_name}\nScenario: {scenario}\nResponse: {user_response}"}
            ],
            model="meta-llama/Meta-Llama-3.1-405B-Instruct",
        )
        print(response)
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(e)
        return {"error": str(e)}
    


def write_scenario():
    scenarios = [
    "You are trapped in a sinking submarine with no escape hatch.",
    "A venomous snake bites you in the middle of a dense jungle.",
    "You wake up buried alive in a wooden coffin.",
    "A malfunctioning elevator plummets from the 50th floor.",
    "You're locked in a burning building with no visible exits.",
    "A massive tidal wave rushes toward you on the beach.",
    "You're stranded in a desert with no water or supplies.",
    "A pack of hungry wolves surrounds you in the snowy wilderness.",
    "You are handcuffed to a train track as a train approaches.",
    "You're falling from an airplane without a parachute.",
    "An assassin aims a sniper rifle at you from a nearby rooftop.",
    "A collapsing mine traps you deep underground.",
    "A bomb is strapped to your chest and set to detonate in one minute.",
    "You're lost in space with only 10 seconds of oxygen left.",
    "A grizzly bear charges at you in the middle of the forest.",
    "You're swimming in the ocean when a great white shark appears.",
    "A killer is hiding in your house, and the lights suddenly go out.",
    "You're hanging from a cliff, gripping the edge with one hand.",
    "You wake up on an empty plane with no pilots onboard.",
    "A giant boulder rolls toward you inside a narrow cave tunnel.",
    "You're locked inside a freezer with the temperature dropping rapidly.",
    "Your car brakes fail while driving toward a cliff.",
    "A swarm of highly venomous spiders crawls toward you.",
    "Your scuba tank runs out of oxygen deep underwater.",
    "A deadly gas starts filling the locked room you’re trapped in.",
    "You step onto a thin layer of ice and hear it cracking beneath you.",
    "You're being pulled into quicksand with no one around to help.",
    "A killer drone is hunting you through an abandoned city.",
    "You're dangling from a broken rope on a mountain ledge.",
    "You wake up chained inside a room filling with rising water.",
    "A horde of zombies surrounds your barricaded hideout.",
    "You're handcuffed to a sinking boat in the middle of the ocean.",
    "A hostile alien ship has locked weapons onto your escape pod.",
    "You're trapped in a room where the walls are slowly closing in.",
    "A high-speed train is heading straight toward your stalled car.",
    "You're lost in an Arctic blizzard with no shelter in sight.",
    "A gunman demands you choose between two impossible choices.",
    "You're on a collapsing bridge with nowhere to run.",
    "You wake up in a cage suspended over a lava pit.",
    "You're locked inside a vault running out of oxygen.",
    "A swarm of angry hornets attacks you in an open field.",
    "You're strapped to a rocket set to launch in one minute.",
    "You're on a sinking cruise ship with no life rafts left.",
    "A military missile is locked onto your exact coordinates.",
    "You're cornered by an aggressive street gang in a dark alley.",
    "A faulty parachute fails to open as you skydive.",
    "You're inside a haunted house where the doors disappear behind you.",
    "A stampede of wild buffalo charges straight toward you.",
    "Your space station is falling out of orbit toward Earth.",
    "A massive earthquake traps you under a collapsed building."
]

    return random.choice(scenarios)




@app.route("/judge", methods=["POST"])
def judge():
    """API endpoint to judge a player's response."""
    data = request.get_json()
    print(data)
    player_name = data.get("player_name")
    scenario = data.get("scenario")
    user_response = data.get("user_response")
    
    if not all([player_name, scenario, user_response]):
        return jsonify({"error": "Missing required fields"}), 400
    
    response = judgement(player_name, scenario, user_response)
    return jsonify(response)


@app.route("/scenario", methods=["GET"])
def get_scenario():
    scenario = write_scenario()
    return scenario


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/play", methods=["GET"])
def play():
    return render_template("game.html")


@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    """API endpoint to get the global leaderboard."""
    try:
        # Load the leaderboard from a file
        with open('leaderboard.json', 'r') as f:
            leaderboard = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        leaderboard = {}
    
    return jsonify(leaderboard)

@app.route("/api/leaderboard", methods=["POST"])
def update_leaderboard():
    """API endpoint to update the global leaderboard."""
    data = request.get_json()
    name = data.get("name")
    score = data.get("score")
    
    if not name or not isinstance(score, int):
        return jsonify({"error": "Invalid data"}), 400
    
    try:
        # Load existing leaderboard
        try:
            with open('leaderboard.json', 'r') as f:
                leaderboard = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            leaderboard = {}
        
        # Only update if this is a new high score for this player
        if name not in leaderboard or score > leaderboard[name]:
            leaderboard[name] = score
            
            # Save updated leaderboard
            with open('leaderboard.json', 'w') as f:
                json.dump(leaderboard, f)
            
            return jsonify({"success": True, "message": "Leaderboard updated"})
        else:
            return jsonify({"success": False, "message": "Not a high score"})
            
    except Exception as e:
        print(f"Error updating leaderboard: {e}")
        return jsonify({"error": "Server error"}), 500

if __name__ == "__main__":
    app.run()
