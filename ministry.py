import os
import json

DB_DIR = "ministry"
REPLACEMENTS = {
	" (original mix)": "",
	" - ": " / ",
	"-" : " / ",
	" / ": "/"
}

def parse_cd(filename, replacements={}):
	"""
	Takes the path to a FreeDB CD file and parses all key/value pairs
	into a dictionary.
	"""
	lines = {}
	with open(filename, "r") as f:
		for line in f.readlines():
			# Remove newline chars
			line = line.rstrip()
			# Ignore any comments or lines without an equals in
			if "=" not in line or line.startswith("#"):
				continue

			# Extract the keys and values, forcing the values to be lower case
			eq_index = line.index("=")
			key = line[:eq_index]
			value = line[eq_index+1:].lower()

			# Take a dictionary of strings to search and replace eg.
			# {" (original mix)": "", " - ": " / "}
			for old, new in replacements.items():
				value = value.replace(old, new)

			# Check for the existence of a partial line in the dictionary first
			# and then append the rest of the value if it exists.
			if key in lines:
				lines[key] += value
			else:
				lines[key] = value
	return lines



if __name__ == "__main__":
	tracks_count = {}

	for filename in os.listdir(DB_DIR):
		# Parse the CD
		cd = parse_cd(os.path.join(DB_DIR, filename), REPLACEMENTS)
		# Extract the tracks
		tracks = [cd[x] for x in cd.keys() if x.startswith("TTITLE")]

		for track in tracks:
			# If the track has appeared already, increment its counter
			# otherwise add it and start it off at 1.
			if track in tracks_count:
				tracks_count[track] += 1
			else:
				tracks_count[track] = 1

	# Finally, sort the tracks_count dictionary by amount of appearances
	for track_count in sorted(tracks_count.items(), key=lambda x: x[1]):
		print "%s: %s" % track_count