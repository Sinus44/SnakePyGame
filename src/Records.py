class Records:
	records = None
	file_path = "../data/records"

	def load():
		with open(Records.file_path) as file:
			raw = file.read()

		records = [record for record in raw.split("\n") if record]
			
		Records.records = {}

		for record in records:
			if len(player := record.split(":")) != 2 or not player[0] or not player[1]:
				continue

			Records.set(player[0], player[1])

		return Records.records

	def get(): return Records.records if Records.records else {}

	def set(name, score):
		if not name:
			return False
		
		if not Records.records:
			 Records.records = {}

		Records.records[name] = max(Records.records.get(name) or 0, int(score or 0))

	def save():
		if not Records.records:
			return

		with open(Records.file_path, "w") as file:
			file.write("\n".join(f"{name}: {Records.records[name]}" for name in Records.records))
