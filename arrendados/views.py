from arrendados.models import Usuario, Tipo_Usuario
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import StreamingHttpResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

#---------------------------- CRUD USUARIOS ------------------------------------------
@csrf_exempt
def Users(request):
    if request.method == 'GET':
        usuarios = Usuario.objects.all()
        usuarios = serializers.serialize("json",usuarios)
        return HttpResponse(usuarios,content_type='application/json')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data['nombre']
            fecha_nacimiento = data['fecha_nacimiento']
            email = data['email']
            password = data['password']
            telefono = data['telefono']
            direccion = data['direccion']
            tipo_usuario = data['tipo_usuario']
            check_offer = data['check_offer']
            tipo_usuario = data['tipo_usuario']

            objeto_tipo_usuario = Tipo_Usuario.objects.get(id=tipo_usuario)

            usuario = Usuario(nombre=nombre,fecha_nacimiento=fecha_nacimiento,email=email,password=password,telefono=telefono,direccion=direccion, check_offer=check_offer,tipo_usuario=objeto_tipo_usuario)
            usuario.save() 

            if usuario.id is None:
                unsuccessful={'Response':'Not Created'}
                successful_json = json.dumps(unsuccesful)
                return HttpResponse(unsuccessful, content_type='application/json', status=400)

            else:
                successful ={'Response':'Created','id':usuario.id}
                successful_json = json.dumps(successful)
                return HttpResponse(successful_json, content_type='application/json', status=201)
        except IntegrityError as c:
            error ={'Response':'Duplicate E-mail'}
            error_json = json.dumps(error)

            return HttpResponse(error_json, content_type='application/json', status=400)

@csrf_exempt
def User(request,id="0"):
    if request.method == 'GET':
        usuario = Usuario.objects.filter(id=id)
        if usuario.exists() == True:
            usuario = serializers.serialize("json",usuario)
            return HttpResponse(usuario, content_type='application/json')
        else:
            error ={'Response':'El usuario no existe'}
            error_json = json.dumps(error)
            return HttpResponse(error_json, content_type='application/json', status=200)


    if request.method == 'DELETE':
        try:
            usuario = Usuario.objects.get(id=id)
            usuario.delete()

            
            if usuario.id is None:
                response ={'response': 'El usuario de id: ' + str(id) + ' ha sido eliminado correctamente', 'code': '200', 'status': 'OK'}
                successful_json = json.dumps(response)
                return HttpResponse(successful_json, content_type='application/json', status=200)

        except ObjectDoesNotExist as c:
                response ={'response': 'El usuario de id: ' + str(id) + ' no existe', 'code': '500', 'status': 'ERROR'}
                successful_json = json.dumps(response)
                return HttpResponse(successful_json, content_type='application/json', status=500)
    
    if request.method == 'PUT':
        try:
            usuario = Usuario.objects.get(id=id)
            data = json.loads(request.body)
            nombre = data['nombre']
            fecha_nacimiento = data['fecha_nacimiento']
            email = data['email']
            password = data['password']
            telefono = data['telefono']
            direccion = data['direccion']
            check_offer= data['check_offer']
            tipo_usuario = data['tipo_usuario']

            objeto_tipo_usuario = Tipo_Usuario.objects.get(id=tipo_usuario)

            usuario = Usuario(id=id,nombre=nombre,fecha_nacimiento=fecha_nacimiento,email=email,password=password,telefono=telefono,direccion=direccion, check_offer=check_offer,tipo_usuario=objeto_tipo_usuario)
            usuario.save() 

            response ={'response': 'Se cambiaron correctamente los registros', 'code': '200', 'status': 'OK'}
            successful_json = json.dumps(response)
            return HttpResponse(successful_json, content_type='application/json', status=200)


        except Exception as c:
            print c
            response ={'response': 'No se cambiaron los registros, ID no encontrada', 'code': '500', 'status': 'ERROR'}
            successful_json = json.dumps(response)
            return HttpResponse(successful_json, content_type='application/json', status=200)

