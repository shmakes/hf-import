from datetime import date, datetime


class BaseDoc(object):
    def __init__(self):
        self.type = ''
        now = datetime.utcnow().isoformat()[0:19] + 'Z'
        self.metadata = { 'created_at': now, 'created_by': '',
                        'updated_at': now, 'updated_by': '' }


class Veteran(BaseDoc):
    def __init__(self):
        super(Veteran, self).__init__()
        self.type = 'Veteran'
        self.app_date = None
        self.app_date_string = ''
        self.name = {}
        self.address = {}
        self.birth_date = None
        self.birth_date_string = ''
        self.age = ''
        self.weight = ''
        self.gender = ''
        self.vet_type = ''
        self.shirt = {}
        self.flight = {}
        self.medical = {}
        self.medical['isWheelchairBound'] = ''
        self.medical['usesWheelchair'] = ''
        self.medical['usesCane'] = ''
        self.medical['usesWalker'] = ''
        self.medical['requiresOxygen'] = ''
        self.medical['limitations'] = ''
        self.medical['category'] = ''
        self.service = {}
        self.service['branch'] = ''
        self.service['rank'] = ''
        self.service['dates'] = ''
        self.service['activity'] = ''
        self.guardian = {}
        self.emerg_contact = {}
        self.emerg_contact['name'] = ''
        self.emerg_contact['relation'] = ''
        self.emerg_contact['address'] = {}
        self.alt_contact = {}
        self.alt_contact['name'] = ''
        self.alt_contact['relation'] = ''
        self.alt_contact['address'] = {}
        self.waiver_received = False

    def adapt_csv(self, valueDict):
        import parsedatetime.parsedatetime as pdt 
        c = pdt.Constants()
        p = pdt.Calendar(c)

        self.app_date_string = valueDict["Postmark Date"].strip()
        appDate = p.parse(valueDict["Postmark Date"])
        if (appDate[1] == 1):
            self.app_date = date(*appDate[0][0:3]).isoformat()
        else:
          self.app_date = date.today().isoformat()[0:10]

        self.name = { 'last': valueDict["Last"].strip().title(), 
                        'first': valueDict["First"].strip().title(),
                        'middle': valueDict["Middle"].strip().title(),
                        'nickname': valueDict["Nick"].strip().title() }
                        
        self.address['street'] = valueDict["Address"].strip().title()
        self.address['city'] = valueDict["City"].strip().title()
        self.address['county'] = "Unknown"
        self.address['state'] = valueDict["ST"].strip().upper()
        self.address['zip'] = valueDict["Zip Code"].strip()
        self.address['phone_day'] = valueDict["Phone Number"].strip()
        self.address['phone_mbl'] = valueDict["Secondary"].strip()
        self.address['email'] = valueDict["Email"].strip()

        self.birth_date_string = valueDict["DOB"].strip()
        appDOB = p.parse(valueDict["DOB"])
        if (appDOB[1] == 1):
            bd = date(*appDOB[0][0:3])
            if (bd is None):
                bd = date.today()
            if (bd > date.today()):
                bd = datetime( bd.year - 100, *bd.timetuple()[1:-2] )
            self.birth_date = bd.isoformat()[0:10]

        self.gender = valueDict["Male/Female"].strip().upper()[:1]
        self.shirt = { 'size': valueDict["Tshirt Size"].strip().upper().replace("XXXXL", "4XL").replace("XXXL", "3XL").replace("XXL", "2XL") }
        #self.guardian = { 'pref_notes': valueDict["Assigned Guardian"].strip(), 'id': '', 'name':'', 'history': [] }
        self.guardian = { 'pref_notes': '', 'id': '', 'name':'', 'history': [] }
        self.vet_type = valueDict["Conflict"].split(' ', 1)[0].strip().title().replace("Korean", "Korea").replace("Wwii", "WWII")
        self.service['branch'] = valueDict["Branch"].strip()
        self.service['dates'] = valueDict["ServiceDates"].strip()
        #self.call = { 'mail_sent': len(valueDict["Letter"].strip()) > 0, 'history': [] }
        self.flight = { 'status': 'Active', 'id': 'None', 'seat': '', 'group': '', 'bus': 'None', 'waiver': valueDict["Waiver"].strip().title() == "Yes", 'history': [] , 'status_note': valueDict["NOTES"] }
        #self.medical = { 'release': valueDict["Health"].strip().title() == "Yes" }
        self.emerg_contact['name'] = valueDict["EContact"].strip()
        self.emerg_contact['address']['phone'] = valueDict["EContactPhone"].strip()


