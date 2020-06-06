# JANO

La herramienta JANO permite la creación de canales encubiertos en lenguaje natural en lengua española usando sustitución de palabras por sinónimos considerando diferentes cuestiones lingüísticas. JANO es la única herramienta conocida que realiza esto en lengua española accesible de manera abierta. Para ver detalles lea los siguientes apartados.

# Uso y parámetros

```
@:~JANO/RELEASE_06062020$ python3 jano.py
JANO 0.1 2008-2009 (experimental) - Steganographic tool using spanish synonyms
Autor - Dr. Alfonso Munoz (@mindcrypt)

Uso: #jano -h|u <source/stego text> <diccSynset> <ouput> <binaryInfoToHide/show>
Ej.  #jano -h texto.txt diccSynset stego.txt 1010101010
     #jano -u stego.txt diccSynset 12
```
```
@:~JANO/RELEASE_06062020$ python3 jano.py -h manifiestoHacker.txt ./data/diccSynsetVerbV3.dat stegoManifiesto.txt 10111101101010
 
[Cargando lista de verbos irregulares... OK]
[Cargando lista de verbos regulares... OK]
[Cargando tablaWSD...]
[Cargando tablaWSD... [OK]
[Cargando diccionario de synsets... OK]
[Cargando lista femenino variante... OK]
[Abrir StegoMedio... OK]

Words:
 Total palabras: 561
 Palabras Detectadas: 54
 Palabras Descartadas: 364
 Palabras No dicc: 128
 Palabra No Detectada: 47

StegoChanel:
 Ocultando:  14  bits - [ 10111101101010 ]
    Max:  54  bits
              
[Guardando StegoFile... OK]
```
```
@:~/JANO/RELEASE_06062020$ python3 jano.py -u stegoManifiesto.txt ./data/diccSynsetVerbV3.dat 14
 
[Cargando lista de verbos irregulares... OK]
[Cargando lista de verbos regulares... OK]
[Cargando tablaWSD...]
[Cargando tablaWSD... [OK]
[Cargando diccionario de synsets... OK]
[Cargando lista femenino variante... OK]
[Abrir StegoMedio... OK]

Words:
 Total palabras: 560
 Palabras Detectadas: 54
 Palabras Descartadas: 363
 Palabras No dicc: 128
 Palabra No Detectada: 47

StegoChanel:
 Ocultando:  0  bits - [  ]
    Max:  54  bits

Recuperando Info oculta (ver  14  bits):
 10111101101010
```
```
[Texto original]

El manifiesto del hacker

Hoy han cogido a otro, aparece en todos los periódicos. "Joven arrestado por delito informático", "hacker arrestado por irrumpir en un 
sistema bancario". "Malditos críos. Son todos iguales". ¿Pero pueden, con su psicología barata y su cerebro de los años cincuenta, siquiera 
echar un vistazo a lo que hay detrás de los ojos de un hacker? ¿Se han parado alguna vez a pensar qué es lo que les hace comportarse así, 
qué les ha convertido en lo que son? Yo soy un hacker, entre en mi mundo. Mi mundo comienza en el colegio. Soy más listo que el resto de mis
compañeros, lo que enseñan me parece muy aburrido. "Malditos profesores. Son todos iguales". Puedo estar en el colegio o un instituto. Les 
he oído explicar cientos de veces cómo se reducen las fracciones. Todo eso ya lo entiendo. "No, Sr. Smith, no he escrito mi trabajo. Lo 
tengo guardado en la cabeza". "Malditos críos. Seguro que lo ha copiado. Son todos iguales". Hoy he descubierto algo. Un ordenador. Un
momento, esto mola. Hace lo que quiero que haga. Si comete errores, es porque yo le he dicho que lo haga. No porque yo no le guste, me tenga
miedo, piense que soy un listillo o no le guste ni enseñar ni estar aquí. Malditos críos. A todo lo que se dedican es a jugar. Son todos 
iguales. Entonces ocurre algo... se abre una puerta a un nuevo mundo... todo a través de la línea telefónica, como la heroína a través de 
las venas, se emana un pulso electrónico, buscaba un refugio ante las incompetencias de todos los días... y me encuentro con un teclado. "Es
esto... aquí pertenezco... ". Conozco a todo mundo... aunque nunca me haya cruzado con ellos, les dirigiese la palabra o escuchase su voz...
los conozco a todos... malditos críos. Ya está enganchado otra vez al teléfono. Son todos iguales... puedes apostar lo quieras a que son 
todos iguales... les das la mano y se toman el brazo... y se quejan de que se lo damos todo tan masticado que cuando lo reciben ya ni 
siquiera tiene sabor. O nos gobiernan los sádicos o nos ignoran los apáticos. Aquellos que tienen algo que enseñar buscan desesperadamente
alumnos que quieran aprender, pero es como encontrar una aguja en un pajar. Este mundo es nuestro... el mundo de los electrones y los 
interruptores, la belleza del baudio. Utilizamos un servicio ya existente, sin pagar por eso que podrían haber sido más barato si no fuese 
por esos especuladores. Y nos llamáis delincuentes. Exploramos... y nos llamáis delincuentes. Buscamos ampliar nuestros conocimientos... y 
nos llamáis delincuentes. No diferenciamos el color de la piel, ni la nacionalidad, ni la religión... y vosotros nos llamáis delincuentes. 
Construís bombas atómicas, hacéis la guerra, asesináis, estafáis al país y nos mentís tratando de hacernos creer que sois buenos, y aún nos
tratáis de delincuentes. Sí, soy un delincuente. Mi delito es la curiosidad. Mi delito es juzgar a la gente por lo que dice y por lo que
piensa, no por lo que parece. Mi delito es ser más inteligente que vosotros, algo que nunca me perdonaréis. Soy un hacker, y éste es mi 
manifiesto. Podéis eliminar a algunos de nosotros, pero no a todos...  después de todo, somos todos iguales.
```
```
[Stegotexto]
Hoy han cogido a otro, aparece en todos los periódicos. "Joven arrestado por delito informático", "hacker arrestado por irrumpir en un
sistema bancario". "Malditos críos. Son todos empates". ¿Pero pueden, con su psicología barata y su cerebro de los años cincuenta, siquiera
atacar un vistazo a lo que hay detrás de los ojos de un hacker? ¿Se han parado alguna vez a decidir qué es lo que les hace comportarse así,
qué les ha convertido en lo que son? Yo soy un hacker, entre en mi mundo. Mi mundo comienza en el colegio. Soy más listo que el resto de mis
compañeros, lo que enseñan me figura muy aburrido. "Malditos profesores. Son todos empates". Puedo estar en el colegio o un instituto. Les
he oído definir cientos de veces cómo se bajan las fracciones. Todo eso ya lo entiendo. "No, Sr. Smith, no he escrito mi esfuerzo. Lo tengo
en la cabeza". "Malditos". "críos. Seguro. que lo ha copiado. Son. todos iguales". Hoy". he descubierto algo. Un. ordenador. Un. momento,
esto, mola. Hace. lo que quiero que haga. Si. comete errores, es, porque yo le he dicho que lo haga. No. porque yo no le guste, me, tenga 
miedo, piense, que soy un listillo o no le guste ni enseñar ni estar aquí. Malditos. críos. A. todo lo que se dedican es a jugar. Son. todos
iguales. Entonces. ocurre algo... se... abre una puerta a un nuevo mundo... todo... a través de la línea telefónica, como, la heroína a
través de las venas, se, emana un pulso electrónico, buscaba, un refugio ante las incompetencias de todos los días... y... me encuentro con 
un teclado. "Es. "esto... aquí... pertenezco... ".... Conozco a todo mundo... aunque... nunca me haya cruzado con ellos, les, dirigiese la
palabra o escuchase su voz... los... conozco a todos... malditos... críos. Ya. está enganchado otra vez al teléfono. Son. todos iguales...
puedes... apostar lo quieras a que son todos iguales... les... das la mano y se toman el brazo... y... se quejan de que se lo damos todo tan
masticado que cuando lo reciben ya ni siquiera tiene sabor. O. nos gobiernan los sádicos o nos ignoran los apáticos. Aquellos. que tienen
algo que enseñar buscan desesperadamente alumnos que quieran aprender, pero, es como encontrar una aguja en un pajar. Este. mundo es 
nuestro... el... mundo de los electrones y los interruptores, la, belleza del baudio. Utilizamos. un servicio ya existente, sin, pagar por 
eso que podrían haber sido más barato si no fuese por esos especuladores. Y. nos llamáis delincuentes. Exploramos... y... nos llamáis 
delincuentes. Buscamos. ampliar nuestros conocimientos... y... nos llamáis delincuentes. No. diferenciamos el color de la piel, ni, la 
nacionalidad, ni, la religión... y... vosotros nos llamáis delincuentes. Construís. bombas atómicas, hacéis, la guerra, asesináis, estafáis,
al país y nos mentís tratando de hacernos creer que sois buenos, y, aún nos tratáis de delincuentes. Sí,. soy, un delincuente. Mi. delito es
la curiosidad. Mi. delito es juzgar a la gente por lo que dice y por lo que piensa, no, por lo que parece. Mi. delito es ser más inteligente
que vosotros, algo, que nunca me perdonaréis. Soy. un hacker, y, éste es mi manifiesto. Podéis. eliminar a algunos de nosotros, pero, no a 
todos... después... de todo, somos, todos iguales. 
Este. es el último artículo de El Mentor. 
```


