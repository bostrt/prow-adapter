### Clone and setup

1. Clone the repository
```
# git clone https://github.com/rvanderp3/prow-adapter
# cd prow-adapter
```
2. Setup Python 3.x virtual environment
```
# virtualenv v
# source v/bin/activate
# python --version
Python 3.7.3
```
3. Install dependencies and prepare scripts in development mode (`editable`)
```
# pip install --editable .
```
4. Make sure you can run `prowler` script:
```
# prowler
usage: prowler [-h] --url BASE_URL [--must-gather MG_ENABLE]
prowler: error: the following arguments are required: --url
```
5. Finally, make your changes and [submit a PR!](https://github.com/rvanderp3/prow-adapter/pulls)
