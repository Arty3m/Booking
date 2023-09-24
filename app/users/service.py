from app.service.mixins import ServiceMixin
from app.users.model import Users


class UserService(ServiceMixin):
    model = Users
