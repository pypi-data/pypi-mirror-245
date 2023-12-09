# check-keepass-passwords

`check-keepass-passwords` is a command-line tool that scans Keepass 2.x databases for weak or compromised passwords.

## Quick Navigation

- [Installation](#installation)
- [Usage](#usage)
- [Background](#background)
- [License](#license)

## Installation

Requires Python version 3.9 or higher and pip.

```bash
pip install check-keepass-passwords
```

## Usage

```bash
check-keepass-passwords /path/to/database.kdbx
```

## Background

- The compromise check is powered by [https://github.com/lionheart/pwnedpasswords](pwnedpasswords). For implementation
  details and security notes, refer to their repository.
- Password scoring is powered by [zxcvbn](https://github.com/dwolfhub/zxcvbn-python), which rates passwords on a scale
  from 0 to 4. By default, `check-keepass-passwords` considers a score of 2 to be sufficiently safe. You can customize
  this threshold using the `--min-score` parameter.

## License

`check-keepass-passwords` is distributed under the terms of the MIT License.
