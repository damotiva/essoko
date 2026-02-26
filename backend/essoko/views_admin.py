# views_admin.py  — Admin-only API views
# Add to your urls.py:  path('api/admin/', include('essoko.urls_admin'))

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum

from .models import User, Godown, ProduceCategory, FarmerDelivery, StockListing, Order, TransportJob
from .serializers import (
    UserSerializer, GodownSerializer, ProduceCategorySerializer,
    FarmerDeliverySerializer, StockListingSerializer, OrderSerializer, TransportJobSerializer
)
from .permissions import IsAdminUser


# ─────────────────────────────────────────────
# STATS
# ─────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdminUser])
def admin_stats(request):
    return Response({
        'total_users':        User.objects.count(),
        'total_farmers':      User.objects.filter(role='farmer').count(),
        'total_consumers':    User.objects.filter(role='consumer').count(),
        'total_transporters': User.objects.filter(role='transporter').count(),
        'total_godowns':      Godown.objects.filter(is_active=True).count(),
        'total_listings':     StockListing.objects.filter(status='available').count(),
        'total_orders':       Order.objects.count(),
        'pending_orders':     Order.objects.filter(status='pending').count(),
        'completed_orders':   Order.objects.filter(status='completed').count(),
        'total_deliveries':   FarmerDelivery.objects.count(),
    })


# ─────────────────────────────────────────────
# USERS
# ─────────────────────────────────────────────

class AdminUserListView(generics.ListAPIView):
    """GET /api/admin/users/"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        qs = User.objects.all().order_by('-date_joined')
        role     = self.request.query_params.get('role')
        verified = self.request.query_params.get('verified')
        search   = self.request.query_params.get('search')
        if role:     qs = qs.filter(role=role)
        if verified: qs = qs.filter(is_verified=verified == 'true')
        if search:   qs = qs.filter(first_name__icontains=search) | qs.filter(phone__icontains=search)
        return qs


class AdminUserDetailView(generics.RetrieveDestroyAPIView):
    """GET / DELETE /api/admin/users/<id>/"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    queryset = User.objects.all()


class AdminVerifyUserView(APIView):
    """POST /api/admin/users/<id>/verify/"""
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def post(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            user.is_verified = True
            user.save()
            return Response(UserSerializer(user).data)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)


# ─────────────────────────────────────────────
# GODOWNS
# ─────────────────────────────────────────────

class AdminGodownListView(generics.ListAPIView):
    """GET /api/admin/godowns/"""
    serializer_class = GodownSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    queryset = Godown.objects.all().order_by('-created_at')


class AdminGodownDetailView(generics.RetrieveUpdateAPIView):
    """GET / PATCH /api/admin/godowns/<id>/"""
    serializer_class = GodownSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    queryset = Godown.objects.all()


# ─────────────────────────────────────────────
# ORDERS
# ─────────────────────────────────────────────

class AdminOrderListView(generics.ListAPIView):
    """GET /api/admin/orders/"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        qs = Order.objects.all().select_related(
            'consumer', 'listing', 'listing__category', 'godown'
        ).order_by('-ordered_at')
        status = self.request.query_params.get('status')
        search = self.request.query_params.get('search')
        if status: qs = qs.filter(status=status)
        if search: qs = qs.filter(consumer__first_name__icontains=search)
        return qs


# ─────────────────────────────────────────────
# DELIVERIES
# ─────────────────────────────────────────────

class AdminDeliveryListView(generics.ListAPIView):
    """GET /api/admin/deliveries/"""
    serializer_class = FarmerDeliverySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        qs = FarmerDelivery.objects.all().select_related(
            'farmer', 'godown', 'category'
        ).order_by('-delivered_at')
        s = self.request.query_params.get('status')
        if s: qs = qs.filter(status=s)
        return qs


# ─────────────────────────────────────────────
# LISTINGS
# ─────────────────────────────────────────────

class AdminListingListView(generics.ListAPIView):
    """GET /api/admin/listings/"""
    serializer_class = StockListingSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        qs = StockListing.objects.all().select_related('godown', 'category').order_by('-created_at')
        s = self.request.query_params.get('status')
        if s: qs = qs.filter(status=s)
        return qs


# ─────────────────────────────────────────────
# TRANSPORT
# ─────────────────────────────────────────────

class AdminTransportListView(generics.ListAPIView):
    """GET /api/admin/transport/"""
    serializer_class = TransportJobSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        qs = TransportJob.objects.all().select_related('transporter', 'order').order_by('-created_at')
        s = self.request.query_params.get('status')
        if s: qs = qs.filter(status=s)
        return qs


# ─────────────────────────────────────────────
# CATEGORIES  (full CRUD for admin)
# ─────────────────────────────────────────────

class AdminCategoryListCreateView(generics.ListCreateAPIView):
    """GET / POST /api/admin/categories/"""
    serializer_class = ProduceCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    queryset = ProduceCategory.objects.all()


class AdminCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET / PUT / DELETE /api/admin/categories/<id>/"""
    serializer_class = ProduceCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    queryset = ProduceCategory.objects.all()

