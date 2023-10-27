from django_q.models import Schedule

Schedule.objects.create(
    func="borrowing_service.utils.check_overdue_borrowings",
    schedule_type=Schedule.DAILY
)
