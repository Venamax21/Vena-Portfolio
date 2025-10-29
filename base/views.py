from django.shortcuts import render
from django.http import JsonResponse
import json
import os
from sendgrid import SendGridAPIClient
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


# Vue form POST endpoint
@csrf_exempt
def sendmail(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)
        print("📩 Form data received:", data)

        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        phone_number = data.get('phone_number', '')
        sender_email = data.get('email', '')
        subject = data.get('subject', 'New message from portfolio')
        message = data.get('message', '')

        full_name = f"{first_name} {last_name}".strip()
        content = f"Name: {full_name}\nPhone: {phone_number}\nEmail: {sender_email}\n\nMessage:\n{message}"

        # Read environment variables
        FROM_EMAIL = os.environ.get("FROM_EMAIL")
        SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

        if not FROM_EMAIL or not SENDGRID_API_KEY:
            raise ValueError("FROM_EMAIL or SENDGRID_API_KEY is not set in environment variables")

        print("DEBUG: FROM_EMAIL =", FROM_EMAIL)
        print("DEBUG: SENDGRID_API_KEY =", SENDGRID_API_KEY[:8] + "...")  # show only first 8 chars

        mail = Mail(
            from_email=FROM_EMAIL,
            to_emails='vena.jh123@gmail.com',
            subject=subject,
            plain_text_content=content,
        )

        if sender_email:
            mail.reply_to = Email(sender_email)

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(mail)

        print("✅ SendGrid Response Code:", response.status_code)

        if response.status_code == 202:
            return JsonResponse({"message": "Email sent successfully!"})
        else:
            return JsonResponse({"error": "Failed to send email", "status": response.status_code}, status=500)

    except Exception as e:
        print("❌ Error sending email:", e)
        return JsonResponse({"error": str(e)}, status=500)
