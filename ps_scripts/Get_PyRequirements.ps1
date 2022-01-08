# Move up 1 directory level
Set-Location (Get-Location | Split-Path)

# Check if file exist, rename if yes
if (Test-Path "requirements\requirements.txt") {
    $cur_date = Get-Date -Format "yyyy-MM-ddTHHmm"
    Rename-Item -Path "requirements\requirements.txt" -NewName "requirements_$cur_date.txt"
}

# Check if folder exist, create if no
if (-not (Test-Path -Path "requirements") ) {
    New-Item -Name "requirements" -ItemType "directory"
}

# Run Python pip for requirements.txt
venv\Scripts\python -m pip freeze > requirements\requirements.txt

# Output Python version
python --version | Out-File -FilePath requirements\PyVersion.txt

Read-Host "Python version and requirements generated`nPress any key to continue..."
