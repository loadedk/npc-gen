# Interactive NPC Generator

## Overview

This project is a Python-based interactive NPC generator that leverages a language model (LM Studio with Qwen2.5) to create detailedNon-Player Characters (NPCs) for tabletop role-playing games, such as Dungeons & Dragons.  It allows you to specify the number of NPCs to generate and their strength level, and then generates a variety of attributes for each NPC, including:

* Name
* Race
* Class
* Alignment
* Background
* Ability Scores
* Saving Throws
* Skills
* Hit Points
* Backstory
* Personality Traits
* Physical Appearance
* Equipment

The generated NPCs are saved to a `generated_npcs.json` file.

## Dependencies

* Python 3.x
* requests: For making API requests to LM Studio.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/loadedk/npc-gen
    cd npc-gen
    ```
    
2.  **Install the Python dependency:**
    ```bash
    pip install requests
    ```

## LM Studio Installation and Setup

1.  **Download LM Studio:**
    * Go to the LM Studio website (<https://lmstudio.ai/>) and download the appropriate version for your operating system.

2.  **Install LM Studio:**
    * Run the downloaded installer and follow the on-screen instructions.

3.  **Download the Qwen2.5 model:**
    * Open LM Studio.
    * Use the model download functionality within LM Studio to download the `qwen2.5-7b-instruct_character_roleplay_dataset_20000` model.  Ensure this model is downloaded and available in LM Studio.

4.  **Start the LM Studio server:**
    * In LM Studio, start the server.  Note the port number that LM Studio is using (the default is 1234).  You'll need this port number in the next step.

## Running the Project

1.  **Run the `interactive_npc_generator.py` script:**
    ```bash
    python npc-gen.py
    ```

2.  **Follow the prompts:**
    * The script will prompt you to enter the number of NPCs to generate and their strength level.
    * Enter the requested information.

3.  **View the generated NPCs:**
    * The generated NPCs will be printed to the console.
    * The NPCs will also be saved to the `generated_npcs.json` file.  This file will be appended to each time you run the script, so previous generations will be preserved.

## To Do

* **Configuration:**
    * Move hardcoded lists (races, classes, etc.) to a configuration file (e.g., JSON or YAML) for easier customization and expansion.
* **Data Sources:**
    * Implement options to pull NPC names and other data from external databases (e.g., SQLite, PostgreSQL) or APIs.  This would allow for more diverse and culturally appropriate names.
* **Expanded Character Options:**
    * Add support for more complex character generation options, such as:
        * Subraces
        * Feats
        * Skills
        * Equipment Packages
* **User Interface:**
    * Develop a simple command-line interface (CLI) or graphical user interface (GUI) to make the tool more user-friendly.
* **Output Formatting:**
    * Provide options to format the output in different ways (e.g., Markdown, HTML) for easier integration with other tools.
* **Ollama/LM Studio Flexibility:**
    * Add support for specifying different language models or adjusting generation parameters.
* **Error Handling:**
    * Implement more robust error handling, including retries and fallbacks for API requests to LM Studio.

