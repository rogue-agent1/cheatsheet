#!/usr/bin/env python3
"""cheatsheet - Quick reference cheat sheets for common CLI tools.

Single-file, zero-dependency CLI.
"""

import sys
import argparse

SHEETS = {
    "git": """Git Cheat Sheet
  git init                          Initialize repo
  git clone <url>                   Clone remote repo
  git add .                         Stage all changes
  git commit -m "msg"               Commit staged changes
  git push / git pull               Push/pull from remote
  git branch <name>                 Create branch
  git checkout <branch>             Switch branch
  git merge <branch>                Merge branch
  git log --oneline -10             Last 10 commits
  git diff                          Show unstaged changes
  git stash / git stash pop         Stash/restore changes
  git reset --hard HEAD~1           Undo last commit (destructive)
  git rebase -i HEAD~3              Interactive rebase last 3
  git cherry-pick <hash>            Apply specific commit
  git remote -v                     List remotes""",

    "docker": """Docker Cheat Sheet
  docker build -t name .            Build image
  docker run -it name               Run interactively
  docker run -d -p 8080:80 name     Run detached with port map
  docker ps / docker ps -a          List running/all containers
  docker images                     List images
  docker exec -it <id> bash         Shell into container
  docker logs -f <id>               Follow logs
  docker stop <id>                  Stop container
  docker rm <id>                    Remove container
  docker rmi <image>                Remove image
  docker compose up -d              Start compose services
  docker compose down               Stop compose services
  docker system prune -a            Clean everything""",

    "curl": """cURL Cheat Sheet
  curl <url>                        GET request
  curl -o file <url>                Download to file
  curl -X POST -d 'data' <url>     POST with data
  curl -H "Auth: Bearer tok" <url>  Custom header
  curl -F "file=@path" <url>       Upload file
  curl -s <url> | jq .             Silent + pipe to jq
  curl -I <url>                    HEAD request (headers only)
  curl -L <url>                    Follow redirects
  curl -k <url>                    Skip TLS verification
  curl -w "%{time_total}" <url>    Show timing
  curl --retry 3 <url>             Retry on failure
  curl -x proxy:port <url>         Use proxy""",

    "tar": """tar Cheat Sheet
  tar czf archive.tar.gz dir/      Create gzip archive
  tar xzf archive.tar.gz           Extract gzip archive
  tar xzf archive.tar.gz -C dest/  Extract to directory
  tar tf archive.tar.gz            List contents
  tar cjf archive.tar.bz2 dir/    Create bzip2 archive
  tar xjf archive.tar.bz2         Extract bzip2
  tar czf - dir/ | ssh h 'cat>a'  Archive over SSH
  tar --exclude='*.log' czf a dir  Exclude pattern""",

    "python": """Python Cheat Sheet
  python -m venv .venv              Create virtualenv
  source .venv/bin/activate         Activate venv
  pip install -r requirements.txt   Install deps
  pip freeze > requirements.txt     Export deps
  python -m pytest                  Run tests
  python -m http.server 8000        Quick HTTP server
  python -c "import json; ..."      One-liner
  python -m pdb script.py           Debug
  python -i script.py               Interactive after run
  python -m cProfile script.py      Profile
  python -m timeit "expr"           Benchmark expression""",

    "ssh": """SSH Cheat Sheet
  ssh user@host                     Connect
  ssh -p 2222 user@host             Custom port
  ssh -i key.pem user@host          Use key file
  ssh-keygen -t ed25519             Generate key
  ssh-copy-id user@host             Copy key to remote
  ssh -L 8080:localhost:80 host     Local port forward
  ssh -R 8080:localhost:80 host     Remote port forward
  ssh -D 1080 host                  SOCKS proxy
  ssh -N -f -L 3306:db:3306 host   Background tunnel
  scp file user@host:path           Copy file to remote
  rsync -avz dir/ user@host:dir/   Sync directory""",
}


def cmd_show(args):
    name = args.name.lower()
    if name in SHEETS:
        print(SHEETS[name])
    else:
        print(f"  Unknown sheet: {name}")
        print(f"  Available: {', '.join(sorted(SHEETS.keys()))}")
        return 1


def cmd_list(args):
    for name in sorted(SHEETS.keys()):
        first_line = SHEETS[name].strip().split("\n")[0]
        print(f"  {name:12s}  {first_line}")


def cmd_search(args):
    query = args.query.lower()
    found = 0
    for name, content in SHEETS.items():
        for line in content.split("\n"):
            if query in line.lower():
                print(f"  [{name}] {line.strip()}")
                found += 1
    if not found:
        print(f"  No matches for '{args.query}'")


def main():
    p = argparse.ArgumentParser(prog="cheatsheet", description="CLI cheat sheets")
    sub = p.add_subparsers(dest="cmd")
    s = sub.add_parser("show", aliases=["s"], help="Show cheat sheet")
    s.add_argument("name")
    sub.add_parser("list", aliases=["ls"], help="List available sheets")
    s = sub.add_parser("search", help="Search across sheets")
    s.add_argument("query")
    args = p.parse_args()
    if not args.cmd: p.print_help(); return 1
    cmds = {"show": cmd_show, "s": cmd_show, "list": cmd_list, "ls": cmd_list, "search": cmd_search}
    return cmds[args.cmd](args) or 0


if __name__ == "__main__":
    sys.exit(main())
