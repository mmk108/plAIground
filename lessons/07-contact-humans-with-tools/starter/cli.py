"""Command line for an agent that can ask questions. Each command is a separate run.

  python lessons/07-contact-humans-with-tools/starter/cli.py launch "Email the total units by region to my boss"
  python lessons/07-contact-humans-with-tools/starter/cli.py status <id>
  python lessons/07-contact-humans-with-tools/starter/cli.py reply <id> "boss@example.com"
"""
import argparse
import json

import human

parser = argparse.ArgumentParser()
sub = parser.add_subparsers(dest="command", required=True)
sub.add_parser("launch").add_argument("request")
sub.add_parser("status").add_argument("id")
p = sub.add_parser("reply")
p.add_argument("id")
p.add_argument("answer")

args = parser.parse_args()
if args.command == "launch":
    result = human.launch(args.request)
elif args.command == "status":
    result = human.get_status(args.id)
else:
    result = human.reply(args.id, args.answer)
print(json.dumps(result, indent=2))
