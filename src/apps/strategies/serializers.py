from rest_framework import serializers


class BacktestRequestSerializer(serializers.Serializer):

    asset_symbol = serializers.CharField()
    initial_capital = serializers.FloatField()

    strategy_type = serializers.CharField(
    required=False,
    default="moving_average"
)

    short_window = serializers.IntegerField(required=False, default=20)
    long_window = serializers.IntegerField(required=False, default=50)