import re


class PhoneNumberValidator:
    """
    A class to validate phone numbers for multiple countries.

    Attributes
    ----------
    patterns : dict
        A dictionary mapping country codes to their respective phone number regex patterns.

    Methods
    -------
    add_country_pattern(country, pattern):
        Adds a new country pattern or updates an existing one.

    validate(phone_number, country):
        Validates the phone number for the specified country.
    """

    def __init__(self):
        """
        Constructs necessary attributes for the PhoneNumberValidator object.

        Initialized with a set of predefined patterns for various countries.
        Additional patterns can be added using the add_country_pattern method.
        """

        self.patterns = {
            "USA": r"^\+1\d{10}$",
            "Canada": r"^\+1\d{10}$",  # Same as USA
            "UK": r"^\+44\d{10}$",
            "Germany": r"^\+49\d{10,11}$",
            "France": r"^\+33\d{9}$",
            "India": r"^\+91\d{10}$",
            "China": r"^\+86\d{11}$",
            "Brazil": r"^\+55\d{10,11}$",
            "Australia": r"^\+61\d{9}$",
            "Japan": r"^\+81\d{9,10}$", 
            "South Korea": r"^\+8210\d{8}$", 
            "Russia": r"^\+7\d{10}$",
            "Italy": r"^\+393\d{9}$",
            "Netherlands": r"^\+31\d{9}$",
            "Spain": r"^\+34\d{9}$",
            "Sweden": r"^\+46\d{7,10}$",
            "Norway": r"^\+47\d{8}$",
            "Poland": r"^\+48\d{9}$",
            "Belgium": r"^\+32\d{9}$",
            "Finland": r"^\+358\d{8,10}$",
            "Denmark": r"^\+45\d{8}$",
            "Switzerland": r"^\+41\d{9}$",
            "Austria": r"^\+43\d{10,11}$",
            "Portugal": r"^\+351\d{9}$",
            "Greece": r"^\+30\d{10}$",
            "Czech Republic": r"^\+420\d{9}$",
            "Romania": r"^\+40\d{9,10}$",
            "Hungary": r"^\+36\d{9}$",
            "Ireland": r"^\+353\d{9}$",
            "Slovakia": r"^\+421\d{9}$",
            "Bulgaria": r"^\+359\d{9}$",
            "Croatia": r"^\+385\d{8,9}$",
            "Lithuania": r"^\+370\d{8}$",
            "Slovenia": r"^\+386\d{8}$",
            "Latvia": r"^\+371\d{8}$",
            "Estonia": r"^\+372\d{7,8}$",
            "Luxembourg": r"^\+352\d{9}$",
            "Malta": r"^\+356\d{8}$",
            "Cyprus": r"^\+357\d{8}$",
            "Iceland": r"^\+354\d{7}$",
            "Turkey": r"^\+90\d{10}$",
            "Israel": r"^\+972\d{9}$",
            "United Arab Emirates": r"^\+971\d{9}$",
            "Saudi Arabia": r"^\+966\d{9}$",
            "South Africa": r"^\+27\d{9}$",
            "Egypt": r"^\+20\d{10}$",
            "Nigeria": r"^\+234\d{10}$",
            "Kenya": r"^\+254\d{9}$",
            "Ghana": r"^\+233\d{9}$",
            "Singapore": r"^\+65\d{8}$",
            "Malaysia": r"^\+60\d{9,10}$",
            "Thailand": r"^\+66\d{9}$",
            "Vietnam": r"^\+84\d{9,10}$",
            "Philippines": r"^\+63\d{10}$",
            "Indonesia": r"^\+62\d{9,10}$",
            "New Zealand": r"^\+64\d{8,9}$",
            "Mexico": r"^\+52\d{10,11}$",
            "Argentina": r"^\+54\d{10,11}$",
            "Chile": r"^\+56\d{9}$",
            "Colombia": r"^\+57\d{10}$",
            "Peru": r"^\+51\d{9}$",
            # Add more patterns as needed
        }

    def add_country_pattern(self, country, pattern):
        """
        Adds a new country phone number pattern or updates an existing one.

        Parameters
        ----------
        country : str
            The name of the country.
        pattern : str
            The regex pattern for validating phone numbers in the specified country.
        """

        self.patterns[country] = pattern

    def validate(self, phone_number, country):
        """
        Validates a phone number for a specific country.

        Parameters
        ----------
        phone_number : str
            The phone number to validate.
        country : str
            The country against which to validate the phone number.

        Returns
        -------
        bool
            True if the phone number matches the pattern for the given country, False otherwise.
        """

        if country not in self.patterns:
            return False  # Return False instead of raising ValueError

        pattern = self.patterns[country]
        return bool(re.match(pattern, phone_number))

