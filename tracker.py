#!/usr/bin/env python3
from datetime import datetime

STARTING = 0
EXITING = 1

def main():
	try:
		from settings import controller_ui_path, game_ids
	except ImportError:
		print("settings.py not found. Follow the readme and try again")
		return

	controller_ui = None
	with open(controller_ui_path, 'r') as f:
		controller_ui = f.readlines()

	# [2021-10-07 05:27:03] Starting app 438100
	parsed_lines = []
	pos = 0
	for line_pos, line in enumerate(controller_ui):
		if 'Starting' in line:
			dt, game_id = line[1:-1].split('] Starting app ')
			action = STARTING
		elif 'Exiting' in line:
			dt, game_id = line[1:-1].split('] Exiting app ')
			action = EXITING
		else:
			continue
		dt = datetime.fromisoformat(dt)
		game_id = int(game_id)
		parsed_lines.append((line_pos, pos, dt, game_id, action))
		pos += 1

	for game_id in game_ids:
		for line_pos, pos, dt, game_id, action in parsed_lines:
			if game_id not in game_ids:
				continue
			if action == STARTING:
				for i in range(pos, len(parsed_lines)):
					current_line_pos, current_pos, current_dt, _, current_action = parsed_lines[i]
					if current_action == EXITING:
						print(f"Found match on lines {line_pos + 1} through {current_line_pos + 1}")
						print("Elapsed time:", current_dt - dt)
						print()
						break
			

if __name__ == "__main__":
	main()