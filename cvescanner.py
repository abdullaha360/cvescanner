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

parser = argparse.ArgumentParser(description="sample argument parser")
parser.add_argument("command", choices=["t", "g"], help="specify t for trivy or g for grype")
args = parser.parse_args()

url = input("what is your VAT link? ")
package = input("What package or CVE? ")

# Parse the URL
parsed_url = urlparse(url)
query_params = parse_qs(parsed_url.query)

# Extract image path and tag
image_path = query_params.get('imageName', [''])[0]
tag = query_params.get('tag', [''])[0]

#final image name after parsing
finalName = f"registry1.dso.mil/ironbank/{image_path}:{tag}"


t_cmd = f"trivy image {finalName} | grep -i '{package}'"
g_cmd = f"grype {finalName} | grep -i '{package}'"

if args.command == "t":
    execscan(t_cmd)
elif args.command == "g":
    execscan(g_cmd)

