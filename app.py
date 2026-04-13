from flask import Flask, jsonify, render_template
import sqlite3
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "majors.db"

app = Flask(__name__, template_folder="templates", static_folder="static")
YEAR_RE = re.compile(r"\b(20\d{2}|19\d{2})\b")


def parse_years(date_text):
    if not date_text:
        return []
    return sorted({match.group(0) for match in YEAR_RE.finditer(date_text)})


def fetch_majors():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT Date, Winner, "Runner-up" AS RunnerUp FROM majors')
        for row in cursor.fetchall():
            yield row["Date"], row["Winner"], row["RunnerUp"]


def build_team_summary():
    summary = {}
    for date_text, winner, runner_up in fetch_majors():
        years = parse_years(date_text)
        year = years[0] if years else None
        if winner:
            team = winner.strip()
            entry = summary.setdefault(team, {"wins": [], "runner_up": []})
            if year and year not in entry["wins"]:
                entry["wins"].append(year)
        if runner_up:
            team = runner_up.strip()
            entry = summary.setdefault(team, {"wins": [], "runner_up": []})
            if year and year not in entry["runner_up"]:
                entry["runner_up"].append(year)
    for entry in summary.values():
        entry["wins"].sort()
        entry["runner_up"].sort()
    return summary


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/teams")
def api_teams():
    summary = build_team_summary()
    return jsonify({"teams": sorted(summary.keys())})


@app.route("/api/team/<path:team_name>")
def api_team(team_name):
    summary = build_team_summary()
    team = summary.get(team_name)
    if not team:
        return jsonify({"error": "Team not found"}), 404
    return jsonify({
        "team": team_name,
        "wins": team["wins"],
        "runner_up": team["runner_up"],
        "count": {"wins": len(team["wins"]), "runner_up": len(team["runner_up"])},
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
