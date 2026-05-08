from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import sqlite3
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "majors.db"

app = FastAPI()
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


@app.get("/")
async def index():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/api/teams")
async def api_teams():
    summary = build_team_summary()
    return {"teams": sorted(summary.keys())}


@app.get("/api/team/{team_name}")
async def api_team(team_name: str):
    summary = build_team_summary()
    team = summary.get(team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return {
        "team": team_name,
        "wins": team["wins"],
        "runner_up": team["runner_up"],
        "count": {"wins": len(team["wins"]), "runner_up": len(team["runner_up"])},
    }


app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
