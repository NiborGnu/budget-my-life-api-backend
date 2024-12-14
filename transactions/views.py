from django.db.models import Sum
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionList(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.filter(profile__owner=user)
        category_id = self.request.query_params.get('category_id')
        subcategory_id = self.request.query_params.get('subcategory_id')

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(profile__owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class TransactionSummary(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        transactions = Transaction.objects.filter(profile__owner=user)

        income_total = transactions.filter(
            transaction_type='income'
        ).aggregate(total=Sum('amount'))['total'] or 0
        expense_total = transactions.filter(
            transaction_type='expense'
        ).aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            'income': income_total,
            'expense': expense_total,
        })
