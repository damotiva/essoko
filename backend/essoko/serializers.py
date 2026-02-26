from rest_framework import serializers
from .models import (
    User, Farmer, Godown, ProduceCategory,
    FarmerDelivery, StockListing, Order, TransportJob
)


# ──────────────────────────────────────────
# AUTH / USER
# ──────────────────────────────────────────

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, label="Confirm Password")

    class Meta:
        model = User
        fields = ['phone', 'username', 'first_name', 'last_name',
                  'role', 'address', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'first_name', 'last_name',
                  'role', 'address', 'is_verified', 'created_at']
        read_only_fields = ['id', 'is_verified', 'created_at']


# ──────────────────────────────────────────
# FARMER
# ──────────────────────────────────────────

class FarmerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Farmer
        fields = ['id', 'user', 'farm_name', 'farm_location',
                  'farm_size_acres', 'crops_grown', 'created_at']
        read_only_fields = ['id', 'created_at']


# ──────────────────────────────────────────
# GODOWN
# ──────────────────────────────────────────

class GodownSerializer(serializers.ModelSerializer):
    operator_name = serializers.CharField(source='operator.get_full_name', read_only=True)

    class Meta:
        model = Godown
        fields = ['id', 'operator', 'operator_name', 'name', 'location',
                  'address', 'capacity_tons', 'phone', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


# ──────────────────────────────────────────
# PRODUCE CATEGORY
# ──────────────────────────────────────────

class ProduceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduceCategory
        fields = ['id', 'name', 'unit']


# ──────────────────────────────────────────
# FARMER DELIVERY
# ──────────────────────────────────────────

class FarmerDeliverySerializer(serializers.ModelSerializer):
    farmer_name  = serializers.CharField(source='farmer.get_full_name', read_only=True)
    godown_name  = serializers.CharField(source='godown.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = FarmerDelivery
        fields = [
            'id', 'farmer', 'farmer_name', 'godown', 'godown_name',
            'category', 'category_name', 'quantity_kg',
            'price_per_kg_paid', 'total_amount', 'grade',
            'notes', 'status', 'delivered_at', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'total_amount']

    def validate(self, data):
        qty  = data.get('quantity_kg', 0)
        price = data.get('price_per_kg_paid', 0)
        data['total_amount'] = qty * price
        return data


# ──────────────────────────────────────────
# STOCK LISTING
# ──────────────────────────────────────────

class StockListingSerializer(serializers.ModelSerializer):
    godown_name     = serializers.CharField(source='godown.name', read_only=True)
    godown_location = serializers.CharField(source='godown.location', read_only=True)
    godown_phone    = serializers.CharField(source='godown.phone', read_only=True)
    category_name   = serializers.CharField(source='category.name', read_only=True)
    category_unit   = serializers.CharField(source='category.unit', read_only=True)
    image_url       = serializers.SerializerMethodField()

    class Meta:
        model = StockListing
        fields = [
            'id', 'godown', 'godown_name', 'godown_location', 'godown_phone',
            'category', 'category_name', 'category_unit',
            'quantity_available_kg', 'min_order_kg', 'price_per_kg',
            'description', 'grade', 'harvest_date', 'best_before',
            'image', 'image_url', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class StockListingCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating/updating listings"""
    class Meta:
        model = StockListing
        fields = [
            'category', 'quantity_available_kg', 'min_order_kg',
            'price_per_kg', 'description', 'grade',
            'harvest_date', 'best_before', 'image', 'status'
        ]


# ──────────────────────────────────────────
# ORDER
# ──────────────────────────────────────────

class OrderSerializer(serializers.ModelSerializer):
    consumer_name   = serializers.CharField(source='consumer.get_full_name', read_only=True)
    consumer_phone  = serializers.CharField(source='consumer.phone', read_only=True)
    listing_detail  = StockListingSerializer(source='listing', read_only=True)
    godown_name     = serializers.CharField(source='godown.name', read_only=True)
    godown_address  = serializers.CharField(source='godown.address', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'consumer', 'consumer_name', 'consumer_phone',
            'listing', 'listing_detail', 'godown', 'godown_name', 'godown_address',
            'quantity_kg', 'price_per_kg', 'total_amount',
            'pickup_method', 'delivery_address',
            'status', 'notes',
            'ordered_at', 'confirmed_at', 'ready_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'total_amount', 'price_per_kg', 'godown',
            'ordered_at', 'confirmed_at', 'ready_at', 'completed_at'
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['listing', 'quantity_kg', 'pickup_method', 'delivery_address', 'notes']

    def validate(self, data):
        listing = data['listing']
        qty = data['quantity_kg']

        if listing.status not in ('available', 'low_stock'):
            raise serializers.ValidationError("This product is not available for order.")

        if qty < listing.min_order_kg:
            raise serializers.ValidationError(
                f"Minimum order is {listing.min_order_kg}kg."
            )

        if qty > listing.quantity_available_kg:
            raise serializers.ValidationError(
                f"Only {listing.quantity_available_kg}kg available."
            )

        return data

    def create(self, validated_data):
        listing = validated_data['listing']
        consumer = self.context['request'].user

        order = Order.objects.create(
            consumer=consumer,
            listing=listing,
            godown=listing.godown,
            price_per_kg=listing.price_per_kg,
            **validated_data
        )

        # Deduct from stock
        listing.quantity_available_kg -= order.quantity_kg
        if listing.quantity_available_kg <= listing.min_order_kg:
            listing.status = 'low_stock'
        if listing.quantity_available_kg <= 0:
            listing.status = 'out_of_stock'
        listing.save()

        return order


# ──────────────────────────────────────────
# TRANSPORT JOB
# ──────────────────────────────────────────

class TransportJobSerializer(serializers.ModelSerializer):
    order_detail    = OrderSerializer(source='order', read_only=True)
    transporter_name = serializers.CharField(source='transporter.get_full_name', read_only=True)

    class Meta:
        model = TransportJob
        fields = [
            'id', 'order', 'order_detail',
            'transporter', 'transporter_name',
            'pickup_location', 'delivery_location',
            'distance_km', 'transport_fee',
            'status', 'notes',
            'assigned_at', 'picked_up_at', 'delivered_at', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']