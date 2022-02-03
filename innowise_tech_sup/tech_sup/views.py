from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, Ticket, Answer
from .serializers import UserProfileSerializer, TicketSerializer, AnswerSerializer


class PermissionMixin(viewsets.ModelViewSet):

    def get_permissions(self):
        if self.action == 'update':  # put
            permission_classes = [permissions.IsAdminUser]
        elif self.action == 'create':  # post
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'partial_update':  # patch
            permission_classes = [permissions.IsAdminUser]
        elif self.action == 'destroy':  # delete
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class TicketViewSet(PermissionMixin):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AnswerViewSet(PermissionMixin):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
