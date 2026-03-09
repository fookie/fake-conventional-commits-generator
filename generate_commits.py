import argparse
import random
import subprocess
import json
import os
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Generate conventional commits for testing.")
    parser.add_argument("--count", type=int, default=5, help="Number of commits to generate")
    parser.add_argument("--include-breaking", action="store_true", help="Guarantee at least one breaking change")
    parser.add_argument("--undo", action="store_true", help="Revert the repository to the state before the last generation")
    args = parser.parse_args()

    dummy_file = "dummy.txt"
    history_file = "history.json"

    if args.undo:
        if not os.path.exists(history_file):
            print("No history file found. Cannot undo.")
            return

        try:
            with open(history_file, 'r') as f:
                history = json.load(f)
            
            target_commit = history.get("OriginalHead")
            if not target_commit:
                print("Invalid history file format. Cannot undo.")
                return

            print(f"Reverting repository to commit: {target_commit}")
            subprocess.run(["git", "reset", "--hard", target_commit], check=True, stdout=subprocess.DEVNULL)

            if os.path.exists(dummy_file):
                os.remove(dummy_file)
            os.remove(history_file)
            
            print("Undo complete!")
            return
        except Exception as e:
            print(f"Error during undo: {e}")
            return

    # Save current HEAD before generating commits
    try:
        current_head = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode('utf-8').strip()
        history_data = {
            "OriginalHead": current_head,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(history_file, 'w') as f:
            json.dump(history_data, f, indent=4)
        print(f"Saving current state ({current_head}) to {history_file}")
    except Exception as e:
        print(f"Failed to save current state: {e}")
        return

    commit_types = [
        {"type": "feat", "scopes": ["", "ui", "api", "core"], "messages": ["add new feature", "implement login", "improve performance", "update layout"]},
        {"type": "fix", "scopes": ["", "ui", "api", "core", "db"], "messages": ["resolve crash on startup", "fix typo in header", "handle null exception", "correct date format"]},
        {"type": "chore", "scopes": ["", "deps"], "messages": ["update dependencies", "clean up unused code", "refactor project structure"]},
        {"type": "docs", "scopes": ["", "readme"], "messages": ["update README", "add api documentation", "fix broken links"]}
    ]

    print(f"Generating {args.count} conventional commits...\n")

    for i in range(args.count):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        with open(dummy_file, "a") as f:
            f.write(f"Commit test content {timestamp}\n")

        subprocess.run(["git", "add", dummy_file], check=True)

        type_obj = random.choice(commit_types)
        scope = random.choice(type_obj["scopes"])
        message = random.choice(type_obj["messages"])

        if scope:
            subject = f"{type_obj['type']}({scope}): {message}"
        else:
            subject = f"{type_obj['type']}: {message}"

        add_body = random.randint(0, 10) > 5
        body = ""
        if add_body:
            body = "Added some extra details for this commit.\nThis helps test multi-line commit messages."

        is_breaking = False
        if args.include_breaking and i == args.count - 1:
            is_breaking = True
        elif args.include_breaking and random.randint(0, 10) > 8:
            is_breaking = True

        if is_breaking:
            if random.randint(0, 1) == 0:
                if scope:
                    subject = f"{type_obj['type']}({scope})!: {message}"
                else:
                    subject = f"{type_obj['type']}!: {message}"
                
                if not add_body:
                    body = "This breaks the previous implementation by changing expected types."
            else:
                body = "BREAKING CHANGE: The existing API is no longer supported and has been replaced.\n\n" + body

        commit_args = ["git", "commit", "-m", subject]
        if body:
            commit_args.extend(["-m", body])
        
        # Suppress the git commit output to make stdout cleaner
        subprocess.run(commit_args, check=True, stdout=subprocess.DEVNULL)
        print(f"Created commit: {subject}")

    print("\nDone! Run 'git log --oneline' to see the commits.")
    print("To revert these commits, run: python generate_commits.py --undo")

if __name__ == "__main__":
    main()
