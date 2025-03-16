#!/usr/bin/env python
import sys
import warnings
import json
import os
from datetime import datetime
from pathlib import Path

from curriculumbuildercrew.crew import Curriculumbuilder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def ensure_input_dir():
    """
    Ensure the input directory exists.
    """
    input_dir = Path("input")
    input_dir.mkdir(exist_ok=True)
    return input_dir

def save_json_input(json_data, filename="skill_input.json"):
    """
    Save input JSON data to a file in the input directory.
    """
    input_dir = ensure_input_dir()
    input_file = input_dir / filename
    
    with open(input_file, "w") as f:
        json.dump(json_data, f, indent=2)
    
    return input_file

def get_skill_from_json(json_data):
    """
    Extract the primary skill to focus on from the JSON data.
    """
    # Check for high priority missing technical skills first
    missing_technical = json_data.get("skill_gaps", {}).get("missing", {}).get("Technical", [])
    if missing_technical:
        # Get the first high priority skill
        for skill_item in missing_technical:
            if skill_item.get("priority") == "High":
                return skill_item.get("skill")
    
    # If no high priority missing technical skills, check other categories
    return "Web3 Development"  # Default fallback if no clear primary skill is found

def run():
    """
    Run the crew with the input JSON data.
    """
    # Use the JSON data from paste.txt or another source
    json_file_path = Path("paste.txt")
    if json_file_path.exists():
        try:
            with open(json_file_path, "r") as f:
                content = f.read()
                # Try to parse as JSON first
                try:
                    json_data = json.loads(content)
                except json.JSONDecodeError:
                    # If not JSON, check if it's the output curriculum
                    if "Curriculum" in content and "Level" in content:
                        print("Found curriculum output in paste.txt. This should be used as output, not input.")
                        # Use default sample data
                        json_data = {
                            "skill_gaps": {
                                "missing": {
                                    "Technical": [
                                        {
                                            "skill": "Web3 Development",
                                            "priority": "High",
                                            "justification": "Critical for developing decentralized applications",
                                            "learning_recommendations": "Enroll in online courses"
                                        }
                                    ]
                                }
                            }
                        }
                    else:
                        print("Could not parse paste.txt as JSON. Using default sample data.")
                        json_data = {
                            "skill_gaps": {
                                "missing": {
                                    "Technical": [
                                        {
                                            "skill": "Web3 Development",
                                            "priority": "High",
                                            "justification": "Critical for developing decentralized applications",
                                            "learning_recommendations": "Enroll in online courses"
                                        }
                                    ]
                                }
                            }
                        }
        except Exception as e:
            print(f"Error reading paste.txt: {e}")
            json_data = {
                "skill_gaps": {
                    "missing": {
                        "Technical": [
                            {
                                "skill": "Web3 Development",
                                "priority": "High",
                                "justification": "Critical for developing decentralized applications",
                                "learning_recommendations": "Enroll in online courses"
                            }
                        ]
                    }
                }
            }
    else:
        # Sample data if paste.txt doesn't exist
        json_data = {
            "skill_gaps": {
                "missing": {
                    "Technical": [
                        {
                            "skill": "Web3 Development",
                            "priority": "High",
                            "justification": "Critical for developing decentralized applications",
                            "learning_recommendations": "Enroll in online courses"
                        }
                    ]
                }
            }
        }
    
    # Save the input data to a file
    input_file = save_json_input(json_data)
    
    # Extract the primary skill to focus on
    primary_skill = get_skill_from_json(json_data)
    
    # Set up the inputs for the crew
    inputs = {
        'skill': primary_skill,
        'skill_data': json_data,
        'current_year': str(datetime.now().year),
        'input_file_path': str(input_file),
        'output_format': 'json'  # Specify JSON output format
    }
    
    try:
        Curriculumbuilder().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    # Load JSON data for training
    json_file_path = Path("paste.txt")
    if json_file_path.exists():
        try:
            with open(json_file_path, "r") as f:
                json_data = json.loads(f.read())
        except:
            json_data = {"skill_gaps": {"missing": {"Technical": [{"skill": "Web3 Development"}]}}}
    else:
        json_data = {"skill_gaps": {"missing": {"Technical": [{"skill": "Web3 Development"}]}}}
    
    primary_skill = get_skill_from_json(json_data)
    
    inputs = {
        "skill": primary_skill,
        "skill_data": json_data,
        "output_format": "json"
    }
    
    try:
        Curriculumbuilder().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Curriculumbuilder().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    # Load JSON data for testing
    json_file_path = Path("paste.txt")
    if json_file_path.exists():
        try:
            with open(json_file_path, "r") as f:
                json_data = json.loads(f.read())
        except:
            json_data = {"skill_gaps": {"missing": {"Technical": [{"skill": "Web3 Development"}]}}}
    else:
        json_data = {"skill_gaps": {"missing": {"Technical": [{"skill": "Web3 Development"}]}}}
    
    primary_skill = get_skill_from_json(json_data)
    
    inputs = {
        "skill": primary_skill,
        "skill_data": json_data,
        "output_format": "json"
    }
    
    try:
        Curriculumbuilder().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()