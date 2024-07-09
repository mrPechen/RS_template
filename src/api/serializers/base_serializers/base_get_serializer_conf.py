from rest_framework.serializers import ModelSerializer


class BaseGetSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_id = self.context.get('user_id', None)
        request_id = self.context.get('request_id', None)

        if user_id != request_id:
            self.fields.pop('password', None)
