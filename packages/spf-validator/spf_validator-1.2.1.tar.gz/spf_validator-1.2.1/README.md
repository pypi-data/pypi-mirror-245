# spf-validator

spf-validator is a Python package for validating Sender Policy Framework strings and records to ensure they are formatted correctly.

The validation returns a list of strings where each string, if any, is an issue with the SPF record.

## Installation

Use pip to install:

```python
pip install spf-validator
```

## Usage

There are two main functions in the package: `validate_spf_string` and `validate_domain_spf`. Both of these will return a list of strings where each string, if any, is an issue with the SPF record.

To validate an SPF string, use `validate_spf_string` by passing it the string.

To use:

```python
from spf_validator import validator

issues_list = validator.validate_spf_string('v=spf1 a mx include:_spf.google.com ~all')
```

To validate an SPF record on a given domain, use `validate_domain_spf` by passing it the domain. This will retrieve the TXT records for the domain, locate the SPF record, and validate it.

To use:

```python
from spf_validator import validator

issues_list = validator.validate_domain_spf('google.com')
```

## Contributing

Community made feature requests, patches, bug reports, and contributions are always welcome.

When contributing please ensure you follow the guidelines below so that we can keep on top of things.

### Creating Issues

* If you have any bugs or feature requests for the plugin itself, please [create an issue](https://github.com/fpcorso/spf-validator/issues/new)
* For bug reports, please clearly describe the bug/issue and include steps on how to reproduce it
* For feature requests, please clearly describe what you would like and how it would be used

### Pull Requests

* Ensure you stick to the [PEP 8](https://peps.python.org/pep-0008/).
* When committing, reference your issue (if present) and include a note about the fix.

## License

This project is licensed under the MIT License. See [LICENSE](https://github.com/fpcorso/spf-validator/blob/main/LICENSE) for more details.