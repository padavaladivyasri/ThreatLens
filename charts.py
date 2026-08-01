

import os
import matplotlib.pyplot as plt

def generate_chart(result):
    os.makedirs("static/charts", exist_ok=True)

    labels = [
        "Failed Logins",
        "Admin Access",
        "404 Errors",
        "500 Errors"
    ]

    values = [
        result["failed_logins"],
        result["admin_access"],
        result["error_404"],
        result["error_500"]
    ]

    plt.figure(figsize=(7, 5))

    plt.bar(labels, values)

    plt.title("ThreatLens Security Analysis")

    plt.xlabel("Event Type")

    plt.ylabel("Number of Events")

    plt.tight_layout()

    chart_path = "static/charts/chart.png"

    plt.savefig(chart_path)

    plt.close()

    return chart_path