from django.core.mail import send_mail
from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

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

    def patch(self, request, pk):
        saved_ticket = get_object_or_404(Ticket.objects.all(), pk=pk)
        data = request.data.get('ticket')
        serializer = TicketSerializer(instance=saved_ticket, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            if Ticket.status == 'r':
                send_mail('Subject',
                          'Good job, your ticket has been decided',
                          'artiom95moskvin@gmail.com',
                          [UserProfile.email],
                          fail_silently=False)
        return Response(serializer.data)


class AnswerViewSet(PermissionMixin):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
