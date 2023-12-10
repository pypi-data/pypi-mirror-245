import ast

from rest_framework import serializers


class PythonField(serializers.Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        """validate python syntax"""
        try:
            ast.parse(data, mode="exec")
            return data
        except SyntaxError:
            raise serializers.ValidationError("invalid syntax provided")

    def to_representation(self, value):
        """show as code"""
        return value


class RatingField(serializers.IntegerField):
    def __init__(self, **kwargs):
        kwargs.setdefault("min_value", 1)
        kwargs.setdefault("max_value", 5)
        super().__init__(**kwargs)


class PercentageField(serializers.DecimalField):
    def __init__(self, **kwargs):
        kwargs.setdefault("max_digits", 2)
        kwargs.setdefault("decimal_places", 2)
        kwargs.setdefault("min_value", 0)
        kwargs.setdefault("max_value", 1)
        super().__init__(**kwargs)


class CurrencyField(serializers.Serializer):
    def __init__(self, amount_field, currency_field, **kwargs):
        super().__init__(**kwargs)
        self.amount_field = amount_field
        self.currency_field = currency_field

    def to_representation(self, instance):
        if not hasattr(instance, self.amount_field):
            raise serializers.ValidationError(
                "{}.{} does not exist".format(
                    instance.__class__.__name__,
                    self.amount_field,
                )
            )

        if not hasattr(instance, self.amount_field):
            raise serializers.ValidationError(
                "{}.{} does not exist".format(
                    instance.__class__.__name__,
                    self.amount_field,
                )
            )

        amount = getattr(instance, self.amount_field)
        currency = getattr(instance, self.currency_field)

        return {
            "amount": amount,
            "currency": currency,
        }

    def to_internal_value(self, data):
        pass


class ColorField(serializers.CharField):
    allowed_schemes = ["rgb", "rgba", "hex"]

    def __init__(self, allowed_schemes=None, **kwargs):
        super().__init__(**kwargs)

        if allowed_schemes:
            self.allowed_schemes = allowed_schemes

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        pass


class HashedField(serializers.CharField):
    pass


class EncryptedField(serializers.CharField):
    pass


class Base64Field(serializers.CharField):
    pass


class LatexField(serializers.CharField):
    pass


class RemoteField(serializers.Field):
    pass


class MarkdownField(serializers.Field):
    pass
