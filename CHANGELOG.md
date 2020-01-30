# CHANGELOG

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/) and [Keep a Changelog](http://keepachangelog.com/).



## Unreleased
---

### New

### Changes
* Using an invalid index type to select a cell now raises a ValueError.

### Fixes

### Breaks


## 2.4.0 - (2020-01-29)
---

### New
* Consistent handling of files with varying row length.

### Changes
* Use Poetry for packaging.
* The `get_column()` and `update_column()` methods of TableRow have been removed as they are unnecessary. Use `row[index]` and `row[index] = value` instead.

### Fixes
* Tabler can now open `ODS` files that were created with tabler.


## 2.3.0 - (2019-07-30)
---

### New
* Python 3.5 compatibilty.

### Changes
* Replace ezodf dependency with pyexcel-ods.

### Fixes
* All files that are opened are closed again.
* Commandline output goes to STDERR, not STDOUT.
