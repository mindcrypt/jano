import sys, os
import operator
import codecs

palabrasNoValidas = {}
diccVerbRegulares = {}
diccFemeninoInvariantes = {}
diccVerbIrregularesYconjugaciones = {}
diccVerIrregulares = {}  #lista [verbo] = {lista ...}
verbYconjugacion = []
tablaWSD = {}
window_max = 1
window_counter = 0

def conviertePalabraFemenino(palabra,flag):

        femenino = palabra
        #Si termina en una terminacion concreta femeneno -> masculino
        if palabra.endswith('ete') == True:     femenino = palabra[:-3]+"eta"
        elif palabra.endswith('ote') == True:   femenino = palabra[:-3]+"ote"
        elif palabra.endswith('an') == True:    femenino = palabra[:-3]+"ana"
        elif palabra.endswith('in') == True:    femenino = palabra[:-3]+"ina"
        elif palabra.endswith('on') == True:    femenino = palabra[:-3]+"ona"
        elif palabra.endswith('or') == True:    femenino = palabra[:-3]+"ora"
        elif palabra.endswith('o') == True:     femenino = palabra[:-1]+"a"

        if flag == True:
            femenino = generaPlural(femenino) #femenino plural

        return femenino

def generaPlural(palabra):

    plural = ""
    if palabra.endswith('z') == True:
        plural = palabra[:-1]+"ces" #Si z -> sustituir por ces   --> rapaz, lombriz, luz
    elif (palabra.endswith('a') == True) or (palabra.endswith('e') == True) or (palabra.endswith('i') == True) or (palabra.endswith('o') == True) or palabra.endswith('u') == True or (palabra.endswith('f') == True) or (palabra.endswith('g') == True) or (palabra.endswith('k') == True) or (palabra.endswith('p') == True) or (palabra.endswith('t') == True):
        # Si a,e,i,o,u,f,g,k,p,t --> a\xf1adir s
        plural = palabra + "s"
    else: #Si b,c,d,h,j,l,m,n,q,r,s,v,w,x,y --> a\xf1adir es
        plural = palabra + "es"

    return plural

def esPalabraEnMasculino(palabra):

    flag = False
    if palabra.endswith('s') == True: #verifico en singular.
        palabra = palabra[:-1]
    if (palabra.endswith('o') == True) or (palabra.endswith('ete') == True) or (palabra.endswith('ote') == True) or (palabra.endswith('an') == True) or (palabra.endswith('in') == True) or (palabra.endswith('on') == True) or (palabra.endswith('or') == True):
        flag = True
    return flag

def conviertePalabraMasculino(palabra,flag):

        masculino = palabra

        if palabra in diccFemeninoInvariantes: #Si est\xe1 en lista variante femenino--> se saca su masculino
            masculino = diccFemeninoInvariantes[palabra]
        #Si termina en una terminacion concreta masculino
        elif palabra.endswith('eta') == True:
            masculino = palabra[:-3]+"ete"
        elif palabra.endswith('ote') == True:
            masculino = palabra[:-3]+"ote"
        elif palabra.endswith('ana') == True:
            masculino = palabra[:-3]+"an"
        elif palabra.endswith('ina') == True:
            masculino = palabra[:-3]+"in"
        elif palabra.endswith('ona') == True:
            masculino = palabra[:-3]+"on"
        elif palabra.endswith('ora') == True:
            masculino = palabra[:-3]+"or"
        elif palabra.endswith('a') == True:
            masculino = palabra[:-1]+"o"

        if flag == True:
            masculino += "s"

        return masculino

def esPlural(palabra):
    if palabra.endswith('s') == True: #verifico en singular.
        return True
    return False

def enSingular(palabra):

    flag = False
    if palabra.endswith('ces') == True:
        palabra = palabra[:-3] + "z"   # veloces, capaces -> capaz, veloz
        flag = True
    elif palabra.endswith('ses') == True:
        palabra = palabra[:-2] # dioses -> dios
        flag = True
    elif palabra.endswith('s') == True: #verifico en singular.
        palabra = palabra[:-1]  #padres
        flag = True
    return palabra,flag

def esPalabraEnFemenino(palabra):
    flag = False

    if palabra.endswith('s') == True: #verifico en singular.
        palabra = palabra[:-1]

    if (palabra.endswith('a') == True) or (palabra in diccFemeninoInvariantes) or (palabra.endswith('eta') == True) or (palabra.endswith('ote') == True) or (palabra.endswith('ana') == True) or (palabra.endswith('ina') == True) or (palabra.endswith('ona') == True) or (palabra.endswith('ora') == True):
        flag = True
    return flag

