from arrendados.models import Usuario, Tipo_Usuario, Propiedad, Tipo_Propiedad, Ciudad
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
    #Obtengo todos los Users de la BD
    if request.method == 'GET':
        #Query que me devuelve todos los usuarios de la BD
        usuarios = Usuario.objects.all()
        #Cada Usuario como objeto lo transforma en json y lo agrega a un arreglo de Json
        usuarios = serializers.serialize("json",usuarios)
        #Retorno el arreglo de Json 
        return HttpResponse(usuarios,content_type='application/json')
    #Agrego un nuevo User A la BD
    if request.method == 'POST':
        try:
            #Guardo en data el contenido del cuerpo del mensaje que viene el Json
            data = json.loads(request.body)
            #Guardo cada valor de los atributos en variables
            nombre = data['nombre']
            fecha_nacimiento = data['fecha_nacimiento']
            email = data['email']
            password = data['password']
            telefono = data['telefono']
            direccion = data['direccion']
            tipo_usuario = data['tipo_usuario']
            check_offer = data['check_offer']
            tipo_usuario = data['tipo_usuario']
            #Obtengo un objeto de tipo Tipo_Usuario con la id del usuario
            objeto_tipo_usuario = Tipo_Usuario.objects.get(id=tipo_usuario)
            #Hago un insert en la BD con los parametros
            usuario = Usuario(nombre=nombre,fecha_nacimiento=fecha_nacimiento,email=email,password=password,telefono=telefono,direccion=direccion, check_offer=check_offer,tipo_usuario=objeto_tipo_usuario)
            usuario.save() 
            #Compruebo que la id del usuario sea correcta para saber si fue agregado
            #Si no existe la id, el usuario no se agrego
            if usuario.id is None:
                #Creo un diccionario de python
                unsuccessful={'Response':'Not Created'}
                #Lo transformo a Json
                successful_json = json.dumps(unsuccesful)
                #Devuelvo el Json con el codigo 400
                return HttpResponse(unsuccessful, content_type='application/json', status=400)
            #Si la id existe, entonces el usuario se agrego
            else:
                #Creo un diccionario de python
                successful ={'Response':'Created','id':usuario.id}
                #Lo transformo a Json
                successful_json = json.dumps(successful)
                #Devuelvo el Json con el codigo 201 (Creado)
                return HttpResponse(successful_json, content_type='application/json', status=201)
        #Manejo de error para la creacion de usuario con email ya existente
        except IntegrityError as c:
            #Creo un diccionario de Python
            error ={'Response':'Duplicate E-mail'}
            #Lo transformo a Json
            error_json = json.dumps(error)
            #Devuelco el Json con el codigo 400
            return HttpResponse(error_json, content_type='application/json', status=400)

