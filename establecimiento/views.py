from django.shortcuts import render

# Create your views here.




# esta vaina hay que agregarla para validad
# from django.core.exceptions import ValidationError
# from .models import Establecimiento, Docente

# def crear_establecimiento(request):
#     if request.method == "POST":
#         nombre = request.POST["nombre"]
#         encargado_id = request.POST["encargado"]
#         encargado = Docente.objects.get(id=encargado_id)
        
#         establecimiento = Establecimiento(nombre=nombre, encargado=encargado)
        
#         try:
#             establecimiento.full_clean()
#             establecimiento.save()
#             # Redirigir a la página de éxito o actualizar la página actual
#         except ValidationError as e:
#             # Manejar el error de validación, como mostrar un mensaje de error en la página
