import re
from collections import Counter

def analyze_log(filepath):

    result = {
        "total_logs": 0,
        "failed_logins": 0,
        "admin_access": 0,
        "error_404": 0,
        "error_500": 0,
        "suspicious_ips": [],
        "threat_level": "Low"
    }

    ip_counter = Counter()

    with open(filepath, "r") as file:
        lines = file.readlines()

    result["total_logs"] = len(lines)

    for line in lines:

        # Extract IP Address
        ip_match = re.match(r"(\d+\.\d+\.\d+\.\d+)", line)

        if ip_match:
            ip = ip_match.group(1)
            ip_counter[ip] += 1

        # Failed Login
        if "401" in line:
            result["failed_logins"] += 1

        # Admin Page Access
        if "/admin" in line:
            result["admin_access"] += 1

        # 404 Error
        if "404" in line:
            result["error_404"] += 1

        # 500 Error
        if "500" in line:
            result["error_500"] += 1

    # Suspicious IPs (more than 5 requests)
    for ip, count in ip_counter.items():
        if count > 5:
            result["suspicious_ips"].append(ip)

    # Threat Level
    score = (
        result["failed_logins"] +
        result["admin_access"] +
        result["error_500"] +
        len(result["suspicious_ips"])
    )

    if score >= 10:
        result["threat_level"] = "High"
    elif score >= 5:
        result["threat_level"] = "Medium"
    else:
        result["threat_level"] = "Low"

    return result