@csrf_exempt
def User(request,id="0"):
    #Obtengo un usuario en especifico por su id
    if request.method == 'GET':
        #Query para filtrar por la id del usuario
        usuario = Usuario.objects.filter(id=id)
        #Si el objeto Usuario con esa id existe (True), entonces devuelvo
        if usuario.exists() == True:
            #Transformo a Json el usuario
            usuario = serializers.serialize("json",usuario)
            #Devuelvo el usuario 
            return HttpResponse(usuario, content_type='application/json')
        #Si el objeto Usuario con esa id no existe (False), entonces devuelvo
        else:
            #Creo un diccionario de python
            error ={'Response':'El usuario no existe'}
            #Lo transformo a Json
            error_json = json.dumps(error)
            #Retorno con codigo 200
            return HttpResponse(error_json, content_type='application/json', status=200)

    #Borro un Usuario en especifico por su id o Borro un usuario junto a su propiedad
    if request.method == 'DELETE':
        #Obtengo un objeto usuario por su id
        usuario = Usuario.objects.filter(pk=id)
        #Obtengo un objeto propiedad por la id del usuario
        propiedad = Propiedad.objects.filter(id_usuario=id)
        #Compruebo que el usuario tiene ligada una propiedad para eliminar ambos (Usuario y su propiedad)
        if usuario.exists()==True and propiedad.exists() == True:
            #Borro el usuario
            usuario.delete()
            #Borro la propiedad
            propiedad.delete()
            #Creo diccionario python con respuesta correcta
            response ={'response': 'El usuario de id: ' + str(id) + ' ha sido eliminado correctamente junto a su propiedad asociada', 'code': '200', 'status': 'OK'}
            #Transformo a Json
            successful_json = json.dumps(response)
            #Devuelvo con codigo 200
            return HttpResponse(successful_json, content_type='application/json', status=200)
        else:
            usuario.delete()
            #Creo diccionario python con respuesta correcta
            response ={'response': 'El usuario de id: ' + str(id) + ' ha sido eliminado correctamente', 'code': '200', 'status': 'OK'}
            #Transformo a Json
            successful_json = json.dumps(response)
            #Devuelvo con codigo 200
            return HttpResponse(successful_json, content_type='application/json', status=200)
    
    #Editar a un usuario en especifico por su id
    if request.method == 'PUT':
        try:
            #Obtengo al usuario que tiene la id
            usuario = Usuario.objects.get(id=id)
            #Recolecto los nuevos datos
            data = json.loads(request.body)
            #Guardo cada atributo en variables
            nombre = data['nombre']
            fecha_nacimiento = data['fecha_nacimiento']
            email = data['email']
            password = data['password']
            telefono = data['telefono']
            direccion = data['direccion']
            check_offer= data['check_offer']
            tipo_usuario = data['tipo_usuario']
            #Obtengo un objeto de tipo Tipo_Usuario por la id
            objeto_tipo_usuario = Tipo_Usuario.objects.get(id=tipo_usuario)
            #Edito en la base de datos con los nuevos parametros
            usuario = Usuario(id=id,nombre=nombre,fecha_nacimiento=fecha_nacimiento,email=email,password=password,telefono=telefono,direccion=direccion, check_offer=check_offer,tipo_usuario=objeto_tipo_usuario)
            usuario.save() 
            #Respondo con respuesta correcta y codigo 200
            response ={'response': 'Se cambiaron correctamente los registros', 'code': '200', 'status': 'OK'}
            successful_json = json.dumps(response)
            return HttpResponse(successful_json, content_type='application/json', status=200)

        #Excepcion para manejar una id no encontrada
        except Exception as c:
            print c
            response ={'response': 'No se cambiaron los registros, ID no encontrada', 'code': '500', 'status': 'ERROR'}
            successful_json = json.dumps(response)
            return HttpResponse(successful_json, content_type='application/json', status=200)
#---------------------------- CRUD PROPIEDADES ----------------------------------------
@csrf_exempt
def Properties(request):
    #Obtengo todas las propiedades de la BD
    if request.method == 'GET':
        #Obtengo como objeto la lista de todas las propiedades de la BD
        propiedades = Propiedad.objects.all()
        #Hago una conversion a formato JSON
        propiedades = serializers.serialize("json",propiedades)
        #Engtrego una respuesta en formato JSON
        return HttpResponse(propiedades, content_type='application/json', status=200)
    #Agrego una nueva propiedad a la BD
    if request.method == 'POST':
        #Obtengo la data del body de la peticion que viene en formato JSON
        data = json.loads(request.body)
        #Guardo en variables cada uno de los atributos
        direccion = data['direccion']
        cantidad_disponible = data['cantidad_disponible']
        cantidad = data['cantidad']
        latitud = data['latitud']
        longitud = data['longitud']
        id_usuario = data['id_usuario']
        ciudad = data['ciudad_id']
        tipo_propiedad = data['tipo_propiedad_id']
        #Obtengo el objeto del tipo de propiedad segun la id del tipo de propiedad
        objeto_tipo_propiedad = Tipo_Propiedad.objects.get(id=tipo_propiedad)
        #Obtengo el objeto de la ciudad segun la id de la ciudad
        objeto_ciudad = Ciudad.objects.get(id=ciudad)
        #Obtengo el objeto usuario segun la id del usuario
        objeto_usuario = Usuario.objects.get(id=id_usuario)
        #Hago un INSERT a la BD en la tabla Propiedad
        datos_propiedad = Propiedad(direccion=direccion,cantidad_disponible=cantidad_disponible,cantidad=cantidad,latitud=latitud,longitud=longitud,id_usuario=id_usuario,ciudad=objeto_ciudad,tipo_propiedad=objeto_tipo_propiedad)
        datos_propiedad.save()
        #Verificamos que la id de la Propiedad 
        #Si es Vacia, hubo un problema y respondimos en formato JSON
        if datos_propiedad.id is None :
            response={'Response':'Hubo un problema al agregar una propiedad'}
            response_json = json.dumps(response)
            return HttpResponse(response_json, content_type='application/json', status=400)
        #Si son correctas es que los datos fueron agregados exitosamente
        else:
            response={'Response':'Propiedad agregada correctamente','id':datos_propiedad.id}
            response_json = json.dumps(response)
            return HttpResponse(response_json, content_type='application/json', status=201)
