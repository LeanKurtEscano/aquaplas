import re
from datetime import datetime

def validate_first_name(first_name: str) -> str:
    regex = r'^[A-Za-z\s]+$'
    repeated_char_regex = r'(.)\1{2,}'
    max_length = 20

    if not first_name:
        return "First name is required."
    if not re.match(regex, first_name.strip()):
        return "First name must not contain special characters or numbers."
    if len(first_name.strip()) < 2:
        return "First name must be at least 2 characters long."
    if len(first_name.strip()) > max_length:
        return f"First name must be at most {max_length} characters long."
    if re.search(repeated_char_regex, first_name.strip()):
        return "First name must not contain repeated characters."
    return ""

def validate_middle_name(middle_name: str) -> str:
    regex = r'^[A-Za-z\s]+$'
    repeated_char_regex = r'(.)\1{2,}'
    max_length = 20

    if middle_name:
        if not re.match(regex, middle_name.strip()):
            return "Middle name must not contain special characters or numbers."
        if len(middle_name.strip()) < 2:
            return "Middle name must be at least 2 characters long."
        if len(middle_name.strip()) > max_length:
            return f"Middle name must be at most {max_length} characters long."
        if re.search(repeated_char_regex, middle_name.strip()):
            return "Middle name must not contain repeated characters."
    return ""

def validate_last_name(last_name: str) -> str:
    regex = r'^[A-Za-z\s]+$'
    repeated_char_regex = r'(.)\1{2,}'
    max_length = 20

    if not last_name:
        return "Last name is required."
    if not re.match(regex, last_name.strip()):
        return "Last name must not contain special characters or numbers."
    if len(last_name.strip()) < 2:
        return "Last name must be at least 2 characters long."
    if len(last_name.strip()) > max_length:
        return f"Last name must be at most {max_length} characters long."
    if re.search(repeated_char_regex, last_name.strip()):
        return "Last name must not contain repeated characters."
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
        'gmail.com',
        'yahoo.com',
        'yahoo.com.ph',
        'outlook.com',
        'hotmail.com',
        'aol.com',
        'icloud.com',
        'gov.ph',
        'dfa.gov.ph',
        'dip.gov.ph',
        'deped.gov.ph',
        'neda.gov.ph',
        'doh.gov.ph',
        'dti.gov.ph',
        'dswd.gov.ph',
        'dbm.gov.ph',
        'pcso.gov.ph',
        'pnp.gov.ph',
        'bsp.gov.ph',
        'prc.gov.ph',
        'psa.gov.ph',
        'dpwh.gov.ph',
        'lto.gov.ph',
        'boi.gov.ph'
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