import os
import random
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from langchain import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Access the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Dictionary of mythical creatures based on birth month and gender
mythical_creatures = {
    'male': {
        1: ["Dragon", "Phoenix", "Griffin"],
        2: ["Unicorn", "Minotaur", "Griffin"],
        3: ["Centaur", "Sphinx", "Basilisk"],
        4: ["Kraken", "Cyclops", "Yeti"],
        5: ["Minotaur", "Leprechaun", "Chimera"],
        6: ["Werewolf", "Banshee", "Gorgon"],
        7: ["Pegasus", "Hydra", "Cerberus"],
        8: ["Elf", "Giant", "Valkyrie"],
        9: ["Vampire", "Zombie", "Ghoul"],
        10: ["Wendigo", "Djinn", "Kraken"],
        11: ["Goblin", "Troll", "Ogre"],
        12: ["Selkie", "Sprite", "Naga"]
    },
    'female': {
        1: ["Phoenix", "Fairy Queen", "Swan Maiden"],
        2: ["Mermaid", "Dryad", "Siren"],
        3: ["Sphinx", "Harpy", "Selene"],
        4: ["Nymph", "Gorgon", "Water Sprite"],
        5: ["Fairy", "Naga", "Chimera"],
        6: ["Banshee", "Lamia", "Hecate"],
        7: ["Valkyrie", "Pegasus", "Selkie"],
        8: ["Elf Queen", "Valkyrie", "Sylph"],
        9: ["Ghoul", "Vampire Queen", "Lamia"],
        10: ["Witch", "Nymph", "Djinn"],
        11: ["Goblin Queen", "Ogress", "Troll"],
        12: ["Selkie", "Sprite", "Naga Queen"]
    }
}

def call_openai_prompt(prompt_text):
    """Function to call OpenAI using Langchain."""
    llm = OpenAI(api_key=openai_api_key)
    response = llm(prompt_text)
    return response

def get_mythical_creature(birth_month, gender):
    """Randomly selects a mythical creature based on birth month and gender."""
    gender = gender.lower()

    if gender not in ['male', 'female']:
        return "Invalid gender. Please enter 'male' or 'female'."
    
    if birth_month < 1 or birth_month > 12:
        return "Invalid month. Please enter a number between 1 and 12."
    
    creatures = mythical_creatures[gender][birth_month]
    selected_creature = random.choice(creatures)
    
    # Use OpenAI (Langchain) to provide extra description
    prompt_text = f"Describe the mythical creature: {selected_creature}."
    description = call_openai_prompt(prompt_text)
    
    return {
        "creature": selected_creature,
        "description": description
    }

# Route to render the frontend HTML form
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-mythical-creature', methods=['POST'])
def mythical_creature_api():
    """API endpoint to get a mythical creature based on birth month and gender."""
    data = request.get_json()

    if not data or 'birth_month' not in data or 'gender' not in data:
        return jsonify({"error": "Invalid input. Please provide birth_month and gender."}), 400

    birth_month = data['birth_month']
    gender = data['gender']

    try:
        birth_month = int(birth_month)
    except ValueError:
        return jsonify({"error": "Birth month must be an integer."}), 400

    result = get_mythical_creature(birth_month, gender)
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
