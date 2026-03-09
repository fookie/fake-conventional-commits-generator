# fake-conventional-commits-generator

This project contains helper scripts designed to generate randomized git commits that follow the [Conventional Commits](https://www.conventionalcommits.org/) format. 

These are primarily used to test the `commit-and-tag-version` tools logic by simulating realistic commit histories (including `feat`, `fix`, `chore`, and `BREAKING CHANGE`).

## Available Scripts

We provide two versions of the script with identical functionality. You can choose whichever environment you prefer.

1. **`GenerateCommits.ps1`** - A Windows PowerShell script.
2. **`generate_commits.py`** - A Python script.

Both scripts perform the following steps for each commit:
1. Append a timestamp to a dummy file (`dummy.txt`).
2. Stage the file (`git add`).
3. Randomly generate a Conventional Commit message (e.g., `feat(ui): add new feature`).
4. Optionally append a multi-line body.
5. Optionally include a breaking change (either with a `!` in the header or `BREAKING CHANGE:` in the body).
6. Execute the commit.

---

## 1. PowerShell Version

### Prerequisites
- Windows PowerShell 5.1 or PowerShell Core.
- `git` must be accessible from your PATH.

### Usage
From within the `GitGenerate` directory, run:

```powershell
.\GenerateCommits.ps1 -Count <Number> [-IncludeBreaking]
```

**Examples:**
- Generate 5 random commits:
  ```powershell
  .\GenerateCommits.ps1 -Count 5
  ```
- Generate 10 commits, ensuring at least one major/breaking change:
  ```powershell
  .\GenerateCommits.ps1 -Count 10 -IncludeBreaking
  ```

---

## 2. Python Version

### Prerequisites
- Python 3.x installed.
- `git` must be accessible from your PATH.

### Usage
From within the `GitGenerate` directory, run:

```bash
python generate_commits.py --count <Number> [--include-breaking]
```

**Examples:**
- Generate 5 random commits:
  ```bash
  python generate_commits.py --count 5
  ```
- Generate 10 commits, ensuring at least one major/breaking change:
  ```bash
  python generate_commits.py --count 10 --include-breaking
  ```

---

## Clean Up / Undo

Because these scripts create actual commits in your local git repository, you may want to revert them after you finish testing your package. 

Before generating commits, both scripts automatically save the current git `HEAD` hash into a `history.json` config file inside this directory.

To quickly undo the last generated test commits and restore your repository to its precise previous state, simply run the script with the undo argument:

**PowerShell:**
```powershell
.\GenerateCommits.ps1 -Undo
```

**Python:**
```bash
python generate_commits.py --undo
```

> **Warning:** Running the undo command uses `git reset --hard` under the hood. It will revert changes and erase any uncommitted work in your directory. Ensure your working directory is clean before generating test commits!
