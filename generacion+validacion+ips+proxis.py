import random
import pandas as pd
from faker import Faker
import smtplib
import dns.resolver
import re
import os
import requests
from tkinter import ttk
from threading import Thread
import tkinter as tk

# Parámetros de generación de emails
locales = ['en_US', 'en_GB', 'fr_FR', 'de_DE', 'it_IT']
sp_character = ["", ".", "-", "_", "+"]
sp_weight = [0.4, 0.2, 0.2, 0.18, 0.02]
user_role = [
    'admin', 'ceo', 'hr', 'sales', 'marketing', 'it', 'finance', 'ops', 'legal', 
    'support', 'manager', 'developer', 'designer', 'analyst', 'team_lead', 
    'supervisor', 'founder', 'customer_support', 'business_dev', 'accountant'
]
domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com", "zoho.com"]
business_keywords = ["tech", "store", "media", "agency", "finance", "clinic", "marketing"]
country_tlds = [".us", ".ca", ".uk", ".fr", ".de", ".es", ".it", ".jp", ".cn", ".in"]

email_formats = [
    "{first}{sp}{last}{e_number}@{domain}",         # Personal con número
    "{first}{sp}{last}@{domain}",                   # Personal sin número
    "{first}{sp}{last}{e_number}@{business}{tld}",  # Business con número
    "{first}{sp}{last}@{business}{tld}",            # Business sin número
    "{role}@{business}{tld}"                        # Rol en empresa
]

def generate_random_email():
    random_locale = random.choice(locales)
    fake = Faker(random_locale)
    random_name = fake.name()
    name_parts = random_name.split()
    first = name_parts[0].lower()
    last = name_parts[1].lower() if len(name_parts) > 1 else ""
    sp = random.choice(sp_character)
    e_number = str(random.randint(1, 9999)) if random.random() < 0.5 else ""
    role = random.choice(user_role)
    domain = random.choice(domains)
    business = random.choice(business_keywords)
    tld = random.choice(country_tlds)
    
    format_choice = random.choice(email_formats)
    email = format_choice.format(first=first, last=last, e_number=e_number, business=business, domain=domain, tld=tld, sp=sp, role=role)
    return {"Generated Email": email}

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)

def get_mx_record(domain):
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        return str(mx_records[0].exchange)
    except:
        return None

# Validar correo usando SMTP
def smtp_verify(email):
    if not is_valid_email(email):
        return False
    domain = email.split('@')[1]
    mx_record = get_mx_record(domain)
    if mx_record is None:
        return False
    try:
        server = smtplib.SMTP(mx_record)
        server.helo()
        server.mail('test@example.com')
        code, _ = server.rcpt(email)
        server.quit()
        return code == 250
    except:
        return False

# Guardar resultados en Excel
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

# Proxies y validación de IPs
def load_proxies(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        return [line.strip() for line in f]

def is_proxy_active(proxy):
    try:
        response = requests.get("http://www.google.com", proxies={"http": proxy, "https": proxy}, timeout=5)
        return response.status_code == 200
    except:
        return False

def save_active_proxies(active_proxies, file_path):
    with open(file_path, 'w') as f:
        f.write("\n".join(active_proxies))

def is_ip_clean(ip):
    try:
        response = requests.get(f"https://api.spamhaus.org/lookup/{ip}")
        return response.status_code == 200 and "NOT LISTED" in response.text
    except:
        return False

def save_clean_ips(clean_ips, file_path):
    with open(file_path, 'w') as f:
        f.write("\n".join(clean_ips))

# Verificación con proxies
def smtp_verify_with_proxy(email, proxy):
    if not is_valid_email(email):
        return False
    domain = email.split('@')[1]
    mx_record = get_mx_record(domain)
    if mx_record is None:
        return False
    try:
        proxy_handler = {"http": proxy, "https": proxy}
        session = smtplib.SMTP(mx_record, timeout=10)
        session.ehlo()
        session.starttls(context=None, proxies=proxy_handler)
        session.mail("test@example.com")
        code, _ = session.rcpt(email)
        session.quit()
        return code == 250
    except:
        return False

# Generar emails y verificar
def generate_and_verify_emails_with_proxies(progress_label, generated_label, active_label, inactive_label):
    total_to_generate = 1000
    generated_emails = []
    active_emails = []
    inactive_emails = []
    
    proxies = load_proxies(r'C:\Users\aoi\Desktop\email nuevo\Email_Scrapping\proxis validos')
    
    for i in range(total_to_generate):
        email_data = generate_random_email()
        generated_emails.append(email_data['Generated Email'])
        proxy = random.choice(proxies) if proxies else None

        if proxy and not is_proxy_active(proxy):
            proxies.remove(proxy)

        is_active = smtp_verify_with_proxy(email_data['Generated Email'], proxy) if proxy else smtp_verify(email_data['Generated Email'])
        if is_active:
            active_emails.append(email_data['Generated Email'])
        else:
            inactive_emails.append(email_data['Generated Email'])

        # Actualización en GUI
        progress_label.config(text=f"Progreso: {i + 1}/{total_to_generate}")
        generated_label.config(text=f"Generados: {len(generated_emails)}")
        active_label.config(text=f"Activos: {len(active_emails)}")
        inactive_label.config(text=f"Inactivos: {len(inactive_emails)}")
        progress_label.update()
        generated_label.update()
        active_label.update()
        inactive_label.update()

    save_results_to_excel(active_emails, inactive_emails)
    save_active_proxies(proxies, r'C:\Users\aoi\Desktop\email nuevo\Email_Scrapping\proxis validos')
    progress_label.config(text="¡Proceso completado!")

# GUI
def setup_gui():
    root = tk.Tk()
    root.title("Generador y Verificador de Emails con Proxies")

    progress_label = ttk.Label(root, text="Progreso: 0/0", font=("Arial", 12))
    progress_label.pack(pady=10)

    generated_label = ttk.Label(root, text="Generados: 0", font=("Arial", 12))
    generated_label.pack(pady=5)

    active_label = ttk.Label(root, text="Activos: 0", font=("Arial", 12))
    active_label.pack(pady=5)

    inactive_label = ttk.Label(root, text="Inactivos: 0", font=("Arial", 12))
    inactive_label.pack(pady=5)

    start_button = ttk.Button(root, text="Iniciar", command=lambda: generate_and_verify_emails_with_proxies(progress_label, generated_label, active_label, inactive_label))
    start_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    setup_gui()
