# handling.py

import json
import os

"""
This module handles the data persistence for the To-Do application.
It is responsible for reading from and writing to the JSON file where tasks are stored.
"""

def load_tasks(file_path):
    """
    Loads tasks from a JSON file.

    If the file does not exist, it creates an empty file and returns an empty list.

    Args:
        file_path (str): The path to the tasks JSON file.

    Returns:
        list: A list of task dictionaries.
    """
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)
        return []
    
    try:
        with open(file_path, 'r') as f:
            tasks = json.load(f)
            return tasks
    except json.JSONDecodeError:
        # If the file is corrupted or empty, handle it gracefully
        return []

def save_tasks(tasks, file_path):
    """
    Saves a list of tasks to a JSON file.

    Args:
        tasks (list): The list of task dictionaries to save.
        file_path (str): The path to the tasks JSON file.
    """
    with open(file_path, 'w') as f:
        json.dump(tasks, f, indent=4)

