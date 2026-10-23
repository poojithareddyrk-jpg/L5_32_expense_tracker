# Lab 5: Issues Found and Fixed (expense_tracker.py)

Line numbers refer to the ORIGINAL `expense_tracker.py`. Check them against your
own before-reports (`bandit_report.txt`, `flake8_report.txt`, `pylint_report.txt`).

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| `os.system("xdg-open " + path)` (Bandit B605) | Security (High) | 61 | Path is concatenated into a shell command, so a crafted path can inject commands. | No shell: validate the path is an existing file, then open it via `webbrowser.open(Path.as_uri())`. |
| `tempfile.mktemp()` (Bandit B306) | Security (Medium) | 55 | Returns a name without creating the file, so there is a race condition (another process can create it first). | Use `tempfile.mkstemp()`, which creates the file atomically, and close the descriptor. |
| Hard-coded `/tmp/expense_reports` (Bandit B108) | Security (Medium) | 8 | Predictable, world-shared temp path. | Build the path from `tempfile.gettempdir()` and create it with `os.makedirs(mode=0o700)`. |
| Hard-coded password `"demo-sync-pass"` (Bandit B105) | Security (Low) | 5 (compare on 50) | Secret committed in source code. Also compared with `==`, which is not constant time. | Read it from the `BANK_SYNC_PASSWORD` environment variable, reject if unset, compare with `hmac.compare_digest`. |
| `except Exception` (Pylint W0718) | Bug / Quality | 41 | Too broad. It would hide real bugs, and it was only there to catch `max()` on an empty list. | Check `if not EXPENSES: return None` instead of using exceptions. |
| `global monthly_budget` (Pylint W0603) | Design | 29 | Rebinding a module global makes state hard to track and test. | Keep the budget in a `SETTINGS` dict and update it in place. |
| `range(len(...))` loop (Pylint C0200) | Quality | 45 | Un-Pythonic indexing. | Use `enumerate(EXPENSES, start=1)`. |
| camelCase names (Pylint C0103) | Style | 7 (`monthly_budget`), 11, 20, 28 (+ arg `newBudget`), 33, 38, 44, 49, 53, 59 (defs), 55 (`reportPath`) | Not PEP 8 snake_case. | Rename (`add_expense`, `set_budget(new_budget)`, ...). |
| Missing docstrings (Pylint C0114/C0116) | Documentation | 1 (module) + every def (11, 20, 28, 33, 38, 44, 49, 53, 59, 64) | No description of behaviour. | Add module and function docstrings. |
| `"amount" : amount` (Flake8 E203) | Style | 15 | Whitespace before `:`. | `"amount": amount`. |
| Missing blank lines (Flake8 E302) | Style | 44 (only 1 blank line before `printLedger`) | PEP 8 needs 2 blank lines. | Add them. |
| Inline comment spacing (Flake8 E261) | Style | 74 | Needs two spaces before `#`. | `...  # after set_budget`. |
| Line too long (Flake8 E501) | Style | 77 | Over 79 characters. | Wrap the call over several lines. |
| `main()` runs on import | Quality | 80 | Importing the module runs the demo. | Wrap in `if __name__ == "__main__":`. |
