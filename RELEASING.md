# RELEASING
Check list for new releases

## Add Changes to CHANGELOG.md
- Add any missing changes to the "UNRELEASED" section of `CHANGELOG.md`
  - `pipenv run changelog (new|change|fix|breaks) "<message>"`
- Check the current project version in `CHANGELOG.md` and `python`, making sure they match
  - `pipenv run changelog current`
  - `pipenv run python -c "import tabler; print(tabler.__version__)"`
- Check suggested version bump type
  - `pipenv run changelog suggest`
- Add the new version to `CHANGELOG.md`
 - `pipenv run changelog release (--patch|--minor|--major)`

## Update Documentation
- Update the documentation files
  - `make docs`

## Check Dependencies

- Refresh development environment
  - `pipenv rm`
  - `make init`
- Update `Pipfile.lock` and `requirements.txt`
 - `make lock`
- Install development dependencies
  - `pipenv sync -d`
- Run tests
  - `make test`

## Create Release Commit
- Create a release branch
  - `git checkout master`
  - `git checkout -b <new version number>`
- Create release commit
  - `pipenv run bumpversion (patch|minor|major)`
- Update the `stable` branch to the new commit
- Merge the new branch into `master`

## Checks
- Check CI has passed
  - https://travis-ci.org/lukeshiner/tabler
- Check documentation
- Check version number is correct in:
 - `tabler/__version__.py`
 - `docs/source/conf.py`
 - `.bumpversion.cfg`

## Create Release
- Test PyPi release
  - `make publish-test`
- Create release on github.
  - https://github.com/lukeshiner/tabler/releases
  - Use change list from `CHANGELOG.md`
- Create PyPi release
  - `make publish`
