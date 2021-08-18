from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

	def test_wait_for_db_ready(self):
		"""Test waiting for db when db is available"""
		with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
			# it replaces django deflt behaviour with the mock object
			gi.return_value = True
			call_command('wait_for_db')
			self.assertEqual(gi.call_count, 1)

	# patch as a dec, and passes gi to the argument too the function
	@patch('time.sleep', return_value=True)
	def test_wait_for_db(self, ts):
		"""Test waiting for db"""
		with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
			# sideeffect
			# 5 times error, 6th time okay
			gi.side_effect = [OperationalError] * 5 + [True]
			call_command('wait_for_db')
			self.assertEqual(gi.call_count, 6)


