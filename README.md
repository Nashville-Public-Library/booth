# booth

![tests](https://github.com/Nashville-Public-Library/booth/actions/workflows/main.yml/badge.svg)
[![GitHub issues](https://img.shields.io/github/issues/Nashville-Public-Library/booth.png)](https://github.com/Nashville-Public-Library/booth/issues)
[![last-commit](https://img.shields.io/github/last-commit/Nashville-Public-Library/booth)](https://github.com/Nashville-Public-Library/booth/commits/master)


[api.nashvilletalkinglibrary.com](https://api.nashvilletalkinglibrary.com)

 a simple web app to assist with TL booth schedule, and for other purposes...

 ----

 ### .ebextensions

 It SEEMS all EC2 instances default to a different time zone (It's UTC, i think). We're able to change our instance's timezone with a `.config` file. This is the `change_timezone.config` file in the `.ebextensions` folder.

### Testing
Run `pytest` at the top level directory to run the basic tests.

### Misc

Don't forget to continually update your `requirement.txt` file as you go: 
````python
pip freeze > requirements.txt
````
