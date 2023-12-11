# ADCM version

## Name
ADCM version

## Description
This package is intended to compare versions of the [ADCM](https://docs.arenadata.io/en/ADCM/current/introduction/intro.html) product.

## Installation
`pip install adcm-version`

## Usage
* `compare_adcm_versions(version_a, version_b)` - Compare two ADCM version strings, return 1 (if `a` is newer), 0 (if versions are equal), or -1 (if `b` is newer)

  ```jupyterpython
  >>> from adcm_version import compare_adcm_versions
  >>> compare_adcm_versions("2021.11.22.15", "2023.11.28.07")
  -1
  ```

* `compare_prototype_versions(version_a, version_b)` - Compare two prototype version strings for ADCM objects, return 1 (if `a` is newer), 0 (if versions are equal), or -1 (if `b` is newer)

  ```jupyterpython
  >>> from adcm_version import compare_prototype_versions
  >>> compare_prototype_versions("2.1.10_b1", "2.1.6_b4")
  1
  ```

* `is_legacy(version)` - return `True`, if ADCM version format is old (for example `2023.11.28.07`), else `False`

  ```jupyterpython
  >>> from adcm_version import is_legacy
  >>> is_legacy("2021.11.22.15")
  True
  ```
