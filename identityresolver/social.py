import csv, urllib, requests
from bs4 import BeautifulSoup

class ResolvedPerson(object):
    def __init__(self,id,**kwargs):
        self.id = id
        for key in SocialProfileResolver.FIELDS:
            argval = kwargs[key] if (key in kwargs) else None
            setattr(self,key,argval)

        if self.full_name and not (self.first_name or self.last_name):
            self.first_name, self.last_name = ResolvedPerson.parse_name(self.full_name)
    
    def from_json(self,json):
        """Fill the fields of this person from a JSON."""
        for key in json:
            setattr(self,key,json[key])

        if self.full_name and not (self.first_name or self.last_name):
            self.first_name, self.last_name = ResolvedPerson.parse_name(self.full_name)

        return self
    
    @classmethod
    def parse_name(cls,full_name):
        """Parse a name string into first and last name."""
        # Gellner, Moritz J. | Gellner, Moritz Julius | Gellner, Moritz
        if ',' in full_name:
            chunks = full_name.split(',')
            return (chunks[1].lstrip(' ').rstrip(' '), 
                    chunks[0].lstrip(' ').rstrip(' '))
        # Moritz Gellner | Moritz J. Gellner | Moritz Julius Gellner
        elif ' ' in full_name:
            chunks = full_name.split(' ')
            return (' '.join(chunks[0:-1]),chunks[-1])
        else:
            return None,None

    def __repr__(self):
        s = "ResolvedPerson<%i>(" % self.id
        for f in SocialProfileResolver.FIELDS:
            s += "%s = %s, " % (f, str(getattr(self,f)))
        return s.rstrip(', ') + ")"

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.first_name == other.first_name and self.last_name == other.last_name and
                   self.age == other.age and self.city == other.city and self.state == other.state)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class SocialProfileResolver(object):
    """
    Match partial identity data (eg. real name) to social media profiles.
    """

    ## FIELDS defines the possible fields for identity resolution. These fields 
    ## are converted into attributes on ResolvedPerson and resolve() relies on
    ## some of these attributes, so change with caution!
    FIELDS =    { 'full_name'           : 0, 
                  'first_name'          : None,
                  'last_name'           : None,
                  'city'                : None,
                  'state'               : None, 
                  'age'                 : None, 
                  'linkedin_username'   : None,
                  'facebook_username'   : None,
                  'twitter_username'    : None }

    def _load_from_csv(self,input_path,**kwargs):
        """Takes a CSV of names and optional other rows (specified by 
            kwargs) and tries to find social media profiles for those
            people. The value of the kwarg corresponds to the row 
            number (ZERO-INDEXED!), or None if not present in the CSV. 
            These are the possible kwargs and their default values.
            - full_name: 1
            - first_name: None
            - last_name: None
            - city: None
            - state: None
            - age: None
            - linkedin_username: None
            - facebook_username: None
            - twitter_username: None
        """
        fields = SocialProfileResolver.FIELDS
        data = []

        with open(input_path,'r') as csvfile:
            reader = csv.reader(csvfile)
            for idx,row in enumerate(reader):
                record = {}
                for key in fields.keys():
                    if key in kwargs:
                        record[key] = row[int(kwargs[key])]
                    elif fields[key] != None:
                        record[key] = row[fields[key]]
                person = ResolvedPerson(idx)
                data.append(person.from_json(record))
        return data

    def resolve_from_csv(self,input_path,output_path=None,**kwargs):
        data = self._load_from_csv(input_path,output_path,kwargs)
        if output_path:
            raise NotImplementedError("Should write to a file!")
        else:
            for person in self.resolve(data):
                yield person

    def _get_username(self,network,url):
        if network == "linkedin":
            # just return URL, since that's the identifier for linkedin
            return url
        if network == "facebook":
            resp = requests.get(url)
            return resp.url.split('/')[-1]
        if network == "twitter":
            return url.split('/')[-1]

    def resolve(self,data):
        for p in data:
            pipl_url = "https://pipl.com/search/?q=%s+%s" % (p.first_name, p.last_name)
            if p.city:
                pipl_url += "&l=%s" % p.city
            if p.state:
                if p.city:
                    pipl_url += urllib.quote(",%s,US" % p.state)
                else:
                    pipl_url += "&" + urllib.quote("l=%s,US" % p.state)
            response = requests.get(pipl_url)
            soup = BeautifulSoup(response.text)
            for elem in soup.findAll("span","name"):
                #print elem.text
                if (p.first_name.lower().split(' ')[0] in elem.text.lower()) and \
                (p.last_name.lower() in elem.text.lower()):
                    link = elem.parent.find("div","url")
                    if link:
                        for sm_name in ["facebook","linkedin","twitter"]:
                            if sm_name in link.text:
                                setattr(p,sm_name + "_username",self._get_username(sm_name,link.text.lstrip('\n\t ').rstrip('\n\t ')))
            yield p
                
