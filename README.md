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

## Telegram bot

1. Create a telegram bot: [Telegram bot guide](https://core.telegram.org/bots#3-how-do-i-create-a-bot)
2. Get your *Webhook* code
3. Get your user ID: write to telegram bot *@myidbot* `/getid`
4. Start bot communication with sending `/start` to your bot

## Contribute

Feel free to fork, edit or request pulls.

## Credits

This script has been created mainly for the awesome [Dennsen86](https://www.twitch.tv/dennsen86) community!

*wirehack7 = wepeelis*