@csrf_exempt
def Property(request,id="0"):
    #Obtengo una propiedad en especifico por su id
    if request.method == 'GET':
        #Query para filtrar por la id de la propiedad
        propiedad = Propiedad.objects.filter(pk=id)
        #Si el objeto Propiedad con esa id existe (True), entonces devuelvo
        if propiedad.exists() == True:
            #Transformo a Json la propiedad
            propiedad = serializers.serialize("json",propiedad)
            #Devuelvo la propiedad
            return HttpResponse(propiedad, content_type='application/json')
        else:
            #Creo un diccionario de python
            error ={'Response':'La propiedad no existe'}
            #Lo transformo a Json
            error_json = json.dumps(error)
            #Retorno con codigo 200
            return HttpResponse(error_json, content_type='application/json', status=200)
    #Borro una propiedad en especifico
    if request.method == 'DELETE':
        #Obtengo un objeto propiedad por su id
        propiedad = Propiedad.objects.filter(id=id)
        #Compruebo que el objeto propiedad este en la BD
        if propiedad.exists()==True:
            #Borro el usuario
            propiedad.delete()
            #Creo diccionario python con respuesta correcta
            response ={'response': 'La propiedad de id: ' + str(id) + ' ha sido eliminada correctamente', 'code': '200', 'status': 'OK'}
            #Transformo a Json
            successful_json = json.dumps(response)
            #Devuelvo con codigo 200
            return HttpResponse(successful_json, content_type='application/json', status=200)
        else: 
            #Creo diccionario de Json
            response ={'response': 'La propiedad de id: ' + str(id) + ' no existe', 'code': '500', 'status': 'ERROR'}
            #Transformo a json
            successful_json = json.dumps(response)
            #Devuelvo con codigo 500
            return HttpResponse(successful_json, content_type='application/json', status=500)
    #Editar una propiedad en especifico por su id
    if request.method == "PUT":
        try:
            #
            #Obtengo al usuario que tiene la id
            propiedad= Propiedad.objects.get(id=id)
            data = json.loads(request.body)
            #Guardo en variables cada uno de los atributos
            direccion = data['direccion']
            cantidad_disponible = data['cantidad_disponible']
            cantidad = data['cantidad']
            latitud = data['latitud']
            longitud = data['longitud']
            id_usuario = data['id_usuario']
            ciudad = data['ciudad_id']
            tipo_propiedad = data['tipo_propiedad_id']

            #Obtengo un objeto de tipo Ciudad por la id
            objeto_ciudad = Ciudad.objects.get(id=ciudad)
            #Obtengo un objeto de tipo Tipo_propiedad
            objeto_tipo_propiedad = Tipo_Propiedad.objects.get(id=tipo_propiedad)

            #Edito en la base de datos con los nuevos parametros
            datos_propiedad = Propiedad(id=id,direccion=direccion,cantidad_disponible=cantidad_disponible,cantidad=cantidad,latitud=latitud,longitud=longitud,id_usuario=id_usuario,ciudad=objeto_ciudad,tipo_propiedad=objeto_tipo_propiedad)
            datos_propiedad.save()

            #Respondo con respuesta correcta y codigo 200
            response ={'response': 'Se cambiaron correctamente los registros', 'code': '200', 'status': 'OK'}
            successful_json = json.dumps(response)
            return HttpResponse(successful_json, content_type='application/json', status=200)
        

        #Excepcion para manejar una id no encontrada
        except Exception as c:
            if str(c) == "Ciudad matching query does not exist.":
                response ={'response': 'No se cambiaron los registros, Ciudad no encontrada', 'code': '500', 'status': 'ERROR'}
                successful_json = json.dumps(response)
                return HttpResponse(successful_json, content_type='application/json', status=200)
            elif str(c) == "Tipo_Propiedad matching query does not exist.":
                response ={'response': 'No se cambiaron los registros, Tipo_Propiedad no encontrada', 'code': '500', 'status': 'ERROR'}
                successful_json = json.dumps(response)
                return HttpResponse(successful_json, content_type='application/json', status=200)
            else:
                response ={'response': 'No se cambiaron los registros, Propiedad no encontrada', 'code': '500', 'status': 'ERROR'}
                successful_json = json.dumps(response)
                return HttpResponse(successful_json, content_type='application/json', status=200)

            
        