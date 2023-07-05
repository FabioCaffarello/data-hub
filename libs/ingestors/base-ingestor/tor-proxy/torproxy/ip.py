import time
import requests
import subprocess

def _kill_tor():
    command = ['docker', 'exec', 'torproxy', 'kill', '-HUP', '1']
    subprocess.run(command)
    time.sleep(5)

def get_current_ip():
    _kill_tor()
    command = ['curl', '--socks5', 'http://localhost:9050', '-L', 'http://ifconfig.me']
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()


if __name__ == "__main__":
    # IP address before IP rotation
    url = "https://ident.me"
    print("Your Public IP:", requests.get(url).text)
    ip = get_current_ip()
    print(f"Current IP: {ip}")
