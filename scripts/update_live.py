#!/usr/bin/env python3
"""Update data/live.json for the 3D office and push to GitHub (uses NABZ_GITHUB_TOKEN).

Examples:
  update_live.py --agent video --state working --task "ریل جدید" --location video
  update_live.py --request "یه ریل درباره X بساز"
  update_live.py --meeting-title "جلسه ریل X" --meeting-clear --all-state in_meeting
  update_live.py --msg ceo-bot "متن" --msg content "متن"
  update_live.py --all-state idle --no-push
Agents: ceo-bot, content, video, growth. States: idle | working | in_meeting.
"""
import argparse, json, os, subprocess, datetime, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
F = ROOT / "data" / "live.json"
AG = ["ceo-bot", "content", "video", "growth"]
p = argparse.ArgumentParser()
p.add_argument("--agent", choices=AG); p.add_argument("--state", choices=["idle", "working", "in_meeting"])
p.add_argument("--task"); p.add_argument("--location")
p.add_argument("--all-state", choices=["idle", "working", "in_meeting"])
p.add_argument("--request"); p.add_argument("--meeting-title"); p.add_argument("--meeting-clear", action="store_true")
p.add_argument("--msg", nargs=2, action="append", metavar=("WHO", "TEXT"))
p.add_argument("--no-push", action="store_true"); p.add_argument("-m", "--commit-msg", default="Update live office state")
a = p.parse_args()
d = json.loads(F.read_text("utf-8"))
d.setdefault("agents", {}); d.setdefault("meeting", {"title": "", "messages": []})
if a.all_state:
    for k in AG:
        s = d["agents"].setdefault(k, {}); s["state"] = a.all_state
        s["location"] = "meeting" if a.all_state == "in_meeting" else ("ceo" if k == "ceo-bot" else k)
if a.agent:
    s = d["agents"].setdefault(a.agent, {})
    if a.state:
        s["state"] = a.state
        if not a.location: s["location"] = "meeting" if a.state == "in_meeting" else ("ceo" if a.agent == "ceo-bot" else a.agent)
    if a.task is not None: s["task"] = a.task
    if a.location: s["location"] = a.location
if a.request is not None: d["yasin_request"] = a.request
if a.meeting_title is not None: d["meeting"]["title"] = a.meeting_title
if a.meeting_clear: d["meeting"]["messages"] = []
for who, text in a.msg or []: d["meeting"]["messages"].append({"who": who, "text": text})
d["updated"] = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
F.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", "utf-8")
print("live.json updated")
if not a.no_push:
    g = lambda *c: subprocess.run(["git", "-C", str(ROOT), *c], check=True)
    g("add", "data/live.json")
    if subprocess.run(["git", "-C", str(ROOT), "diff", "--cached", "--quiet"]).returncode:
        g("-c", "user.name=yasinfallahati", "-c", "user.email=yasinfallahati@users.noreply.github.com", "commit", "-qm", a.commit_msg)
        g("push", "-q", f"https://x-access-token:{os.environ['NABZ_GITHUB_TOKEN']}@github.com/yasinfallahati/nabz-company.git", "HEAD:main")
        print("pushed")
