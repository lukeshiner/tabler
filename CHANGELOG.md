# CHANGELOG

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/) and [Keep a Changelog](http://keepachangelog.com/).



## Unreleased
---

### New

### Changes
* Add support for Python 3.12
* Drop support for Python 3.7

### Fixes

### Breaks


## 2.4.2 - (2021-12-09)
---

### Changes
* Remove support for Python 3.6


## 2.4.1 - (2021-07-05)
---

### Changes
* Raise ValueError when passing an unrecognised key to TableRow.__getitem__ or TableRow.__setitem__.
* Allow a template to be passed when creating an HTML table.
* Opening an empty file raises ValueError.
* Dropped support for Python 3.5.
* Opening empty files raises ValueError.
* Using an invalid index type to select a cell now raises a ValueError.


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
