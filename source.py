import random
import pandas as pd
from faker import Faker

# Predefined lists for each criterion
# Personal use domain platforms
domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com", "icloud.com", "zoho.com", "mail.com", 
    "protonmail.com", "yandex.com", "gmx.com", "tutanota.com", "me.com", "live.com", "msn.com", "comcast.net", 
    "att.net", "verizon.net", "bellsouth.net", "me.com", "fastmail.com", "inbox.com", "hushmail.com", "lycos.com", 
    "mail.ru", "look.com", "webmail.co.za", "tiscali.co.uk", "rocketmail.com", "mailspring.com",
    "rediffmail.com", "sbcglobal.net", "optonline.net"
]
# Business domain platforms (Bussiness+country tld)
business_keywords = ["com", "biz", "info", "org", "net", "co", "pro", "mobi", "tv", "me", "xyz", "name", "cloud", "online", "shop", "store", #general business
    "tech", "store", "shop", "fashion", "media", "agency", "finance", "law", "health", "clinic", #Industry-Specific Domains
    "education", "marketing", "consulting", "design", "photography", "realty", "accounting", #Industry-Specific Domains
    "architect", "construction", "restaurant", "auto", "music", "photo", "events", "insurance", #Industry-Specific Domains
    "financial", "insurance", "cloud", "ventures", "fund", "group", "jobs", "lawyer", #Industry-Specific Domains
    "company", "ventures", "fund", "group", "cloud", "jobs", "lawyer", "financial", "web", #Other Business-Related Domains
    "social", "online", "market", "ecommerce", "biz", "startup", "consulting", "brand", "network", #Other Business-Related Domains
    "trade", "solutions", "digital", "marketing", "service", "enterprise", "media", "mobile" #Other Business-Related Domains
]
country_tlds = [".us", ".ca", ".mx",  # North America
    ".br", ".ar", ".bo", ".cl", ".co", ".uy", ".ve", ".pe", ".ec", ".py",  # South America
    ".gt", ".cr", ".pa", ".hn", ".sv", ".ni", ".bz",  # Central America and Caribbean
    ".uk", ".fr", ".de", ".it", ".ru", ".es", ".nl", ".pl", ".se", ".ch", ".pt", ".gr", ".be", ".dk", ".no", ".ua", #Europe
    ".at", ".cz", ".fi", ".ie", ".hu", ".sk", ".ro", ".lt", ".lv", ".ee", ".bg", ".hr", ".si", ".is", ".al", ".mt", #Europe
    ".md", ".lu", ".li", ".ba", ".mk", ".me", ".rs", ".by", ".fo", ".sm", ".gi", ".im",  #Europe
    ".cn", ".jp", ".in", ".pk", ".sg", ".hk", ".th", ".vn", ".ph", ".id", ".my", ".kr", ".bd", ".lk", ".af", ".np", #Asia
    ".mn", ".kh", ".mm", ".la", ".bn", ".tw", ".ir", ".sa", ".ae", ".qa", ".kw", ".om", ".bh", ".ye", ".il", ".jo", #Asia
    ".sy", ".lb", ".iq", ".uz", ".kz", ".tm", ".tj", ".kg", ".az", ".ge", ".am", #Asia
    ".za", ".ng", ".eg", ".dz", ".ke", ".ma", ".gh", ".tn", ".et", ".ug", ".sd", ".cm", ".tz", ".zm", ".ci", ".sn", #Africa
    ".mz", ".bw", ".rw", ".na", ".bf", ".ga", ".mg", ".cg", ".cv", ".bj", ".ne", ".lr", ".tg", ".ss", ".sl", ".bi", #Africa
    ".ml", ".mw", ".gq", ".gw", ".so", ".td", ".er", ".mr", ".st", ".km", ".dj", ".sc", ".ly", ".ao", ".zw", ".ls", #Africa
    ".au", ".nz", ".fj", ".pg", ".sb", ".vu", ".to", ".ws", ".as", ".ck", ".tv", ".nf", ".nu", ".ki", ".fm", ".pw", ".mh" #Australis and Ocean
]


# List of available locales
locales = ['en_US', 'en_GB', 'fr_FR', 'de_DE', 'it_IT', 'ja_JP', 'zh_CN', 'ar_SA', 'ru_RU']

# Randomly choose a locale
random_locale = random.choice(locales)

# Initialize Faker with the chosen locale
fake = Faker(random_locale)

# Generate a random name
random_name = fake.name()
print(f"Random Name from {random_locale}: {random_name}")


first_names = ["Alice", "Bob", "Charlie", "Diana"]   
last_names = ["Smith", "Brown", "Ali", "Maxim", "Ben"]  #random name and number
sp_character = ["", ".", "-", "_", "+"]
sp_weight = [0.4, 0.2, 0.2, 0.1, 0.1]
#role = []  #role and department

# Email formats
email_formats = [
    "{first}{sp}{last}{e_number}@{domain}" #-Personal(username@domain) username:{first}{sp}{last}{e_number}

    #-Custom Business(username@bussiness)
    #-Role-Based Business Email Address Template(role@bussiness)
    #-Department-Based Email Address Template(department@bussiness)
    #-Custom Email Address Template
]

# Function to generate random email
def generate_random_email():
    first = random_name
    #first = random.choice(first_names).lower()
    last = random.choice(last_names).lower()
    business = random.choice(business_keywords).lower()
    domain = random.choice(domains).lower()
    tld = random.choice(country_tlds).lower()
    sp = random.choices(sp_character, weights=sp_weight, k=1)[0]
    e_number = random.randint(10, 999)
    
    format_choice = random.choice(email_formats)
    email = format_choice.format(first=first, last=last, business=business, domain=domain, tld=tld, sp=sp, e_number=e_number)
    return {"Generated Email": email}

# Generate multiple emails
email_data = [generate_random_email() for _ in range(10)]  # Generate 10000 email records

# Convert to DataFrame
df = pd.DataFrame(email_data)

# Save to Excel
output_file = "random_emails.xlsx"
df.to_excel(output_file, index=False)

# print("Data saved to {output_file}")