def cargarListaPalabrasNoValidas():
    global palabrasNoValidas
    determinante=['aquel','aquella','aquellas','aquellos','esa','esas','ese','esos','esta','estas','este','estos','mi','mis','tu','tus','su','sus','nuestra','nuestras','nuestro','nuestros','vuestra','vuestras','vuestro','vuestros','suya','suyas','suyo','suyos','cuanta','cuantas','cuantos','cuanto','que','alguna','algunas','alguno','algun','algunos','bastante','bastantes','cada','ninguna','ningunas','ninguno','ningun','otra','otras','otro','otros','sendas','sendos','tantas','tanta','tantos','tanto','todas','toda','todos','todo','varios','varias','cuyas','cuya']
    articulos=['el','la','los','las','un','una','unos','unas','lo','al','del','ella','ellas','ellos']
    conjunciones=['o','u','y']
    preposiciones=['a','ante','bajo','cabe','con','contra','de','desde','durante','en','entre','hacia','hasta','mediante','para','por','segun','sin','sobre','tras']
    pronombre=['se']
    particulasVerbo=['he','has','ha','hemos','hab\xe9is','han','hab\xeda','hab\xedas','hab\xeda','hab\xedamos','hab\xedais','hab\xedan','hube','hubiste','hubo','hubimos','hubisteis','hubieron','habr\xe9','habr\xe1s','habr\xe1','habremos','habr\xe9is','habr\xe1n','habr\xeda','habr\xedas','habr\xeda','habr\xedamos','habr\xedais','habr\xedan','haya','hayas','haya','hayamos','hay\xe1is','hayan','hubiera','hubieras','hubiera','hubi\xe9ramos','hubierais','hubieran','hubiese','hubieses','hubiese','hubi\xe9semos','hubieseis','hubiesen','hubiere','hubieres','hubiere','hubi\xe9remos','hubiereis','hubieren']

    tmp=determinante+articulos+conjunciones+preposiciones+pronombre+particulasVerbo
    for item in tmp:
        palabrasNoValidas[item] = True

def palabraValida(palabraTexto):
    #- Detecto si es una palabra que no puede tener sinonimos -> no le aplico reglas (conj, art, det, pronombre)
    return False

def esVerboRegular(palabraTexto):
    #Ejemplo nadando
    tam = len(palabraTexto)
    totalCaracteres = 1
    flag = False
    global verbYconjugacion
    while totalCaracteres < tam+1:
        if palabraTexto[:-totalCaracteres]+'ar' in diccVerbRegulares:
            #print("====",palabraTexto[:-totalCaracteres]+'ar')
            #print("====",palabraTexto[-totalCaracteres:])
            #print(palabraTexto[-totalCaracteres:] in conjugacionesAR)
            if palabraTexto[-totalCaracteres:] in conjugacionesAR:
                flag = True
                verbYconjugacion.append(palabraTexto[:-totalCaracteres]+'ar')
                verbYconjugacion.append(palabraTexto[-totalCaracteres:])
            break
        elif palabraTexto[:-totalCaracteres]+'er' in diccVerbRegulares:
            if palabraTexto[-totalCaracteres:] in conjugacionesER:
                flag = True
                verbYconjugacion.append(palabraTexto[:-totalCaracteres]+'er')
                verbYconjugacion.append(palabraTexto[-totalCaracteres:])
            break
        elif palabraTexto[:-totalCaracteres]+'ir' in diccVerbRegulares:

            if palabraTexto[-totalCaracteres:] in conjugacionesIR:
                flag = True
                verbYconjugacion.append(palabraTexto[:-totalCaracteres]+'ir')
                verbYconjugacion.append(palabraTexto[-totalCaracteres:])
            break
        totalCaracteres += 1
    return flag
    #conjugacionesAR=['o','as','a','amos','\xe1is','an','aba','abas','aba','\xe1bamos','abais','aban','\xe9','aste','\xf3','amos','asteis','aron','ar\xe9','ar\xe1s','ar\xe1','aremos','ar\xe9is','ar\xe1n','ar\xeda','ar\xedas','ar\xeda','ar\xedamos','ar\xedais','ar\xedan','e','es','e','emos','\xe9is','en','ara','aras','ara','\xe1ramos','arais','aran','ase','ases','ase','\xe1semos','aseis','asen','are','ares','are','\xe1remos','areis','aren']

def cargaFicheroStegoMedio(stegomedio):

            with open(stegomedio,'rt', encoding='iso-8859-1') as f:
                textoProcesar = f.readlines();
            print("[Abrir StegoMedio... OK]");
            textoProcesar=" ".join(textoProcesar)
            textoProcesar=textoProcesar.replace('\n','')
            #print("[",textoProcesar,"]")
            return textoProcesar

