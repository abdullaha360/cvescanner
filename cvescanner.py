from urllib.parse import urlparse, parse_qs
import subprocess
import sys
import argparse

def execscan(cmd):
    try:
        print(f"Executing command: {cmd}")
        p = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        output = p.decode("utf-8")
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(e.output.decode("utf-8"))

def check_and_install(tool, tap=None):
    try:
        subprocess.check_output(f"brew list --formula | grep -w {tool}", shell=True)
        print(f"{tool} is already installed.")
    except subprocess.CalledProcessError:
        if tap:
            print(f"Tapping {tap}...")
            try:
                subprocess.check_call(f"brew tap {tap}", shell=True)
                print(f"{tap} tapped successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to tap {tap}: {e}")
                sys.exit(1)
        
        print(f"{tool} is not installed. Installing {tool}...")
        try:
            subprocess.check_call(f"brew install {tool}", shell=True)
            print(f"{tool} has been installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {tool}: {e}")
            sys.exit(1)

# Check and install trivy, grype, and fzf if necessary
check_and_install("trivy")
check_and_install("grype", "anchore/grype")

parser = argparse.ArgumentParser(description="Sample argument parser")
parser.add_argument("command", nargs='?', choices=["t", "g"], help="specify 't' for trivy or 'g' for grype")
args = parser.parse_args()

url = input("What is your VAT link? ")
package = input("What package or CVE? ")

# Parse the URL
parsed_url = urlparse(url)
query_params = parse_qs(parsed_url.query)

# Extract image path and tag
image_path = query_params.get('imageName', [''])[0]
tag = query_params.get('tag', [''])[0]

# Construct the final image name
finalName = f"registry1.dso.mil/ironbank/{image_path}:{tag}"
print(f"Final image name: {finalName}")

# Build the command strings with grep for the package or CVE
t_cmd = f"trivy image {finalName} --scanners vuln | grep -i '{package}'"
g_cmd = f"grype {finalName} | grep -i '{package}'"

# Execute the selected command or both if no command is provided
if args.command == "t":
    execscan(t_cmd)
elif args.command == "g":
    execscan(g_cmd)
else:
    execscan(t_cmd)
    execscan(g_cmd)
