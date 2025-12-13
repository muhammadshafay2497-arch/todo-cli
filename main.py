# main.py

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from handling import load_tasks, save_tasks
from task import add_task, list_tasks, toggle_task_status, update_task, delete_task

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
    console.print(
        Panel(
            "[bold cyan]1.[/bold cyan] Add Task\n"
            "[bold cyan]2.[/bold cyan] List Tasks\n"
            "[bold cyan]3.[/bold cyan] Toggle_task_status\n"
            "[bold cyan]4.[/bold cyan] Update Task\n"
            "[bold cyan]5.[/bold cyan] Delete Task\n"
            "[bold red]6.[/bold red] Exit",
            title="[bold green]==== TODO APP ====[/bold green]",
            expand=False,
            border_style="blue"
        )
    )

def main():
    """
    The main function that runs the application loop.
    """
    # Load tasks from the file at the start of the application
    tasks = load_tasks(FILE_PATH)

    while True:
        tasks_modified = False # Flag to track if tasks were modified in the current iteration
        print_menu()
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6"], default="2")

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
            update_task(tasks)
            tasks_modified = True
            list_tasks(tasks)
            console.print("[bold yellow]Press Enter to return to menu...[/bold yellow]")
            input()
        elif choice == '5':
            delete_task(tasks)
            tasks_modified = True
            list_tasks(tasks)
            console.print("[bold yellow]Press Enter to return to menu...[/bold yellow]")
            input()
        elif choice == '6':
            console.print("[bold blue]Goodbye! 👋[/bold blue]")
            break
        
        # Save tasks if any modifications were made
        if tasks_modified:
            save_tasks(tasks, FILE_PATH)
            
if __name__ == "__main__":
    main()
