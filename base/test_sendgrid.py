import os
from sendgrid import SendGridAPIClient

sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

try:
    response = sg.client.user.profile.get()
    print("✅ API Key works! Status code:", response.status_code)
except Exception as e:
    print("❌ Error:", e)


# EXPECTED RESPONSE \ SENDGRIT & DJANGO

#✅ SendGrid Response Code: 202
#✅ SendGrid Response Body: b''
#✅ SendGrid Headers: Server: nginx
