# rtl433_to_mqtt

Convert information from `rtl_433` script (in JSON) to MQTT.

Requires Python >= 3.8


## Use fake data to test

Use the `-f` option.


## Create package in `majordome` GitLab PyPI repository

Build distribution

```shell
python3 -m build
```

Set `TWINE_PASSWORD` and `TWINE_USERNAME`.

Upload to GitLab PyPI repository

```shell
python3 -m twine upload --repository-url http://majordome:8050/api/v4/projects/jonathan%2Frtl433_to_mqtt/packages/pypi --verbose dist/*
```

## Installation on `majordome`

Do not use `pip` directly, even when the virtual environment is activated: it's not the right `pip`!

Install this package:

```shell
python3 -m venv ~/rtl433_to_mqtt
source ~/rtl433_to_mqtt/bin/activate
python3 -m pip install rtl433-to-mqtt --trusted-host majordome --extra-index-url "http://__token__:${GITLAB_PERSONAL_TOKEN}@majordome:8050/api/v4/projects/9/packages/pypi/simple"
mkdir /home/majordome/rtl433_to_mqtt/log
```

We use `supervisor` to handle this script.

```shell
curl http://majordome:8050/jonathan/rtl433_to_mqtt/-/raw/main/supervisor.conf | sudo tee /etc/supervisor/conf.d/rtl433_to_mqtt.conf
sudo supervisorctl reread
sudo supervisorctl update
```

## Update on `majordome`

Do not use `pip` directly, even when the virtual environment is activated: it's not the right `pip`!

```shell
source ~/rtl433_to_mqtt/bin/activate
python -m pip install -U rtl433-to-mqtt --trusted-host majordome --extra-index-url "http://__token__:${GITLAB_PERSONAL_TOKEN}@majordome:8050/api/v4/projects/9/packages/pypi/simple"
sudo supervisorctl restart rtl433_to_mqtt
```
