# Reflection


**1. Which issues were easiest to fix and which were hardest?**
The style issues from Flake8 (blank lines, spacing, line length) and the Pylint
renames and docstrings were easy because the tool says exactly what to change.
The hardest were the security fixes, because they need a design decision.
Replacing `os.system` meant choosing a safe way to open a file. Replacing
`mktemp` meant understanding the race condition. Removing the hard-coded
password meant deciding where the secret should live.

**2. Did the tools report any false positives?**
The hard-coded password finding (B105) is flagged because of the variable name
and a string literal. In this demo the value is a placeholder, so it is
technically a low-risk finding. Even so, it is a good habit to take secrets out
of source code. Pylint's broad-except warning was also partly a design
choice: the original code used an exception for a normal case (an empty list).

**3. How would you integrate static analysis into your workflow?**
Run Flake8 and Pylint on every commit through a pre-commit hook, and run Bandit
in the CI pipeline on every pull request, failing the build on high or medium
findings. This catches problems before code review and keeps the team's
standard consistent.

**4. What tangible improvements did you see in code quality and security?**
The code now follows PEP 8 naming, has docstrings, and has no global mutable
state rebinding. The Pylint score went up from 5.27/10 to 10.00/10. The shell-injection and temp-file race vulnerabilities are gone, the
secret is out of the repository, and the program's output is unchanged.
