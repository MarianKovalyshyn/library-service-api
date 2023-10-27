from datetime import datetime, timedelta
import pytz

from borrowing_service.models import Borrowing
from notifications_service.notification_function import send_telegram_message


def check_overdue_borrowings():
    today = datetime.now(pytz.utc)
    tomorrow = today + timedelta(days=1)

    borrowings = Borrowing.objects.all()

    overdue_borrowings = []
    for b in borrowings:
        if b.expected_return_date <= tomorrow and b.actual_return_date is None:
            overdue_borrowings.append(b)

    for borrowing in overdue_borrowings:
        message = f"Borrowing is overdue! Details: \n{borrowing}"
        send_telegram_message(message)
