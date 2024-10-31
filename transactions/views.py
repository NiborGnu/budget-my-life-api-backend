from rest_framework import generics, permissions
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionList(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Allow users to only access their own transactions
        return Transaction.objects.filter(profile__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Allow users to only access their own transactions
        return Transaction.objects.filter(profile__owner=self.request.user)
