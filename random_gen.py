import random
import pandas as pd
from faker import Faker
import smtplib
import dns.resolver
import re

# Step:1 Generate Email address in this format username@domain.com
# -Username(role) Part 
locales = ['en_US', 'en_GB', 'fr_FR', 'de_DE', 'it_IT'] # List of available locales for random name generation for personal username

sp_character = ["", ".", "-", "_", "+"]   # username split part
sp_weight = [0.4, 0.2, 0.2, 0.18, 0.02]   # username split part random weight

user_role = [
    'admin', 'ceo', 'cfo', 'cto', 'hr', 'support', 'sales', 'marketing', 'it', 'finance', 
    'ops', 'legal', 'pr', 'recruitment', 'consultant', 'manager', 'director', 'assistant', 
    'customer_support', 'business_dev', 'operations_manager', 'coo', 'developer', 'product_manager', 
    'accountant', 'designer', 'analyst', 'team_lead', 'strategist', 'executive', 'assistant_manager', 
    'supervisor', 'chief_of_staff', 'founder', 'partner', 'head_of_sales', 'head_of_hr'                             #bussiness role

    'hr', 'sales', 'it', 'finance', 'marketing', 'legal', 'research', 'ops', 'design', 'engineering', 
    'operations', 'customer_service', 'admin', 'compliance', 'strategy', 'logistics', 'procurement', 
    'development', 'accounts', 'support', 'communications', 'product', 'project_management', 'quality_assurance', 
    'security', 'training', 'it_support', 'public_relations', 'customer_success', 'event_management', 
    'finance_team', 'marketing_team', 'legal_team', 'customer_care', 'business_operations', 'data_analytics'        
    'user_experience', 'data_science', 'brand_management'                                                           #bussiness department
]   #role and department for bussiness email

# -Domain Platform Part
domains = [
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com", "icloud.com", "zoho.com", "mail.com", 
    "protonmail.com", "yandex.com", "gmx.com", "tutanota.com", "me.com", "live.com", "msn.com", "comcast.net", 
    "att.net", "verizon.net", "bellsouth.net", "me.com", "fastmail.com", "inbox.com", "hushmail.com", "lycos.com", 
    "mail.ru", "look.com", "webmail.co.za", "tiscali.co.uk", "rocketmail.com", "mailspring.com",
    "rediffmail.com", "sbcglobal.net", "optonline.net"
]   # Domain platforms for personal user 

business_keywords = [
    "com", "biz", "info", "org", "net", "co", "pro", "mobi", "tv", "me", "name", "cloud", "online", "shop", "store",#general business
    "tech", "store", "shop", "fashion", "media", "agency", "finance", "law", "health", "clinic",                    #Industry-Specific Domains
    "education", "marketing", "consulting", "design", "photography", "realty", "accounting",                        #Industry-Specific Domains
    "architect", "construction", "restaurant", "auto", "music", "photo", "events", "insurance",                     #Industry-Specific Domains
    "financial", "insurance", "cloud", "ventures", "fund", "group", "jobs", "lawyer",                               #Industry-Specific Domains
    "company", "ventures", "fund", "group", "cloud", "jobs", "lawyer", "financial", "web",                          #Other Business-Related Domains
    "social", "online", "market", "ecommerce", "biz", "startup", "consulting", "brand", "network",                  #Other Business-Related Domains
    "trade", "solutions", "digital", "marketing", "service", "enterprise", "media", "mobile"                        #Other Business-Related Domains
]   # Business domain platforms (Bussiness + country tld)

country_tlds = [".us", ".ca", ".mx",                                                                                # North America
    ".br", ".ar", ".bo", ".cl", ".co", ".uy", ".ve", ".pe", ".ec", ".py",                                           # South America
    ".gt", ".cr", ".pa", ".hn", ".sv", ".ni", ".bz",                                                                # Central America and Caribbean
    ".uk", ".fr", ".de", ".it", ".ru", ".es", ".nl", ".pl", ".se", ".ch", ".pt", ".gr", ".be", ".dk", ".no", ".ua", #Europe
    ".at", ".cz", ".fi", ".ie", ".hu", ".sk", ".ro", ".lt", ".lv", ".ee", ".bg", ".hr", ".si", ".is", ".al", ".mt", #Europe
    ".md", ".lu", ".li", ".ba", ".mk", ".me", ".rs", ".by", ".fo", ".sm", ".gi", ".im",                             #Europe
    ".cn", ".jp", ".in", ".pk", ".sg", ".hk", ".th", ".vn", ".ph", ".id", ".my", ".kr", ".bd", ".lk", ".af", ".np", #Asia
    ".mn", ".kh", ".mm", ".la", ".bn", ".tw", ".ir", ".sa", ".ae", ".qa", ".kw", ".om", ".bh", ".ye", ".il", ".jo", #Asia
    ".sy", ".lb", ".iq", ".uz", ".kz", ".tm", ".tj", ".kg", ".az", ".ge", ".am",                                    #Asia
    ".za", ".ng", ".eg", ".dz", ".ke", ".ma", ".gh", ".tn", ".et", ".ug", ".sd", ".cm", ".tz", ".zm", ".ci", ".sn", #Africa
    ".mz", ".bw", ".rw", ".na", ".bf", ".ga", ".mg", ".cg", ".cv", ".bj", ".ne", ".lr", ".tg", ".ss", ".sl", ".bi", #Africa
    ".ml", ".mw", ".gq", ".gw", ".so", ".td", ".er", ".mr", ".st", ".km", ".dj", ".sc", ".ly", ".ao", ".zw", ".ls", #Africa
    ".au", ".nz", ".fj", ".pg", ".sb", ".vu", ".to", ".ws", ".as", ".ck", ".tv", ".nf", ".nu", ".ki", ".fm", ".pw"  #Australis and Ocean
]   # Country name part for bussiness email

