from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


# ──────────────────────────────────────────
# USERS
# ──────────────────────────────────────────

class User(AbstractUser):
    ROLES = [
        ('farmer',      'Farmer'),
        ('godown',      'Godown Operator'),
        ('transporter', 'Transporter'),
        ('consumer',    'Consumer / Family'),
        ('admin',       'Admin'),
    ]

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone       = models.CharField(max_length=20, unique=True)
    role        = models.CharField(max_length=20, choices=ROLES)
    address     = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD  = 'phone'
    REQUIRED_FIELDS = ['username', 'role']

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"


# ──────────────────────────────────────────
# FARMER
# ──────────────────────────────────────────

class Farmer(models.Model):
    """Extended profile for users with role='farmer'"""
    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    farm_name    = models.CharField(max_length=200)
    farm_location= models.CharField(max_length=300)
    farm_size_acres = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    crops_grown  = models.TextField(help_text="Comma-separated list of crops")
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.farm_name} — {self.user.get_full_name()}"


# ──────────────────────────────────────────
# GODOWN  (Warehouse)
# ──────────────────────────────────────────

class Godown(models.Model):
    """A registered warehouse / storage facility"""
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operator     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='godowns',
                                     limit_choices_to={'role': 'godown'})
    name         = models.CharField(max_length=200)
    location     = models.CharField(max_length=300)
    address      = models.TextField()
    capacity_tons = models.DecimalField(max_digits=10, decimal_places=2)
    phone        = models.CharField(max_length=20)
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.location}"


# ──────────────────────────────────────────
# PRODUCE  (Farmer → Godown intake)
# ──────────────────────────────────────────

class ProduceCategory(models.Model):
    name  = models.CharField(max_length=100, unique=True)   # Maize, Tomato, Rice…
    unit  = models.CharField(max_length=20, default='kg')   # kg, tonnes, bags

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Produce Categories"


class FarmerDelivery(models.Model):
    """
    Step 1: Farmer delivers produce to Godown.
    Records what came in, from whom, when, and at what purchase price.
    """
    STATUS = [
        ('pending',  'Pending Inspection'),
        ('accepted', 'Accepted into Stock'),
        ('rejected', 'Rejected'),
    ]

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deliveries',
                                    limit_choices_to={'role': 'farmer'})
    godown      = models.ForeignKey(Godown, on_delete=models.CASCADE, related_name='incoming_deliveries')
    category    = models.ForeignKey(ProduceCategory, on_delete=models.PROTECT)
    quantity_kg = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_kg_paid = models.DecimalField(max_digits=10, decimal_places=2,
                                             help_text="Price godown pays farmer per kg")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    grade       = models.CharField(max_length=5, choices=[('A','Grade A'),('B','Grade B'),('C','Grade C')],
                                   default='B')
    notes       = models.TextField(blank=True)
    status      = models.CharField(max_length=20, choices=STATUS, default='pending')
    delivered_at = models.DateTimeField(default=timezone.now)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.farmer} → {self.godown.name} | {self.category} {self.quantity_kg}kg"


# ──────────────────────────────────────────
# STOCK LISTING  (Godown → Website)
# ──────────────────────────────────────────

class StockListing(models.Model):
    """
    Step 2: Godown operator publishes available stock on the website.
    Consumers will see these listings and place orders.
    """
    STATUS = [
        ('available',   'Available'),
        ('low_stock',   'Low Stock'),
        ('out_of_stock','Out of Stock'),
        ('paused',      'Paused'),
    ]

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    godown      = models.ForeignKey(Godown, on_delete=models.CASCADE, related_name='listings')
    category    = models.ForeignKey(ProduceCategory, on_delete=models.PROTECT)

    # Stock info
    quantity_available_kg = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_kg = models.DecimalField(max_digits=8, decimal_places=2, default=1.0)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)

    # Details
    description  = models.TextField(blank=True)
    grade        = models.CharField(max_length=5, choices=[('A','Grade A'),('B','Grade B'),('C','Grade C')],
                                    default='B')
    harvest_date = models.DateField(null=True, blank=True)
    best_before  = models.DateField(null=True, blank=True)
    image        = models.ImageField(upload_to='produce/', null=True, blank=True)

    status       = models.CharField(max_length=20, choices=STATUS, default='available')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} @ {self.godown.name} — {self.quantity_available_kg}kg @ {self.price_per_kg}/kg"

    class Meta:
        ordering = ['-created_at']


# ──────────────────────────────────────────
# ORDERS  (Consumer → places order)
# ──────────────────────────────────────────

class Order(models.Model):
    """
    Step 3: Consumer places an order against a StockListing.
    They will pick up from the Godown (or a Transporter fetches it).
    """
    STATUS = [
        ('pending',    'Pending Confirmation'),
        ('confirmed',  'Confirmed by Godown'),
        ('ready',      'Ready for Pickup'),
        ('in_transit', 'In Transit'),
        ('completed',  'Completed'),
        ('cancelled',  'Cancelled'),
    ]

    PICKUP_METHOD = [
        ('self_pickup',  'Self Pickup'),
        ('transporter',  'Transporter'),
    ]

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    consumer    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders',
                                    limit_choices_to={'role': 'consumer'})
    listing     = models.ForeignKey(StockListing, on_delete=models.PROTECT, related_name='orders')
    godown      = models.ForeignKey(Godown, on_delete=models.PROTECT, related_name='orders')

    # Order details
    quantity_kg     = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_kg    = models.DecimalField(max_digits=10, decimal_places=2,
                                          help_text="Locked at time of order")
    total_amount    = models.DecimalField(max_digits=12, decimal_places=2)

    pickup_method   = models.CharField(max_length=20, choices=PICKUP_METHOD, default='self_pickup')
    delivery_address= models.TextField(blank=True, help_text="If transporter delivery")

    status          = models.CharField(max_length=20, choices=STATUS, default='pending')
    notes           = models.TextField(blank=True)

    # Timestamps
    ordered_at      = models.DateTimeField(auto_now_add=True)
    confirmed_at    = models.DateTimeField(null=True, blank=True)
    ready_at        = models.DateTimeField(null=True, blank=True)
    completed_at    = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-calculate total
        if self.quantity_kg and self.price_per_kg:
            self.total_amount = self.quantity_kg * self.price_per_kg
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{str(self.id)[:8]} — {self.consumer} | {self.quantity_kg}kg {self.listing.category}"

    class Meta:
        ordering = ['-ordered_at']


# ──────────────────────────────────────────
# TRANSPORT  (Pickup / Delivery)
# ──────────────────────────────────────────

class TransportJob(models.Model):
    """
    Step 4: A transporter is assigned to (or bids on) an order pickup from Godown.
    """
    STATUS = [
        ('open',       'Open for Bids'),
        ('assigned',   'Transporter Assigned'),
        ('picked_up',  'Picked Up from Godown'),
        ('delivered',  'Delivered to Consumer'),
        ('cancelled',  'Cancelled'),
    ]

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order       = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='transport_job')
    transporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='transport_jobs',
                                    limit_choices_to={'role': 'transporter'})

    pickup_location  = models.CharField(max_length=300)   # Godown address
    delivery_location= models.CharField(max_length=300)
    distance_km      = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    transport_fee    = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    status          = models.CharField(max_length=20, choices=STATUS, default='open')
    notes           = models.TextField(blank=True)

    assigned_at     = models.DateTimeField(null=True, blank=True)
    picked_up_at    = models.DateTimeField(null=True, blank=True)
    delivered_at    = models.DateTimeField(null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transport for Order #{str(self.order.id)[:8]}"