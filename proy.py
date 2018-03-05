#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT

#Disner Marco Antonio
#Gonzalez Ramirez Miguel Angel

import re
import sys
import argparse
from requests import get
from requests.exceptions import ConnectionError
import requests
import re


def addOptions():
    """

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-A','--agent',dest='agent',default=None,help='Modifica agente de usuario') 
    parser.add_argument('-P','--proxy',dest='proxy',default=None,help='Especifica el uso de proxy') 
    parser.add_argument('-H','--https',dest='https',default=None,action='store_true',help='Especifica el uso de https') 
    parser.add_argument('-p','--port', dest='port', default=None, help='Puerto de escucha del servidor')
    parser.add_argument('-s','--server', dest='server', default=None, help='Servidor')
    args = parser.parse_args()
    return args
 

def crea_url(servidor,puerto,protocolo='http'):
    """
    Regresa la URL formada por los argumentos de entrada
    Argumentos:
        servidor (str) : El DNS o IPv4 del servidor web
        puerto (str) : El puerto del servidor
        protocolo (str) : Protocolo de transferencia de hipertexto
    Salida:
        url (str) : La URL formada
    """
    if puerto:
        puerto = ':%s' % puerto
        url = '%s://%s%s' % (protocolo,servidor,puerto)
    else:
        url = '%s://%s' % (protocolo,servidor)
    return url

def crea_sesion(proxy,agent=None):
    """
    Crea una objeto sesion
    Argumentos:
        tor (bool) : verdadero para usar tor como proxy
    Salida:
        sesion (session) : Un objeto session de la libreria requests
    """
    sesion = requests.session()
    if proxy:
        url = '%s' % (proxy)
        sesion.proxies = {'http':url,'https':url}

    if agent:
        sesion.headers.update({'user-agent':agent})


    return sesion

def printError(msg, exit = False):
    """
    Funcion para escapar de la ejecucion del programa
    Argumentos:
        msg (str) : Mensaje de error
        exit (bool) : Verdadero escapa del programa, falso continua ejecucion
    Salidas:
        Ninguna
    """
    sys.stderr.write('Error:\t%s\n' % msg)
    if exit:
        sys.exit(1)


def crawl(url,sesion):
    """
    Genera una lista de URL's a partir de un recurso Web.
    Argumentos:

    url (str) : La URL del recurso actual
    Salida:

    urls (str[]): Un arreglo con todos los recursos encontrados
    """
    try:
        lst = [] 
        for rec in re.findall('.*\.js',sesion.get(url).content):
            m = re.match(".*(\'|\")(.*\.js).*",rec)
            if m:
                lst.append(m.group(2))
        urls = []
        http = []
        dos = []
        una = []
        let = []
        for rec in lst:
            a = re.compile("http")
            http.extend(filter(a.match,lst))
            b = re.compile("^//")
            dos.extend(filter(b.match, lst))
            c = re.compile("^/[^/]")
            una.extend(filter(c.match,lst))
            d = re.compile("[a-zA-Z][^\:]*$")
            let.extend(filter(d.match,lst))
        for h in http:
            urls.append(h)
        for d in dos:
            dd = "http:" + d
            urls.append(dd)
        for u in una:
            uu = url + u
            urls.append(uu)
        for l in let:
            ll = url + '/' + l
            urls.append(ll)
        urls.append(url)
        return urls
    except Exception as e:
        print "Error:" + str(e)

def peticiones(urls):
    """
    Busca Peticiones asincronas en una lista de urls
    Argumentos:
        urls (str[*]) : La lista de urls donde se buscaran peticiones adincronas
    Salida:
        
    """
    try:
        lst = []
        for url in urls:
            respuesta = requests.get(url)
            for pet in re.findall('XMLHttpRequest[^\;]*\;',respuesta.content):
                print pet
    except Exception as e:
        print str(e)


if __name__ == '__main__':
    """
    Se debe indicar el DNS del servidor web, por defecto el protocolo utilizado es http, se puede indicar un
    servidor proxy y modificar el agente de usuario
    
    python proy.py -s <server DNS> [-p <puerto>] [-A <agente>] [-P <proxy ip>] 

    Ejemplo:

    python proy.py -s www.unam.mx -A "Creep 1.0"
    python proy.py -s www.google.com -A "Creep 1.0" -H 

    """
    try:
        opts = addOptions()
        if not opts.server:
            printError('No se ha indicado servidor',True)
        if opts.https:
            url = crea_url(opts.server,opts.port,'https')
        else:
            url = crea_url(opts.server,opts.port)
        urls = crawl(url,crea_sesion(opts.proxy,opts.agent))
        for i in urls:
            print i 

        peticiones(urls)

    except Exception as e:
        printError('Ocurrio un error inesperado')
        printError(e, True)

