# Architech
# Start.py

import inspect
from colorama import Fore, Style

def name(model_name):
    result = (
        f"{Fore.RED}Loading Environment...\n"
        f"{Fore.GREEN}Successfully loaded environment.\n"
        f"{Style.RESET_ALL}The model's name has been set to \"{model_name}\"."
    )
    return result

def hello(model_name, choice):
    types = {
        "a1": "Hello! How may I help you?",
        "a2": "Hello. How may I assist you today?",
        "a3": "Yo. What's up.",
        "a4": "Greetings! How can I be of service?",
        "a5": "Hi! What brings you here?",
        "a6": "Salutations! Ready for a chat?",
        "a7": "Ahoy there! What brings you here?",
        "a8": "Hello! Anything exciting happening?",
        "a9": "Hey! What's the plan for today?",
        "a10": "Yo! What's the latest news?",
    }

    if choice in types:
        return (
            f"\n{model_name.capitalize()} says: {types[choice]}"
        )
    else:
        caller_frame = inspect.currentframe().f_back
        error_message = (
            f"ERROR: Invalid choice in the function {hello.__name__} at line {caller_frame.f_lineno}. "
            f"Please refer to the documentation for further support."
        )
        return error_message

def hello_output(user_name, sentence):
    return (
        f"{user_name.capitalize()} says: {sentence}\n\n"
        f"{Fore.BLUE}Process 'START' complete.\n"
    )
