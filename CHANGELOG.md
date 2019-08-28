# CHANGELOG

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/) and [Keep a Changelog](http://keepachangelog.com/).


## Unreleased
---

### New
* Open CSV files with rows of varying length.

### Changes
* Empty values in CSV files are now represented as `None`. Empty strings are still written to CSV files. Ensure all checks for `''` are changed to checks for `None`.

### Fixes

### Breaks

## 2.3.0 - (2019-07-30)
---

### New
* Python 3.5 compatibilty.

### Changes
* Replace ezodf dependency with pyexcel-ods.

### Fixes
* All files that are opened are closed again.
* Commandline output goes to STDERR, not STDOUT.
