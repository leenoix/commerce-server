from django.contrib.auth import logout, login
from django.db import transaction

from commerce.models.user import UserSession, User
from commerce.views import JsonView


class UserSignUpView(JsonView):
    REQUIRED_FIELDS = {
        'POST': {'phone_number', 'password'},
    }

    @transaction.atomic()
    def post(self, request):
        phone_number = request.POST['phone_number']
        if User.objects.filter(phone_number=phone_number).exists():
            return {'code': 'USER_EXISTS', 'message': 'Phone number has been registered'}, 400

        user = User(
            phone_number=request.POST['phone_number'],
        )
        user.set_random_username()
        user.set_password(request.POST['password'])

        user.save()

        request.session.flush()
        login(request, user)
        request.session.set_expiry(5184000)

        return {
            'code': 'success',
            'user': {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'phone_number': user.phone_number,
            }
        }


class UserSignInView(JsonView):
    REQUIRED_FIELDS = {'phone_number', 'password'}

    def post(self, request):
        user = User.objects.filter(
            customer__email=request.POST['phone_number'],
            deleted_at__isnull=True
        ).first()
        if not user:
            return dict(code='USER_NOT_FOUND', message='User is not found'), 401

        if not user.check_password(request.POST['password']):
            return {'code': 'INVALID_PASSWORD', 'message': 'Password is not valid'}, 401

        user.save()

        login(request, user)
        request.session.set_expiry(5184000)
        return {
            'code': 'success',
            'user': {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'phone_number': user.phone_number,
            }
        }


class UserSignOutView(JsonView):
    LOGIN_REQUIRED = True

    def get(self, request):
        UserSession.objects.filter(user=request.user).delete()
        logout(request)
        return {'code': 'success', 'message': 'success'}