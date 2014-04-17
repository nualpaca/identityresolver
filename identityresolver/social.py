import csv

class ResolvedPerson(object):
	def __init__(self,id,**kwargs):
		self.id = id
		for key in SocialProfileResolver.FIELDS:
			argval = kwargs[key] if (key in kwargs) else None
			setattr(self,key,argval)

		if self.full_name and not (self.first_name or self.last_name):
			self.first_name, self.last_name = ResolvedPerson.parse_name()
	
	def from_json(self,json):
		"""Fill the fields of this person from a JSON."""
		for key in json:
			setattr(self,key,json[key])

		if self.full_name and not (self.first_name or self.last_name):
			self.first_name, self.last_name = ResolvedPerson.parse_name()
	
	def parse_name(full_name):
		"""Parse a name string into first and last name."""
		# Gellner, Moritz J. | Gellner, Moritz Julius | Gellner, Moritz
		if ',' in full_name:
			chunks = full_name.split(',')
			return (chunks[1].lstrip(' ').rstrip(' '), 
					chunks[0].lstrip(' ').rstrip(' '))
		# Moritz Gellner | Moritz J. Gellner | Moritz Julius Gellner
		elif ' ' in full_name:
			chunks = full_name.split(' ')
			return (chunks[0:-1],chunks[-1])
		else:
			return None,None

	def __repr__(self):
		s = "ResolvedPerson<%i>(" % self.id
		for f in SocialProfileResolver.FIELDS:
			s += "%s = %s" % f, str(getattr(self,f))
		return s + ")"

	def __str__(self):
		return repr(self)

			


class SocialProfileResolver(object):
	"""
	Match partial identity data (eg. real name) to social media profiles.
	"""

	## FIELDS defines the possible fields for identity resolution. These fields 
	## are converted into attributes on ResolvedPerson and resolve() relies on
	## some of these attributes, so change with caution!
	FIELDS = 	{ 'full_name' 		 	: 0, 
				  'first_name'			: None,
				  'last_name'			: None,
				  'state'			 	: None, 
				  'age'				 	: None, 
				  'linkedin_username'	: None,
				  'facebook_username'	: None,
				  'twitter_username' 	: None }

	def resolve_from_csv(self,path,**kwargs):
		"""Takes a CSV of names and optional other rows (specified by 
			kwargs) and tries to find social media profiles for those
			people. The value of the kwarg corresponds to the row 
			number (ZERO-INDEXED!), or None if not present in the CSV. 
			These are the possible kwargs and their default values.
			- full_name: 1
			- first_name: None
			- last_name: None
			- state: None
			- age: None
			- linkedin_username: None
			- facebook_username: None
			- twitter_username: None
		"""
		fields = SocialProfileResolver.FIELDS
		data = []

		with open(path,'r',encoding='utf-8') as csvfile:
			reader = csv.reader(csvfile)
			for idx,row in enumerate(reader):
				record = {}
				for key in fields.keys():
					if key in kwargs:
						record[key] = row[int(kwargs[key])]
					elif fields[key] != None:
						record[key] = row[fields[key]]
				person = ResolvedPerson(idx)
				data.append(person.load_from_json(record))

		resolved_data = self.resolve(data)


	def resolve(self,data):
		pass