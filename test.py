import subprocess
import re
import time

def launch_cloudflared_tunnel(ip, port):
    # Command to launch the cloudflared tunnel
    command = [
        "cloudflared", "tunnel",
        "--url", f"http://{ip}:{port}"
    ]

    # Run the command and capture the output
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Read the output line by line
    url_printed = False
    while True:
        output = process.stderr.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            # Use regex to extract the tunnel URL (ignoring developer links)
            match = re.search(r'https://[a-zA-Z0-9.-]+\.trycloudflare\.com', output)
            if match and not url_printed:
                print("Tunnel URL:", match.group(0))
                url_printed = True
        
        # Keep the script running to keep the tunnel alive
        time.sleep(1)

if __name__ == "__main__":
    ip = "192.168.8.183"
    port = "8000"
    launch_cloudflared_tunnel(ip, port)