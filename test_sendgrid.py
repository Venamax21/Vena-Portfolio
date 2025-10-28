
import os
from sendgrid import SendGridAPIClient

sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
response = sg.client.user.profile.get()
print(response.status_code)
