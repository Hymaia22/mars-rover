#!/usr/bin/env python3
import json
import os
import sys

data = json.load(sys.stdin)
command = data.get("tool_input", {}).get("command", "")
if "deploy" in command and "production" in command:
    if not os.path.exists("release-approval.txt"):
        print(
            "Une mise en production demande l'autorisation nommée du Release "
            "Manager. Dépose release-approval.txt à la racine avant de relancer.",
            file=sys.stderr,
        )
        sys.exit(2)
sys.exit(0)
