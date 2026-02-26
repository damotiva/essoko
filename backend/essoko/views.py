from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    User, Farmer, Godown, ProduceCategory,
    FarmerDelivery, StockListing, Order, TransportJob
)
from .serializers import (
    RegisterSerializer, UserSerializer, FarmerProfileSerializer,
    GodownSerializer, ProduceCategorySerializer,
    FarmerDeliverySerializer, StockListingSerializer,
    StockListingCreateSerializer, OrderSerializer,
    OrderCreateSerializer, TransportJobSerializer
)
from .permissions import IsGodownOperator, IsFarmer, IsConsumer, IsTransporter


# ══════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════

class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Issue JWT tokens on registration
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


class MeView(generics.RetrieveUpdateAPIView):
    """GET/PUT /api/auth/me/"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ══════════════════════════════════════════
# FARMER PROFILE
# ══════════════════════════════════════════

class FarmerProfileView(generics.RetrieveUpdateAPIView):
    """GET/PUT /api/farmers/profile/"""
    serializer_class = FarmerProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsFarmer]

    def get_object(self):
        profile, _ = Farmer.objects.get_or_create(user=self.request.user)
        return profile


# ══════════════════════════════════════════
# GODOWN
# ══════════════════════════════════════════

class GodownListView(generics.ListAPIView):
    """GET /api/godowns/ — Public list of all active godowns"""
    serializer_class = GodownSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Godown.objects.filter(is_active=True)


class GodownDetailView(generics.RetrieveAPIView):
    """GET /api/godowns/<id>/ — Single godown detail"""
    serializer_class = GodownSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Godown.objects.filter(is_active=True)


class MyGodownView(generics.ListCreateAPIView):
    """GET/POST /api/godowns/mine/ — Operator manages their godowns"""
    serializer_class = GodownSerializer
    permission_classes = [permissions.IsAuthenticated, IsGodownOperator]

    def get_queryset(self):
        return Godown.objects.filter(operator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(operator=self.request.user)


class MyGodownUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/godowns/mine/<id>/"""
    serializer_class = GodownSerializer
    permission_classes = [permissions.IsAuthenticated, IsGodownOperator]

    def get_queryset(self):
        return Godown.objects.filter(operator=self.request.user)


# ══════════════════════════════════════════
# PRODUCE CATEGORIES
# ══════════════════════════════════════════

class ProduceCategoryListView(generics.ListAPIView):
    """GET /api/categories/ — All produce categories"""
    serializer_class = ProduceCategorySerializer
    permission_classes = [permissions.AllowAny]
    queryset = ProduceCategory.objects.all()


# ══════════════════════════════════════════
# FARMER DELIVERIES  (Farmer → Godown)
# ══════════════════════════════════════════

class FarmerDeliveryListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/deliveries/         — Farmer sees their own deliveries
    POST /api/deliveries/         — Farmer records a new delivery to a godown
    """
    serializer_class = FarmerDeliverySerializer
    permission_classes = [permissions.IsAuthenticated, IsFarmer]

    def get_queryset(self):
        return FarmerDelivery.objects.filter(farmer=self.request.user).order_by('-delivered_at')

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)


class GodownIncomingDeliveriesView(generics.ListAPIView):
    """
    GET /api/godowns/<godown_id>/deliveries/
    Godown operator sees all incoming farmer deliveries
    """
    serializer_class = FarmerDeliverySerializer
    permission_classes = [permissions.IsAuthenticated, IsGodownOperator]

    def get_queryset(self):
        godown_id = self.kwargs['godown_id']
        return FarmerDelivery.objects.filter(
            godown__id=godown_id,
            godown__operator=self.request.user
        ).order_by('-delivered_at')


class DeliveryAcceptView(APIView):
    """
    POST /api/deliveries/<id>/accept/
    Godown operator accepts the delivery — changes status to 'accepted'
    """
    permission_classes = [permissions.IsAuthenticated, IsGodownOperator]

    def post(self, request, pk):
        try:
            delivery = FarmerDelivery.objects.get(
                id=pk, godown__operator=request.user
            )
        except FarmerDelivery.DoesNotExist:
            return Response({'error': 'Delivery not found.'}, status=404)

        if delivery.status != 'pending':
            return Response({'error': 'Delivery already processed.'}, status=400)

        delivery.status = 'accepted'
        delivery.save()
        return Response(FarmerDeliverySerializer(delivery).data)


class DeliveryRejectView(APIView):
    """POST /api/deliveries/<id>/reject/"""
    permission_classes = [permissions.IsAuthenticated, IsGodownOperator]

    def post(self, request, pk):
        try:
            delivery = FarmerDelivery.objects.get(
                id=pk, godown__operator=request.user
            )
        except FarmerDelivery.DoesNotExist:
            return Response({'error': 'Delivery not found.'}, status=404)

        delivery.status = 'rejected'
        delivery.save()
        return Response(FarmerDeliverySerializer(delivery).data)


# ══════════════════════════════════════════
# STOCK LISTINGS  (Godown → Website)
# ══════════════════════════════════════════

class StockListingPublicView(generics.ListAPIView):
    """
    GET /api/listings/
    Public: All available stock listings consumers can browse.
    Supports filtering by ?category=&godown=&min_price=&max_price=
    """
    serializer_class = StockListingSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = StockListing.objects.filter(
            status__in=['available', 'low_stock']
        ).select_related('godown', 'category')

        category = self.request.query_params.get('category')
        godown   = self.request.query_params.get('godown')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if category:
            qs = qs.filter(category__id=category)
        if godown:
            qs = qs.filter(godown__id=godown)
        if min_price:
            qs = qs.filter(price_per_kg__gte=min_price)
        if max_price:
            qs = qs.filter(price_per_kg__lte=max_price)

        return qs


class StockListingDetailView(generics.RetrieveAPIView):
    """GET /api/listings/<id>/ — Single listing detail"""
    serializer_class = StockListingSerializer
    permission_classes = [permissions.AllowAny]
    queryset = StockListing.objects.all()


class GodownStockManageView(generics.ListCreateAPIView):
    """
    GET  /api/godowns/<godown_id>/stock/  — Godown sees their own listings
    POST /api/godowns/<godown_id>/stock/  — Godown creates a new listing
    """
    permission_classes = [permissions.IsAuthenticated, IsGodownOperator]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StockListingCreateSerializer
        return StockListingSerializer

    def get_queryset(self):
        return StockListing.objects.filter(
            godown__id=self.kwargs['godown_id'],
            godown__operator=self.request.user
        )

    def perform_create(self, serializer):
        godown = Godown.objects.get(
            id=self.kwargs['godown_id'],
            operator=self.request.user
        )
        serializer.save(godown=godown)


class GodownStockDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PUT/DELETE /api/godowns/<godown_id>/stock/<id>/
    Godown operator updates or removes a listing
    """
    permission_classes = [permissions.IsAuthenticated, IsGodownOperator]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return StockListingCreateSerializer
        return StockListingSerializer

    def get_queryset(self):
        return StockListing.objects.filter(
            godown__id=self.kwargs['godown_id'],
            godown__operator=self.request.user
        )


# ══════════════════════════════════════════
# ORDERS  (Consumer places order)
# ══════════════════════════════════════════

class PlaceOrderView(generics.CreateAPIView):
    """
    POST /api/orders/
    Consumer places an order on a StockListing.
    Auto-locks price & deducts from godown stock.
    """
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsConsumer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class MyOrdersView(generics.ListAPIView):
    """GET /api/orders/mine/ — Consumer sees their own orders"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsConsumer]

    def get_queryset(self):
        return Order.objects.filter(consumer=self.request.user).select_related(
            'listing', 'godown', 'listing__category'
        )


class OrderDetailView(generics.RetrieveAPIView):
    """GET /api/orders/<id>/ — Single order detail"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'consumer':
            return Order.objects.filter(consumer=user)
        if user.role == 'godown':
            return Order.objects.filter(godown__operator=user)
        return Order.objects.none()


