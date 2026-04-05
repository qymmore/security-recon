import subprocess

def enumerate_subdomains(domain):
    try:
        result = subprocess.check_output(
            ["subfinder", "-d", domain],
            text=True
        )
        return result.splitlines()
    except Exception as e:
        return [str(e)]