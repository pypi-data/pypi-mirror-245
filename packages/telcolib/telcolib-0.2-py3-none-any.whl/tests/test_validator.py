import pytest
from telcolib.validator import PhoneNumberValidator

# Instantiate the PhoneNumberValidator
validator = PhoneNumberValidator()

# Test cases as tuples (phone_number, country, expected_result)
test_data = [
    # USA
    ("+14445556666", "USA", True),
    ("+19999999999", "USA", True),
    ("+1444555666", "USA", False),  # Incorrect length

    # UK
    ("+441234567890", "UK", True),
    ("+440123456789", "UK", True),
    # Germany
    ("+493012345678", "Germany", True),
    ("+4930123456789", "Germany", True),
    ("+4930123456", "Germany", False),  # Incorrect length

    # France
    ("+33123456789", "France", True),
    ("+3312345678", "France", False),  # Incorrect length

    # India
    ("+919812345678", "India", True),
    ("+91981234567", "India", False),  # Incorrect length

    # China
    ("+8612345678901", "China", True),
    ("+86123456789", "China", False),  # Incorrect length

    # Brazil
    ("+5511987654321", "Brazil", True),
    ("+551198765432", "Brazil", True),
    ("+55119876543", "Brazil", False),  # Incorrect length

    # Australia
    ("+61412345678", "Australia", True),
    ("+6141234567", "Australia", False),  # Incorrect length

    # Japan
    ("+819012345678", "Japan", True),  # Incorrect length

    # South Korea
    ("+821012345678", "South Korea", True),
    ("+81901234567", "Japan", True), # Incorrect length

    # Russia
    ("+79101234567", "Russia", True),
    ("+7910123456", "Russia", False),  # Incorrect length


    # Spain
    ("+34612345678", "Spain", True),
    ("+3461234567", "Spain", False),  # Incorrect length

    # Canada
    ("+14161234567", "Canada", True),
    ("+1416123456", "Canada", False),  # Incorrect length

    # Test for an unsupported country
    ("+1234567890", "Mars", False),  # Unsupported country
]

@pytest.mark.parametrize("phone_number,country,expected", test_data)
def test_phone_number_validation(phone_number, country, expected):
    assert validator.validate(phone_number, country) == expected
