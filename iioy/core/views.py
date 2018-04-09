from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheck(APIView):
    def get(self, *args, **kwargs):
        return Response(data={
            'ok': True,
            'now': datetime.utcnow().isoformat(),
        })
