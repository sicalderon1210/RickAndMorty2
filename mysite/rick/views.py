from django.shortcuts import render
from django.http import HttpResponse
import json
import requests 


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    def buscar_info(URL, num):
        query = """query {
                        episodes (page: """ + str(num) + """){
                            results {
                            id
                            name
                            air_date
                            episode
                            }
                        }
                    }"""
        r = requests.post(url, json={'query': query})
        json_data = json.loads(r.text)
        df_data = json_data['data']['episodes']['results']
        num += 1
        if num == 3:
            return df_data
        else:    
            return df_data + buscar_info(url, num)
    url = 'https://integracion-rick-morty-api.herokuapp.com/graphql/episode'
    aux = buscar_info(url, 1)
    context = {"info": aux}
    return render(request, 'index.html', context)

def personaje(request, personaje_id):
    if(personaje_id/20 == personaje_id//20):
        num = personaje_id//20
    else:
        num = int((1+ personaje_id / 20)//1)
    def buscar_info(URL, num):
        query = """query {
                        characters(page:""" + str(num) + """) {
                            results {
                            id
                            name
                            status
                            species
                            type
                            gender
                            origin{
                                name
                                id
                            }
                            location{
                                name
                                id
                            }
                            image
                            episode{
                                id
                                name
                            }
                            }
                        }
                    }"""
        r = requests.post(url, json={'query': query})
        json_data = json.loads(r.text)
        df_data = json_data['data']['characters']['results']
        return df_data
        
    url = 'https://integracion-rick-morty-api.herokuapp.com/graphql/character'
    aux = buscar_info(url, num)
    for elem in aux:
        if elem["id"] == str(personaje_id):
            a_retornar = elem
            break
    lista_cap = []
    for elem in a_retornar['episode']:
        algo = {}
        algo['name'] = elem['name']
        algo['id'] = elem['id']
        lista_cap.append(algo)
        
    if a_retornar['location']['name'] == 'unknown':
        location_id = 0
    else:
        location_id = a_retornar['location']['id']

    if a_retornar['origin']['name'] == 'unknown':
        origen_id = 0
    else:
        origen_id = a_retornar['origin']['id']
    enviar = {'context': a_retornar, 'cap': lista_cap, 'location': location_id, 'origen': origen_id}
    return render(request, 'personaje.html', enviar)

def lugar(request, lugar_id):
    if(lugar_id/20 == lugar_id//20):
        num = lugar_id//20
    else:
        num = int((1+ lugar_id / 20)//1)
    def buscar_info(URL, num):
            query = """query {
                            locations(page: """ + str(num) + """) {
                                results {
                                id
                                name
                                type
                                dimension
                                residents{
                                    id
                                    name
                                }
                                }
                            }
                        }"""
            r = requests.post(url, json={'query': query})
            json_data = json.loads(r.text)
            df_data = json_data['data']['locations']['results']
            return df_data

    url = 'https://integracion-rick-morty-api.herokuapp.com/graphql/location'
    aux = buscar_info(url, num)
    for elem in aux:
        if elem['id'] == str(lugar_id):
            lugar = elem
            break

    lista = []
    for elem in lugar['residents']:
        algo = {}
        algo['name'] = elem['name']
        algo['id'] = elem['id']
        lista.append(algo)
    enviar = {'context': lugar, 'residentes': lista}
    return render(request, 'lugar.html', enviar)

def capitulo(request, capitulo_id):
    if(capitulo_id/20 == capitulo_id//20):
        num = capitulo_id//20
    else:
        num = int((1+ capitulo_id / 20)//1)
    def buscar_info(URL, num):
        query = """query {
                        episodes(page: """ + str(num) + """) {
                            results {
                            id
                            name
                            air_date
                            episode
                            characters{
                                id
                                name
                            }
                            }
                        }
                    }"""
        r = requests.post(url, json={'query': query})
        json_data = json.loads(r.text)
        df_data = json_data['data']['episodes']['results']
        num += 1
        return df_data

    url = 'https://integracion-rick-morty-api.herokuapp.com/graphql/episode'
    aux = buscar_info(url, num)
    for elem in aux:
        if elem['id'] == str(capitulo_id):
            a_retornar = elem
            break
    lista = []
    for elem in a_retornar['characters']:
        aux = {}
        aux['name'] = elem['name']
        aux['id'] = elem['id']
        lista.append(aux)
    enviar = {'context': a_retornar, 'personajes': lista}
    return render(request, 'capitulo.html', enviar)

def not_found(request, lugar_id):
    data = {}
    return render(request, 'not_found.html', data)

def search(request):
    name = str(request.GET.get('name', None))
    def buscar_info_capitulos(URL, num):
        query = """query {
                    episodes (page: """ + str(num) + """){
                        results {
                        id
                        name
                        air_date
                        episode
                        characters{
                            id
                            name
                        }
                        }
                    }
                }"""
        r = requests.post(url, json={'query': query})
        json_data = json.loads(r.text)
        df_data = json_data['data']['episodes']['results']
        num += 1
        if num == 3:
            return df_data
        else:    
            return df_data + buscar_info_capitulos(url, num)
        return df_data
    url = 'https://integracion-rick-morty-api.herokuapp.com/graphql/episode/'
    capitulos = buscar_info_capitulos(url, 1)
    filtro_cap = []
    for cap in capitulos:
        if name.lower() in cap['name'].lower():
            filtro_cap.append(cap)


    def buscar_info_lugar(URL, num):
        query = """query {
                        locations (page:""" + str(num) + """){
                            results {
                            id
                            name
                            type
                            dimension
                            residents{
                                id
                                name
                            }
                            }
                        }
                    }"""
        r = requests.post(url, json={'query': query})
        json_data = json.loads(r.text)
        df_data = json_data['data']['locations']['results']
        num += 1
        if num == 5:
            return df_data
        else:    
            return df_data + buscar_info_lugar(url, num)

    url = 'https://integracion-rick-morty-api.herokuapp.com/graphql/location/'
    lugares = buscar_info_lugar(url, 1)
    filtro_lugares = []
    for lug in lugares:
        if name.lower() in lug['name'].lower():
            filtro_lugares.append(lug)
            
    def buscar_info_personajes(URL, num):
            query = """query {
                            characters(page:""" + str(num) + """) {
                                results {
                                id
                                name
                                status
                                species
                                type
                                gender
                                origin{
                                    name
                                    id
                                }
                                location{
                                    name
                                    id
                                }
                                image
                                episode{
                                    id
                                    name
                                }
                                }
                            }
                        }"""
            r = requests.post(url, json={'query': query})
            json_data = json.loads(r.text)
            df_data = json_data['data']['characters']['results']
            num += 1
            if num == 26:
                return df_data
            else:    
                return df_data + buscar_info_personajes(url, num)
        
    url = 'https://integracion-rick-morty-api.herokuapp.com/graphql/character'
    personajes = buscar_info_personajes(url, 1)
    filtro_personajes = []
    for per in personajes:
        if name.lower() in per['name'].lower():
            filtro_personajes.append(per)
    context = {}
    context['lugares'] = filtro_lugares
    context['capitulos'] = filtro_cap
    context['personajes'] = filtro_personajes
    return render(request, 'busqueda.html', context)

