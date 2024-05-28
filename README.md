# CVE Scanner

This script allows you to scan a Docker image from P1's VAT platform for vulnerabilities using either `trivy` or `grype` and filter the results for a specific package or CVE.

## Prerequisites

Ensure you have `trivy` and `grype` installed on your system.

- [Trivy Installation Guide](https://github.com/aquasecurity/trivy)
- [Grype Installation Guide](https://github.com/anchore/grype)

## Usage
   git clone https://github.com/abdullaha360/cvescanner.git
   cd cvescanner
   python3 cvescanner.py [command] (t for trivy or g for grype)

