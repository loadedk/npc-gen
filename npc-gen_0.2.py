import random
import requests
import json
import os

# LM Studio/Ollama API endpoint (确认 LM Studio 的配置)
OLLAMA_API_URL = "http://localhost:1234/v1/chat/completions"  # Default LM Studio, adjust as needed.  Check the port in LM Studio.

# 5e 2024 Ruleset (Expanded)
RACES = ["Human", "Elf", "Dwarf", "Halfling", "Gnome", "Tiefling", "Dragonborn"]
CLASSES = ["Fighter", "Rogue", "Wizard", "Cleric", "Barbarian", "Bard", "Sorcerer"]
ALIGNMENTS = ["Lawful Good", "Neutral Good", "Chaotic Good", "Lawful Neutral", "Neutral",
              "Chaotic Neutral", "Lawful Evil", "Neutral Evil", "Chaotic Evil"]
BACKGROUNDS = ["Acolyte", "Charlatan", "Criminal", "Entertainer", "Folk Hero", "Guild Artisan", "Hermit",
               "Noble", "Outlander", "Sage", "Sailor", "Soldier", "Urchin"]
SKILLS = ["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History", "Insight",
          "Intimidation", "Investigation", "Medicine", "Nature", "Perception", "Performance", "Persuasion",
          "Religion", "Sleight of Hand", "Stealth", "Survival"]

# Expanded name lists (you can add more!)
HUMAN_NAMES = ["Alice", "Bob", "Charlie", "David", "Emily", "Ethan", "Fiona", "George", "Hannah", "Henry"]
ELF_NAMES = ["Lyra", "Elorin", "Sylas", "Aria", "Thaldir", "Nayana", "Valen", "Seraphina", "Kaelen", "Elandra"]
DWARF_NAMES = ["Borin", "Gimli", "Fargrim", "Disa", "Kildrak", "Morana", "Belar", "Sigrun", "Dwalin", "Astrid"]
HALFLING_NAMES = ["Frodo", "Lily", "Pippin", "Rose", "Merry", "Daisy", "Bilbo", "Primrose", "Samwise", "Jasmine"]
GNOME_NAMES = ["Fizzle", "Bimble", "Zook", "Trixie", "Glim", "NImble", "Wiz", "Pippa", "Jorn", "Elara"]
TIEFLING_NAMES = ["Asmodeus", "Lilith", "Xaphon", "Morwenna", "Zael", "Bryseis", "Vaxil", "Shiara", "Kael", "Inferna"]
DRAGONBORN_NAMES = ["Arjhan", "Valeris", "Torinn", "Immerse", "Kriv", "Medrash", "Surina", "Nala", "Jorr", "Myrddin"]

def get_random_name(race, gender):
    """Gets a random name based on the race and gender, or generates one using LM Studio."""
    if race == "Human":
        if gender == "Male":
            return random.choice(HUMAN_NAMES)
        else:
            return random.choice(HUMAN_NAMES)
    elif race == "Elf":
        if gender == "Male":
            return random.choice(ELF_NAMES)
        else:
            return random.choice(ELF_NAMES)
    elif race == "Dwarf":
        if gender == "Male":
            return random.choice(DWARF_NAMES)
        else:
            return random.choice(DWARF_NAMES)
    elif race == "Halfling":
        if gender == "Male":
            return random.choice(HALFLING_NAMES)
        else:
            return random.choice(HALFLING_NAMES)
    elif race == "Gnome":
        if gender == "Male":
            return random.choice(GNOME_NAMES)
        else:
            return random.choice(GNOME_NAMES)
    elif race == "Tiefling":
        if gender == "Male":
            return random.choice(TIEFLING_NAMES)
        else:
            return random.choice(TIEFLING_NAMES)
    elif race == "Dragonborn":
        if gender == "Male":
            return random.choice(DRAGONBORN_NAMES)
        else:
            return random.choice(DRAGONBORN_NAMES)
    else:
        prompt = f"Suggest a full name for a {gender} {race} character."
        return generate_ollama_text(prompt)

