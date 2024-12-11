import re
from datetime import datetime


def validate_first_name(first_name: str) -> str:
    regex = r'^[A-Z][a-z]*([ ]([A-Z][a-z]*))*$'  # Proper capitalization rule
    invalid_chars_regex = r'[^A-Za-z\s]'  # Checks for special characters or numbers
    repeated_char_regex = r'(.)\1{2,}'  # Checks for repeated characters
    max_length = 20
    repeated_word_pattern = r'^(\b\w+\b)(?:\s+\1){1}$'  # Regex to allow exactly two occurrences of the same word (e.g., "Jan Jan")

    random_combination_regex = r'^[A-Za-z]+([ ]([A-Z][a-z]*))*$'
    words = first_name.strip().split()  # Splits by any whitespace

    # If the name consists of a single word and the length of that word is greater than 10
    if len(words) == 1 and len(first_name) > 10:
        # Regex to prevent a single unstructured word (e.g., random characters, no spaces, too long)
        unstructured_regex = r'^[a-zA-Z]+$'  # Ensures only letters, no spaces, and no special characters
        if re.match(unstructured_regex, first_name):
            return "Name must not consist of a single unstructured word with more than 10 characters."

    # Prevent long sequences of characters that appear random
    random_sequence_regex = r'([a-zA-Z])\1{3,}'  # Looks for sequences of the same letter repeated more than 3 times

    # Check if the first name is empty
    if not first_name:
        return "First name is required."

    # Check for invalid characters like numbers or special characters
    if re.search(invalid_chars_regex, first_name.strip()):
        return "First name must not contain special characters or numbers."

    # Validate capitalization rule (only first letters are capitalized properly)
    if not re.match(regex, first_name.strip()):
        return "Capitalization is allowed only at the start of each word in name"

    # Check if the name length is within the valid range
    if len(first_name.strip()) < 2:
        return "First name must be at least 2 characters long."
    if len(first_name.strip()) > max_length:
        return f"First name must be at most {max_length} characters long."

    lower_case_name = first_name.strip().lower()

    # Check for random 2- or 3-letter combinations, but allow the first word to be random
    if re.match(random_combination_regex, first_name.strip()):
        pass  # No need to check for random combinations after the first word
    else:
        return "First name must not contain random two letter combinations"

    # Check for long sequences of the same character (e.g., "aaaa")
    if re.search(random_sequence_regex, first_name.strip()):
        return "First name must not contain long sequences of the same character."

    # Check for repeated characters
    if re.search(repeated_char_regex, lower_case_name):
        return "First name must not contain repeated characters."

    # Check for exactly two repeated words (e.g., "Jan Jan")
    if re.match(repeated_word_pattern, first_name.strip()):
        return ""  # Allow repeated valid names (e.g., "Jan Jan")

    # Check for other invalid duplicated patterns (three or more repetitions)
    three_or_more_repeats_pattern = r'(\b\w+\b)(?:\s+\1){2,}'  # Three or more occurrences
    if re.search(three_or_more_repeats_pattern, first_name.strip()):
        return "First name must not contain duplicated patterns"

    return ""