class Guardian(BaseDoc):
    def __init__(self):
        super(Guardian, self).__init__()
        self.type = 'Guardian'
        self.app_date = None
        self.app_date_string = ''
        self.name = {}
        self.address = {}
        self.birth_date = None
        self.birth_date_string = ''
        self.age = ''
        self.weight = ''
        self.gender = ''
        self.shirt = {}
        self.flight = {}
        self.preferred_airport = ''
        self.medical = {}
        self.notes = {}
        self.veteran = {}
        self.marketing = {}
        self.marketing['how_discover_hf'] = ''
        self.marketing['how_discover_hf_note'] = ''
        self.waiver_received = False
        self.training_complete = False

    def adapt_csv(self, valueDict):
        import parsedatetime.parsedatetime as pdt 
        c = pdt.Constants()
        p = pdt.Calendar(c)

        self.app_date_string = valueDict["Postmark Date"].strip()
        appDate = p.parse(valueDict["Postmark Date"])
        if (appDate[1] == 1):
            self.app_date = date(*appDate[0][0:3]).isoformat()
        else:
          self.app_date = date.today().isoformat()[0:10]

        self.name = { 'last': valueDict["Last"].strip().title(), 
                        'first': valueDict["First"].strip().title(),
                        'middle': valueDict["Middle"].strip().title(),
                        'nickname': valueDict["Nick"].strip().title() }
                        
        self.address['street'] = valueDict["Address"].strip().title()
        self.address['city'] = valueDict["City"].strip().title()
        self.address['county'] = "Unknown"
        self.address['state'] = valueDict["ST"].strip().upper()
        self.address['zip'] = valueDict["Zip Code"].strip()
        self.address['phone_day'] = valueDict["Phone Number"].strip()
        #self.address['phone_mbl'] = valueDict["Secondary"].strip()
        self.address['email'] = valueDict["Email"].strip()

        self.birth_date_string = valueDict["DOB"].strip()
        appDOB = p.parse(valueDict["DOB"])
        if (appDOB[1] == 1):
            bd = date(*appDOB[0][0:3])
            if (bd is None):
                bd = date.today()
            if (bd > date.today()):
                bd = datetime( bd.year - 100, *bd.timetuple()[1:-2] )
            self.birth_date = bd.isoformat()[0:10]

        #self.gender = valueDict["Male/Female"].strip().upper()[:1]
        self.shirt = { 'size': valueDict["Tshirt Size"].strip().upper().replace("XXXXL", "4XL").replace("XXXL", "3XL").replace("XXL", "2XL") }
        self.veteran = { 'pref_notes': valueDict["Assigned Veteran"].strip(), 'pairings': [], 'history': [] }

        #self.call = { 'email_sent': len(valueDict["Letter"].strip()) > 0, 'history': [] }
        self.flight = { 'status': 'Active', 'id': 'None', 'seat': '', 'group': '', 'bus': 'None', 'waiver': False, 'paid': len(valueDict["Donation"].strip()) > 0, 'status_note': valueDict["NOTES"] , 'history': [] }
        #self.medical = { 'release': valueDict["Health"].strip().title() == "Yes" }

class Volunteer(BaseDoc):
    def __init__(self):
        super(Volunteer, self).__init__()
        self.type = 'Volunteer'
        self.app_date = None
        self.app_date_string = ''
        self.name = {}
        self.address = {}
        self.birth_date = None
        self.birth_date_string = ''
        self.notes = {}
        self.waiver_received = False
        self.training_complete = False

    def adapt_csv(self, valueDict):
        import parsedatetime.parsedatetime as pdt 
        c = pdt.Constants()
        p = pdt.Calendar(c)

        self.app_date_string = valueDict["App Recvd"].strip()
        appDate = p.parse(valueDict["App Recvd"])
        if (appDate[1] == 1):
            self.app_date = date(*appDate[0][0:3]).isoformat()

        firstMiddle = valueDict["First Name"].partition(' ')
        self.name = { 'last': valueDict["Last Name"].strip().title(), 
                        'first': firstMiddle[0].strip().title(),
                        'middle': firstMiddle[2].strip().title(),
                        'nickname': '' }
                        
        self.address['street'] = valueDict["Address"].strip().title()
        self.address['city'] = valueDict["City"].strip().title()
        self.address['state'] = valueDict["State"].strip().upper()
        self.address['zip'] = valueDict["Zip"].strip()
        self.address['phone_day'] = valueDict["Phone (Day)"].strip()
        self.address['phone_eve'] = valueDict["Evening phone"].strip()
        self.address['phone_mbl'] = valueDict["Mobile phone"].strip()
        self.address['email'] = valueDict["Email"].strip()

        self.birth_date_string = valueDict["DOB"].strip()
        appDOB = p.parse(valueDict["DOB"])
        if (appDOB[1] == 1):
            self.birth_date = date(*appDOB[0][0:3]).isoformat()

        self.notes = { 'other': valueDict["Comments"].strip() }


