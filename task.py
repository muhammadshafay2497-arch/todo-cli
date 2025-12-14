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

def find_task(tasks, task_id):
    """Finds a task by its ID.

    Args:
        tasks (list): The list of tasks.
        task_id (int): The ID of the task to find.

    Returns:
        dict: The task with the matching ID, or None if not found.
    """
    for task in tasks:
        if task.get("id") == task_id:
            return task
    return None

def search_tasks(tasks, search_term):
    """
    Searches for tasks by a search term in the title or description.

    Args:
        tasks (list): The list of tasks.
        search_term (str): The term to search for.

    Returns:
        list: A list of tasks that match the search term.
    """
    found_tasks = []
    search_term = search_term.lower()
    for task in tasks:
        if search_term in task.get("title", "").lower() or search_term in task.get("description", "").lower():
            found_tasks.append(task)
    return found_tasks

def filter_tasks(tasks, filter_criterion):
    """
    Filters tasks by status or priority.

    Args:
        tasks (list): The list of tasks.
        filter_criterion (str): The criterion to filter by (status or priority).

    Returns:
        list: A list of tasks that match the filter criterion.
    """
    found_tasks = []
    filter_criterion = filter_criterion.lower()
    for task in tasks:
        if task.get("status", "").lower() == filter_criterion or task.get("priority", "").lower() == filter_criterion:
            found_tasks.append(task)
    return found_tasks

def add_task(tasks):
    """
    Prompts the user for task details and adds a new task to the list.
    """
    console.print("[bold cyan]Add a New Task[/bold cyan]")
    title = Prompt.ask("Enter Task Title (or type 'back' to return to the menu)")
    if title.lower() == 'back':
        console.print("[yellow]Cancelled.[/yellow]")
        return
    # If title is empty, set default to "Task"
    if not title:
        title = "Task"

    description = "-"
    while True:
        console.print(f"Current Title: [bold]{escape(title)}[/bold]")
        description_input = Prompt.ask("Enter Task Description (optional, or type 'edit title', 'back')")
        if description_input.lower() == 'back':
            console.print("[yellow]Cancelled.[/yellow]")
            return
        if description_input.lower() == 'edit title':
            title = Prompt.ask("Enter New Task Title", default=title)
            if not title:
                title = "Task"
            continue
        if description_input:
            description = description_input
        break

    while True:
        console.print(f"Current Title: [bold]{escape(title)}[/bold]")
        console.print(f"Current Description: [bold]{escape(description)}[/bold]")
        priority_input = Prompt.ask("Enter Priority (Low/Medium/High, or type 'edit title', 'edit description', 'back')", default="Medium").lower()
        if priority_input.lower() == 'back':
            console.print("[yellow]Cancelled.[/yellow]")
            return
        if priority_input.lower() == 'edit title':
            title = Prompt.ask("Enter New Task Title", default=title)
            if not title:
                title = "Task"
            continue
        if priority_input.lower() == 'edit description':
            description = Prompt.ask("Enter New Task Description", default=description)
            if not description:
                description = "-"
            continue
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

    status_styles = {
        "pending": "bold red",
        "completed": "bold green",
    }
    priority_styles = {
        "high": "bold red",
        "medium": "bold yellow",
        "low": "bold green"
    }

    for task in sorted(tasks, key=lambda t: t.get("id", 0)):
        task_id_str = escape(str(task.get("id", "N/A")))
        
        # Determine status and row style
        status = task.get("status", "pending")
        status_style = status_styles.get(status, "white")
        row_style = "dim" if status == "completed" else ""
        
        # Determine priority style
        priority = task.get("priority", "medium").lower()
        priority_style = priority_styles.get(priority, "white")

        try:
            table.add_row(
                task_id_str,
                f"[{status_style}]{status.capitalize()}[/]",
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
            task_id_str = Prompt.ask(prompt_text + " (or type 'back' to return to the menu)")
            if task_id_str.lower() == 'back':
                console.print("[yellow]Cancelled.[/yellow]")
                return None
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
    if task_id is None:
        return
    
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

    while True: # Outer loop for task ID selection and re-selection
        list_tasks(tasks)
        console.print("\n[bold cyan]Update a Task[/bold cyan]")
        task_id = get_task_id("Enter the ID of the task to update", tasks)
        if task_id is None:
            return # User chose to go back to the main menu

        task = next((t for t in tasks if t.get("id") == task_id), None)
        if not task:
            console.print("[bold red]Task not found. Please enter a valid ID.[/bold red]")
            continue # Ask for ID again

        console.print(f"Updating task: [bold]{escape(task['title'])}[/bold]. [yellow]Leave fields blank to keep current values.[/yellow]")

        new_title = task["title"]
        new_description = task.get("description", "")
        new_priority = task.get("priority", "medium")

        # Flag to indicate if we need to restart the outer loop (edit ID)
        restart_task_selection = False

        while True: # Loop for title
            console.print(f"Current Title: [bold]{escape(new_title)}[/bold]")
            title_input = Prompt.ask(f"New title (or type 'back' to return, 'edit id' to change task)", default=new_title)
            if title_input.lower() == 'back':
                console.print("[yellow]Cancelled.[/yellow]")
                return
            if title_input.lower() == 'edit id':
                restart_task_selection = True
                break # Break from title loop, outer loop will restart
            new_title = title_input
            break # Exit title loop

        if restart_task_selection:
            continue # Restart outer loop for task ID selection

        while True: # Loop for description
            console.print(f"Current Description: [bold]{escape(new_description)}[/bold]")
            description_input = Prompt.ask(f"New description (or type 'edit title', 'edit id', 'back')", default=new_description)
            if description_input.lower() == 'back':
                console.print("[yellow]Cancelled.[/yellow]")
                return
            if description_input.lower() == 'edit title':
                new_title = Prompt.ask("Enter New Task Title", default=new_title)
                if not new_title:
                    new_title = "Task"
                # Do not break here, stay in description loop
                continue
            if description_input.lower() == 'edit id':
                restart_task_selection = True
                break # Break from description loop, outer loop will restart
            new_description = description_input
            break # Exit description loop

        if restart_task_selection:
            continue # Restart outer loop for task ID selection

        while True: # Loop for priority
            console.print(f"Current Priority: [bold]{escape(new_priority.capitalize())}[/bold]")
            priority_input = Prompt.ask("New priority (Low/Medium/High, or type 'edit title', 'edit description', 'edit id', 'back')", default=new_priority.capitalize()).lower()
            if priority_input.lower() == 'back':
                console.print("[yellow]Cancelled.[/yellow]")
                return
            if priority_input.lower() == 'edit title':
                new_title = Prompt.ask("Enter New Task Title", default=new_title)
                if not new_title:
                    new_title = "Task"
                continue
            if priority_input.lower() == 'edit description':
                new_description = Prompt.ask("Enter New Task Description", default=new_description)
                if not new_description:
                    new_description = "-"
                continue
            if priority_input.lower() == 'edit id':
                restart_task_selection = True
                break # Break from priority loop, outer loop will restart
            if priority_input in ["low", "medium", "high"]:
                new_priority = priority_input
                break
            else:
                console.print("[bold red]Invalid priority. Please choose from Low, Medium, or High.[/bold red]")

        if restart_task_selection:
            continue # Restart outer loop for task ID selection
        
        # If we reach here, all fields are processed for the selected task
        break # Exit the outer task ID selection loop

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