def validate_middle_name(middle_name: str) -> str:
    regex = r'^[A-Z][a-z]*([ ]([A-Z][a-z]*))*$'
    invalid_chars_regex = r'[^A-Za-z\s]'
    repeated_char_regex = r'(.)\1{2,}'
    max_length = 20
    repeated_word_pattern = r'^(\b\w+\b)(?:\s+\1){1}$'

    random_combination_regex = r'^[A-Za-z]+([ ]([A-Z][a-z]*))*$'
    words = middle_name.strip().split()

    if len(words) == 1 and len(middle_name) > 10:
        unstructured_regex = r'^[a-zA-Z]+$'
        if re.match(unstructured_regex, middle_name):
            return "Middle name must not consist of a single unstructured word with more than 10 characters."

    random_sequence_regex = r'([a-zA-Z])\1{3,}'

    if not middle_name:
        return "Middle name is required."

    if re.search(invalid_chars_regex, middle_name.strip()):
        return "Middle name must not contain special characters or numbers."

    if not re.match(regex, middle_name.strip()):
        return "Capitalization is allowed only at the start of each word in name"

    if len(middle_name.strip()) < 2:
        return "Middle name must be at least 2 characters long."
    if len(middle_name.strip()) > max_length:
        return f"Middle name must be at most {max_length} characters long."

    lower_case_name = middle_name.strip().lower()

    if re.match(random_combination_regex, middle_name.strip()):
        pass
    else:
        return "Middle name must not contain random two letter combinations"

    if re.search(random_sequence_regex, middle_name.strip()):
        return "Middle name must not contain long sequences of the same character."

    if re.search(repeated_char_regex, lower_case_name):
        return "Middle name must not contain repeated characters."

    if re.match(repeated_word_pattern, middle_name.strip()):
        return ""

    three_or_more_repeats_pattern = r'(\b\w+\b)(?:\s+\1){2,}'
    if re.search(three_or_more_repeats_pattern, middle_name.strip()):
        return "Middle name must not contain duplicated patterns"

    return ""


def validate_last_name(last_name: str) -> str:
    regex = r'^[A-Z][a-z]*([ ]([A-Z][a-z]*))*$'
    invalid_chars_regex = r'[^A-Za-z\s]'
    repeated_char_regex = r'(.)\1{2,}'
    max_length = 20
    repeated_word_pattern = r'^(\b\w+\b)(?:\s+\1){1}$'

    random_combination_regex = r'^[A-Za-z]+([ ]([A-Z][a-z]*))*$'
    words = last_name.strip().split()

    if len(words) == 1 and len(last_name) > 10:
        unstructured_regex = r'^[a-zA-Z]+$'
        if re.match(unstructured_regex, last_name):
            return "Last name must not consist of a single unstructured word with more than 10 characters."

    random_sequence_regex = r'([a-zA-Z])\1{3,}'

    if not last_name:
        return "Last name is required."

    if re.search(invalid_chars_regex, last_name.strip()):
        return "Last name must not contain special characters or numbers."

    if not re.match(regex, last_name.strip()):
        return "Capitalization is allowed only at the start of each word in name"

    if len(last_name.strip()) < 2:
        return "Last name must be at least 2 characters long."
    if len(last_name.strip()) > max_length:
        return f"Last name must be at most {max_length} characters long."

    lower_case_name = last_name.strip().lower()

    if re.match(random_combination_regex, last_name.strip()):
        pass
    else:
        return "Last name must not contain random two letter combinations"

    if re.search(random_sequence_regex, last_name.strip()):
        return "Last name must not contain long sequences of the same character."

    if re.search(repeated_char_regex, lower_case_name):
        return "Last name must not contain repeated characters."

    if re.match(repeated_word_pattern, last_name.strip()):
        return ""  

    three_or_more_repeats_pattern = r'(\b\w+\b)(?:\s+\1){2,}'
    if re.search(three_or_more_repeats_pattern, last_name.strip()):
        return "Last name must not contain duplicated patterns"

    return ""

