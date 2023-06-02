import requests
from urllib.parse import urlencode, urljoin
from dacite import from_dict

from habitica.constants import *
from habitica.models import *


class HabiticaException(Exception):
	pass


class HabiticaAPI:
	def __init__(self, api_user=None, api_key=None):
		if not api_user or not api_key:
			raise HabiticaException("Both an API user and key are required")
		self.api_user = api_user
		self.api_key = api_key
		self.api_client = self.api_user + " - python API client"
		self.session = None
		self._cached_user = None

	def login(self, username, password):
		data = {"username": username, "password": password}
		response = self._api_request("post", "user/auth/local/login", json=data)
		return response

	def register_user(self, username, email, password, confirm_password):
		data = {
			"username": username,
			"email": email,
			"password": password,
			"confirmPassword": confirm_password,
		}
		response = self._api_request("post", "user/auth/local/register", json=data)
		return response

	def reset_password(self, email):
		data = {"email": email}
		response = self._api_request("post", "user/reset-password", json=data)
		return response

	def content(self):
		return api_request("get", "content")

	def get_user(self):
		response = self._api_request("get", "user")
		data = response["data"]
		# the class field conflicts with the python keyword
		if "class" in data.get("stats", {}):
			data["stats"]["class_"] = data["stats"]["class"]
			del data["stats"]["class"]
		user = from_dict(User, data)
		self._cached_user = user
		return user

	def get_task(self, task_id):
		response = self._api_request("get", f"tasks/:{task_id}")
		return from_dict(Task, response["data"])

	def get_tasks_for_user(self, task_type=None):
		if task_type and task_type not in self.valid_task_types:
			raise ValueError(
				f"Invalid task type {task_type}. Valid task types are: {', '.join(self.valid_task_types)}"
			)
		params = {"type": task_type} if task_type else {}
		response = self._api_request("get", "tasks/user", params=params)
		old_data = response["data"]
		response["data"] = []
		for item in old_data:
			response["data"].append(from_dict(Task, item))
		return response

	def create_task(self, type, text, **kwargs):
		if type not in create_task_types:
			raise ValueError(
				f"Invalid task type {task_type}. Valid task types are: {', '.join(self.create_task_types)}"
			)
		data = {"type": type, "text": text, **kwargs}
		return self._api_request("post", "tasks/user", json=data)

	def delete_task(self, task_id):
		path = f"tasks/{task_id}"
		return self._api_request("delete", path)

	def update_task(self, task_id, **kwargs):
		path = f"tasks/{task_id}"
		return self._api_request("put", path, json=kwargs)

	def data_export_json(self):
		return self._api_request("get", "export/userdata.json", private_api=True)

	def data_export_xml(self):
		"""This XML export feature is not currently working"""
		return self._api_request("get", "export/userdata.xml", private_api=True)

	def export_inbox_html(self):
		return self._api_request("get", "export/inbox.html", private_api=True)

	def export_tasks_csv(self):
		"""History is only available for habits and dailies so todos and rewards won't be included."""
		return self._api_request("get", "export/history.csv", private_api=True)

	def move_task(self, task_id, position):
		path = f"tasks/{task_id}/move/to/{position}"
		return self._api_request("post", path)

	def score_task(self, task_id, direction):
		if direction not in ["up", "down"]:
			raise ValueError("Invalid direction. Valid directions are 'up' or 'down'.")
		path = f"tasks/{task_id}/score/{direction}"
		response = self._api_request("post", path)
		if response["success"]:
			data = response["data"]
			# the class field conflicts with the python keyword
			if "class" in data:
				data["class_"] = data["class"]
				del data["class"]
			# cache the user's stats from this response to prevent the need for another API call
			## we selectively update only these, as fields returned from a score call are incomplete
			to_cache = [
				"hp",
				"mp",
				"exp",
				"gp",
				"lvl",
				"class_",
				"points",
				"str",
				"con",
				"int",
				"per",
			]
			for stat in to_cache:
				setattr(self._cached_user.stats, stat, data[stat])
		return response

	def reset_user(self):
		return self._api_request("post", "user/reset")

	def revive_user(self):
		return self._api_request("post", "user/revive")

	def _api_request(self, method, path, private_api=False, **kwargs):
		if not self.session:
			self.session = self._create_requests_session()
		# if we're using the website-only endpoints, which are for all intents and purposes unsupported/subject to change at any time
		if private_api:
			url = urljoin(base_url, path)
		else:
			url = urljoin(self.api_url, path)
		r = self.session.request(method, url, **kwargs)
		r.raise_for_status()
		return r.json()

	def _create_requests_session(self):
		session = requests.session()
		session.headers["Content-Type"] = "application/json"
		session.headers["x-api-user"] = self.api_user
		session.headers["x-api-key"] = self.api_key
		session.headers["x-client"] = self.api_client
		return session

	@property
	def api_url(self):
		return urljoin(base_url, base_params)

	@property
	def cached_user(self):
		if self._cached_user:
			return self._cached_user
		return self.get_user()
