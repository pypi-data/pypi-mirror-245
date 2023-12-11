from aiida_worktree.cli.cmd_worktree import worktree
import subprocess
import click
import os
import signal
from pathlib import Path


REACT_PORT = "3000"


def get_package_root():
    """Returns the root directory of the package."""
    current_file = Path(__file__)
    # Root directory of your package
    return current_file.parent


def get_pid_file_path():
    """Get the path to the PID file in the desired directory."""
    home_dir = Path.home()
    aiida_daemon_dir = home_dir / '.aiida' / 'daemon'

    # Create the directory if it does not exist
    aiida_daemon_dir.mkdir(parents=True, exist_ok=True)

    return aiida_daemon_dir / 'web_processes.pid'


def kill_process_on_port(port):
    try:
        # Find processes listening on the port
        result = subprocess.check_output(["lsof", "-i", f":{port}", "-sTCP:LISTEN", "-t"])
        pids = result.decode().strip().split('\n')
        
        for pid in pids:
            click.echo(f"Killing process {pid} on port {port}")
            os.kill(int(pid), signal.SIGKILL)
    except subprocess.CalledProcessError:
        click.echo(f"No process found running on port {port}")


@worktree.group("web")
def web():
    """Commands to manage the web application (both backend and frontend)."""



@web.command()
def start():
    """Start the web application."""
    click.echo('Starting the web application...')
    pid_file_path = get_pid_file_path()

    with open(pid_file_path, 'w') as pid_file:
        # Starting FastAPI backend
        backend_process = subprocess.Popen(["uvicorn", "aiida_worktree.web.backend.app.api:app", "--reload", "--port", "8000"])
        pid_file.write(f'backend:{backend_process.pid}\n')

        # Starting React frontend
        package_root = get_package_root()
        frontend_path = package_root /".." / 'web' / 'frontend'
        frontend_process = subprocess.Popen(["npm", "start", "--prefix", str(frontend_path)])
        pid_file.write(f'frontend:{frontend_process.pid}\n')

@web.command()
def stop():
    """Stop the web application."""
    pid_file_path = get_pid_file_path()

    if not pid_file_path.exists():
        click.echo('No running web application found.')
        return

    with open(pid_file_path, 'r') as pid_file:
        for line in pid_file:
            proc_name, pid = line.strip().split(':')
            try:
                os.kill(int(pid), signal.SIGTERM)
                click.echo(f'Stopped {proc_name} (PID: {pid})')
            except ProcessLookupError:
                click.echo(f'{proc_name} (PID: {pid}) not found')
    # kill the processes on the ports
    # TODO after this command, the terminal does not response
    # kill_process_on_port(REACT_PORT)  # Assuming React runs on port REACT_PORT

    os.remove(pid_file_path)