def cargarVerbosIrregulares():
            print("[Cargando lista de verbos irregulares... OK]");
            with open('./data/verbosIrregulares.dat','rt', encoding='iso-8859-1') as f:
                listaVerbosIrregulares = f.readlines();
                #55 -> 1+54  54/6=9   realmente son 7 + 1 (que son dos subjuntivo imperfecto muriera o muriese)
            for conjugacionesVerIrregular in listaVerbosIrregulares:
                conjugacionesDelVerboIrregular=(conjugacionesVerIrregular.replace('\n','')).split("|")
                diccVerIrregulares[conjugacionesDelVerboIrregular[0]]=conjugacionesDelVerboIrregular[1:]
                for conjugacion in conjugacionesDelVerboIrregular:
                    diccVerbIrregularesYconjugaciones[conjugacion] = conjugacionesDelVerboIrregular[0] # le meto siempre el verbo en infinito
#--------------------
conjugacionesAR=['o','as','a','amos','\xe1is','an','aba','abas','aba','\xe1bamos','abais','aban','\xe9','aste','\xf3','amos','asteis','aron','ar\xe9','ar\xe1s','ar\xe1','aremos','ar\xe9is','ar\xe1n','ar\xeda','ar\xedas','ar\xeda','ar\xedamos','ar\xedais','ar\xedan','e','es','e','emos','\xe9is','en','ara','aras','ara','\xe1ramos','arais','aran','ase','ases','ase','\xe1semos','aseis','asen','are','ares','are','\xe1remos','areis','aren']
conjugacionesER=['o','es','e','emos','\xe9is','en','\xeda','\xedas','\xeda','iamos','\xedais','\xedan','\xed','iste','i\xf3','imos','isteis','ieron','er\xe9','er\xe1s','er\xe1','eremos','er\xe9is','er\xe1n','er\xeda','er\xedas','er\xeda','er\xedamos','er\xedais','er\xedan','a','as','a','amos','\xe1is','an','iera','ieras','iera','i\xe9ramos','ierais','ieran','iese','ieses','iese','i\xe9semos','ieseis','iesen','iere','ieres','iere','i\xe9remos','iereis','ieren']
conjugacionesIR=['o','es','e','imos0','\xeds','en','\xeda','\xedas','\xeda','\xedamos','\xedais','\xedan','\xed','iste','i\xf3','imos0','isteis','ieron','ir\xe9','ir\xe1s','ir\xe1','iremos','ir\xe9is','ir\xe1n','ir\xeda','ir\xedas','ir\xeda','ir\xedamos','ir\xedais','ir\xedan','a','as','a','amos','\xe1is','an','iera','ieras','iera','i\xe9ramos','ierais','ieran','iese','ieses','iese','i\xe9semos','ieseis','iesen','iere','ieres','iere','i\xe9remos','iereis','ieren']

def cargarVerbosRegulares():
        print("[Cargando lista de verbos regulares... OK]");
        with open('./data/verbosRegulares.dat','rt', encoding='iso-8859-1') as f:
            verbosRegulares = f.readlines();
        '''
        presenteIndicativoConjAR preteritoImperfectoIndicativoConjAR preteritoPerfectoSimpleIndicativoConjAR
        futuroIndicativoConjAR condicionalIndicativoConjAR preteritoImperfectoISubjuntivoConjAR
        preteritoImperfectoIISubjuntivoConjAR futuroSubjuntivoConjAR
        '''
        for verboRegular in verbosRegulares:
            verboRegular=verboRegular.replace('\n','')
            cadenaConjugaciones = ""
            if verboRegular.endswith('ar'):
                cadenaConjugaciones=conjugacionesAR
            if verboRegular.endswith('er'):
                cadenaConjugaciones=conjugacionesER
            if verboRegular.endswith('ir'):
                cadenaConjugaciones=conjugacionesIR
            diccVerbRegulares[verboRegular]=cadenaConjugaciones #regla de conjugaciones
            #print(verboRegular,":",diccVerbRegulares[verboRegular])
#--------------------
def cargarPayload(bitString): #para cuando se lea de fichero
    return bitString

def cargarListaFemeninoVariante():
    print("[Cargando lista femenino variante... OK]");

    with open('./data/tablaFemeninoVariante.txt','rt', encoding='iso-8859-1') as f:
        listaFemeninosVariante = f.readlines();

    for femeninoInvariante in listaFemeninosVariante:
        itemFemeninoInvariante=(femeninoInvariante.replace('\n','')).split(" ")
        diccFemeninoInvariantes[itemFemeninoInvariante[1]]=itemFemeninoInvariante[0] #femenino = masculino

