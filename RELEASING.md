# RELEASING

Check list for new releases

## Add Changes to CHANGELOG.md

- Add any missing changes to the "UNRELEASED" section of `CHANGELOG.md`
  - `poetry run changelog (new|change|fix|breaks) "<message>"`
- Check the current project version in `CHANGELOG.md` and `python`, making sure they match
  - `poetry run changelog current`
  - `poetry run python -c "import tabler; print(tabler.__version__)"`
- Check suggested version bump type
  - `poetry run changelog suggest`
- Add the new version to `CHANGELOG.md`
  - `poetry run changelog release (--patch|--minor|--major)`

## Update Documentation

- Update the documentation files
  - `make docs`

## Check Dependencies

- Refresh development environment
  - `poetry env remove python`
  - `poetry install`
- Update `poetry.lock` and `requirements.txt`
  - `poetry lock`
  - `poetry run pip freeze > requirements.txt`
- Run tests
  - `poetry run pytest`

## Create Release Commit

- Create a release branch
  - `git checkout main`
  - `git checkout -b <new version number>`
- Create release commit
  - `poetry run bumpversion (patch|minor|major)`
- Update the `stable` branch to the new commit
- Merge the new branch into `main`

## Checks

- Check CI has passed
  - <https://travis-ci.org/lukeshiner/tabler>
- Check documentation
- Check version number is correct in:
  - `pyproject.toml`
  - `tabler/__version__.py`
  - `docs/source/conf.py`
  - `.bumpversion.cfg`

## Create Release

- Test PyPi release
  - `make publish-test`
- Create release on github.
  - <https://github.com/lukeshiner/tabler/releases>
  - Use change list from `CHANGELOG.md`
- Create PyPi release
  - `make publish`
