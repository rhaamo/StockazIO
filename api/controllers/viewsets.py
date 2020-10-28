from rest_framework.viewsets import ModelViewSet


class MultiSerializerViewSet(ModelViewSet):
    serializers = {
        "default": None,
        # list, detail, create, retrieve, default, update, destroy
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers["default"])