wsd = {}
def cargaWSD():
    print("[Cargando tablaWSD...]");
    with open('./data/TABLA_WSD_WIKIv1.txt','rt', encoding='iso-8859-1') as f:
        lineastablaWSD = f.readlines();
    #wsd["esto vi"]=1
    for i in lineastablaWSD:  #Obtengo el valor en el WSD - #11 esto vi\n
        i=i.strip("\n")
        tmp=i.split()
        if len(tmp) == 3:
            clave = tmp[1]+" "+tmp[2]
            wsd[clave]=tmp[0]

    print("[Cargando tablaWSD... [OK]");

def eligeStegoPalabra(antes,seleccion,despues):

    listaCandidatosSinonimos = seleccion.split("|")  # viento|bendabal|...
    antes = antes.lower()
    despues = despues.lower()
    prioridadSinonimos = {}

    for p in range(len(listaCandidatosSinonimos)):
        prioridadSinonimos[listaCandidatosSinonimos[p]]=0
        if antes+" "+listaCandidatosSinonimos[p] in wsd:
            prioridadSinonimos[listaCandidatosSinonimos[p]] = prioridadSinonimos[listaCandidatosSinonimos[p]]+ int(wsd[antes+" "+listaCandidatosSinonimos[p]])
        if listaCandidatosSinonimos[p]+" "+despues in wsd:
            prioridadSinonimos[listaCandidatosSinonimos[p]] = prioridadSinonimos[listaCandidatosSinonimos[p]]+ int(wsd[listaCandidatosSinonimos[p]+" "+despues])

    prioridadSinonimos=sorted(prioridadSinonimos.items(),key=operator.itemgetter(1),reverse=True)
    #stegoPalabra = ""
    #if bitOcultar == 0: #print(prioridadSinonimos[0])
        #print(prioridadSinonimos[0][0],end="") #1er probable
    #    stegoPalabra = prioridadSinonimos[0][0]
    #else:
        #print(prioridadSinonimos[1][0],end="") #2nd probable
    #    stegoPalabra = prioridadSinonimos[1][0]
    #return stegoPalabra
    return prioridadSinonimos

diccSinonimosRegla = {}
diccSinonimos = {}

def cargarSynsets(url):
        print("[Cargando diccionario de synsets... OK]");
        with open(url,'rt', encoding='iso-8859-1') as f:
            synsets = f.readlines();
        contador=0
        for reglaDiccSyn in synsets:
            reglaDiccSyn = reglaDiccSyn.replace('\n','')
            diccSinonimosRegla[contador]=reglaDiccSyn # dicc[0]=regla de sinonimos
            sinonimosEnLaRegla=reglaDiccSyn.split("|")
            for sinonimo in sinonimosEnLaRegla:
                diccSinonimos[sinonimo] = contador  #    dicc[cadaPalabra]=meto en que linea est\xe1
            contador = contador + 1

def imprimeDetalles(totalPalabras, palabrasDetectadas, palabraDescartada,palabraNoEnDiccionario,palabraNoDetectada,bitStringOculto):

    print("")
    print("Words:")
    print(" Total palabras:",totalPalabras);
    print(" Palabras Detectadas:", palabrasDetectadas);
    print(" Palabras Descartadas:",palabraDescartada);
    print(" Palabras No dicc:", palabraNoEnDiccionario);
    print(" Palabra No Detectada:",palabraNoDetectada);
    print("")
    print("StegoChanel:")
    print(" Ocultando: ",len(bitStringOculto)," bits - [",bitStringOculto,"]");
    print("    Max: ",palabrasDetectadas," bits") #limitado por el tamano de window util para WSD

def filtraPalabra(palabra):

    prefijo = ""
    sufijo = ""

    posPre = 0
    posSuf = 0
    for i in range(0,len(palabra)):
        if palabra[i] == '¿' or palabra[i] == '¡' or palabra[i] == '"' or palabra[i] == "," or palabra[i] == "." or palabra[i] == ";" or palabra[i] == ":" or palabra[i] == '(' or palabra[i] == '[' or palabra[i] == '\'':
            posPre = posPre + 1
        else:
            break
    prefijo = palabra[0:posPre]

    for i in range(len(palabra)-1,-1,-1):
        if palabra[i] == "?" or palabra[i] == "!" or palabra[i] == '"' or palabra[i] == "," or palabra[i] == "." or palabra[i] == ";" or palabra[i] == ":" or palabra[i] == ")" or palabra[i] == "]" or palabra[i] == '\'':
            posSuf = posSuf + 1
        else:
            break

    if posSuf == 0:  posSuf = -len(palabra)

    if posPre == len(palabra):
        sufijo = ""
        prefijo = ""
    else:
        sufijo = palabra[-posSuf:]
        palabra = palabra[posPre:-posSuf]


    return prefijo,sufijo,palabra

def updateStegoText(palabrasDetectadas,textoCodificado,nuevoTexto):
       global window_counter
       palabrasDetectadas = palabrasDetectadas + 1
       textoCodificado=textoCodificado+nuevoTexto
       window_counter = window_counter + 1
       return palabrasDetectadas,textoCodificado

