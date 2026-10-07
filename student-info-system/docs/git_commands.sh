#!/usr/bin/env bash
# Suggested Git workflow that produces a meaningful commit history and
# uses feature branches. Run from the project root AFTER creating the
# empty GitHub repo "student-info-system". Edit the URL first.
set -e

git init -b main
git add .gitignore requirements.txt logs/.gitkeep
git commit -m "chore: initial project setup with .gitignore and requirements"
git remote add origin https://github.com/<your-username>/student-info-system.git
git push -u origin main

git checkout -b feature/config-logging
git add config src/utils/config.py src/utils/logger.py src/utils/__init__.py src/__init__.py
git commit -m "feat: add configuration loader and rotating logger"

git checkout main && git merge --no-ff feature/config-logging -m "Merge feature/config-logging"
git checkout -b feature/student-model
git add src/models
git commit -m "feat: add Student model with dict conversion"
git checkout main && git merge --no-ff feature/student-model -m "Merge feature/student-model"

git checkout -b feature/student-service
git add src/utils/validators.py src/services data
git commit -m "feat: implement student CRUD service with JSON persistence"
git commit --allow-empty -m "feat: add validation, search and CSV export"
git checkout main && git merge --no-ff feature/student-service -m "Merge feature/student-service"

git checkout -b feature/cli
git add src/main.py
git commit -m "feat: add console menu interface with error handling"
git checkout main && git merge --no-ff feature/cli -m "Merge feature/cli"

git checkout -b feature/tests
git add tests
git commit -m "test: add unit tests for service and validation"
git checkout main && git merge --no-ff feature/tests -m "Merge feature/tests"

git add README.md docs
git commit -m "docs: add README and git workflow guide"
git push origin --all
