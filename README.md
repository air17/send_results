# Send results
A simple app to send emails with results to users specified in a json file.

### Install
1. Clone this repo `git clone https://github.com/air17/send_results.git` and go to it's root directory.
2. Install dependencies: `pip install -r requirements.txt`
3. Rename `.env.template` to `.env` and fill it with your data

#### Run
1. Add `results.json` to a root directory.
2. Run  `python main.py`

results.json format:
```
[
  {
    "name": str,
    "email": str,
    "result": float
  }
]
```