class GodownOrdersView(generics.ListAPIView):
    """GET /api/godowns/<godown_id>/orders/ — Godown sees incoming orders"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsGodownOperator]

    def get_queryset(self):
        return Order.objects.filter(
            godown__id=self.kwargs['godown_id'],
            godown__operator=self.request.user
        ).select_related('consumer', 'listing', 'listing__category')


class OrderStatusUpdateView(APIView):
    """
    POST /api/orders/<id>/confirm/   → Godown confirms order
    POST /api/orders/<id>/ready/     → Godown marks ready for pickup
    POST /api/orders/<id>/complete/  → Godown/Transporter marks completed
    POST /api/orders/<id>/cancel/    → Consumer or Godown cancels
    """
    permission_classes = [permissions.IsAuthenticated]

    STATUS_TRANSITIONS = {
        'confirm':  ('pending',   'confirmed',  'confirmed_at'),
        'ready':    ('confirmed', 'ready',      'ready_at'),
        'complete': ('ready',     'completed',  'completed_at'),
        'cancel':   (None,        'cancelled',  None),
    }

    def post(self, request, pk, action):
        if action not in self.STATUS_TRANSITIONS:
            return Response({'error': 'Invalid action.'}, status=400)

        try:
            # Godown operators and consumers can access relevant orders
            if request.user.role == 'godown':
                order = Order.objects.get(id=pk, godown__operator=request.user)
            elif request.user.role == 'consumer':
                order = Order.objects.get(id=pk, consumer=request.user)
            else:
                return Response({'error': 'Forbidden.'}, status=403)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=404)

        required_status, new_status, timestamp_field = self.STATUS_TRANSITIONS[action]

        if required_status and order.status != required_status:
            return Response(
                {'error': f"Order must be '{required_status}' to perform this action. Current: '{order.status}'"},
                status=400
            )

        order.status = new_status
        if timestamp_field:
            setattr(order, timestamp_field, timezone.now())
        order.save()

        return Response(OrderSerializer(order).data)


# ══════════════════════════════════════════
# TRANSPORT JOBS
# ══════════════════════════════════════════

class OpenTransportJobsView(generics.ListAPIView):
    """GET /api/transport/jobs/ — Transporter sees all open jobs"""
    serializer_class = TransportJobSerializer
    permission_classes = [permissions.IsAuthenticated, IsTransporter]

    def get_queryset(self):
        return TransportJob.objects.filter(status='open').select_related(
            'order', 'order__godown', 'order__listing__category'
        )


class AssignTransportJobView(APIView):
    """POST /api/transport/jobs/<id>/assign/ — Transporter assigns themselves"""
    permission_classes = [permissions.IsAuthenticated, IsTransporter]

    def post(self, request, pk):
        try:
            job = TransportJob.objects.get(id=pk, status='open')
        except TransportJob.DoesNotExist:
            return Response({'error': 'Job not available.'}, status=404)

        job.transporter = request.user
        job.status = 'assigned'
        job.assigned_at = timezone.now()
        job.save()

        # Update order status to in_transit
        job.order.status = 'in_transit'
        job.order.save()

        return Response(TransportJobSerializer(job).data)


class UpdateTransportStatusView(APIView):
    """
    POST /api/transport/jobs/<id>/pickup/   — Mark as picked up from godown
    POST /api/transport/jobs/<id>/deliver/  — Mark as delivered to consumer
    """
    permission_classes = [permissions.IsAuthenticated, IsTransporter]

    def post(self, request, pk, action):
        try:
            job = TransportJob.objects.get(id=pk, transporter=request.user)
        except TransportJob.DoesNotExist:
            return Response({'error': 'Job not found.'}, status=404)

        if action == 'pickup':
            if job.status != 'assigned':
                return Response({'error': 'Must be assigned first.'}, status=400)
            job.status = 'picked_up'
            job.picked_up_at = timezone.now()

        elif action == 'deliver':
            if job.status != 'picked_up':
                return Response({'error': 'Must be picked up first.'}, status=400)
            job.status = 'delivered'
            job.delivered_at = timezone.now()
            job.order.status = 'completed'
            job.order.completed_at = timezone.now()
            job.order.save()

        else:
            return Response({'error': 'Invalid action.'}, status=400)

        job.save()
        return Response(TransportJobSerializer(job).data)


class MyTransportJobsView(generics.ListAPIView):
    """GET /api/transport/jobs/mine/ — Transporter's own jobs"""
    serializer_class = TransportJobSerializer
    permission_classes = [permissions.IsAuthenticated, IsTransporter]

    def get_queryset(self):
        return TransportJob.objects.filter(
            transporter=self.request.user
        ).select_related('order', 'order__godown', 'order__listing__category')


# ══════════════════════════════════════════
# DASHBOARD STATS
# ══════════════════════════════════════════

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    """GET /api/dashboard/stats/ — Role-based summary stats"""
    user = request.user

    if user.role == 'farmer':
        deliveries = FarmerDelivery.objects.filter(farmer=user)
        return Response({
            'total_deliveries': deliveries.count(),
            'total_kg_delivered': sum(d.quantity_kg for d in deliveries),
            'total_earned': sum(d.total_amount for d in deliveries.filter(status='accepted')),
            'pending_deliveries': deliveries.filter(status='pending').count(),
        })

    if user.role == 'godown':
        godowns = Godown.objects.filter(operator=user)
        listings = StockListing.objects.filter(godown__in=godowns)
        orders = Order.objects.filter(godown__in=godowns)
        return Response({
            'total_godowns': godowns.count(),
            'active_listings': listings.filter(status='available').count(),
            'total_orders': orders.count(),
            'pending_orders': orders.filter(status='pending').count(),
            'confirmed_orders': orders.filter(status='confirmed').count(),
        })

    if user.role == 'consumer':
        orders = Order.objects.filter(consumer=user)
        return Response({
            'total_orders': orders.count(),
            'pending_orders': orders.filter(status__in=['pending','confirmed']).count(),
            'completed_orders': orders.filter(status='completed').count(),
            'total_spent': sum(o.total_amount for o in orders.filter(status='completed')),
        })

    if user.role == 'transporter':
        jobs = TransportJob.objects.filter(transporter=user)
        return Response({
            'total_jobs': jobs.count(),
            'active_jobs': jobs.filter(status__in=['assigned','picked_up']).count(),
            'completed_jobs': jobs.filter(status='delivered').count(),
            'open_jobs': TransportJob.objects.filter(status='open').count(),
        })

    return Response({'detail': 'No stats for this role.'})