class Flight(BaseDoc):
    def __init__(self):
        super(Flight, self).__init__()
        self.type = 'Flight'
        self.name = ''
        self.capacity = 0
        self.flight_date = None
        self.completed = False

    def adapt_csv(self, valueDict):
        import parsedatetime.parsedatetime as pdt 
        c = pdt.Constants()
        p = pdt.Calendar(c)

        self.name = valueDict["FlightName"].strip()
        self.capacity = valueDict["FlightCapacity"]
        flightDate = p.parse(valueDict["FlightDate"])
        if (flightDate[1] == 1):
            self.flight_date = date(*flightDate[0][0:3]).isoformat()
        self.completed = valueDict["Completed"] == "true"

class Location(object):
    def __init__(self):
        super(Location, self).__init__()
        self.type = 'Location'

    def adapt_csv(self, valueDict):
        self.zip = valueDict["Zip"].strip()
        self._id = "loc-" + self.zip
        self.lat = valueDict["Latitude"].strip()
        self.long = valueDict["Longitude"].strip()
        self.city = valueDict["City"].strip().title()
        self.state = valueDict["State"].strip().upper()
        self.county = valueDict["County"].strip().title()
        #self.code_type = valueDict["CodeType"].strip()


class Crew(BaseDoc):
    def __init__(self):
        super(Crew, self).__init__()
        self.type = 'Guardian'
        self.app_date = None
        self.name = {}
        self.address = {}
        self.birth_date = None
        self.age = ''
        self.gender = ''
        self.shirt = {}
        self.flight = {}
        self.preferred_airport = ''
        self.medical = {}
        self.notes = {}
        self.veteran = {}

    def adapt_csv(self, valueDict):
        import parsedatetime.parsedatetime as pdt 
        c = pdt.Constants()
        p = pdt.Calendar(c)

        appDate = p.parse(valueDict["app_date"])
        if (appDate[1] == 1):
            self.app_date = date(*appDate[0][0:3]).isoformat()

        self.name = { 'last': valueDict["last_name"].strip().title(), 
                        'first': valueDict["first_name"].strip().title(),
                        'middle': valueDict["middle_name"].strip().title(),
                        'nickname': '' }
                        
        self.address['street'] = valueDict["addr_street"].strip().title()
        self.address['city'] = valueDict["addr_city"].strip().title()
        self.address['county'] = valueDict["addr_county"].strip().title()
        self.address['state'] = valueDict["addr_state"].strip().upper()
        self.address['zip'] = valueDict["addr_zip"].strip()
        self.address['phone_day'] = valueDict["addr_phone_day"].strip()
        self.address['phone_eve'] = valueDict["addr_phone_eve"].strip()
        self.address['phone_mbl'] = valueDict["addr_phone_mbl"].strip()
        self.address['email'] = valueDict["addr_email"].strip()

        appDOB = p.parse(valueDict["birth_date"])
        if (appDOB[1] == 1):
            self.birth_date = date(*appDOB[0][0:3]).isoformat()

        self.gender = valueDict["gender"].strip().upper() 
        self.shirt = { 'size': valueDict["shirt_size"].strip().upper() }
        self.flight = { 'status': 'Active', 'status_note': '', 'id': 'SSHF-Nov2013', 'seat': '', 'bus': 'None', 'history': [], 'confirmed_date': '', 'confirmed_by': '' }
        self.preferred_airport = ''
        self.medical = { 'limitations': '', 'experience': '(FC) ' + valueDict["medical_experience"].strip(), 'release': 'Y' }
        self.notes = { 'service': valueDict["notes_service"].strip(), 'previous_hf': valueDict["notes_previous_hf"].strip(), 'other': valueDict["notes_other"].strip() }
        self.veteran = { 'pref_notes': '(FC)', 'pairings': [], 'history': [] }

