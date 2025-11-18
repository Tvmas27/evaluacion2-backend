from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

def home(request):
    return JsonResponse({
        "message": "Bienvenido al Sistema de Ventas - API REST",
        "status": "active",
        "endpoints": {
            "admin": "/admin/",
            "api_docs": "/api/",
            "categorias": "/api/categorias/",
            "productos": "/api/productos/",
            "clientes": "/api/clientes/",
            "ventas": "/api/ventas/",
            "detalles_venta": "/api/detalles-venta/"
        }
    })

@api_view(['GET'])
def api_root(request):
    return Response({
        "api_name": "Sistema de Ventas API",
        "version": "1.0",
        "endpoints": {
            "categorias": {
                "url": "/api/categorias/",
                "methods": ["GET", "POST", "PUT", "DELETE"]
            },
            "productos": {
                "url": "/api/productos/",
                "methods": ["GET", "POST", "PUT", "DELETE"],
                "filters": ["categoria", "precio", "search"]
            },
            "clientes": {
                "url": "/api/clientes/",
                "methods": ["GET", "POST", "PUT", "DELETE"]
            },
            "ventas": {
                "url": "/api/ventas/",
                "methods": ["GET", "POST", "PUT", "DELETE"]
            },
            "detalles_venta": {
                "url": "/api/detalles-venta/",
                "methods": ["GET", "POST", "PUT", "DELETE"]
            }
        }
    })