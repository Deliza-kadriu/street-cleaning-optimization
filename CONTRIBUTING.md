# Contributing

This is a collaborative Advanced Algorithms course project. Keep contributions small, explain your approach, and make results reproducible.

## Choose a task

Create or select a GitHub issue before starting substantial work. State the intended result and acceptance criteria, and comment that you are taking the task so work is not duplicated. Agree on shared input/output formats before implementing modules that depend on each other.

## Work on a branch

Start with a clean working tree. Commit or safely save any existing work before switching branches.

```bash
git switch main
git pull --ff-only origin main
git switch -c feature/short-task-name
```

Use descriptive branch names such as `feature/graph-model`, `fix/route-validation`, or `docs/problem-definition`. Do not commit or push directly to `main`.

## Implement and check your changes

- Keep each pull request focused on one task.
- Follow the project's existing conventions and update relevant documentation.
- For algorithms, document assumptions, constraints, and time and space complexity. Distinguish proven guarantees from heuristic behavior.
- Use shared datasets and metrics when comparing algorithms. Record random seeds for randomized experiments.
- Include appropriate tests for implemented behavior, including edge cases and invalid inputs.
- Do not commit credentials, local environments, dependencies, or large generated outputs.

The repository currently has no runnable application, dependency setup, or test suite. Until these are added, describe the checks you actually performed. Do not report tests as passing when they do not exist. Contributions that introduce runnable code should document dependencies and exact run/test commands.

## Open a pull request

Stage only the files relevant to your task, then commit and push your branch:

```bash
git add <changed-file-paths>
git commit -m "docs: describe contribution workflow"
git push -u origin HEAD
```

On GitHub, open a pull request targeting `main` and fill in the template. Link the issue with `Closes #123` when the PR fully resolves it. Use a draft PR for work that is not ready for review.

## Review and merge

The two designated repository administrators coordinate review and merge. Request review from an administrator; when an administrator authors a PR, the other administrator reviews it. Authors must not approve their own work.

Reviewers check correctness, scope, readability, documentation, and validation evidence. Address feedback and resolve discussions before merging. Obtain at least one administrator's approval of the current changes; request another review after substantial updates.

Only the designated administrators should merge into `main`. This is the team's workflow policy; enforcing it requires GitHub repository settings. Documenting it here does not automatically configure permissions or branch protection.

After merging, delete the merged branch on GitHub and update your local `main` before starting another task.
