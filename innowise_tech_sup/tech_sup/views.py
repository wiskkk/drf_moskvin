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

    # @action(detail=True, methods=['partial_update'])
    # def status_update(self, request, pk):
    #     print('test2')
    #     ticket = self.get_object()
    #     print('test3')
    #     serializer = TicketSerializer(data=request.data)
    #     print('test4')
    #     if serializer.is_valid():
    #         ticket.status_update(serializer.validated_data['status'])
    #         ticket.save()
    #         print('test')
    #         return Response({'status': 'status update'})
    #     else:
    #         print('test1')
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # @action(detail=True, methods=['partial_update'])
    # def update_status(self, request, pk):
    #     if self.action == 'partial_update':
    #         saved_ticket = get_object_or_404(Ticket.objects.all(), pk=pk)
    #         data = request.data.get('ticket')
    #         serializer = TicketSerializer(instance=saved_ticket, data=data, partial=True)
    #         if serializer.is_valid(raise_exception=True):
    #             serializer.save()
    #             if saved_ticket.status == 'r':
    #                 print('test')
    #                 status_updated.delay(pk)
    #                 print('test1')
    #             print('test2')
    #         print('test3')
    #     return Response(serializer.data)

    # @action(detail=True, methods=['partial_update'])
    # def update_status(self, request, pk):
    #     saved_ticket = get_object_or_404(Ticket.objects.all(), pk=pk)
    #     # saved_ticket = self.get_object()
    #     if self.action == 'partial_update':
    #         data = request.data.get('ticket')
    #         serializer = TicketSerializer(instance=saved_ticket, data=data, partial=True)
    #         if serializer.is_valid(raise_exception=True):
    #             if Ticket.status == 'r':
    #                 status_updated.delay(pk)
    #                 print('test')
    #             print('test1')
    #             serializer.save()

    # if Ticket.status == 'r':
    #     send_mail('Subject',
    #               'Good job, your ticket has been decided',
    #               'artiom95moskvin@gmail.com',
    #               [UserProfile.email],
    #               fail_silently=False)


class AnswerViewSet(PermissionMixin):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
