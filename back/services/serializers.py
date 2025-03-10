from rest_framework import serializers

from .models import Bike, Order, OrderItem, Vrac


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ["id", "name", "is_borrowed", "borrower_id"]


class VracSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vrac
        fields = ["id", "name", "type", "price", "stock", "stock_available"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "name", "products", "prices", "quantity"]


class CreateOrderSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    products = serializers.ListField(child=serializers.CharField(max_length=100))
    prices = serializers.ListField(
        child=serializers.ListField(
            child=serializers.DecimalField(max_digits=10, decimal_places=2)
        )
    )
    quantities = serializers.ListField(
        child=serializers.ListField(child=serializers.IntegerField(min_value=0))
    )

    def validate(self, data):
        if not (
            len(data["products"]) == len(data["prices"]) == len(data["quantities"])
        ):
            raise serializers.ValidationError(
                "Les listes products, prices et quantities doivent avoir la même taille"
            )

        if "Thé" in data["products"]:
            raise serializers.ValidationError(
                {"error": "I'm an epicier, not a teapot!"}, code=418
            )

        # Vérifier que chaque produit existe
        for product_name in data["products"]:
            if not Vrac.objects.filter(name=product_name).exists():
                raise serializers.ValidationError(
                    f"Le produit {product_name} n'existe pas"
                )

        return data


class OrderSummarySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    total_quantities = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "name", "products", "total_quantities", "total_price"]

    def get_products(self, obj):
        return [item.vrac.name for item in obj.orderitem_set.all()]

    def get_total_quantities(self, obj):
        return [sum(item.quantities) for item in obj.orderitem_set.all()]

    def get_total_price(self, obj):
        return obj.get_total_price()
