# F3 Wikidata Bot

f3wikidatabot is a python module and command-line tool for the [wikidata Forges project](https://www.wikidata.org/wiki/Wikidata:WikiProject_Informatics/Forges).

## Setup

```sh
git clone --recursive https://lab.forgefriends.org/friendlyforgeformat/f3-wikidata-bot.git
cd f3-wikidata-bot
echo layout python3 > .envrc
direnv allow
pip install poetry
poetry install
```

## Usage

From the source tree:

```sh
PYTHONPATH=$(pwd) python bin/f3wikidatabot  --help
```

Using the module [from PyPI](https://pypi.org/project/f3wikidatabot/):

```python
from f3wikidatabot import bot

b = bot.Bot.factory(["--verbose", "--show", "--plugin", "Features"])

for forge in b.run_query():
    print(forge)
```

## Publish

```sh
$ poetry config pypi-token.pypi {pypi token}
$ poetry version patch
$ poetry build
$ poetry publish
```

## License

This project is licensed under the GPLv3+ License.

## Funding

This project is funded through the [NGI Assure Fund](https://nlnet.nl/assure), a fund established by [NLnet](https://nlnet.nl) with financial support from the European Commission's [Next Generation Internet](https://ngi.eu) program. Learn more on the [NLnet project page](https://nlnet.nl/project/F3-FriendlyForgeFormat).

[<img src="https://nlnet.nl/logo/banner.png" alt="NLnet foundation logo" width="20%" />](https://nlnet.nl)
[<img src="https://nlnet.nl/image/logos/NGIAssure_tag.svg" alt="NGI Assure Logo" width="20%" />](https://nlnet.nl/assure)
