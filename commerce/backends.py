from django.contrib.auth import backends
from commerce.models import User


class ModelBackend(backends.ModelBackend):

    UserModel = backends.UserModel

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
