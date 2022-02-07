from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserProfile, Ticket, Answer
from .serializers import UserProfileSerializer, TicketSerializer, AnswerSerializer
from .tasks import status_updated


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

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_updated.delay(kwargs.get('pk'))
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        serializer.save(owner_email=self.request.user.email)


class AnswerViewSet(PermissionMixin):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
