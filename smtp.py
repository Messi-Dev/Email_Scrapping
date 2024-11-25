import pandas as pd
import smtplib
import dns.resolver
import re

def validate_emails(email_list):
    active_emails = []
    inactive_emails = []

    for email in email_list:
        is_active, message = smtp_verify(email)
        if is_active:
            active_emails.append(email)
        else:
            inactive_emails.append(email)

    return active_emails, inactive_emails

def save_to_excel(active_emails, inactive_emails):
    df_active = pd.DataFrame(active_emails, columns=['Active Emails'])
    df_inactive = pd.DataFrame(inactive_emails, columns=['Inactive Emails'])

    with pd.ExcelWriter('verified_emails.xlsx') as writer:
        df_active.to_excel(writer, sheet_name='Active Emails', index=False)
        df_inactive.to_excel(writer, sheet_name='Inactive Emails', index=False)

# Example usage
if __name__ == "__main__":
    # Replace this list with your own emails
    emails_to_verify = [
        "shingomurakami9524@gmail.com",
        "user2@invalid.com",
        "user3@gmail.com"
    ]
    
    active_emails, inactive_emails = validate_emails(emails_to_verify)
    
    save_to_excel(active_emails, inactive_emails)
    
    print(f"Active emails: {len(active_emails)}, Inactive emails: {len(inactive_emails)}")