from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from analyzer import analyze_log
from charts import generate_chart
from report import generate_report

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)
os.makedirs("static/charts", exist_ok=True)


# ---------------- LOGIN ----------------

@app.route("/")
def login():
    return render_template("login.html")


@app.route("/dashboard", methods=["POST"])
def dashboard():

    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "admin123":
        return render_template("dashboard.html")

    return render_template(
        "login.html",
        error="Invalid Username or Password"
    )


# ---------------- HOME ----------------

@app.route("/home")
def home():
    return render_template("index.html")


# ---------------- ANALYZE ----------------

@app.route("/analyze", methods=["POST"])
def analyze():

    if "logfile" not in request.files:
        return "No file uploaded."

    file = request.files["logfile"]

    if file.filename == "":
        return "Please select a log file."

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    result = analyze_log(filepath)

    generate_chart(result)

    generate_report(result)

    return render_template(
        "result.html",
        result=result
    )


# ---------------- PDF ----------------

@app.route("/reports/<filename>")
def download_report(filename):

    return send_from_directory(
        "reports",
        filename,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)