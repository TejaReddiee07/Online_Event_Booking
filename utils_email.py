# utils_email.py
import smtplib
from email.mime.text import MIMEText
from config import Config


def _send_raw_email(to_email: str, subject: str, body: str):
    """Low-level email sender with proper TLS and error handling."""
    msg = MIMEText(body, _subtype="plain", _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = Config.MAIL_FROM
    msg["To"] = to_email

    # Guard against missing credentials
    if not Config.SMTP_USER or not Config.SMTP_PASSWORD:
        raise RuntimeError("SMTP credentials not configured")

    with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT, timeout=20) as server:
        if Config.SMTP_TLS:
            server.starttls()
        server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
        server.send_message(msg)


def send_booking_confirm_email(to_email, hall_name, hall_address,
                               from_date, to_date, total_price):
    subject = "Your hall booking is confirmed - EventHub"
    maps_link = (
        f"https://www.google.com/maps/search/?api=1&query="
        f"{hall_address.replace(' ', '+')}"
    )
    body = (
        "Dear Organizer,\n\n"
        "Your booking has been APPROVED!\n\n"
        f"Hall: {hall_name}\n"
        f"Address: {hall_address}\n"
        f"Google Maps: {maps_link}\n"
        f"Dates: {from_date} to {to_date}\n"
        f"Total Price: ₹{total_price}\n\n"
        "Regards,\n"
        "EventHub Team"
    )
    _send_raw_email(to_email, subject, body)


def send_booking_confirm_email_with_food(
    to_email,
    hall_name,
    hall_location,
    from_date,
    to_date,
    hall_price,
    food_details,
    total_amount,
    booking_id,
    base_url="https://online-event-booking-8.onrender.com",  # CHANGE: no localhost
):
    subject = "Your booking is confirmed - Payment Required - EventHub"
    payment_link = f"{base_url}/organizer/payment/{booking_id}"

    body = (
        "Dear Organizer,\n\n"
        "✅ Your booking has been APPROVED!\n\n"
        f"🏛️ Hall: {hall_name}\n"
        f"📍 Location: {hall_location}\n"
        f"📆 Dates: {from_date} to {to_date}\n"
        f"💰 Hall Price: ₹{hall_price}\n"
        f"{food_details}\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💳 TOTAL AMOUNT: ₹{total_amount}\n\n"
        "Complete your payment here:\n"
        f"{payment_link}\n\n"
        "Payment Options:\n"
        "• UPI: eventhub@upi\n"
        "• Card: Pay at venue counter\n"
        "• Cash: Accepted at venue\n\n"
        "You have booked hall and food for your event!\n\n"
        "Thank you for using EventHub!\n"
        "Team EventHub"
    )

    _send_raw_email(to_email, subject, body)
