<#
.SYNOPSIS
    Safe, automated shipping script for the Food Packaging AI project.
.DESCRIPTION
    Implements a strict pipeline: VERIFY -> REVIEW -> COMMIT -> PUSH.
    Guarantees that verification checks pass, secret files are never committed,
    and changes are pushed only to the designated remote and branch without force-pushing.
.PARAMETER Message
    Conventional commit message.
.PARAMETER DryRun
    Runs all safety and verification checks without committing or pushing.
.PARAMETER Branch
    Target git branch (default: "main").
.PARAMETER Remote
    Target git remote (default: "origin").
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Message,

    [switch]$DryRun,

    [string]$Branch = "main",
    [string]$Remote = "origin"
)

$ErrorActionPreference = "Stop"

# Project root directory resolution
$rootDir = (Get-Item $PSScriptRoot).Parent.FullName
Set-Location $rootDir

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " SAFE AUTO-SHIP PIPELINE: Food-Packaging-AI" -ForegroundColor Cyan
Write-Host " Mode: $(if ($DryRun) { 'DRY RUN (no commit/push)' } else { 'LIVE SHIP' })" -ForegroundColor Cyan
Write-Host " Root: $rootDir" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# 1. BRANCH & CONFLICT CHECKS
$currentBranch = (git branch --show-current).Trim()
if (-not $currentBranch) {
    # If initial commit hasn't been made yet, verify current symbolic ref
    $currentBranch = "main"
}

Write-Host "[1/5] Checking branch state..." -ForegroundColor Yellow
Write-Host "      Current Branch: $currentBranch"
if ($currentBranch -ne $Branch) {
    Write-Error "Safety Abort: Expected branch '$Branch', but currently on '$currentBranch'."
}

# Check for merge conflicts
$conflictFiles = git diff --name-only --diff-filter=U
if ($conflictFiles) {
    Write-Error "Safety Abort: Unresolved merge conflicts detected:`n$conflictFiles"
}

# 2. SECRET & FORBIDDEN ARTIFACT AUDIT
Write-Host "[2/5] Auditing for secrets and untracked build artifacts..." -ForegroundColor Yellow

$forbiddenPatterns = @(
    "^\.env$",
    "^\.env\..+$",
    "\.pem$",
    "\.key$",
    "\.p12$",
    "id_rsa",
    "node_modules",
    "\.venv",
    "frontend/dist",
    "__pycache__",
    "\.pytest_cache",
    "\.ruff_cache",
    "\.db$",
    "\.sqlite",
    "\.sqlite3$"
)

# Allowed exceptions to the above regexes
$allowedExceptions = @(
    "^\.env\.example$"
)

# Inspect all modified/untracked files
$statusLines = git status --porcelain
foreach ($line in $statusLines) {
    $filePath = $line.Substring(3).Trim()
    
    # Check if this matches an allowed exception
    $isAllowed = $false
    foreach ($allow in $allowedExceptions) {
        if ($filePath -match $allow) {
            $isAllowed = $true
            break
        }
    }
    if ($isAllowed) { continue }

    foreach ($pattern in $forbiddenPatterns) {
        if ($filePath -match $pattern) {
            Write-Error "Safety Abort: Detected forbidden file/secret '$filePath' matching rule '$pattern'."
        }
    }
}
Write-Host "      Secret & forbidden artifact audit PASSED." -ForegroundColor Green

# 3. VERIFICATION SUITE EXECUTION
Write-Host "[3/5] Running automated verification test suite..." -ForegroundColor Yellow

$pythonExe = Join-Path $rootDir "backend\.venv\Scripts\python.exe"
$ruffExe = Join-Path $rootDir "backend\.venv\Scripts\ruff.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Error "Python virtual environment not found at '$pythonExe'. Please initialize Phase 0."
}

# 3a. Backend Pytest
Write-Host "      Running Backend Pytest..." -ForegroundColor Gray
& $pythonExe -m pytest
if ($LASTEXITCODE -ne 0) {
    Write-Error "Verification Failure: Backend test suite failed."
}

