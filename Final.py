import asyncio
from concurrent.futures import ThreadPoolExecutor
import random
import pandas as pd
from faker import Faker
import smtplib
import dns.resolver
import re
import os
import tkinter as tk
from tkinter import ttk
from threading import Thread

# Step:1 Generate Email address in this format username@domain.com
# Username(role) Part 
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

# Domain Platform Part
domains = [
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com", "icloud.com", "zoho.com", "mail.com", 
    "protonmail.com", "yandex.com", "gmx.com", "tutanota.com", "me.com", "live.com", "msn.com", "comcast.net", 
    "att.net", "verizon.net", "bellsouth.net", "me.com", "fastmail.com", "inbox.com", "hushmail.com", "lycos.com", 
    "mail.ru", "look.com", "webmail.co.za", "tiscali.co.uk", "rocketmail.com", "mailspring.com", "web.de",
    "rediffmail.com", "sbcglobal.net", "optonline.net", "163.com", "swissmail.com", "freenet.de", "rakuten.jp",
    "hushmail.com", "runbox.com", "laposte.net", "rediffmail.com", "126.com", "naver.com", "gmx.net", "rocketmail.com",
    "mail.ru", "yandex.ru", "zoho.com", "yeah.net", "qq.com"
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
]   # Country name part for bussiness email (tld)

# Email formats
email_formats = [
    "{first}{sp}{last}{e_number}@{domain}",         # Personal email format with number
    "{first}{sp}{last}@{domain}",                   # Personal email format
    "{first}{sp}{last}{e_number}@{business}{tld}",  # Custom Business format with number(username@bussiness.tld)
    "{first}{sp}{last}@{business}{tld}",            # Custom Business format(username@bussiness.tld)
    "{role}@{business}{tld}"                        # Custom Business format(role/department@bussiness.tld) 
                                                    # Custom Email Address Template
]

def generate_random_email():
    random_locale = random.choice(locales)
    fake = Faker(random_locale)
    random_name = fake.name()
    name_parts = random_name.split()
    first = name_parts[0].lower()
    last = name_parts[1].lower() if len(name_parts) > 1 else ""
    sp = random.choice(sp_character)
    role = random.choice(user_role)
    domain = random.choice(domains)
    business = random.choice(business_keywords)
    tld = random.choice(country_tlds)
    
    format_choice = random.choice(email_formats)
    email = format_choice.format(first=first, last=last, business=business, domain=domain, tld=tld, sp=sp, role=role, enumber=e_number)
    return {"Generated Email": email}

# Email validation regex
def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)

# Get MX record for a domain
def get_mx_record(domain):
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        return str(mx_records[0].exchange)
    except Exception:
        return None

# SMTP verification function
def smtp_verify(email):
    if not is_valid_email(email):
        return False
    
    domain = email.split('@')[1]
    mx_record = get_mx_record(domain)
    
    if mx_record is None:
        return False
    
    try:
        with smtplib.SMTP(mx_record) as server:
            server.set_debuglevel(0)  # Disable debug output
            server.helo()
            server.mail('l78482154@gmail.com')
            code, _ = server.rcpt(email)
            return code == 250
    except Exception:
        return False

# Save results to Excel file
def save_results_to_excel(active_emails, inactive_emails):
    output_dir = r'C:\Users\aoi\Desktop\email nuevo\Email_Scrapping'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'verified_emails.xlsx')
    
    df_active = pd.DataFrame(active_emails, columns=['Active Emails'])
    df_inactive = pd.DataFrame(inactive_emails, columns=['Inactive Emails'])

    with pd.ExcelWriter(output_path) as writer:
        df_active.to_excel(writer, sheet_name='Active Emails', index=False)
        df_inactive.to_excel(writer, sheet_name='Inactive Emails', index=False)

    return output_path

# Asynchronous email verification using threads for faster processing
def generate_and_verify_emails(progress_label, generated_label, active_label, inactive_label):
    total_to_generate = 10000
    generated_emails = []
    active_emails = []
    inactive_emails = []

    def verify_email(email_data):
        email = email_data['Generated Email']
        generated_emails.append(email)

        is_active = smtp_verify(email)
        if is_active:
            active_emails.append(email)
        else:
            inactive_emails.append(email)

        # Update UI labels in a thread-safe manner
        progress_label.config(text=f"Progreso: {len(generated_emails)}/{total_to_generate}")
        generated_label.config(text=f"Generados: {len(generated_emails)}")
        active_label.config(text=f"Activos: {len(active_emails)}")
        inactive_label.config(text=f"Inactivos: {len(inactive_emails)}")
        
        progress_label.update()
        generated_label.update()
        active_label.update()
        inactive_label.update()

    # Create threads for each email verification to run concurrently
    threads = []
    for _ in range(total_to_generate):
        email_data = generate_random_email()  # Assume this function generates a random email
        thread = Thread(target=verify_email, args=(email_data,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    save_results_to_excel(active_emails, inactive_emails)
    progress_label.config(text="¡Proceso completado!")

# Start the process in a separate thread to keep the UI responsive
def start_process(progress_label, generated_label, active_label, inactive_label):
    thread = Thread(target=generate_and_verify_emails, args=(progress_label, generated_label, active_label, inactive_label))
    thread.start()

# Interfaz Gráfica (GUI)
def setup_gui():
    root = tk.Tk()
    root.title("Generador y Verificador de Emails")
    
    # Set the size and position of the window
    root.geometry("400x200+800+400")  # Width x Height + X offset + Y offset

    progress_label = ttk.Label(root, text="Progreso: 0/0", font=("Arial", 12))
    progress_label.pack(pady=10)

    generated_label = ttk.Label(root, text="Generados: 0", font=("Arial", 12))
    generated_label.pack(pady=5)

    active_label = ttk.Label(root, text="Activos: 0", font=("Arial", 12))
    active_label.pack(pady=5)

    inactive_label = ttk.Label(root, text="Inactivos: 0", font=("Arial", 12))
    inactive_label.pack(pady=5)

    start_button = ttk.Button(root, text="Iniciar", command=lambda: start_process(progress_label, generated_label, active_label, inactive_label))
    start_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    setup_gui()
