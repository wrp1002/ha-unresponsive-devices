# ha-unresponsive-devices

python script that will query all Home Assistant devices and report those that are unresponsive

## Install dependencies
```
pip3 install -r requirements.txt
```

## Setup api info

in `main.py`
- set `HA_URL` to your Home Assistant URL
- set `API_KEY` to an api key you have created

## Run the script

```
python3 main.py
```