from habitica.constants import *


def get_consecutive_clicks(values):
	return consecutive_clicks[_get_n(value)]


def get_value_description(value):
	return values[_get_n(value)]


def _get_n(value):
	if value > 10:
		n = 6
	elif value > 5:
		n = 5
	elif value > 1:
		n = 4
	elif value > -1:
		n = 3
	elif value > -10:
		n = 4
	elif value > -20:
		n = 5
	else:
		n = 6
	return n
