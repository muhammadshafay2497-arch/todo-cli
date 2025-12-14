# main.py

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from file_handling import load_tasks, save_tasks
from task import add_task, list_tasks, toggle_task_status, update_task, delete_task, find_task, search_tasks, filter_tasks

"""
This is the main entry point for the To-Do CLI application.
It orchestrates the application flow, handling the main menu loop
and calling functions from the 'task' and 'handling' modules.
"""

# Define the file path for the tasks JSON file
FILE_PATH = "tasks.json"

# Initialize Rich Console
console = Console()

def print_menu():

    """Prints the main menu of the application."""

    console.print(Panel(

        "[bold green]==== TODO APP ====[/bold green]",

        expand=False,

        border_style="blue"

    ))

    console.print(

        Panel(

            "[bold green]1.[/bold green] Add Task.\n"
            "[bold green]2.[/bold green] List Tasks.\n"
            "[bold green]3.[/bold green] Toggle_task_status.\n"
            "[bold green]4.[/bold green] Find Task by ID.\n"
            "[bold green]5.[/bold green] Search Tasks.\n"
            "[bold green]6.[/bold green] Filter Tasks.\n"
            "[bold green]7.[/bold green] Update Task.\n"
            "[bold green]8.[/bold green] Delete Task.\n"
            "[bold red]9.[/bold red] Exit.",

            title="[bold green]Menu[/bold green]",

            border_style="red",

            title_align="center"

        )

    )

def find_task_by_id(tasks):
    """
    Prompts the user for a task ID and displays the task details.
    """
    console.print("[bold cyan]Find Task by ID[/bold cyan]")
    task_id = Prompt.ask("Enter the task ID to find")
    try:
        task_id = int(task_id)
        task = find_task(tasks, task_id)
        if task:
            console.print(Panel(
                f"[bold]Title:[/bold] {task['title']}\n"
                f"[bold]Description:[/bold] {task['description']}\n"
                f"[bold]Priority:[/bold] {task['priority']}\n"
                f"[bold]Status:[/bold] {task['status']}",
                title=f"[bold]Task Details for ID: {task_id}[/bold]",
                expand=False,
                border_style="cyan"
            ))
        else:
            console.print(f"[bold red]Task with ID '{task_id}' not found.[/bold red]")
    except ValueError:
        console.print("[bold red]Invalid input. Please enter a valid integer ID.[/bold red]")
    
    console.print("[bold yellow]Press Enter to return to menu...[/bold yellow]")
    input()

def search_tasks_by_term(tasks):
    """
    Prompts the user for a search term and displays matching tasks.
    """
    console.print("[bold cyan]Search Tasks[/bold cyan]")
    search_term = Prompt.ask("Enter the search term")
    found_tasks = search_tasks(tasks, search_term)
    if found_tasks:
        list_tasks(found_tasks)
    else:
        console.print(f"[bold red]No tasks found with the search term '{search_term}'.[/bold red]")
    
    console.print("[bold yellow]Press Enter to return to menu...[/bold yellow]")
    input()

def filter_tasks_by_criterion(tasks):
    """
    Prompts the user for a filter criterion and displays matching tasks.
    """
    console.print("[bold cyan]Filter Tasks[/bold cyan]")
    filter_criterion = Prompt.ask("Enter the filter criterion (e.g., pending, completed, high, medium, low)")
    found_tasks = filter_tasks(tasks, filter_criterion)
    if found_tasks:
        list_tasks(found_tasks)
    else:
        console.print(f"[bold red]No tasks found with the filter criterion '{filter_criterion}'.[/bold red]")
    
    console.print("[bold yellow]Press Enter to return to menu...[/bold yellow]")
    input()

def main():
    """
    The main function that runs the application loop.
    """
    # Load tasks from the file at the start of the application
    tasks = load_tasks(FILE_PATH)

    while True:
        tasks_modified = False # Flag to track if tasks were modified in the current iteration
        print_menu()
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"], default="2")

        if choice == '1':
            add_task(tasks)
            tasks_modified = True
            list_tasks(tasks)
            console.print("[bold yellow]Press Enter to return to menu...[/bold yellow]")
            input()
        elif choice == '2':
            list_tasks(tasks)
            console.print("[bold yellow]Press Enter to return to menu...[/bold yellow]")
            input()
        elif choice == '3':
            toggle_task_status(tasks)
            tasks_modified = True
            list_tasks(tasks)
            console.print("[bold yellow]Press Enter to return to menu...[/bold yellow]")
            input()
        elif choice == '4':
            find_task_by_id(tasks)
        elif choice == '5':
            search_tasks_by_term(tasks)
        elif choice == '6':
            filter_tasks_by_criterion(tasks)
        elif choice == '7':
            update_task(tasks)
            tasks_modified = True
            list_tasks(tasks)
            console.print("[bold yellow]Press Enter to return to menu...[/bold yellow]")
            input()
        elif choice == '8':
            delete_task(tasks)
            tasks_modified = True
            list_tasks(tasks)
            console.print("[bold yellow]Press Enter to return to menu...[/bold yellow]")
            input()
        elif choice == '9':
            console.print("[bold blue]Goodbye! 👋[/bold blue]")
            break
        
        # Save tasks if any modifications were made
        if tasks_modified:
            save_tasks(tasks, FILE_PATH)
            
if __name__ == "__main__":
    main()