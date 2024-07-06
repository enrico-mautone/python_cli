import os
import subprocess
import sys
import click
import pkgutil
from rich.console import Console

console = Console()

def get_python_executable():
    """Return the path to the Python executable."""
    if getattr(sys, 'frozen', False):
        # If the application is frozen (i.e., running as a PyInstaller bundle), look for the system Python
        for path in os.environ['PATH'].split(os.pathsep):
            python_executable = os.path.join(path, 'python.exe')
            if os.path.isfile(python_executable):
                return python_executable
        console.print("[bold red]Error:[/bold red] No Python executable found in PATH")
        sys.exit(1)
    else:
        return sys.executable

def create_venv(venv_dir, prompt=None):
    console.print(f"Creating virtual environment in [bold green]{venv_dir}[/bold green]...")

    python_executable = get_python_executable()
    command = [python_executable, "-m", "venv", venv_dir]
    if prompt:
        command.extend(["--prompt", prompt])

    subprocess.run(command, check=True)

    console.print(f"Virtual environment created in [bold green]{venv_dir}[/bold green]")

    activate_script = os.path.join(venv_dir, 'Scripts', 'activate') if os.name == 'nt' else os.path.join(venv_dir, 'bin', 'activate')
    console.print(f"To activate the virtual environment, run:\n[bold cyan]{'source ' if os.name != 'nt' else ''}{activate_script}[/bold cyan]")

def create_project(project_name):
    if os.path.exists(project_name):
        console.print(f"[bold red]La cartella {project_name} già esiste[/bold red]")
        return
    os.makedirs(project_name)
    console.print(f"[bold green]Cartella {project_name} creata[/bold green]")
    
    # Create the virtual environment
    venv_dir = os.path.join(project_name, ".venv")
    create_venv(venv_dir, prompt=project_name)

    # Create an empty requirements.txt file
    requirements_path = os.path.join(project_name, "requirements.txt")
    open(requirements_path, 'w').close()
    console.print(f"[bold green]requirements.txt creato in {requirements_path}[/bold green]")

def get_standard_libs():
    std_libs = {name for _, name, _ in pkgutil.iter_modules()}
    std_libs.update(sys.builtin_module_names)
    return std_libs

def generate_requirements(py_file=None):
    standard_libs = get_standard_libs()
    if py_file and os.path.exists(py_file):
        requirements = set()
        with open(py_file, 'r') as file:
            for line in file:
                if line.strip().startswith("import "):
                    parts = line.strip().split()
                    if len(parts) > 1:
                        module = parts[1].split('.')[0]
                        if module not in standard_libs:
                            requirements.add(module)
                elif line.strip().startswith("from "):
                    parts = line.strip().split()
                    if len(parts) > 1:
                        module = parts[1].split('.')[0]
                        if module not in standard_libs:
                            requirements.add(module)
        with open("requirements.txt", 'w') as req_file:
            for req in sorted(requirements):
                req_file.write(f"{req}\n")
        console.print("[bold green]requirements.txt creato con i requisiti trovati.[/bold green]")
    else:
        open("requirements.txt", 'w').close()
        console.print("[bold yellow]requirements.txt vuoto creato.[/bold yellow]")

def install_requirements():
    if not os.path.exists("requirements.txt"):
        console.print("[bold red]Error:[/bold red] requirements.txt non trovato")
        return
    console.print("Installing dependencies from requirements.txt...")
    subprocess.run([get_python_executable(), "-m", "pip", "install", "-r", "requirements.txt"], check=True)

@click.group()
def cli():
    pass

@cli.command()
@click.option('-n', '--name', default='.venv', help='The directory for the virtual environment.')
@click.option('-p', '--prompt', help='The prompt name for the virtual environment.')
@click.option('-s', '--start', is_flag=True, help='Provide instructions to activate the virtual environment.')
def venv(name, prompt, start):
    """Create a virtual environment"""
    create_venv(name, prompt)

@cli.command()
@click.argument('project_name')
def project(project_name):
    """Create a new project directory with a virtual environment and requirements.txt"""
    create_project(project_name)

@cli.command()
@click.option('--file', 'py_file', help='Path to the Python file to analyze for requirements.')
def req(py_file):
    """Generate a requirements.txt file"""
    generate_requirements(py_file)

@cli.command()
def install():
    """Install dependencies from requirements.txt"""
    install_requirements()

@cli.command()
def help():
    """Display help message"""
    help_text = """
    Available commands:
    venv -n <dir> [-p <name>] [--start] - Create a virtual environment in the specified directory with the specified prompt name. Use --start to provide activation instructions.
    project <project_name> - Create a new project directory with a virtual environment and an empty requirements.txt file.
    req [--file <path_to_py_file>] - Generate a requirements.txt file based on the specified Python file. If no file is specified, creates an empty requirements.txt.
    install - Install dependencies from requirements.txt.
    help - Display this help message.
    To deactivate the virtual environment, use the command 'deactivate'.
    """
    console.print(help_text, style="bold cyan")

if __name__ == '__main__':
    cli()