def validate_birthday(birthday: str, age: int) -> str:
    if not birthday:
        return "Birthday is required."

    try:
        birthday_date = datetime.strptime(birthday, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format."

    current_date = datetime.now()
    sixty_years_ago = datetime(1964, 1, 1)

    if birthday_date > current_date:
        return "Birthday cannot be a future date."
    if birthday_date < sixty_years_ago:
        return "The birthdate must not be earlier than January 1, 1964, based on app standards."

    calculated_age = current_date.year - birthday_date.year
    if (current_date.month, current_date.day) < (birthday_date.month, birthday_date.day):
        calculated_age -= 1

    if calculated_age != age:
        return f"The age ({age}) does not match the birthday."

    return ""

def validate_age(age: int) -> str:
    if age is None:
        return "Age is required."
    if age < 18:
        return "Age must be at least 18."
    if age > 60:
        return "Age must be less than or equal to 60."
    return ""

def validate_contact_number(contact_number: str) -> str:
    regex = r'^09\d{9}$'

    if not contact_number:
        return "Contact number is required."

    trimmed_contact_number = contact_number.strip()

    if not re.match(regex, trimmed_contact_number):
        return "Contact number must be a valid Philippine mobile number."
    if re.search(r'(\d)\1{3,}', trimmed_contact_number):
        return "Contact number must not contain 4 or more repeating digits."

    return ""


def validate_email(email: str) -> str:
   
    valid_providers = [
    'gmail.com', 'yahoo.com', 'yahoo.com.ph', 'outlook.com', 'hotmail.com', 'aol.com', 
    'icloud.com', 'gov.ph', 'dfa.gov.ph', 'dip.gov.ph', 'deped.gov.ph', 'neda.gov.ph', 
    'doh.gov.ph', 'dti.gov.ph', 'dswd.gov.ph', 'dbm.gov.ph', 'pcso.gov.ph', 'pnp.gov.ph', 
    'bsp.gov.ph', 'prc.gov.ph', 'psa.gov.ph', 'dpwh.gov.ph', 'lto.gov.ph', 'boi.gov.ph',
    'hotmail.co.uk', 'hotmail.fr', 'msn.com', 'yahoo.fr', 'wanadoo.fr', 'orange.fr', 
    'comcast.net', 'yahoo.co.uk', 'yahoo.com.br', 'yahoo.com.in', 'live.com', 
    'rediffmail.com', 'free.fr', 'gmx.de', 'web.de', 'yandex.ru', 'ymail.com', 
    'libero.it', 'uol.com.br', 'bol.com.br', 'mail.ru', 'cox.net', 'hotmail.it', 
    'sbcglobal.net', 'sfr.fr', 'live.fr', 'verizon.net', 'live.co.uk', 'googlemail.com', 
    'yahoo.es', 'ig.com.br', 'live.nl', 'bigpond.com', 'terra.com.br', 'yahoo.it', 
    'neuf.fr', 'yahoo.de', 'alice.it', 'rocketmail.com', 'att.net', 'laposte.net', 
    'facebook.com', 'bellsouth.net', 'yahoo.in', 'hotmail.es', 'charter.net', 
    'yahoo.ca', 'yahoo.com.au', 'rambler.ru', 'hotmail.de', 'tiscali.it', 'shaw.ca', 
    'yahoo.co.jp', 'sky.com', 'earthlink.net', 'optonline.net', 'freenet.de', 
    't-online.de', 'aliceadsl.fr', 'virgilio.it', 'home.nl', 'qq.com', 'telenet.be', 
    'me.com', 'yahoo.com.ar', 'tiscali.co.uk', 'yahoo.com.mx', 'voila.fr', 'gmx.net', 
    'mail.com', 'planet.nl', 'tin.it', 'live.it', 'ntlworld.com', 'arcor.de', 
    'yahoo.co.id', 'frontiernet.net', 'hetnet.nl', 'live.com.au', 'yahoo.com.sg', 
    'zonnet.nl', 'club-internet.fr', 'juno.com', 'optusnet.com.au', 'blueyonder.co.uk', 
    'bluewin.ch', 'skynet.be', 'sympatico.ca', 'windstream.net', 'mac.com', 
    'centurytel.net', 'chello.nl', 'live.ca', 'aim.com', 'bigpond.net.au',
    'up.edu.ph', 'addu.edu.ph', 'ateneo.edu.ph', 'dlsu.edu.ph', 'ust.edu.ph', 'lu.edu.ph'
]

   
    email = email.strip()

    if not email:
        return "Email is required."

  
    local_part = email.split('@')[0]
    if len(local_part) > 64:
        return "The local part (before the '@') of the email address cannot exceed 64 characters."

   
    email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}(\.[a-z]{2,})?$')

    if not email_regex.match(email):
        return "Invalid email format. Please enter a valid email address."

    
    domain = email.split('@')[1]

    
    is_strict_gov_ph = any(re.fullmatch(f'^{provider}$', domain) for provider in valid_providers)

    if not is_strict_gov_ph:
        return f"Invalid email domain. {domain} is not a recognized email provider."

    return ""