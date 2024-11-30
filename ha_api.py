import requests
import json


class HAAPI():
    def __init__(self, url, api_key):
        self.api_key = api_key
        self.url = url
        self.ha_headers = {
            "Authorization": f"Bearer {api_key}",
            "content-type": "application/json",
        }


    def test(self):
        try:
            res = self.ha_get("/api/")
            res.raise_for_status()
            print(f"Successfully connected to Home Assistant API\n")
            return True
        except Exception as e:
            print(f"Failed to connect to Home Assistant API: {e}")
            return False


    def ha_get(self, resource, data={}):
        return requests.get(self.url + resource, headers=self.ha_headers, json=data)


    def ha_post(self, resource, data={}):
        return requests.post(self.url + resource, headers=self.ha_headers, json=data)


    def get_entity_status(self, entity_id):
        return self.ha_get(f"/api/states/{entity_id}").json()


    def send_hoeass_tts(self, message, entity_id):
        data = {
            "entity_id": entity_id,
            "message": message,
        }
        res = self.ha_post("/api/services/tts/google_translate_say", data=data)
        return res.status_code == 200


    def is_jokepod_playing(self, entity_id):
        states = self.get_entity_status(entity_id)
        return states.get("state") == "playing"

    def get_all_entities(self):
        return self.ha_get(f"/api/states").json()


    def get_all_devices_and_entities(self):
        template = """
            {% set devices = states | map(attribute='entity_id') | map('device_id') | unique | reject('eq', None) | list %}
            {%- set ns = namespace(device_names = {}) %}
            {%- for device in devices %}
                {%- set device_name = device_attr(device, 'name') %}
                {%- set entities = device_entities(device) | list %}

                {%- if device_name and entities %}
                    {% set new_dict = {device_name: entities } %}
                    {% set ns.device_names = dict(ns.device_names, **new_dict) %}
                {%- endif %}
            {%- endfor %}
            {{ ns.device_names }}
        """
        return json.loads(self.ha_post("/api/template", data={"template": template}).text.replace("'", "\""))
