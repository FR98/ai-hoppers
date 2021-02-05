"""
---------------------------------------------------------------------------------------------------
	Author
	    Francisco Rosal 18676
---------------------------------------------------------------------------------------------------
"""

from math import sqrt

class Player(object):

	def __init__(self, value, is_ai=False):
		self.value = value
		self.is_ai = is_ai
