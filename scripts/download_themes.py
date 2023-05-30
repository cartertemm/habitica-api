from habitica import themes_manager


def menu(prompt, items):
	"""Constructs and shows a simple commandline menu.
	Returns the user input."""
	for i in range(len(items)):
		print(str(i+1) + ": " + items[i])
	result = None
	while True:
		result = input(prompt)
		if result and result.isdigit():
			result = int(result)
			break
	if result == 0:
		return
	return result-1


def main():
	themes = [theme[0] for theme in themes_manager.themes]
	themes.append("Download All")
	choice = menu("Choose a theme to download or select 'Download All': ", themes)
	if choice is not None:
		destination = input("Enter a destination (defaults to 'sounds'): ")
		if not destination:
			destination = 'sounds'
		if themes[choice] == "Download All":
			failed_themes = themes_manager.download_all_themes(destination)
			if failed_themes:
				print("Failed to download these themes: ", failed_themes)
			else:
				print("All themes downloaded successfully!")
		else:
			theme = themes[choice]
			failed_sounds = themes_manager.download_theme(theme, destination)
			if failed_sounds:
				print("Failed to download these sounds: ", failed_sounds)
			else:
				print(f"Theme '{theme}' downloaded successfully!")

if __name__ == "__main__":
	main()
