from django.db import transaction
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from goals.models import Board, Goal
from goals.permissions import BoardPermission
from goals.serializers import BoardSerializer, BoardListSerializer, BoardCreateSerializer


class BoardCreateView(CreateAPIView):
    permission_classes = [BoardPermission]
    serializer_class = BoardCreateSerializer


class BoardListView(ListAPIView):
    model = BoardPermission
    permission_classes = [BoardPermission]
    serializer_class = BoardListSerializer
    ordering = ['title']

    def get_queryset(self):
        return Board.objects.filter(
            participants__user_id=self.request.user.id,
            is_deleted=False,
        )


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [BoardPermission]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.prefetch_related('participants').filter(
            participants__user_id=self.request.user.id,
            is_deleted=False,
        )

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted', ))
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)

        return instance