# Ability Score Generation and Modifiers
def generate_ability_scores(strength_level):
    """Generates ability scores based on the specified strength level."""
    print(f"generate_ability_scores(strength_level={strength_level})")  # Debug print
    scores = {}
    if strength_level == "weak":
        scores = {stat: random.randint(8, 12) for stat in
                  ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]}
    elif strength_level == "average":
        scores = {stat: random.randint(10, 15) for stat in
                  ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]}
    elif strength_level == "strong":
        scores = {stat: random.randint(13, 18) for stat in
                  ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]}
    elif strength_level == "very strong":
        base = [random.randint(15, 18) for _ in range(3)] + [random.randint(10, 14) for _ in range(3)]
        random.shuffle(base)
        scores = dict(zip(["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"], base))
    elif strength_level == "godly":
        base = [random.randint(18, 20) for _ in range(3)] + [random.randint(15, 18) for _ in range(3)]
        random.shuffle(base)
        scores = dict(zip(["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"], base))
    else:
        scores = {stat: random.randint(3, 18) for stat in
                  ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]}
    print(f"  Generated scores: {scores}")  # Debug print
    return scores


def calculate_modifier(score):
    """Calculates the ability score modifier."""
    print(f"calculate_modifier(score={score})")  # Debug print
    modifier = (score - 10) // 2
    print(f"  Modifier: {modifier}")  # Debug print
    return modifier


def calculate_saves(ability_scores, class_name):
    """Calculates saving throw bonuses."""
    print(f"calculate_saves(ability_scores={ability_scores}, class_name={class_name})")  # Debug print
    saves = {}
    proficiencies = {"Fighter": ["Strength", "Constitution"], "Rogue": ["Dexterity", "Intelligence"],
                     "Wizard": ["Intelligence", "Wisdom"], "Cleric": ["Wisdom", "Charisma"],
                     "Barbarian": ["Strength", "Constitution"], "Bard": ["Dexterity", "Charisma"],
                     "Sorcerer": ["Constitution", "Charisma"]}
    for stat in ability_scores:
        modifier = calculate_modifier(ability_scores[stat])
        saves[stat] = modifier + (2 if stat in proficiencies.get(class_name, []) else 0)
    print(f"  Saves: {saves}")  # Debug print
    return saves


def calculate_skills(ability_scores, class_name):
    """Calculates skill bonuses."""
    print(f"calculate_skills(ability_scores={ability_scores}, class_name={class_name})")  # Debug print
    skills = {}
    for skill in SKILLS:
        stat = {"Acrobatics": "Dexterity", "Animal Handling": "Wisdom", "Arcana": "Intelligence",
                "Athletics": "Strength", "Deception": "Charisma", "History": "Intelligence", "Insight": "Wisdom",
                "Intimidation": "Charisma", "Investigation": "Intelligence", "Medicine": "Wisdom",
                "Nature": "Intelligence", "Perception": "Wisdom", "Performance": "Charisma",
                "Persuasion": "Charisma", "Religion": "Intelligence", "Sleight of Hand": "Dexterity",
                "Stealth": "Dexterity", "Survival": "Wisdom"}[skill]
        modifier = calculate_modifier(ability_scores[stat])
        skills[skill] = modifier + random.choice([0, 2])  # basic proficiency
    print(f"  Skills: {skills}")  # Debug print
    return skills


def calculate_hit_points(ability_scores, class_name):
    """Calculates hit points."""
    print(f"calculate_hit_points(ability_scores={ability_scores}, class_name={class_name})")  # Debug print
    hit_die = {"Fighter": 10, "Rogue": 8, "Wizard": 6, "Cleric": 8, "Barbarian": 12, "Bard": 8, "Sorcerer": 6}[
        class_name]
    hp = hit_die + calculate_modifier(ability_scores["Constitution"])
    print(f"  Hit Points: {hp}")  # Debug print
    return hp


# Ollama/LM Studio Interaction
def generate_ollama_text(prompt, model="qwen2.5-7b-instruct_character_roleplay_dataset_20000"):
    """Generates text using Ollama or LM Studio."""
    print(f"generate_ollama_text(prompt=\"{prompt[:50]}...\", model=\"{model}\")")
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}  # Use the Chat Completions format
        ],
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=data)
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"]  # Extract from chat completions format
        print(f"  Response: \"{text[:50]}...\"")
        return text
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with LM Studio/Ollama: {e}")
        return "Could not generate."



