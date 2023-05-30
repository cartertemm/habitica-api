import os
import requests
from habitica.constants import *
from concurrent.futures import ThreadPoolExecutor


def get_slug(theme_or_slug):
	for name, slug in themes:
		if name == theme_or_slug or slug == theme_or_slug:
			return slug
	return None


def get_sound(sound_name):
	for sound in sound_list:
		if sound_name == sound:
			return sound
		lower = sound.lower()
		if sound_name.lower() == lower or lower.replace("_", "") == sound_name.replace("_", "").lower():
			return sound


def join_sound_url(slug, sound):
	return f"{base_audio_url}{slug}/{sound}.ogg"


def get_sound_urls(name_or_slug):
	slug = get_slug(name_or_slug)
	if not slug:
		return {}
	urls = {}
	for sound in sound_list:
		url = join_sound_url(slug, sound)
		urls[sound] = url
	return urls


def download_theme(name_or_slug, destination, force_create=True):
	slug = get_slug(name_or_slug)
	if not slug:
		print(f"No sounds found for theme {name_or_slug}")
		return
	if not os.path.isdir(destination) and not force_create:
		return False
	print(f"downloading {slug}")
	urls = get_sound_urls(name_or_slug)
	failed = []
	for sound, url in urls.items():
		if sound == "name" or sound == "slug":
			continue
		filename = f"{sound}.ogg"
		dirpath = f"{destination}/{slug}"
		filepath = f"{dirpath}/{filename}"
		print(f"{filename}")
		response = requests.get(url)
		if response.status_code != 200 or not response.text.startswith("OggS"):
			failed.append(sound)
			print(f"error downloading file ({response.status_code}, {response.reason})")
			continue
		if not os.path.isdir(dirpath) and force_create:
			os.makedirs(dirpath)
		with open(filepath, "wb") as f:
			f.write(response.content)
	if len(failed) > 0:
		return failed
	return True


def download_all_themes(destination, force_create=True):
	failed = {}
	for _, theme in themes:
		failed_sounds = download_theme(theme, destination, force_create=force_create)
		if isinstance(failed_sounds, list) and len(failed_sounds) > 0:
			for sound in failed_sounds:
				if not theme in failed:
					failed[theme] = []
				failed[theme].append(sound)
	if len(failed) > 0:
		return failed
	return True
