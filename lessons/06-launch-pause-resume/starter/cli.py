"""Command line for the agent service. Each command is a separate run, like a real app.

  python lessons/06-launch-pause-resume/starter/cli.py launch "Email total units by region to boss@example.com"
  python lessons/06-launch-pause-resume/starter/cli.py status <id>
  python lessons/06-launch-pause-resume/starter/cli.py resume <id> --approve    (or --reject)
  python lessons/06-launch-pause-resume/starter/cli.py list
"""
import argparse
import json

import service

parser = argparse.ArgumentParser()
sub = parser.add_subparsers(dest="command", required=True)
sub.add_parser("launch").add_argument("request")
sub.add_parser("status").add_argument("id")
p = sub.add_parser("resume")
p.add_argument("id")
group = p.add_mutually_exclusive_group(required=True)
group.add_argument("--approve", action="store_true")
group.add_argument("--reject", action="store_true")
sub.add_parser("list")

args = parser.parse_args()
if args.command == "launch":
    result = service.launch(args.request)
elif args.command == "status":
    result = service.get_status(args.id)
elif args.command == "resume":
    result = service.resume(args.id, approved=args.approve)
else:
    result = service.list_agents()
print(json.dumps(result, indent=2))
