import hashlib
import os
import subprocess
import sys


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def file_hash(path):
    try:
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except OSError:
        return None


def main():
    repo = os.getenv("UPSTREAM_REPO", "").strip()
    branch = os.getenv("UPSTREAM_BRANCH", "main").strip() or "main"

    if not repo:
        print("[UPSTREAM] UPSTREAM_REPO not set, skipping.", flush=True)
        return

    old_req = file_hash("requirements.txt")

    if not os.path.isdir(".git"):
        run(["git", "init"])
    if run(["git", "remote", "set-url", "origin", repo])[0] != 0:
        run(["git", "remote", "add", "origin", repo])

    code, out = run(["git", "fetch", "origin", branch])
    if code != 0:
        print(f"[UPSTREAM] Fetch failed: {out}", flush=True)
        return

    code, out = run(["git", "checkout", "-f", "-B", branch, "FETCH_HEAD"])
    if code != 0:
        print(f"[UPSTREAM] Checkout failed: {out}", flush=True)
        return

    run(["git", "config", f"branch.{branch}.remote", "origin"])
    run(["git", "config", f"branch.{branch}.merge", f"refs/heads/{branch}"])
    run(["git", "config", "pull.rebase", "false"])
    print(f"[UPSTREAM] Updated from {repo} ({branch})", flush=True)

    if file_hash("requirements.txt") != old_req:
        print("[UPSTREAM] Installing new requirements...", flush=True)
        run([sys.executable, "-m", "pip", "install", "--no-cache-dir", "-r", "requirements.txt"])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[UPSTREAM] Error: {e}", flush=True)
