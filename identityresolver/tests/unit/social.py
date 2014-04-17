import unittest, os
from ...social import SocialProfileResolver,ResolvedPerson

# from mock import patch 
# @mock.patch('requests.get', mock.Mock(side_effect = lambda k:{'aurl': 'a response', 'burl' : 'b response'}.get(k, 'unhandled request %s'%k) ))

class TestTwitterScraper(unittest.TestCase):

	def setUp(self):

		self.resolver = SocialProfileResolver()

	def test_from_csv_1(self):
		test_set = [ResolvedPerson(0,full_name = 'Moritz Gellner', age = '22'),
					ResolvedPerson(1,full_name = 'Al Johri', age = '21'),
					ResolvedPerson(2,full_name = 'Carson H. Potter', age = '23')]

		resolved_people = self.resolver._load_from_csv(os.getcwd() + '/identityresolver/tests/unit/test_identities_1.csv', age=1)
		self.assertEqual(test_set,resolved_people)

	# def test_from_csv_2(self):
	# 	self.resolver.resolve_from_csv()

if __name__ == "__main__":
	unittest.main()