# Email formats
email_formats = [
    "{first}{sp}{last}{e_number}@{domain}",         # Personal email format with number
    "{first}{sp}{last}@{domain}",                   # Personal email format
    "{first}{sp}{last}{e_number}@{business}{tld}",  # Custom Business format with number(username@bussiness.tld)
    "{first}{sp}{last}@{business}{tld}",            # Custom Business format(username@bussiness.tld)
    "{role}@{business}{tld}"                        # Custom Business format(role/department@bussiness.tld) 
                                                    # Custom Email Address Template
]

# Function to generate a random email
def generate_random_email():

    # username format
    random_locale = random.choice(locales)          # Randomly choose a locale
    fake = Faker(random_locale)                     # Initialize Faker with the chosen locale
    random_name = fake.name()                       # Generate a random name for every email
    name_parts = random_name.split()                # Split the name into parts (first and last)

    if len(name_parts) == 1:                        # Split random_name into first and last name for email generation
        first = name_parts[0].lower()
        last = ""                                   # No last name
    else:
        first = name_parts[0].lower()
        last = name_parts[1].lower()
    sp = random.choice(sp_character)    # Special characters 
    e_number = random.randint(10, 999)              # Random number for email uniqueness 
    role = random.choice(user_role)                 # username format for business

    # domain format
    domain = random.choice(domains).lower()         
    business = random.choice(business_keywords).lower()
    tld = random.choice(country_tlds).lower()

    # email format   
    format_choice = random.choice(email_formats)
    email = format_choice.format(first=first, last=last, business=business, domain=domain, tld=tld, sp=sp, e_number=e_number, role=role)
    return {"Generated Email": email}

# Generate multiple emails
generated_email_data = [generate_random_email() for _ in range(1000)]

# Convert to DataFrame
df_emails = pd.DataFrame(generated_email_data)

# Save to Excel
output_file = "random_generated_emails.xlsx"
df_emails.to_excel(output_file, index=False)

# Confirm the process
print(f"Random generated emails are saved to {output_file}")


# Step:2 Verify Email Addresses Using SMTP
# Email Format Validation is true?
def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)

# MX Record Retrieval
def get_mx_record(domain):
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        return str(mx_records[0].exchange)
    except Exception as e:
        print(f"MX record lookup failed for {domain}: {e}")
        return None

# SMTP Verification of domain
def smtp_verify(email):
    if not is_valid_email(email):
        return False
    
    domain = email.split('@')[1]
    mx_record = get_mx_record(domain)
    
    if mx_record is None:
        return False

    try:
        server = smtplib.SMTP(mx_record)
        server.set_debuglevel(0)  # Set to 1 for debugging output
        server.helo()   # sends a HELO command to identify the client to the mail server.
        
        server.mail('shingomurakami9524@gmail.com')  # Use a valid sender address
        code, message = server.rcpt(email)  # Check recipient
        
        server.quit()
        
        return code == 250
    
    except Exception as e:
        print(f"Error during verification for {email}: {e}")
        return False


# Step:3 Validate Emails and Save Results
# Validation of email
def validate_emails(email_list):
    active_emails = []
    inactive_emails = []

    for email in email_list:
        is_active = smtp_verify(email['Generated Email'])
        if is_active:
            active_emails.append(email['Generated Email'])
        else:
            inactive_emails.append(email['Generated Email'])

    return active_emails, inactive_emails

# Classify active or inactive email and save to excel
def save_results_to_excel(active_emails, inactive_emails):
    df_active = pd.DataFrame(active_emails, columns=['Active Emails'])
    df_inactive = pd.DataFrame(inactive_emails, columns=['Inactive Emails'])

    with pd.ExcelWriter('verified_emails.xlsx') as writer:
        df_active.to_excel(writer, sheet_name='Active Emails', index=False)
        df_inactive.to_excel(writer, sheet_name='Inactive Emails', index=False)

# Main Execution Block
if __name__ == "__main__":
    # Load previously generated emails from Excel or generate new ones
    df_generated_emails = pd.read_excel("random_generated_emails.xlsx")
    
    active_emails, inactive_emails = validate_emails(df_generated_emails.to_dict(orient='records'))
    
    save_results_to_excel(active_emails, inactive_emails)
    
    print(f"Active emails: {len(active_emails)}, Inactive emails: {len(inactive_emails)}")

