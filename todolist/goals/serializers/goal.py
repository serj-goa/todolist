from typing import Type

from rest_framework import serializers as s
from rest_framework.exceptions import PermissionDenied

from core.serializers import ProfileSerializer
from goals.models import Board, BoardParticipant, Goal, GoalCategory, GoalComment


class GoalCategoryCreateSerializer(s.ModelSerializer):
    user = s.HiddenField(default=s.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user', 'is_deleted')
        fields = '__all__'

    def validate_board(self, value: Board):
        if value.is_deleted:
            raise s.ValidationError('Not allowed to delete category')

        if not BoardParticipant.objects.filter(
            board=value,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user=self.context['request'].user
        ).exists():
            raise s.ValidationError('You must be owner or writer')

        return value


class GoalCategorySerializer(s.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'board', )


class GoalCreateSerializer(s.ModelSerializer):
    category = s.PrimaryKeyRelatedField(queryset=GoalCategory.objects.filter(is_deleted=False))
    user = s.HiddenField(default=s.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', )

    def validate_category(self, value: GoalCategory):
        if self.context['request'].user != value.user:
            raise PermissionDenied

        if not BoardParticipant.objects.filter(
            board_id=value.board_id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user=self.context['request'].user,
        ).exists():
            raise PermissionDenied

        return value


class GoalSerializer(s.ModelSerializer):
    category = s.PrimaryKeyRelatedField(queryset=GoalCategory.objects.filter(is_deleted=False))

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', )

    def validate_category(self, value: Type[GoalCategory]):
        if self.context['request'].user != value.user:
            raise PermissionDenied

        return value


class GoalCommentCreateSerializer(s.ModelSerializer):
    user = s.HiddenField(default=s.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', )


class GoalCommentSerializer(s.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'goal', )
