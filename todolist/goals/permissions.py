from rest_framework import permissions as p

from goals.models import BoardParticipant, Goal, GoalCategory, Board, GoalComment


class IsOwnerOrReadOnly(p.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in p.SAFE_METHODS:
            return True

        return obj.user_id == request.user.id


class BoardPermission(p.IsAuthenticated):
    def has_object_permission(self, request, view, obj: Board):
        filters = {'user': request.user, 'board': obj}

        if request.method not in p.SAFE_METHODS:
            filters['role'] = BoardParticipant.Role.owner

        return BoardParticipant.objects.filter(**filters).exists()


class GoalCategoryPermissions(p.IsAuthenticated):
    def has_object_permission(self, request, view, obj: GoalCategory):
        filters = {'user': request.user, 'board': obj.board}

        if request.method not in p.SAFE_METHODS:
            filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]

        return BoardParticipant.objects.filter(**filters).exists()


class GoalPermissions(p.IsAuthenticated):
    def has_object_permission(self, request, view, obj: Goal):
        filters = {'user': request.user, 'board': obj.category.board}

        if request.method not in p.SAFE_METHODS:
            filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]

        return BoardParticipant.objects.filter(**filters).exists()


class CommentsPermissions(p.IsAuthenticated):
    def has_object_permission(self, request, view, obj: GoalComment):
        return any((
            request.method in p.SAFE_METHODS,
            obj.user_id == request.user.id
        ))
