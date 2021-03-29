# Analogue shop alerting

This script will alert you via Telegram if an article of the Analogue shop is available.

## Usage (Linux)

Create a virtual Python environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Copy `config.ini.dst` to `config.ini`. Edit this file.

### Run it

```bash
python main.py
```

Check `alerting.log`

### Run in background

There are several ways to run a script in background on Linux. You might try these:

```bash
python main.py &
```

Or:

```bash
nohup python main.python
```

Or via *systemd* service. Or *init.d*. Or any other way you might find.

## Contribute

Feel free to fork, edit or request pulls.