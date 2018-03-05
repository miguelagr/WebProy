import sys
import re
import requests

def crawl(url):
    """
    Genera una lista de URL's a partir de un recurso Web.
    Argumentos:

    url (str) : La URL del recurso actual
    Salida:

    urls (str[]): Un arreglo con todos los recursos encontrados
    """
    try:
        lst = []
        respuesta = requests.get(url)
        for rec in re.findall('.*\.js',respuesta.content):
            m = re.match(".*(\'|\")(.*\.js).*",rec)
            if m:
                lst.append(m.group(2))
        urls = []
        http = []
        for rec in lst:
            a = re.compile("http")
            http.extend(filter(a.match,lst))
            b = re.compile("^//")
            dos = filter(b.match, lst)
            c = re.compile("^/[^/]")
            una = filter(c.match,lst)
            d = re.compile("[a-zA-Z][^\:]*$")
            let = filter(d.match,lst)
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



if len(sys.argv) > 1:
    urls = []
    urls.append(sys.argv[1])
    urls.extend(crawl(sys.argv[1]))
    for i in urls:
        print i
    peticiones(urls)
else:
    print "Indicar URL"
    print "\n"

