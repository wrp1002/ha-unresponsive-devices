from datetime import datetime
from dateutil.tz import tzlocal
from dateutil import parser

from ha_api import HAAPI

HA_URL = ""
API_KEY = ""
UNRESPONSIVE_DAY_THRESHOLD = 2


def main():
	now = datetime.now(tz=tzlocal())
	ha_api = HAAPI(HA_URL, API_KEY)

	if not ha_api.test():
		return

	device_info = ha_api.get_all_devices_and_entities()

	for device_name, entity_ids in device_info.items():
		#print(device_name)
		unresponsive = True
		unresponsive_days = 0
		entity_info = []

		for entity_id in entity_ids:
			entity = ha_api.get_entity_status(entity_id)
			entity_info.append(entity)

			id = entity.get("entity_id")
			friendly_name = entity.get("attributes", {}).get("friendly_name")
			state = entity.get("state")

			last_updated = entity.get("last_updated")
			last_reported = entity.get("last_reported")
			last_changed = entity.get("last_changed")

			last_updated_dt = parser.parse(last_updated)
			last_reported_dt = parser.parse(last_reported)
			last_changed_dt = parser.parse(last_changed)

			last_updated_days = (now - last_updated_dt).days
			last_reported_days = (now - last_reported_dt).days
			last_changed_days = (now - last_changed_dt).days

			#print(entity)
			#print(f"{friendly_name} ({id}) - {last_updated}    -    {last_updated_days} {last_reported_days} {last_changed_days}")
			if last_updated_days < unresponsive_days or unresponsive_days == 0:
				unresponsive_days = last_updated_days

			if not (state == "unavailable" and last_updated_days > UNRESPONSIVE_DAY_THRESHOLD):
				unresponsive = False


		if unresponsive:
			print(f"{device_name} has been unresponsive for {unresponsive_days} days")


	print("Done")







if __name__ == "__main__":
	main()