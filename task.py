# task.py

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.markup import escape

"""
This module contains the core logic for task manipulation.
It handles adding, listing, updating, completing, and deleting tasks.
All user-facing interactions and presentations are managed here using the 'rich' library.
"""

# Initialize Rich Console for beautiful output
console = Console()

def add_task(tasks):
    """
    Prompts the user for task details and adds a new task to the list.
    """
    console.print("[bold cyan]Add a New Task[/bold cyan]")
    title = Prompt.ask("Enter Task Title")
    description = Prompt.ask("Enter Task Description (optional)")
    while True:
        priority_input = Prompt.ask("Enter Priority (Low/Medium/High)", default="Medium").lower()
        if priority_input in ["low", "medium", "high"]:
            priority = priority_input
            break
        else:
            console.print("[bold red]Invalid priority. Please choose from Low, Medium, or High.[/bold red]")

    # Find the maximum existing ID and add 1, or start from 1 if no tasks exist
    new_id = max([task.get("id", 0) for task in tasks] + [0]) + 1

    new_task = {
        "id": new_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "pending"  # Changed from 'completed'
    }
    tasks.append(new_task)
    console.print(f"\n[bold green]✅ Task '{escape(title)}' added successfully![/bold green]")

def list_tasks(tasks):
    """
    Displays all tasks in a formatted table.
    """
    if not tasks:
        console.print("[bold yellow]No tasks found. Add one to get started![/bold yellow]")
        return

    table = Table(title="[bold blue]Your To-Do List[/bold blue]", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Status", width=10)
    table.add_column("Title", min_width=20)
    table.add_column("Description", min_width=20, no_wrap=False)
    table.add_column("Priority", width=10)

    priority_styles = {
        "high": "bold red",
        "medium": "bold yellow",
        "low": "bold green"
    }

    for task in sorted(tasks, key=lambda t: t.get("id", 0)):
        task_id_str = escape(str(task.get("id", "N/A")))
        
        # Determine status and row style
        status = task.get("status", "pending")
        row_style = "dim" if status == "completed" else ""
        
        # Determine priority style
        priority = task.get("priority", "medium").lower()
        priority_style = priority_styles.get(priority, "white")

        try:
            table.add_row(
                task_id_str,
                status.capitalize(),
                escape(task["title"]),
                escape(task.get("description", "")),
                f"[{priority_style}]{escape(priority.capitalize())}[/]",
                style=row_style
            )
        except Exception as e:
            console.print(f"[bold red]Error rendering task ID {task_id_str}: {e}[/bold red]")
            console.print(f"[bold red]Problematic task data: {task}[/bold red]")
    
    console.print(table)

def get_task_id(prompt_text, tasks):
    """Helper function to get a valid task ID from the user."""
    if not tasks:
        console.print("[bold yellow]No tasks available to select.[/bold yellow]")
        return None

    valid_ids = [task["id"] for task in tasks]
    while True:
        try:
            task_id_str = Prompt.ask(prompt_text)
            task_id = int(task_id_str)
            if task_id in valid_ids:
                return task_id
            else:
                raise ValueError
        except (ValueError, TypeError):
            console.print(f"[bold red]Error: Invalid ID. Please choose from {', '.join(map(str, sorted(valid_ids)))}.[/bold red]")

def toggle_task_status(tasks):
    """
    Toggles a task's status between 'pending' and 'completed'.
    """
    if not tasks:
        console.print("[bold yellow]No tasks to mark.[/bold yellow]")
        return
        
    list_tasks(tasks)
    console.print("\n[bold cyan]Toggle Task Status[/bold cyan]")
    task_id = get_task_id("Enter the ID of the task to toggle", tasks)
    
    # Find the task with the matching ID
    task = next((t for t in tasks if t.get("id") == task_id), None)
    if not task:
        console.print("[bold red]Task not found.[/bold red]")
        return
        
    # Toggle status between 'pending' and 'completed'
    if task["status"] == "completed":
        task["status"] = "pending"
        status_text = "pending"
    else:
        task["status"] = "completed"
        status_text = "completed"
    
    console.print(f"\n[bold green]✅ Task '{escape(task['title'])}' marked as {status_text}![/bold green]")

def update_task(tasks):
    """
    Updates the details of an existing task.
    """
    if not tasks:
        console.print("[bold yellow]No tasks to update.[/bold yellow]")
        return

    list_tasks(tasks)
    console.print("\n[bold cyan]Update a Task[/bold cyan]")
    task_id = get_task_id("Enter the ID of the task to update", tasks)
    
    # Find the task with the matching ID
    task = next((t for t in tasks if t.get("id") == task_id), None)
    if not task:
        console.print("[bold red]Task not found.[/bold red]")
        return

    console.print(f"Updating task: [bold]{escape(task['title'])}[/bold]. Leave fields blank to keep current values.")

    new_title = Prompt.ask(f"New title", default=task["title"])
    new_description = Prompt.ask(f"New description", default=task.get("description", ""))
    while True:
        priority_input = Prompt.ask(
            "New priority (Low/Medium/High)",
            default=task.get("priority", "medium").capitalize()
        ).lower()
        if priority_input in ["low", "medium", "high"]:
            new_priority = priority_input
            break
        else:
            console.print("[bold red]Invalid priority. Please choose from Low, Medium, or High.[/bold red]")

    task["title"] = new_title
    task["description"] = new_description
    task["priority"] = new_priority
    
    console.print(f"\n[bold green]✅ Task '{escape(new_title)}' updated successfully![/bold green]")

def delete_task(tasks):
    """
    Deletes a task from the list and re-numbers the remaining tasks.
    """
    if not tasks:
        console.print("[bold yellow]No tasks to delete.[/bold yellow]")
        return

    list_tasks(tasks)
    console.print("\n[bold cyan]Delete a Task[/bold cyan]")
    task_id = get_task_id("Enter the ID of the task to delete", tasks)
    
    if task_id is None:
        return

    task_to_delete = next((task for task in tasks if task["id"] == task_id), None)
    if not task_to_delete:
        console.print("[bold red]Task not found.[/bold red]")
        return

    task_title = task_to_delete['title']
    
    if Confirm.ask(f"Are you sure you want to delete the task '[bold red]{escape(task_title)}[/bold red]'?"):
        # Remove the task
        tasks.remove(task_to_delete)
        
        # Re-number the remaining tasks
        for i, task in enumerate(tasks):
            task["id"] = i + 1
            
        console.print(f"\n[bold green]✅ Task '{escape(task_title)}' deleted and tasks re-numbered successfully![/bold green]")
    else:
        console.print("\n[bold yellow]Task deletion cancelled.[/bold yellow]")

