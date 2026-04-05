import subprocess

def run_nmap(target):
    try:
        return subprocess.check_output(
            ["nmap", "-sV", target],
            text=True
        )
    except Exception as e:
        return str(e)