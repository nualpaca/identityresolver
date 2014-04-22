import unittest
from ...social import SocialProfileResolver,ResolvedPerson

# from mock import patch 
# @mock.patch('requests.get', mock.Mock(side_effect = lambda k:{'aurl': 'a response', 'burl' : 'b response'}.get(k, 'unhandled request %s'%k) ))

class TestTwitterScraper(unittest.TestCase):

	def setUp(self):

		self.resolver = SocialProfileResolver()
		self.test_set = [ResolvedPerson(0,full_name = 'Rich Gordon', city='Evanston',state='IL')]
						 # ResolvedPerson(1,full_name = 'Al Johri', city='Chicago',state='IL',age = '21'),
						 # ResolvedPerson(2,full_name = 'Carson H. Potter', city='Chicago',state='IL', age = '23'),
						 # ResolvedPerson(3,full_name = 'Daniel Thirman', city='Wilmette',state='IL', age = '21')]

	def test_resolve(self):
		for person in self.resolver.resolve(self.test_set):
			print person
		self.assertEqual(True,True)

if __name__ == "__main__":
	unittest.main()