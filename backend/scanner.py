import subprocess

def run_scan(target: str) -> str:
    try:
        result = subprocess.check_output(
            ["nmap", "-sV", target],
            stderr=subprocess.STDOUT,
            text=True,
            timeout=60
        )
        return result
    except Exception as e:
        return str(e)