#!/usr/bin/env python3
import os, http.server, socketserver, json, subprocess

PORT = 8765
DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.environ.get("COMPENDIUM_SKILLS_DIR", os.path.expanduser("~/.claude/skills"))
BACKUP_DIR = os.environ.get("COMPENDIUM_BACKUP_DIR", os.path.expanduser("~/.claude/skills-backup"))
os.chdir(DIR)

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

def find_browser():
    for p in EDGE_PATHS:
        if os.path.exists(p):
            return p
    for p in CHROME_PATHS:
        if os.path.exists(p):
            return p
    # fallback: check user local
    local = os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    if os.path.exists(local):
        return local
    return None

class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, f, *a): pass

    def do_GET(self):
        if self.path == "/api/stats":
            self._json_response(self._stats())
            return

        if self.path == "/api/backup":
            self._json_response(self._backup_stats())
            return

        if self.path.startswith("/api/restore-backup"):
            qs = self.path.split("?")[1] if "?" in self.path else ""
            name = ""
            for p in qs.split("&"):
                if p.startswith("skill="):
                    name = p[6:]
                    break
            ok = False
            if name:
                src = os.path.join(BACKUP_DIR, name)
                dst = os.path.join(SKILLS_DIR, name)
                if os.path.isdir(src) and not os.path.exists(dst):
                    import shutil
                    shutil.move(src, dst)
                    ok = True
            self._json_response({"ok": ok, "skill": name})
            return

        if self.path.startswith("/api/backup-skill"):
            qs = self.path.split("?")[1] if "?" in self.path else ""
            name = ""
            for p in qs.split("&"):
                if p.startswith("skill="):
                    name = p[6:]
                    break
            ok = False
            if name:
                src = os.path.join(SKILLS_DIR, name)
                dst = os.path.join(BACKUP_DIR, name)
                if os.path.isdir(src):
                    import shutil
                    os.makedirs(BACKUP_DIR, exist_ok=True)
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.move(src, dst)
                    ok = True
            self._json_response({"ok": ok, "skill": name})
            return

        if self.path == "/api/launch-vertical":
            url = "http://127.0.0.1:8765/vertical.html"
            self._json_response({"ok": True})

            browser = find_browser()
            if browser:
                subprocess.Popen(
                    [browser, "--app=" + url, "--window-size=420,700"],
                    creationflags=0x00000008 | 0x08000000)  # DETACHED | CREATE_NO_WINDOW
            else:
                os.system("start " + url)
            return

        return super().do_GET()

    def _json_response(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _read_skill_desc(self, name):
        p = os.path.join(SKILLS_DIR, name, "SKILL.md")
        if not os.path.isfile(p): return ""
        try:
            with open(p, encoding='utf-8') as f:
                content = f.read(4096)
            import re
            m = re.search(r'description:\s*(.+?)(?:\n\w+:|$)', content, re.DOTALL)
            if m:
                desc = m.group(1).strip().replace('\n', ' ')
                return desc[:200]
        except: pass
        return ""

    def _stats(self):
        try:
            dirs = [d for d in os.listdir(SKILLS_DIR)
                    if os.path.isdir(os.path.join(SKILLS_DIR, d))]
        except FileNotFoundError:
            dirs = []
        skills = []
        for d in sorted(dirs):
            skills.append({"name": d, "desc": self._read_skill_desc(d)})
        return {"total_skills": len(skills), "skills": skills}

    def _backup_stats(self):
        try:
            dirs = [d for d in os.listdir(BACKUP_DIR)
                    if os.path.isdir(os.path.join(BACKUP_DIR, d))]
        except FileNotFoundError:
            dirs = []
        return {"total_skills": len(dirs), "skills": sorted(dirs)}

if __name__ == "__main__":
    with socketserver.ThreadingTCPServer(("127.0.0.1", PORT), H) as h:
        h.daemon_threads = True
        try:
            h.serve_forever()
        except KeyboardInterrupt:
            pass
