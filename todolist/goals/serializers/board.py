from django.db import transaction
from rest_framework import serializers as s

from core.models import CustomUser
from goals.models import Board, BoardParticipant


class BoardCreateSerializer(s.ModelSerializer):
    user = s.HiddenField(default=s.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ('id', 'is_deleted', 'created', 'updated')
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(user=user, board=board, role=BoardParticipant.Role.owner)

        return board


class BoardParticipantSerializer(s.ModelSerializer):
    role = s.ChoiceField(required=True, choices=BoardParticipant.Role.choices[1:])
    user = s.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())

    class Meta:
        model = BoardParticipant
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'board')


class BoardSerializer(s.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = s.HiddenField(default=s.CurrentUserDefault())

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated')

    def update(self, instance, validated_data):
        owner = validated_data.pop('user')
        new_participants = validated_data.pop('participants')
        new_by_id = {part['user'].id: part for part in new_participants}

        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:

                if old_participant.user_id not in new_by_id:
                    old_participant.delete()

                else:
                    if old_participant.role != new_by_id[old_participant.user_id]['role']:
                        old_participant.role = new_by_id[old_participant.user_id]['role']
                        old_participant.save()

                    new_by_id.pop(old_participant.user_id)

            for new_part in new_by_id.values():
                BoardParticipant.objects.create(board=instance, user=new_part['user'], role=new_part['role'])

            if title := validated_data.get('title'):
                instance.title = title
                instance.save()

        return instance


class BoardListSerializer(s.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'
