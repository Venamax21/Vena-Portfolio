from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import json
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail import Mail, Email
from django.views.decorators.csrf import csrf_exempt

# Normal page views
def home(request):
    return render(request, 'base/home.html')

def project(request):
    return render(request, 'base/project.html')

def about(request):
    return render(request, 'base/about.html')

def contact(request):
    return render(request, 'base/contact.html')

sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
print("API Key:", os.environ.get("SENDGRID_API_KEY"))


# Vue form POST endpoint
@csrf_exempt
def sendmail(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("📩 Form data received:", data)
            
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            phone_number = data.get('phone_number', '')
            email = data.get('email', '')
            subject = data.get('subject', 'New message from portfolio')
            message = data.get('message', '')

            # Combine names
            full_name = f"{first_name} {last_name}".strip()

            # Email body content
            content = (
                f"Name: {full_name}\n"
                f"Phone: {phone_number}\n"
                f"Email: {email}\n\n"
                f"Message:\n{message}"
            )

            # Create the SendGrid Mail object
            mail = Mail(
                from_email = os.environ.get("FROM_EMAIL"),
                to_emails='vena.jh123@gmail.com',     # your inbox
                subject=subject,
                plain_text_content=content,
            )

            # Optional: reply-to
            if email:
                mail.reply_to = Email(email)

            # Send email
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.send(mail)

            # Debug logs
            print("✅ SendGrid Response Code:", response.status_code)
            print("✅ SendGrid Response Body:", response.body)
            print("✅ SendGrid Headers:", response.headers)

            # 202 means SendGrid accepted it successfully
            if response.status_code == 202:
                return JsonResponse({"message": "Email sent successfully!"})
            else:
                return JsonResponse({"error": "Failed to send email", "status": response.status_code}, status=500)

        except Exception as e:
            print("❌ Error sending email:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)
