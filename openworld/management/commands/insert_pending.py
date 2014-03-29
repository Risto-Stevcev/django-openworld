from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from openworld.models import User, Source, Entry, ExtraEntry, Pending
import json
import re

class Command(BaseCommand):
    args = "<pending_id pending_id ...>"
    help = "Adds an entry for each item in the pending item's data if it's valid."
    states = {
            'AK': 'Alaska',
            'AL': 'Alabama',
            'AR': 'Arkansas',
            'AS': 'American Samoa',
            'AZ': 'Arizona',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DC': 'District of Columbia',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'GU': 'Guam',
            'HI': 'Hawaii',
            'IA': 'Iowa',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'MA': 'Massachusetts',
            'MD': 'Maryland',
            'ME': 'Maine',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MO': 'Missouri',
            'MP': 'Northern Mariana Islands',
            'MS': 'Mississippi',
            'MT': 'Montana',
            'NA': 'National',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'NE': 'Nebraska',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NV': 'Nevada',
            'NY': 'New York',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'PR': 'Puerto Rico',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VA': 'Virginia',
            'VI': 'Virgin Islands',
            'VT': 'Vermont',
            'WA': 'Washington',
            'WI': 'Wisconsin',
            'WV': 'West Virginia',
            'WY': 'Wyoming'
    }


    def get_icarol211_location(self, url):
        city = None
        match_city = re.search(r'(?<=city\=)[A-Za-z ]*', url)
        if match_city:
            city = match_city.group(0)

        state = None
        match_state = re.search(r'(?<=sp\=)[A-Za-z ]*', url)
        if match_state:
            state = self.states.get(match_state.group(0))

        country = None
        match_country = re.search(r'(?<=country\=)[A-Za-z ]*', url)
        if match_country:
            country = match_country.group(0)

        return city, state, country


    def insert_icarol211(self, jsondata, user, source):
        for item in jsondata:
            try:
                name = item.get('program') 
                description = item.get('description')
                city, state, country = self.get_icarol211_location(item.get('program_url'))
                tags = item.get('tags')
                entry = Entry(user=user, source=source, name=name, description=description, city=city, state=state, country=country, tags=tags)
                entry.save()

                url = item.get('program_url')
                agency = item.get('agency')
                agency_url = item.get('agency_url')
                phone = item.get('phone')
                icarol_id = item.get('icarol_id')
                extra_entry = ExtraEntry(entry=entry, url=url, agency=agency, agency_url=agency_url, phone=phone, icarol_id=icarol_id)
                extra_entry.save()

                # Silently ignore duplicate entries (violating UNIQUE constraint)
            except IntegrityError:
                pass


    def insert(self, id):
        pending_item = Pending.objects.get(id=id)
        jsondata = json.loads(pending_item.data)
        if jsondata.get('data'):
            jsondata = jsondata['data']
        source = Source.objects.get(name=pending_item.source)

        if pending_item.source == 'icarol211':
            self.insert_icarol211(jsondata, pending_item.user, source)


    def handle(self, *args, **options):
        for pending_id in args:
            #try:
            self.insert(pending_id)
            #except:
            #    raise CommandError("Adding the pending entry failed.")

            self.stdout.write("Successfully entered pending entry '%s'." % pending_id)