class Veteran2(BaseDoc):
    def __init__(self):
        super(Veteran2, self).__init__()
        self.type = 'Veteran'
        self.app_date = None
        self.app_date_string = ''
        self.name = {}
        self.address = {}
        self.birth_date = None
        self.birth_date_string = ''
        self.age = ''
        self.weight = ''
        self.gender = ''
        self.vet_type = ''
        self.shirt = {}
        self.flight = {'status': 'Active', 'history': []}
        self.medical = {}
        self.medical['isWheelchairBound'] = ''
        self.medical['usesWheelchair'] = ''
        self.medical['usesCane'] = ''
        self.medical['usesWalker'] = ''
        self.medical['requiresOxygen'] = ''
        self.medical['limitations'] = ''
        self.medical['category'] = ''
        self.service = {}
        self.service['branch'] = ''
        self.service['rank'] = ''
        self.service['dates'] = ''
        self.service['activity'] = ''
        self.guardian = {}
        self.emerg_contact = {}
        self.emerg_contact['name'] = ''
        self.emerg_contact['relation'] = ''
        self.emerg_contact['address'] = {}
        self.alt_contact = {}
        self.alt_contact['name'] = ''
        self.alt_contact['relation'] = ''
        self.alt_contact['address'] = {}
        self.mail_call = {}
        self.mail_call['name'] = ''
        self.mail_call['relation'] = ''
        self.mail_call['address'] = {}
        self.waiver_received = False

    def fix_phone_numbers(self, phone_num):
        return phone_num.replace("(", "").replace(")", "").replace(" ", "-")

    def adapt_csv(self, valueDict):

        self.app_date = valueDict["app_date"]
        self.vet_type = valueDict["conflict"].strip() 

        self.name = { 'last': valueDict["last_name"].strip(), 
                        'first': valueDict["first_name"].strip(),
                        'middle': valueDict["middle_name"].strip(),
                        'nickname': valueDict["nick_name"].strip() }
                        
        self.address['street'] = valueDict["addr_street"].strip()
        self.address['city'] = valueDict["addr_city"].strip()
        self.address['county'] = valueDict["addr_county"].strip()
        self.address['state'] = valueDict["addr_state"].strip().upper()
        self.address['zip'] = valueDict["addr_zip"].strip()
        self.address['phone_day'] = self.fix_phone_numbers(valueDict["addr_phone_day"].strip())
        self.address['phone_mbl'] = self.fix_phone_numbers(valueDict["addr_phone_eve"].strip())
        self.address['phone_eve'] = self.fix_phone_numbers(valueDict["addr_phone_mbl"].strip())
        self.address['email'] = valueDict["addr_email"].strip()

        self.birth_date = valueDict["birth_date"].strip()
        self.gender = valueDict["gender"].strip().upper()
        size = valueDict["shirt_size"].strip().upper() or 'None'
        self.shirt = { 'size': size }

        self.service['branch'] = valueDict["service_branch"].strip()
        self.service['rank'] = valueDict["service_rank"].strip()
        self.service['dates'] = valueDict["service_dates"].strip()
        self.service['activity'] = valueDict["service_activity"].strip()

        self.emerg_contact['relation'] = valueDict["ec_relation"].strip()
        self.emerg_contact['name'] = valueDict["ec_name"].strip()
        self.emerg_contact['address']['street'] = valueDict["ec_addr_street"].strip()
        self.emerg_contact['address']['city'] = valueDict["ec_addr_city"].strip()
        self.emerg_contact['address']['state'] = valueDict["ec_addr_state"].strip()
        self.emerg_contact['address']['zip'] = valueDict["ec_addr_zip"].strip()
        self.emerg_contact['address']['phone'] = self.fix_phone_numbers(valueDict["ec_addr_phone"].strip())
        self.emerg_contact['address']['phone_eve'] = self.fix_phone_numbers(valueDict["ec_addr_phone_eve"].strip())
        self.emerg_contact['address']['phone_mbl'] = self.fix_phone_numbers(valueDict["ec_addr_phone_mbl"].strip())

        self.alt_contact['relation'] = valueDict["ac_relation"].strip()
        self.alt_contact['name'] = valueDict["ac_name"].strip()
        self.alt_contact['address']['street'] = valueDict["ac_addr_street"].strip()
        self.alt_contact['address']['city'] = valueDict["ac_addr_city"].strip()
        self.alt_contact['address']['state'] = valueDict["ac_addr_state"].strip()
        self.alt_contact['address']['zip'] = valueDict["ac_addr_zip"].strip()
        self.alt_contact['address']['phone'] = self.fix_phone_numbers(valueDict["ac_addr_phone"].strip())
        self.alt_contact['address']['phone_eve'] = self.fix_phone_numbers(valueDict["ac_addr_phone_eve"].strip())
        self.alt_contact['address']['phone_mbl'] = self.fix_phone_numbers(valueDict["ac_addr_phone_mbl"].strip())
        self.alt_contact['address']['email'] = self.fix_phone_numbers(valueDict["ac_addr_email"].strip())

        self.mail_call['relation'] = valueDict["mail_call_relation"].strip()
        self.mail_call['name'] = valueDict["mail_call_name"].strip()
        self.mail_call['address']['phone'] = self.fix_phone_numbers(valueDict["mail_call_addr_phone"].strip())
        self.mail_call['address']['email'] = self.fix_phone_numbers(valueDict["mail_call_addr_email"].strip())

        self.flight['status_note'] = valueDict["flight_status_note"].strip()
        self.flight['group'] = valueDict["flight_group"].strip()

        self.medical['limitations'] = valueDict["medical_limitations"].strip()
        self.medical['usesCane'] = valueDict["medical_uses_cane"].strip() == 'Yes'
        self.medical['usesWalker'] = valueDict["medical_uses_walker"].strip() == 'Yes'
        self.medical['usesWheelchair'] = valueDict["medical_uses_wheelchair"].strip() == 'Yes'
        self.medical['isWheelchairBound'] = valueDict["medical_is_wheelchair_bound"].strip() == 'Yes'
        self.medical['requiresOxygen'] = valueDict["medical_requires_oxygen"].strip() == 'Yes'

        self.guardian = { 'pref_notes': valueDict["guardian_pref_notes"].strip(), 'id': '', 'name':'', 'history': [] }

