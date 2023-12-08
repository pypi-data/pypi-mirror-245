import os
import tempfile
import sys
import json5 as json


# get a temp file location
def get_temp_file() -> str:
	tmp = tempfile.NamedTemporaryFile(
		prefix="owega_temp.",
		suffix=".json",
		delete=False
	)
	filename = tmp.name
	tmp.close()
	return filename


# gets the user home directory, cross platform
def get_home_dir() -> str:
	return os.path.expanduser('~')


# returns the ANSI escape sequence for the given color
def clr(color: str) -> str:
	esc = '\033['
	colors = {
		"red": f"{esc}91m",
		"green": f"{esc}92m",
		"yellow": f"{esc}93m",
		"blue": f"{esc}94m",
		"magenta": f"{esc}95m",
		"cyan": f"{esc}96m",
		"white": f"{esc}97m",
		"reset": f"{esc}0m",
	}
	return colors[color]


# prints text in color between square brackets
def clrtxt(color: str, text: str) -> str:
	return "[" + clr(color) + text + clr("reset") + "]"


# prints text if debug is enabled
def debug_print(text: str, debug: bool = False) -> None:
	if debug:
		print(clrtxt("magenta", "  DEBUG ") + ": " + text)


# standard success message
def success_msg():
	return clrtxt("cyan", "  INFO  ") + ": Owega exited successfully!"


# clear the terminal screen, depends on system (unix or windows-based)
def clearScreen():
	if os.name == 'nt':
		os.system('cls')
	else:
		print("\033[2J\033[0;0f", end="")


# quits and delete the given file if exists
def do_quit(msg="", value=0, temp_file="", is_temp=False, should_del=False):
	if (temp_file):
		if should_del:
			try:
				os.remove(temp_file)
			except Exception:
				pass
		else:
			if is_temp:
				try:
					with open(temp_file, 'r') as f:
						contents = json.loads(f.read())
						if not (
							(len(contents.get("messages", [])) > 0)
							or (len(contents.get("souvenirs", [])) > 0)
						):
							os.remove(temp_file)
				except Exception:
					pass
	if (msg):
		print()
		print(msg)
	sys.exit(value)


# prints an info message
def info_print(msg):
	print(clrtxt("cyan", "  INFO  ") + ": ", end='')
	print(msg)


# prints a command message
def command_text(msg):
	return clrtxt("red", "COMMAND ") + ": " + msg


# prints the command help
def print_help(commands_help={}):
	commands = list(commands_help.keys())
	longest = 0
	for command in commands:
		if len(command) > longest:
			longest = len(command)
	longest += 1
	print()
	info_print("Enter your question after the user prompt, and it will be answered by OpenAI")
	info_print("other commands are:")
	for cmd, hstr in commands_help.items():
		command = '/' + cmd
		info_print(f"   {command:>{longest}}  - {hstr}")
	print()
