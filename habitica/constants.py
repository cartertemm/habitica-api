base_url = "https://habitica.com"
base_audio_url = "https://habitica.com/static/audio/"
base_params = "/api/v4/"
valid_task_types = ("habits", "dailys", "todos", "rewards")
create_task_types = ("habit", "daily", "todo", "reward")
user_attributes = ("str", "int", "per", "con")
default_task_attribute = "str"

themes = (
	("Daniel the Bard", "danielTheBard"),
	("Watts' Theme", "wattsTheme"),
	("Gokul Theme", "gokulTheme"),
	("LuneFox's Theme", "luneFoxTheme"),
	("Rosstavo's Theme", "rosstavoTheme"),
	("Dewin's Theme", "dewinTheme"),
	("Airu's Theme", "airuTheme"),
	("Beatscribe's NES Theme", "beatscribeNesTheme"),
	("Arashi's Theme", "arashiTheme"),
	("Pizilden's Theme", "pizildenTheme"),
	("MAFL Theme", "maflTheme"),
	("Farvoid Theme", "farvoidTheme"),
	("SpacePenguin's Theme", "spacePenguinTheme"),
	("Lunasol Theme", "lunasolTheme"),
	("Triumph Theme", "triumphTheme"),
)

sound_list = [
	"Todo",
	"Item_Drop",
	"Plus_Habit",
	"Minus_Habit",
	"Daily",
	"Achievement_Unlocked",
	"Level_Up",
	"Reward",
	"Death",
	"Chat",
]

difficulties = {
	"Trivial": 0.1,
	"Easy": 1,
	"Medium": 1.5,
	"Hard": 2,
}

default_difficulty = 1

consecutive_clicks = (
	"12 positive",
	"6 positive",
	"1 positive",
	"0 clicks",
	"1 negative",
	"9 negative",
	"16 negative",
)

colors = (
	"Bright Blue",
	"Light Blue",
	"Green",
	"Yellow",
	"Orange",
	"Red",
	"Dark Red",
)

values = (
	"worst",
	"worse",
	"bad",
	"neutral",
	"good",
	"better",
	"best",
)

frequencies = (
	"daily",
	"weekly",
	"monthly",
	"yearly"
)

repeat_days = (
	"su",
	"m",
	"t",
	"w",
	"th",
	"f",
	"s"
)
