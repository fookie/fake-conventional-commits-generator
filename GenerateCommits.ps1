param (
    [int]$Count = 5,
    [switch]$IncludeBreaking = $false
)

$DummyFile = "dummy.txt"

# Array of commit types and messages
$CommitTypes = @(
    @{ Type = "feat"; Scopes = @("", "ui", "api", "core"); Messages = @("add new feature", "implement login", "improve performance", "update layout") },
    @{ Type = "fix"; Scopes = @("", "ui", "api", "core", "db"); Messages = @("resolve crash on startup", "fix typo in header", "handle null exception", "correct date format") },
    @{ Type = "chore"; Scopes = @("", "deps"); Messages = @("update dependencies", "clean up unused code", "refactor project structure") },
    @{ Type = "docs"; Scopes = @("", "readme"); Messages = @("update README", "add api documentation", "fix broken links") }
)

Write-Host "Generating $Count conventional commits..." -ForegroundColor Cyan

for ($i = 0; $i -lt $Count; $i++) {
    # Generate random content for the dummy file
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff"
    "Commit test content $Timestamp" | Out-File -Append -FilePath $DummyFile

    # Stage the file
    git add $DummyFile

    # Pick a random commit structure
    $TypeIndex = Get-Random -Maximum $CommitTypes.Count
    $TypeObj = $CommitTypes[$TypeIndex]
    
    $ScopeIndex = Get-Random -Maximum $TypeObj.Scopes.Count
    $Scope = $TypeObj.Scopes[$ScopeIndex]
    
    $MsgIndex = Get-Random -Maximum $TypeObj.Messages.Count
    $Message = $TypeObj.Messages[$MsgIndex]

    $Subject = ""
    if ($Scope) {
        $Subject = "$($TypeObj.Type)($Scope): $Message"
    }
    else {
        $Subject = "$($TypeObj.Type): $Message"
    }

    # Add optional body
    $AddBody = (Get-Random -Minimum 0 -Maximum 10) -gt 5
    $Body = ""
    if ($AddBody) {
        $Body = "Added some extra details for this commit.`nThis helps test multi-line commit messages."
    }

    # Decide if this is a breaking change (if requested, guarantee at least one, or random chance otherwise)
    $IsBreaking = $false
    if ($IncludeBreaking -and $i -eq ($Count - 1)) {
        $IsBreaking = $true # Make the last one breaking to guarantee it
    }
    elseif ($IncludeBreaking -and (Get-Random -Minimum 0 -Maximum 10) -gt 8) {
        $IsBreaking = $true
    }

    if ($IsBreaking) {
        # Randomly choose between ! in header or BREAKING CHANGE in body
        if ((Get-Random) % 2 -eq 0) {
            # ! in header
            if ($Scope) {
                $Subject = "$($TypeObj.Type)($Scope)!: $Message"
            }
            else {
                $Subject = "$($TypeObj.Type)!: $Message"
            }
            if (-not $AddBody) {
                # Still add a body to explain the breaking change
                $Body = "This breaks the previous implementation by changing expected types."
            }
        }
        else {
            # BREAKING CHANGE in body
            $Body = "BREAKING CHANGE: The existing API is no longer supported and has been replaced.`n`n" + $Body
        }
    }

    # Execute git commit
    if ($Body) {
        # Using array to pass arguments securely, taking advantage of PowerShell's argument handling
        $CommitArgs = @("commit", "-m", $Subject, "-m", $Body)
        & git @CommitArgs | Out-Null
    }
    else {
        $CommitArgs = @("commit", "-m", $Subject)
        & git @CommitArgs | Out-Null
    }

    Write-Host "Created commit: $Subject" -ForegroundColor Green
}

Write-Host "Done! Run 'git log --oneline' to see the commits." -ForegroundColor Cyan
