# Changelog

## [1.3.1 - 2023-11-29](https://gitlab.com/fame-framework/fame-protobuf/-/tags/v1.3.1)
### Changed
- Loosen maximum supported Python version #33 (@dlr-cjs @dlr_fn)

## [1.3.0 - 2023-11-22](https://gitlab.com/fame-framework/fame-protobuf/-/tags/v1.3.0)
### Changed 
- Switch to pyproject.toml to replace setup.py #32 (@dlr-cjs)
- Reformat Changelog to follow style guide #29 (@dlr-cjs)
- Update to latest protobuf version 24 #31 (@dlr-cjs)
- Update README.md #32 (@dlr-cjs, @dlr_fn)

### Added
- Provide Python interface files (#30 @dlr-cjs)

## [1.2.1 - 2023-05-03](https://gitlab.com/fame-framework/fame-protobuf/-/tags/v1.2.1)
### Changed
- Remove `ProgramParam` from InputData - regarded as non-breaking as it was not used so far

### Added
- Store a schema in InputData
- Add optional MetaData field to AgentDao 
- Add optional MetaData field to ProtoContract 
- Update to latest protobuf version 22

## [1.2 - 2022-07-08](https://gitlab.com/fame-framework/fame-protobuf/-/tags/v1.2)
### Changed
- Output messages may now contain multiple key-value mappings per column
- Update to latest protobuf version 21

## [1.1.5 - 2021-06-10](https://gitlab.com/fame-framework/fame-protobuf/-/tags/v1.1.5)
### Changed
- Extract version number from `pom.xml` in setup.py
- Ensure that files are compiled before committing to PyPI

## [1.1.4 - 2021-0607](https://gitlab.com/fame-framework/fame-protobuf/-/tags/v1.1.4)
### Added
- Add missing setup.yaml parameters
- Add long values for Fields

### Changed
- Make long, int, and string repeatable for Fields

### Removed
- Remove default values of Fields

## 1.1.3 - Retracted

## [1.1.2 - 2021-0311](https://gitlab.com/fame-framework/fame-protobuf/-/tags/v1.1.2)
### Changed
- Update Contracts to feature recursive fields

## [1.1.1 - 2021-02-19](https://gitlab.com/fame-framework/fame-protobuf/-/tags/v1.1.1)
### Changed
- Restructure Inputs to allow nested Fields  

## [1.1.0 - 2021-02-11](https://gitlab.com/fame-framework/fame-protobuf/-/tags/v1.1.0)
### Changed
- Automate packaging to PyPI

## [1.0 - 2021-02-09](https://gitlab.com/fame-framework/fame-protobuf/-/tags/v1.0)
_Initial release._