# NPC Generation
def generate_npc(strength_level="average"):
    """Generates a single NPC."""
    print(f"generate_npc(strength_level=\"{strength_level}\")")  # Debug print
    #randomly select gender
    gender = random.choice(["Male", "Female"])
    npc = {
        "race": random.choice(RACES),
        "class": random.choice(CLASSES),
        "alignment": random.choice(ALIGNMENTS),
        "background": random.choice(BACKGROUNDS),
        "gender": gender, #added gender
    }
    npc["name"] = get_random_name(npc["race"], gender)  # Add name here, pass gender
    print(f"  Initial NPC: {npc}")  # Debug print
    npc["ability_scores"] = generate_ability_scores(strength_level)
    npc["saves"] = calculate_saves(npc["ability_scores"], npc["class"])
    npc["skills"] = calculate_skills(npc["ability_scores"], npc["class"])
    npc["hit_points"] = calculate_hit_points(npc["ability_scores"], npc["class"])

    prompt_backstory = f"Generate a detailed backstory for a {npc['gender']} {npc['race']} {npc['class']} named {npc['name']} with the background of a {npc['background']}. Their alignment is {npc['alignment']}. Aim for around 100-150 words." #changed prompt
    npc["backstory"] = generate_ollama_text(prompt_backstory) #moved up

    prompt_traits = f"Generate 2-3 personality traits for this NPC named {npc['name']}, considering their background and alignment. {npc['backstory']} Keep it brief."  # Changed prompt to include backstory
    prompt_appearance = f"Describe the physical appearance of this {npc['race']} {npc['class']} named {npc['name']}.  Provide a detailed description, including their age, gender, height, weight, and any distinctive features. Aim for around 75-100 words."
    prompt_equipment = f"Suggest some appropriate equipment for a {strength_level} {npc['class']} named {npc['name']}.  List only the most important items, and list them clearly and concisely (e.g., \"Longsword, Shield, Leather Armor\")." #changed prompt

    npc["traits"] = generate_ollama_text(prompt_traits)
    npc["appearance"] = generate_ollama_text(prompt_appearance)
    npc["equipment"] = generate_ollama_text(prompt_equipment)
    print(f"  Final NPC: {npc}")  # Debug print
    return npc


def generate_npcs(num_npcs=1, strength_level="average"):
    """Generates multiple NPCs with the same strength level."""
    npcs = []
    for _ in range(num_npcs):
        npcs.append(generate_npc(strength_level))
    return npcs


