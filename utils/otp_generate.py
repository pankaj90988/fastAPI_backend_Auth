import secrets,string

digits=string.digits

def generate_otp():
     otp=""
     for _ in range(6):
          otp+=secrets.choice(digits)
     return otp