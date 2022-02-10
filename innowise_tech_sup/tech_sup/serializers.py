from rest_framework import serializers

from .models import Answer, Ticket, UserProfile


class FilterAnswerListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    is_staff = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        list_serializer_class = FilterAnswerListSerializer
        model = Answer
        fields = ('owner', 'parent', 'answer_text', 'ticket', 'children',)


class TicketSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Ticket
        fields = ('owner', 'owner_email', 'status', 'title', 'body', 'answers', 'updated_on')
