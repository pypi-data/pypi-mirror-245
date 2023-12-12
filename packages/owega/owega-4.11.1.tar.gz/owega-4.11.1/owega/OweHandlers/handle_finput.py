import os
import time
import tempfile
import openai
import prompt_toolkit as pt
from ..config import baseConf
from ..utils import (
	clrtxt,
	estimated_tokens,
	info_print,
	play_opus,
)
from ..ask import ask
from ..OwegaFun import existingFunctions, functionlist_to_toollist
from ..OwegaSession import OwegaSession as ps


# get input from a file instead of the terminal
def handle_finput(temp_file, messages, given="", temp_is_temp=False):
	given = given.strip()
	given = given.split(' ')[0]
	if given:
		file_path = given
	else:
		file_path = ps['load'].prompt(pt.ANSI(
			clrtxt("yellow", " FILE LOCATION ") + ": ")).strip()
	if (os.path.exists(file_path)):
		user_prompt = ps['main'].prompt(pt.ANSI(
			clrtxt("yellow", " PRE-FILE PROMPT ") + ": ")).strip()
		with open(file_path, "r") as f:
			file_contents = f.read()
			full_prompt = f"{user_prompt}\n```\n{file_contents}\n```\n'"
			if baseConf.get("estimation", False):
				etkn = estimated_tokens(
					full_prompt,
					messages,
					functionlist_to_toollist(existingFunctions.getEnabled())
				)
				cost_per_token = (
					0.03
					if 'gpt-4' in baseConf.get("model", "")
					else 0.003
				) / 1000
				cost = cost_per_token * etkn
				print(f"\033[37mestimated tokens: {etkn}\033[0m")
				print(f"\033[37mestimated cost: {cost:.5f}\033[0m")
			if baseConf.get("debug", False):
				pre_time = time.time()
			messages = ask(
				prompt=full_prompt,
				messages=messages,
				model=baseConf.get("model", ""),
				temperature=baseConf.get("temperature", 0.8),
				max_tokens=baseConf.get("max_tokens", 3000),
				top_p=baseConf.get("top_p", 1.0),
				frequency_penalty=baseConf.get("frequency_penalty", 0.0),
				presence_penalty=baseConf.get("presence_penalty", 0.0)
			)
			if baseConf.get("debug", False):
				post_time = time.time()
				print(f"\033[37mrequest took {post_time-pre_time:.3f}s\033[0m")
			print()
			print(' ' + clrtxt("magenta", " Owega ") + ": ")
			print()
			print(messages.last_answer())
			if baseConf.get('tts_enabled', False):
				tmpfile = tempfile.NamedTemporaryFile(
					prefix="owegatts.",
					suffix=".opus",
					delete=False
				)
				tmpfile.close()
				tts_answer = openai.audio.speech.create(
					model='tts-1',
					voice='nova',
					input=messages.last_answer()
				)
				if baseConf.get("debug", False):
					posttts_time = time.time()
					print(f"\033[37mrequest took {posttts_time-pre_time:.3f}s\033[0m")
				tts_answer.stream_to_file(tmpfile.name)
				play_opus(tmpfile.name)
				os.remove(tmpfile.name)
	else:
		info_print(f"Can't access {file_path}")
	return messages


item_finput = {
	"fun": handle_finput,
	"help": "sends a prompt and a file from the system",
	"commands": ["file_input"],
}
