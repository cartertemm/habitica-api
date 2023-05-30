import json
from typing import Optional
from dataclasses import dataclass

from habitica.utils import get_value_description


class Jsonable:
	def to_json(self, use_dict={}, include_dunders=True, **json_kwargs):
		# use_dict in case you want to overwrite the below logic, or exclude uninitialized values or whatever
		use_dict = use_dict or self.__dict__
		if not json_kwargs:
			json_kwargs = {"indent": "\t"}
		res = {}
		for k, v in use_dict.items():
			if k.startswith("_") and not include_dunders:
				continue
			try:
				json.dumps({k: v})
				res[k] = v
			except (TypeError, OverflowError):
				print(f'Error: The key-value pair "{k}: {v}" is not JSON serializable')
				continue
		return json.dumps(res, **json_kwargs)


@dataclass
class Task(Jsonable):
	_id: Optional[str]
	userId: str
	text: str
	alias: Optional[str]
	type: str
	byHabitica: Optional[bool]
	notes: str
	tags: Optional[list]
	checklist: Optional[list]
	collapseChecklist: Optional[bool]
	value: Optional[float]
	priority: Optional[float]
	frequency: Optional[str]
	attribute: Optional[str]
	challenge: Optional[dict]
	group: Optional[dict]
	reminders: Optional[list]
	createdAt: str
	updatedAt: str
	history: Optional[list]
	down: Optional[bool]
	up: Optional[bool]
	isDue: Optional[bool]
	id: Optional[str]
	completed: Optional[bool]
	streak: Optional[int]
	repeat: Optional[dict]

	def __str__(self):
		value_description = get_value_description(self.value)
		if self.type == "habit":
			return f"{self.text}, value: {value_description}"
		elif self.type == "todo":
			complete = "complete" if self.completed else "incomplete"
			return f"{complete}, {self.text}, value: {value_description}"
		elif self.type == "daily":
			due = "due" if not self.completed else "completed"
			return f"{due}, {self.text}, value: {value_description}"
		return self.text


@dataclass
class Buffs(Jsonable):
	str: int
	int: int
	per: int
	con: int
	stealth: int
	streaks: bool
	snowball: bool
	spookySparkles: bool
	shinySeed: bool
	seafoam: bool


@dataclass
class Training(Jsonable):
	str: int
	int: int
	per: int
	con: int


@dataclass
class ClassBonuses(Jsonable):
	str: int
	int: int
	per: int
	con: int
	total: int


@dataclass
class Stats(Jsonable):
	hp: float
	mp: float
	exp: float
	gp: float
	lvl: int
	class_: Optional[str]
	points: int
	str: int
	con: int
	int: int
	per: int
	toNextLevel: Optional[int]
	maxHealth: Optional[int]
	maxMP: Optional[int]
	buffs: Buffs
	training: Training
	classBonus: Optional[ClassBonuses]


@dataclass
class User(Jsonable):
	auth: dict
	achievements: dict
	backer: dict
	contributor: dict
	permissions: dict
	purchased: dict
	flags: dict
	history: dict
	items: dict
	invitations: dict
	party: dict
	preferences: dict
	profile: dict
	stats: Stats
	inbox: dict
	tasksOrder: dict
	_v: int
	balance: int
	_subSignature: str
	challenges: list
	guilds: list
	loginIncentives: int
	invitesSent: int
	pinnedItemsOrder: list
	_id = str
	lastCron: str
	newMessages: dict
	notifications: list
	tags: list
	extra: dict
	pushDevices: list
	webhooks: list
	pinnedItems: list
	unpinnedItems: list
	id: str
	needsCron: bool

	def diff_stats(self, other_stats):
		"""Compare the stats of this user with another.
		This could be used to i.e. calculate what has changed after scoring a habit.

		args:
				other_stats (habitica.api.Stats): The basis for comparison (assumed to be newer)

		returns:
				str: A formatted explanation of what changed.
		"""
		final = []
		stats = ["hp", "mp", "exp", "points"]
		lvl = other_stats.lvl - self.stats.lvl
		if lvl > 0:
			final.append(f"level increased by {lvl}")
			stats.remove("exp")
		for stat in stats:
			value = getattr(other_stats, stat) - getattr(self.stats, stat)
			if value > 0:
				final.append(f"{stat} increased by {value}")
			elif value < 0:
				final.append(f"{stat} decreased by {value}")
		return ", ".join(final)