class Guardian2(BaseDoc):
    def __init__(self):
        super(Guardian2, self).__init__()
        self.type = 'Guardian'
        self.app_date = None
        self.app_date_string = ''
        self.name = {}
        self.address = {}
        self.birth_date = None
        self.birth_date_string = ''
        self.age = ''
        self.weight = ''
        self.gender = ''
        self.shirt = {}
        self.flight = {'status': 'Active', 'history': []}
        self.notes = {'service': 'N', 'other': ''}
        self.guardian = {}

    def fix_phone_numbers(self, phone_num):
        return phone_num.replace("(", "").replace(")", "").replace(" ", "-")

    def adapt_csv(self, valueDict):

        self.app_date = valueDict["app_date"]

        self.name = { 'last': valueDict["last_name"].strip(), 
                        'first': valueDict["first_name"].strip(),
                        'middle': valueDict["middle_name"].strip(),
                        'nickname': valueDict["nick_name"].strip() }
                        
        self.address['street'] = valueDict["addr_street"].strip()
        self.address['city'] = valueDict["addr_city"].strip()
        self.address['county'] = valueDict["addr_county"].strip()
        self.address['state'] = valueDict["addr_state"].strip().upper()
        self.address['zip'] = valueDict["addr_zip"].strip()
        self.address['phone_day'] = self.fix_phone_numbers(valueDict["addr_phone_day"].strip())
        self.address['phone_mbl'] = self.fix_phone_numbers(valueDict["addr_phone_eve"].strip())
        self.address['phone_eve'] = self.fix_phone_numbers(valueDict["addr_phone_mbl"].strip())
        self.address['email'] = valueDict["addr_email"].strip()

        self.birth_date = valueDict["birth_date"].strip()
        self.gender = valueDict["gender"].strip().upper()
        size = valueDict["shirt_size"].strip().upper() or 'None'
        self.shirt = { 'size': size }

        self.notes['service'] = valueDict["notes_service"].strip()
        self.notes['other'] = valueDict["notes_other"].strip()

        self.flight['status_note'] = valueDict["flight_status_note"].strip()

        self.veteran = { 'pref_notes': valueDict["veteran_pref_notes"].strip(), 'pairings': [], 'history': [] }
