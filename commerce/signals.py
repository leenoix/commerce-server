from django.contrib.auth import user_logged_in

from commerce.models.user import UserSession


def user_logged_in_handler(sender, user, request, **kwargs):
    session, created = UserSession.objects.get_or_create(
        user=user,
        session_id=request.session.session_key,
    )

    old_sessions = UserSession.objects.select_related(
        'session'
    ).filter(
        user__phone_number=user.phone_number,
        user__deleted_at__isnull=True
    ).exclude(
        id=session.id,
        endpoint_arn=session.endpoint_arn
    )

    for row in old_sessions:
        if hasattr(row, 'session') and row.session:
            row.session.delete()
        row.delete()


user_logged_in.connect(user_logged_in_handler)