def write_json_file(filename, data, append=False):
    """Writes data to a JSON file, optionally appending."""
    if append and os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]  # Ensure it's a list
                existing_data.extend(data)  # Extend the list
                data = existing_data
        except json.JSONDecodeError:
            print(f"Warning: {filename} was not valid JSON. Overwriting.")

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def generate_npc_html(npcs):
    """Generates an HTML file to display the NPC information."""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated NPCs</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f5f5f5;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            max-width: 800px;
            width: 95%;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }

        h1 {
            color: #2a6496;
            text-align: center;
            margin-bottom: 20px;
            border-bottom: 2px solid #2a6496;
            padding-bottom: 10px;
        }

        h2 {
            color: #4a90e2;
            margin-top: 25px;
            margin-bottom: 10px;
            border-bottom: 1px solid #4a90e2;
            padding-bottom: 5px;
        }

        h3 {
            color: #666;
            margin-top: 20px;
            margin-bottom: 5px;
        }

        p {
            margin-bottom: 10px;
            line-height: 1.6;
        }

        ul {
            list-style-type: disc;
            padding-left: 20px;
            margin-bottom: 10px;
        }

        .npc-section {
            margin-bottom: 30px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: #f9f9f9;
        }

        .ability-scores {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 10px;
        }

        .ability-scores div {
            background-color: #e9ecef;
            padding: 8px;
            border-radius: 4px;
            text-align: center;
        }

        .saves-throws {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 10px;
        }

        .saves-throws div {
            background-color: #f0f0f0;
            padding: 8px;
            border-radius: 4px;
            text-align: center;
        }

        .skills {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 10px;
        }

        .skills div {
            background-color: #f0f0f0;
            padding: 8px;
            border-radius: 4px;
            text-align: center;
        }

        @media (max-width: 600px) {
            .ability-scores, .saves-throws, .skills {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Generated NPCs</h1>
        """
    for i, npc in enumerate(npcs):
        html_content += f"""
        <div class="npc-section">
            <h2>NPC {i + 1}: {npc['name']}</h2>
            <h3>Race: {npc['race']}</h3>
            <h3>Class: {npc['class']}</h3>
            <h3>Alignment: {npc['alignment']}</h3>
            <h3>Background: {npc['background']}</h3>
            <h3>Gender: {npc['gender']}</h3>

            <h3>Ability Scores:</h3>
            <div class="ability-scores">
                <div>Strength: {npc['ability_scores']['Strength']}</div>
                <div>Dexterity: {npc['ability_scores']['Dexterity']}</div>
                <div>Constitution: {npc['ability_scores']['Constitution']}</div>
                <div>Intelligence: {npc['ability_scores']['Intelligence']}</div>
                <div>Wisdom: {npc['ability_scores']['Wisdom']}</div>
                <div>Charisma: {npc['ability_scores']['Charisma']}</div>
            </div>

            <h3>Saving Throws:</h3>
            <div class="saves-throws">
                <div>Strength: {npc['saves']['Strength']}</div>
                <div>Dexterity: {npc['saves']['Dexterity']}</div>
                <div>Constitution: {npc['saves']['Constitution']}</div>
                <div>Intelligence: {npc['saves']['Intelligence']}</div>
                <div>Wisdom: {npc['saves']['Wisdom']}</div>
                <div>Charisma: {npc['saves']['Charisma']}</div>
            </div>

            <h3>Skills:</h3>
            <div class="skills">
                """
        for skill, bonus in npc['skills'].items():
            html_content += f"<div>{skill}: {bonus}</div>"
        html_content += """
            </div>

            <h3>Hit Points:</h3>
            <p>{}</p>

            <h3>Backstory:</h3>
            <p>{}</p>

            <h3>Traits:</h3>
            <p>{}</p>

            <h3>Appearance:</h3>
            <p>{}</p>

            <h3>Equipment:</h3>
            <p>{}</p>
        </div>
        """.format(npc['hit_points'], npc['backstory'], npc['traits'], npc['appearance'], npc['equipment'])
    html_content += """
    </div>
</body>
</html>
"""
    return html_content


def main():
    # Interactive Input
    while True:
        try:
            num_npcs_to_generate = int(input("Enter the number of NPCs to generate: "))
            if num_npcs_to_generate <= 0:
                print("Please enter a positive number of NPCs.")
                continue  # Go back to the beginning of the while loop
            break  # Exit the loop if input is valid
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        npc_strength = input(
            "Enter the strength level ('weak', 'average', 'strong', 'very strong', 'godly'): ").lower()
        if npc_strength in ["weak", "average", "strong", "very strong", "godly"]:
            break  # Exit the loop if input is valid
        else:
            print("Invalid strength level. Please choose from 'weak', 'average', 'strong', 'very strong', 'godly'.")

    generated_npcs = generate_npcs(num_npcs_to_generate, npc_strength)

    print(f"Generated {num_npcs_to_generate} NPCs with strength: {npc_strength}")
    for i, npc in enumerate(generated_npcs):
        print(f"\nNPC {i + 1}:")
        # Print with word wrapping
        print(f"  Name: {npc['name']}")
        print(f"  Race: {npc['race']}")
        print(f"  Class: {npc['class']}")
        print(f"  Alignment: {npc['alignment']}")
        print(f"  Background: {npc['background']}")
        print(f"  Gender: {npc['gender']}")
        print("  Ability Scores:")
        for stat, score in npc['ability_scores'].items():
            print(f"    {stat}: {score}")
        print("  Saving Throws:")
        for stat, save in npc['saves'].items():
            print(f"    {stat}: {save}")
        print("  Skills:")
        for skill, bonus in npc['skills'].items():
            print(f"    {skill}: {bonus}")
        print(f"  Hit Points: {npc['hit_points']}")
        print(f"  Backstory: {npc['backstory']}")
        print(f"  Traits: {npc['traits']}")
        print(f"  Appearance: {npc['appearance']}")
        print(f"  Equipment: {npc['equipment']}")

    write_json_file("generated_npcs.json", generated_npcs, append=True) #changed to append

    print("\nNPCs generated and saved to generated_npcs.json")

    # Generate and save HTML file
    html_content = generate_npc_html(generated_npcs)
    with open("generated_npcs.html", "w") as f:
        f.write(html_content)
    print("\nNPCs generated and saved to generated_npcs.html")


if __name__ == "__main__":
    main()

