from rest_framework.permissions import BasePermission


class IsGodownOperator(BasePermission):
    message = "Only godown operators can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'godown'


class IsFarmer(BasePermission):
    message = "Only farmers can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'farmer'


class IsConsumer(BasePermission):
    message = "Only consumers can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'consumer'


class IsTransporter(BasePermission):
    message = "Only transporters can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'transporter'


class IsAdminUser(BasePermission):
    message = "Only admins can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'