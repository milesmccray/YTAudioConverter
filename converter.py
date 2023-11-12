"""
Goals:
- Download YT Video --- DONE
- Convert YouTube link to ogg -- DONE
- Choose conversion type -- DONE
- Allow selecting of a file and converting -- DONE
- Checks if filename already exists and appends number next to it
- Storing User information -- JSON? Maybe have a setup screen
- Show YT information before downloading

-BONUS
- Setup loading bar? (on_progress function?)
- Better File path system. -- Look into tkinter filedialog/.withdraw
- Instead of user input use args? run directly from console?
ex: python3 converter.py --path --YouTube link
"""
from pydub import AudioSegment  # Used for editing audio
from pytube import YouTube      # Used for downloading YT Video
import pytube.exceptions        # Used for pytube specific exceptions
import os                       # Used for clearing terminal/removing files

SAVE_PATH = 'audio_files'
USR_CONVERT_PATH = 'convert_audio'
YT_FILE_NAME = 'yt_audio.mp4'
AUDIO_TYPES = ['.mp3', '.wav', '.ogg', '.mp4']


def youtube_download(ytv):
	"""Takes a YouTube video link and downloads it to SAVE_PATH"""
	title = ytv.title()
	usr_download = input(f'Is "{title}" the video you want to download? (Y/N)'
		  '\n>>> ')
	if usr_download.lower() == 'y':
		# noinspection PyBroadException
		try:
			audio_query = ytv.streams.get_audio_only()
			audio_query.download(SAVE_PATH, YT_FILE_NAME)
		except:
			input('Connection/Video Error...Try again')
			start_program()
		yt_choice = input(
			'\nDownload complete...Do you want to convert this right '
			'away? (Y/N): ')

		if yt_choice.lower() == 'y':
			convert_yt_file()
		elif yt_choice.lower() == 'n':
			start_program()
		else:
			input('Error in response...Returning to Menu')
			start_program()

	else:
		start_program()


def convert_yt_file():
	"""Converts the downloaded YT video to desired audio type """
	os.system('clear||cls')
	sound = AudioSegment.from_file(f'{SAVE_PATH}/{YT_FILE_NAME}')
	file_type = input(f'Enter the audio extension you want to convert to: '
					  f'{AUDIO_TYPES}'
					  '\n>>> ')
	if file_type in AUDIO_TYPES:
		sound.export(f'{SAVE_PATH}/audio{file_type}', format=f'{file_type[1:]}')
		os.remove(f'{SAVE_PATH}/{YT_FILE_NAME}')
	else:
		print('You entered an invalid extension. Did you forget a "."?...')
		input('')


def convert_usr_file():
	"""Converts an existing audio file to a desired audio type"""
	os.system('clear||cls')
	sound = None
	usr_file_name = input('NOTE: Put the audio files you want to convert in '
						  'the "convert_audio" folder in this directory'
		  '\n\n What is the name of the file you want to convert including '
						  'extension?'
		  '\n>>> ')
	try:
		sound = AudioSegment.from_file(f'{USR_CONVERT_PATH}/{usr_file_name}')
	except FileNotFoundError:
		input('File name not found...')
		start_program()
	usr_file_type = input(f'Enter the audio extension you want to convert to: '
					  f'{AUDIO_TYPES}'
					  '\n>>> ')
	if usr_file_type in AUDIO_TYPES:
		sound.export(f'{SAVE_PATH}/audio{usr_file_type}',
					 format=f'{usr_file_type[1:]}')
		usr_file_remove = input('File converted... Do you want to delete '
								'the original file? (Y/N)'
								'\n>>> ')
		if usr_file_remove.lower() == 'y':
			os.remove(f'{USR_CONVERT_PATH}/{usr_file_name}')
			input('File removed...')
			start_program()
		else:
			start_program()
	else:
		print('ERROR: Invalid extension. Did you forget a "."?')
		input('')


def start_program():
	"""Starts the program and shows menu screen"""
	os.system('clear||cls')  # clears terminal depending on OS
	choice = input("===== Welcome to Miles' Audio Converter ====="
				   '\n1) Convert from YouTube URL'
				   '\n2) Convert from Existing File'
				   '\n\n>>> ')
	if choice == '1':
		os.system('clear||cls')
		link = input('Youtube Link: ')
		try:
			youtube_video = YouTube(link)
			youtube_download(youtube_video)
		except pytube.exceptions.RegexMatchError:
			input('Enter a valid YouTube URL...')
			start_program()
	elif choice == '2':
		os.system('clear||cls')
		convert_usr_file()
	else:
		input('Enter a valid selection...')
		start_program()


start_program()
