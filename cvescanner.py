from urllib.parse import urlparse, parse_qs
import subprocess
import argparse
import platform

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

    os_type = platform.system()
    if os_type == 'Darwin':
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
    elif os_type == 'Windows':
        try:
            subprocess.check_call(f"where {tool}", shell=True)
            print(f"{tool} is already installed.")
        except subprocess.CalledProcessError:
            if tool == "trivy":
                print("Installing Trivy...")
                try:
                    subprocess.check_call(
                        "Invoke-WebRequest -Uri https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.22.0_Windows-64bit.zip -OutFile trivy.zip; "
                        "Expand-Archive -Path trivy.zip -DestinationPath .; "
                        "Move-Item trivy.exe C:\\Windows\\System32", shell=True
                    )
                    print("Trivy installed successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to install Trivy: {e}")
                    sys.exit(1)
            elif tool == "grype":
                print("Installing Grype...")
                try:
                    subprocess.check_call(
                        "Invoke-WebRequest -Uri https://github.com/anchore/grype/releases/latest/download/grype_0.15.0_windows_amd64.zip -OutFile grype.zip; "
                        "Expand-Archive -Path grype.zip -DestinationPath .; "
                        "Move-Item grype.exe C:\\Windows\\System32", shell=True
                    )
                    print("Grype installed successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to install Grype: {e}")
                    sys.exit(1)
    elif os_type == 'Linux':
        try:
            subprocess.check_output(f"command -v {tool}", shell=True)
            print(f"{tool} is already installed.")
        except subprocess.CalledProcessError:
            if tool == "trivy":
                print("Installing Trivy...")
                try:
                    subprocess.check_call("curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh", shell=True)
                    print("Trivy installed successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to install Trivy: {e}")
                    sys.exit(1)
            elif tool == "grype":
                print("Installing Grype...")
                try:
                    subprocess.check_call("curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin", shell=True)
                    print("Grype installed successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to install Grype: {e}")
                    sys.exit(1)
# Check and install trivy, grype, and fzf if necessary
check_and_install("trivy")
check_and_install("grype", "anchore/grype")

parser = argparse.ArgumentParser(description="Sample argument parser")
parser.add_argument("url", help="Paste VAT link")
args = parser.parse_args()

url = args.url
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
if args.url:
    execscan(t_cmd)
    execscan(g_cmd)