def menu():
    print("")
    print("JANO 0.1 2008-2009 (experimental) - Steganographic tool using spanish synonyms");
    print("Autor - Dr. Alfonso Munoz (@mindcrypt)");
    print("")
    print("Uso: #jano -h|u <source/stego text> <diccSynset> <ouput> <binaryInfoToHide/show>");
    print("Ej.  #jano -h texto.txt diccSynset stego.txt 1010101010");
    print("     #jano -u stego.txt diccSynset 12");
    print("")

def main(paramIn):

    totalPalabras = 0
    palabrasDetectadas = 0
    palabraNoEnDiccionario = 0
    palabraDescartada = 0
    palabraNoDetectada = 0
    textoCodificado = ""

    if len(sys.argv)<5:  #jano u|h file output binary
        menu()
    elif sys.argv[1]!='-h' and sys.argv[1]!='-u':
        menu()
    elif sys.argv[1]=='-h' and len(sys.argv)!=6:
        menu()
    elif sys.argv[1]=='-u' and len(sys.argv)!=5:  #jano u file tam
        menu()
    else:
        print(" ")
        cargarVerbosIrregulares()
        cargarVerbosRegulares()
        cargaWSD()
        cargarSynsets(sys.argv[3])
        cargarListaFemeninoVariante()
        cargarListaPalabrasNoValidas()
        option = sys.argv[1]
        textoProcesar=cargaFicheroStegoMedio(sys.argv[2]);
        payload=""
        if sys.argv[1]=='-h':
          payload=cargarPayload(sys.argv[5])

        global window_counter,window_max

        for palabra in textoProcesar.split(): # proceso palabra a palabra del TEXTO
            totalPalabras = totalPalabras + 1
            prefijo,sufijo,palabra=filtraPalabra(palabra)

            if window_counter < window_max:
                #print("PALABRA PROCEAR:",palabra)
                if (palabra not in palabrasNoValidas) and (palabra.islower() == True):  #palabrasValidas, descarto las que empiezan por mayuscula
                    candidatosPosiblesOcultacion = ''
                    flag = False
                    palabraEnSingular,flagPlural = enSingular(palabra)
                    if palabra in diccSinonimos: # Regla1 está en diccionario
                        #print("en dicc")
                        palabrasDetectadas,textoCodificado=updateStegoText(palabrasDetectadas,textoCodificado,diccSinonimosRegla[diccSinonimos[palabra]]+" ")

                    elif palabraEnSingular in diccSinonimos:
                        #print("en dicc =>")
                        candidatosPosiblesSinonimos = diccSinonimosRegla[diccSinonimos[palabraEnSingular]].split("|")
                        candidatosPosiblesSinonimos.pop()
                        for candidatoSinonimo in candidatosPosiblesSinonimos:
                             candidatosPosiblesOcultacion += generaPlural(candidatoSinonimo)+"|"
                        palabrasDetectadas,textoCodificado=updateStegoText(palabrasDetectadas,textoCodificado,candidatosPosiblesOcultacion+" ")

                    elif esVerboRegular(palabra) == True:
                        global verbYconjugacion
                        if verbYconjugacion[0] in diccSinonimos: # verbYconjugacion = [verbo, conjugacion]
                            candidatosPosiblesSinonimos = (diccSinonimosRegla[diccSinonimos[verbYconjugacion[0]]].split("|"))
                            candidatosPosiblesSinonimos.pop()

                            for candidatoSinonimo in candidatosPosiblesSinonimos:
                                if candidatoSinonimo in diccVerbIrregularesYconjugaciones: # si es irregular
                                    candidatoSinonimo = diccVerbIrregularesYconjugaciones[candidatoSinonimo] #ejemplo ser|cosa
                                    todasLasCongugacionVerIrregularCandidato=diccVerIrregulares[candidatoSinonimo] # Le metes el verbo en infinitivo y te devuelven las conjugaciones (la palabra entera)

                                    if verbYconjugacion[0].endswith('ar') == True:
                                        candidatosPosiblesOcultacion += todasLasCongugacionVerIrregularCandidato[conjugacionesAR.index(verbYconjugacion[1])] + "|"   #verbYconjugacion[1] tengo la conjugacion solo parte final
                                    if verbYconjugacion[0].endswith('er') == True:
                                        candidatosPosiblesOcultacion += todasLasCongugacionVerIrregularCandidato[conjugacionesER.index(verbYconjugacion[1])] + "|"   #verbYconjugacion[1] tengo la conjugacion solo parte final
                                    if verbYconjugacion[0].endswith('ir') == True:
                                        candidatosPosiblesOcultacion += todasLasCongugacionVerIrregularCandidato[conjugacionesIR.index(verbYconjugacion[1])] + "|"   #verbYconjugacion[1] tengo la conjugacion solo parte final
                                #si es regular
                                elif candidatoSinonimo in diccVerbRegulares:
                                        verboRegularRaiz = candidatoSinonimo[:-2]
                                        conjugacionesVerboRegular=diccVerbRegulares[candidatoSinonimo]
                                        conjugacionCandidata = ''
                                        if verbYconjugacion[0].endswith('ar') == True:
                                            conjugacionCandidata=conjugacionesVerboRegular[conjugacionesAR.index(verbYconjugacion[1])]
                                        if verbYconjugacion[0].endswith('er') == True:
                                            conjugacionCandidata=conjugacionesVerboRegular[conjugacionesER.index(verbYconjugacion[1])]
                                        if verbYconjugacion[0].endswith('ir') == True:
                                            conjugacionCandidata=conjugacionesVerboRegular[conjugacionesIR.index(verbYconjugacion[1])]

                                        candidatosPosiblesOcultacion += verboRegularRaiz + conjugacionCandidata + "|"
                                else:
                                        candidatosPosiblesOcultacion += candidatoSinonimo + "|"

                            palabrasDetectadas,textoCodificado=updateStegoText(palabrasDetectadas,textoCodificado,candidatosPosiblesOcultacion+" ")

                        else: #[PALABRA DESCARTADA SIN CAPACIDAD DE OCULTACION]
                            textoCodificado=textoCodificado+palabra+" "
                            palabraNoEnDiccionario += 1
                        verbYconjugacion = []
                    elif palabra in diccVerbIrregularesYconjugaciones:
                        #print("============>")
                        if flag == False:
                            #print("VERBO LEIDO: IRREGULAR",palabra)
                            verIrregular=diccVerbIrregularesYconjugaciones[palabra] #cojo el verbosIrregular en infinitivo
                            #print("INFINitivo:",verIrregular)
                            if verIrregular in diccSinonimos: # en el dicc están en infinitivo
                                reglaSinonimos=diccSinonimosRegla[diccSinonimos[verIrregular]] #meto la linea y obtengo la regla
                                candidatosPosiblesSinonimos = (reglaSinonimos.split("|"))
                                #print("Posibles sinonimos:",candidatosPosiblesSinonimos)
                                candidatosPosiblesSinonimos.pop()
                                for candidatoSinonimo in candidatosPosiblesSinonimos:
                                    if candidatoSinonimo in diccVerbIrregularesYconjugaciones:
                                        candidatoSinonimo = diccVerbIrregularesYconjugaciones[candidatoSinonimo] #ejemplo ser|cosa
                                        todasLasCongugacionVerIrregularCandidato=diccVerIrregulares[candidatoSinonimo] # TODAS LAS CONJUGACIONES DEL SINONIMO CANDIDATO (QUE ES VERB IRREGULAR) A LA PALABRA DETECTADA (VERBO IRREGULAR)
                                        todasLasCongugacionVerIrregularDetectado=diccVerIrregulares[verIrregular]  #TODAS LAS CONJUGACIONES DE LA PALABRA DETECTADA EN EL TEXTO
                                        candidatosPosiblesOcultacion += todasLasCongugacionVerIrregularCandidato[todasLasCongugacionVerIrregularDetectado.index(palabra)] + "|"
                                    elif candidatoSinonimo in diccVerbRegulares:
                                        verboRegularRaiz = candidatoSinonimo[:-2]
                                        #print("CANDIDATO PROBANDO VERB REGULAR:",candidatoSinonimo)
                                        todasLasCongugacionVerIrregularDetectado=diccVerIrregulares[verIrregular]  #TODAS LAS CONJUGACIONES DE LA PALABRA DETECTADA EN EL TEXTO
                                        #print("Conjug Ver Irregular Dectado:",todasLasCongugacionVerIrregularDetectado)
                                        conjugacionesVerboRegular=diccVerbRegulares[candidatoSinonimo]

                                        #print("Conjug verb regular:",conjugacionesVerboRegular)
                                        #print("Pos:",todasLasCongugacionVerIrregularDetectado.index(palabra));
                                        conjugacionCandidata=conjugacionesVerboRegular[todasLasCongugacionVerIrregularDetectado.index(palabra)] # se que conjugacion es la palabra, luego calculo la posicion en VERBO regular
                                        #print("PEPE")
                                        candidatosPosiblesOcultacion += verboRegularRaiz + conjugacionCandidata + "|"
                                    else:
                                        candidatosPosiblesOcultacion += candidatoSinonimo + "|"

                                palabrasDetectadas,textoCodificado=updateStegoText(palabrasDetectadas,textoCodificado,candidatosPosiblesOcultacion+" ")
                            else: #DESCARTADA")
                                textoCodificado=textoCodificado+palabra+" "
                                palabraNoEnDiccionario += 1
                                palabraDescartada += 1

                    elif esPalabraEnFemenino(palabra) == True:
                        #print("===========================>")
                        palabraProcesar,flag = enSingular(palabra)
                        masculino = conviertePalabraMasculino(palabraProcesar, False)
                        if masculino in diccSinonimos:
                            candidatosPosiblesSinonimos = (diccSinonimosRegla[diccSinonimos[masculino]].split("|"))
                            candidatosPosiblesSinonimos.pop()
                            for candidatoSinonimo in candidatosPosiblesSinonimos:
                                candidatosPosiblesOcultacion += conviertePalabraFemenino(candidatoSinonimo,flag)+"|"
                            palabrasDetectadas,textoCodificado=updateStegoText(palabrasDetectadas,textoCodificado,candidatosPosiblesOcultacion+" ")
                        else: #[PALABRA DESCARTADA SIN CAPACIDAD DE OCULTACION]")
                            textoCodificado=textoCodificado+palabra+" "
                            palabraNoEnDiccionario += 1
                    elif esPalabraEnMasculino(palabra) == True:
                            #print("=======================================>")
                            if palabra.endswith('ido') == False:
                                palabraProcesar,flag = enSingular(palabra)
                                if palabraProcesar in diccSinonimos:
                                        candidatosPosiblesSinonimos = (diccSinonimosRegla[diccSinonimos[palabraProcesar]].split("|"))
                                        candidatosPosiblesSinonimos.pop()
                                        for candidatoSinonimo in candidatosPosiblesSinonimos:
                                                candidatosPosiblesOcultacion += conviertePalabraMasculino(candidatoSinonimo,flag)+"|"
                                        palabrasDetectadas,textoCodificado=updateStegoText(palabrasDetectadas,textoCodificado,candidatosPosiblesOcultacion+" ")
                                else:
                                    textoCodificado=textoCodificado+palabra+" "
                                    palabraNoEnDiccionario += 1
                            else:
                                textoCodificado=textoCodificado+palabra+" "
                                palabraDescartada += 1
                    else:
                            textoCodificado=textoCodificado+palabra+" "
                            palabraNoDetectada += 1
                else:
                    #print("*")
                    textoCodificado=textoCodificado+palabra+" "
                    palabraDescartada += 1
            else:
                #print("***")
                window_counter = 0
                textoCodificado=textoCodificado+palabra+" "
                palabraDescartada += 1

        imprimeDetalles(totalPalabras, palabrasDetectadas, palabraDescartada,palabraNoEnDiccionario,palabraNoDetectada,payload)
        window_max = 1
        window_counter = 0

        if sys.argv[1]=='-h':
            if len(sys.argv[5]) > palabrasDetectadas:
                print("No hay espacio en el stegomedio para ocultar")
            else:
                listaPalabras = textoCodificado.split()
                indexPayload = 0
                palabrasImprimidas = 0
                stegoTexto = ""
                for i in range(len(listaPalabras)): #stegotexto con las opciones
                    # al desincronizar
                    if indexPayload == len(payload): # ya he ocultado todo imprimo directamente el texto de entrada
                        texto=textoProcesar.split()
                        for word in range(palabrasImprimidas+1,len(texto)):
                            #print(texto[word]+" ", end="")
                            stegoTexto = stegoTexto+texto[word]+" "
                        break;
                    elif listaPalabras[i].find("|") == -1: # Proceso una palabra que No tiene candidatos
                        #print(""+listaPalabras[i]+" ",end="")
                        stegoTexto = stegoTexto+""+listaPalabras[i]+" "
                        palabrasImprimidas = palabrasImprimidas + 1
                        window_counter = 0
                    else: #Palabra con capacidad de ocultación
                            antes = "" #si es la primera palabra -> considero solo la posterior
                            despues = "" #Si es la ultima solo la anterior
                            bitOcultar = int(payload[indexPayload])
                            indexPayload = indexPayload + 1
                            if i<len(listaPalabras):
                                despues = listaPalabras[i+1]
                            if i>0:
                                antes = listaPalabras[i-1]
                            #stegoTexto = stegoTexto+eligeStegoPalabra(antes,listaPalabras[i],despues)+" "
                            prioridadSinonimos = eligeStegoPalabra(antes,listaPalabras[i],despues) # funcion para W=1
                            '''
                            print("---------------------")
                            print(bitOcultar,"|0|",prioridadSinonimos[0][0],"|1|",prioridadSinonimos[1][0])
                            print("ANTES:",antes)
                            print("DESPUES:",despues)
                            print(" ")
                            print(listaPalabras[i])
                            print(prioridadSinonimos)
                            print(" ")
                            print("---------------------")
                            print("---------------------")
                            '''
                            #print(repr(prioridadSinonimos[1][0].encode('iso-8859-1')))
                            stegoPalabra = ""
                            if bitOcultar == 0: #print(prioridadSinonimos[0])
                                    #print(prioridadSinonimos[0][0],end="") #1er probable
                                    stegoPalabra = prioridadSinonimos[0][0]
                            else:
                                    #print(prioridadSinonimos[1][0],end="") #2nd probable
                                    stegoPalabra = prioridadSinonimos[1][0]

                            stegoTexto = stegoTexto+stegoPalabra+" "
                            palabrasImprimidas = palabrasImprimidas + 1
                            print(" ",end="")
                #print(stegoTexto)
                stegoTexto=addExtraChar(stegoTexto,textoProcesar)
                print("")
                print("[Guardando StegoFile... OK]")
                print("")
                f=codecs.open(sys.argv[4],"w","ISO-8859-1")
                f.write(stegoTexto)
                f.close()
                #print(stegoTexto)  print("")  #print(textoProcesar)
        else:
            print("")
            print("Recuperando Info oculta (ver ",sys.argv[4]," bits):")
            print(" ",end="")
            listaPalabras = textoCodificado.split()
            listaTextoOriginal = textoProcesar.split()
            bitsRecuperados = 0
            print("")
            print(" ",end="")
            stringRecuperado = ""
            for i in range(len(listaPalabras)): #stegotexto con las opciones
                #print("COMPROBANDO:",listaPalabras[i])
                if window_counter<window_max and (bitsRecuperados < int(sys.argv[4])):
                    #print("=>")
                    if listaPalabras[i].find("|") != -1: # para las palabras que tienen candidatos
                        #print("=>>")
                        antes = "" #si es la primera palabra -> considero solo la posteior
                        despues = "" #Si es la ultima solo la anterior

                        '''
                        print("PALABRA ANTES:",listaPalabras[i-1])
                        print("PALABRA ACTUAL:",listaPalabras[i])
                        print("PALABRA DESPU:",listaPalabras[i+1])
                        '''

                        if i<len(listaPalabras):
                            despues = listaPalabras[i+1]
                        if i>0:
                            antes = listaPalabras[i-1]

                        #print("ANTES:",antes," DESPUES:",despues)
                        prioridadSinonimos = eligeStegoPalabra(antes,listaPalabras[i],despues)
                        #print(prioridadSinonimos)
                        prefijo,sufijo, palabraOculta = filtraPalabra(listaTextoOriginal[i])
                        #indentifices -> identifiques
                        '''
                        print("--------------------------------------------")
                        print(prioridadSinonimos)

                        print("Seleccionado =",end="")

                        '''
                        if palabraOculta == prioridadSinonimos[0][0]:
                            print("0",end="")
                            stringRecuperado=stringRecuperado+"0"
                        if palabraOculta == prioridadSinonimos[1][0]:
                            print("1",end="")
                            stringRecuperado=stringRecuperado+"1"

                        '''
                        if bitsRecuperados == int(sys.argv[4]):
                            print("\n")
                            print(stringRecuperado)
                            exit(); #dejo de leer mas y cierro programa
                        '''

                        bitsRecuperados = bitsRecuperados + 1

                        window_counter = window_counter + 1

                        '''
                        print(" [",listaTextoOriginal[i],"] |0|",prioridadSinonimos[0][0],"|1|",prioridadSinonimos[1][0])
                        print(prioridadSinonimos)
                        print("Bit 0:",prioridadSinonimos[0][0])
                        print("Bit 1:",prioridadSinonimos[1][0])
                        print("--------------------------------------------")
                        '''
                        #stegoPalabra = prioridadSinonimos[0][0]
                        #stegoPalabra = prioridadSinonimos[1][0]
                else:
                        #print("ventana ko")
                        window_counter = 0
            print("\n")

def addExtraChar(stegoTexto,textoProcesar):
    contador = 0
    wordSteg=stegoTexto.split()
    tmpStegoText = ""

    for i in textoProcesar.split():

        if contador < len(wordSteg):
            prefijo,sufijo,i=filtraPalabra(i)

            if wordSteg[contador].endswith(sufijo) == True:
                sufijo = ""
            if wordSteg[contador].startswith(prefijo) == True:
                prefijo = ""

            tmpStegoText=tmpStegoText+prefijo+wordSteg[contador]+sufijo+" "
            #print("----------")
            #print("Original [",i,"]")
            #print("[",prefijo,"][",wordSteg[contador],"][",sufijo,"]")
        contador += 1

    return tmpStegoText
main(sys.argv)
