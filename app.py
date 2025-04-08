from flask import Flask, render_template, request
import re
import dns.resolver
import socket

app = Flask(__name__)

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def get_domain(email):
    return email.split('@')[-1] if '@' in email else None

def check_mx_record(domain):
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except Exception:
        return False

def is_free_email(domain):
    common_free = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'protonmail.com']
    return domain.lower() in common_free

def is_disposable_email(domain):
    disposable = ['mailinator.com', 'tempmail.com', '10minutemail.com', 'guerrillamail.com']
    return domain.lower() in disposable

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    if request.method == 'POST':
        email = request.form['email']
        result['email'] = email

        if is_valid_email(email):
            domain = get_domain(email)
            result['domain'] = domain
            result['valid_format'] = True
            result['has_mx'] = check_mx_record(domain)
            result['free'] = is_free_email(domain)
            result['disposable'] = is_disposable_email(domain)
        else:
            result['valid_format'] = False

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)