# 3b. Backend Ruff Lint Check
Write-Host "      Running Ruff Lint Check..." -ForegroundColor Gray
& $ruffExe check backend data
if ($LASTEXITCODE -ne 0) {
    Write-Error "Verification Failure: Ruff lint check failed."
}

# 3c. Backend Ruff Format Check
Write-Host "      Running Ruff Format Check..." -ForegroundColor Gray
& $ruffExe format --check backend data
if ($LASTEXITCODE -ne 0) {
    Write-Error "Verification Failure: Ruff format check failed."
}

# 3d. Frontend TypeScript Check
Write-Host "      Running Frontend TypeScript Check..." -ForegroundColor Gray
Push-Location (Join-Path $rootDir "frontend")
try {
    npm run typecheck
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Verification Failure: Frontend TypeScript check failed."
    }

    # 3e. Frontend Production Build
    Write-Host "      Running Frontend Build..." -ForegroundColor Gray
    npm run build
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Verification Failure: Frontend production build failed."
    }
}
finally {
    Pop-Location
}

Write-Host "      All verification checks PASSED successfully." -ForegroundColor Green

# 4. REVIEW STAGED / UNSTAGED CHANGES
Write-Host "[4/5] Reviewing changes to ship..." -ForegroundColor Yellow

if (-not $statusLines) {
    Write-Host "No changes detected. Working tree clean." -ForegroundColor Green
    return
}

# Stage files
git add .

# Double-check staged files against forbidden patterns
$stagedFiles = git diff --name-only --cached
foreach ($staged in $stagedFiles) {
    $isAllowed = $false
    foreach ($allow in $allowedExceptions) {
        if ($staged -match $allow) {
            $isAllowed = $true
            break
        }
    }
    if ($isAllowed) { continue }

    foreach ($pattern in $forbiddenPatterns) {
        if ($staged -match $pattern) {
            git reset HEAD $staged
            Write-Error "Safety Abort: Forbidden file staged: '$staged'. Reset staged changes."
        }
    }
}

Write-Host "Files to be committed:" -ForegroundColor Cyan
$stagedFiles | ForEach-Object { Write-Host "  + $_" -ForegroundColor DarkCyan }

# Handle DryRun exit
if ($DryRun) {
    Write-Host ""
    Write-Host "[DRY-RUN] Safety checks and verifications completed successfully." -ForegroundColor Green
    Write-Host "[DRY-RUN] Staging uncommitted changes reset. Nothing was committed or pushed." -ForegroundColor Green
    git reset
    return
}

# Validate Commit Message
if (-not $Message) {
    Write-Error "Safety Abort: A commit message is required. Example: -Message 'feat: add phase 1 data models'"
}

$conventionalRegex = "^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-zA-Z0-9_\-]+\))?:\s.+$"
if ($Message -notmatch $conventionalRegex) {
    Write-Warning "Commit message does not match strict Conventional Commits format ($conventionalRegex)."
    Write-Warning "Recommended format: '<type>(<scope>): <subject>' (e.g., 'feat(data): add initial fixtures')"
}

# 5. COMMIT & PUSH
Write-Host "[5/5] Committing and shipping to $Remote/$Branch..." -ForegroundColor Yellow

git commit -m "$Message"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Git commit failed."
}

$commitHash = (git rev-parse --short HEAD).Trim()
Write-Host "      Committed: $commitHash" -ForegroundColor Green

Write-Host "      Pushing to $Remote $Branch (Safe push, no force)..." -ForegroundColor Gray
git push -u $Remote $Branch
if ($LASTEXITCODE -ne 0) {
    Write-Error "Git push failed. Ensure origin remote is configured and network is accessible."
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host " SHIP COMPLETE" -ForegroundColor Green
Write-Host " Commit: $commitHash" -ForegroundColor Green
Write-Host " Branch: $Branch" -ForegroundColor Green
Write-Host " Remote: $Remote ($((git remote get-url $Remote).Trim()))" -ForegroundColor Green
Write-Host " Result: Success" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
