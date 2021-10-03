# rtl433_to_mqtt

Convert information from `rtl_433` script (in JSON) to MQTT.

## Use fake data to test

Use the `-f` option.


## Deploy on `majordome`

Install this package:

```shell
python3 -m venv ~/rtl433_to_mqtt
source ~/rtl433_to_mqtt/bin/activate
pip install git+http://majordome:8050/jonathan/rtl433_to_mqtt.git
mkdir /home/majordome/rtl433_to_mqtt/log
```

We use `supervisor` to handle this script.

```shell
curl http://majordome:8050/jonathan/rtl433_to_mqtt/-/raw/main/supervisor.conf | sudo tee /etc/supervisor/conf.d/rtl433_to_mqtt.conf
sudo supervisorctl reread
sudo supervisorctl update
```

## Upate on `majordome`

```shell
source ~/rtl433_to_mqtt/bin/activate
pip install -U git+http://majordome:8050/jonathan/rtl433_to_mqtt.git
sudo supervisorctl restart rtl433_to_mqtt
```
