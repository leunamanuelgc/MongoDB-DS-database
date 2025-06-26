# Diseño e implementación de una Base de Datos en MongoDB
| Gestión de Datos en Medios Digitales | Curso 2024/25 |
| --- | --- |

- Alberto Alegre Burcio
- Rodrigo Dueñas Herrero
- Manuel Gutiérrez Castro
- Lucas Rodríguez Bravo
- Antón Rodríguez Seselle
- Bernat Roselló Muñoz

## Índice
- 1.	Introducción	5
- 2.	Identificación de las consultas	7
- 3.	Creación de Documentos	10
- 4.	Diseño de operaciones CRUD	16
- 5.	Conclusiones	45
- 6.	Bibliografía	46
 
# 1.	Introducción
En este documento se detalla y justifica el proceso de rediseño y adaptación a MongoDB de la base de datos creada en las anteriores prácticas, sobre el videojuego Dark Souls, así como las decisiones tomadas según las consultas.
![image](https://github.com/user-attachments/assets/ea12e130-d994-41e9-a684-369826dd7322)

Dark Souls se trata de una saga de videojuegos de rol y acción, desarrollados por FromSoftware. Estos juegos se caracterizan por su profundo Worldbuilding, en el que el jugador asume el papel de un no-muerto que viaja por un mundo oscuro, luchando contra una diversidad de monstruos implacables. 
El jugador deberá explorar y descubrir los secretos ocultos a lo largo del juego, mientras consigue equipamiento (como armas, armaduras, hechizos y otros objetos) que lo potencia y que permita maximizar las posibilidades de sobrevivir y matar a los jefes más fuertes. Al acabar con estos conseguirá grandes cantidades de almas, que le permitirá mejorarse sus estadísticas y mejorar su equipamiento.
Además, en estos juegos se permite la conexión con otros jugadores a través de invasiones, que pueden ser de distintos tipos: invasión como aliado, o invasión como enemigo.
 
## 1.1.	Glosario de términos
- Elemento imbuido. En Dark Souls, la mayoría de las armas pueden aumentar su nivel utilizando unos minerales, mejorando sus estadísticas de daño. Además, mediante determinados unas gemas, es posible añadirles efectos concretos (p.ej: imbuir un arma con una gema de cristal, le añadirá daño de magia. Una gema de fuego, en cambio, le añadirá daño de fuego).
- Efecto (en los hechizos). Se trata de una descripción de lo que realiza este hechizo en concreto.
- Pieza de armadura. Una pieza de armadura es una parte de un conjunto completo de armadura. Además, el slot de armadura se refiere a qué parte del cuerpo pertenece esa pieza de armadura (p.ej: yelmo de hierro es una pieza del conjunto de hierro, que pertenece al slot de armadura de la cabeza).
- Ítem. Hemos denominado ítem a cualquier objeto útil de Dark Souls, que no es ni arma, armadura ni hechizo (p.ej: frasco de Estus. Un objeto que permite que el jugador se cure).
- Almas. Se trata de la moneda universal del juego. Sirven para subir de nivel tu personaje, comprar objetos, mejorar armas y armaduras, entre otros. Además, al morir desaparecen estas, y para recuperarlas, es necesario volver al último lugar donde el jugador perdió. En caso de no lograrlo, perderá las almas obtenidas para siempre (pues se reemplazarán por las almas que tenía en el último momento al morir de nuevo).
- Pacto. Un Pacto es una facción a la que el jugador puede unirse. Por una parte, formar parte de uno otorga varios beneficios y recompensas, pero, por otro lado, impone ciertas reglas al jugador. Romperlas puede generar efectos negativos. Ciertos pactos tienen efecto en las interacciones en línea del jugador.
- Partida. Se refiere a una partida concreta de un jugador concreto. Esta tendría todas las estadísticas del mundo y del jugador que pertenece a esa partida.
- Invasión. Una de las interacciones en línea que permite el juego es mediante invasiones. Existen dos tipos de invasiones en el juego: invasión como enemigo, en el que un jugador invade la partida de otro jugador para enfrentarse a él; e invasión como aliado, en el que se invade la partida para ayudarle, tanto para acabar con jefes del juego en sí, como para defenderte de invasiones enemigas. Las invasiones pueden ocurrir en contra de la voluntad del jugador (siempre que se tenga el juego configurado para ello), permitiendo ser atacado por sorpresa por otro jugador.
- Zona. El juego cuenta con un extenso mundo dividido en distintas zonas, en las que se encuentran distintos enemigos, jefes y objetos del juego.
- Mancha de sangre. En el juego, las muertes dentro del mundo se representan mediante las “Manchas de sangre”. Al interactuar con estas, un jugador puede ver los instantes previos a la muerte de otros jugadores. En nuestra base de datos, se ha decidido implementar esto como cierta información que indica el momento de la muerte en el tiempo que lleva de partida, la zona de muerte, la causa y lo que lleva equipado. 

# 2.	Identificación de las consultas
DarkSouls es un juego en el que la dificultad y la muerte de los jugadores es clave para su popularidad. Además, la muerte de los jugadores se comparte en línea entre las distintas partidas en tiempo real, mediante las “manchas de sangre” (consultar Glosario de términos). Debido a esto, es imprescindible tener mucha información de todas las muertes de los jugadores para poder reproducirlas dentro del juego.	 
![image](https://github.com/user-attachments/assets/0a5ae7d0-a3c3-4143-964c-b8f282d2a61d)

Es por ello por lo que, para la Base de Datos de MongoDB, se ha querido añadir más información a los jugadores, mediante las manchas de sangre.

## 2.1.	Consultas más frecuentes
Antes de realizar los cambios necesarios en la BBDD, se ha determinado que el tipo de consultas más frecuentes para nuestro videojuego serían las que tengan que ver con los jugadores (para poder ver la información concreta de cada uno en el momento en el que se encuentran), y la información de sus muertes (que reflejan muy bien el estado de las partidas desde el principio), para poder balancear los enemigos, la cantidad de enemigos que aparecen en cada zona, las estadísticas de las armas, etc.

| Consultas frecuentes con el fin de equilibrar el juego |
| --- |
- Causa de muerte que se repite con mayor frecuencia, momento y zona en el que ocurre en la partida.
- Cantidad de muertes de los jugadores por cada zona.
- Mayor cantidad de almas perdidas por los jugadores.
- Jugadores con menor número de muertes y jugadores con mayor número de muertes.
- Búsqueda de las mayores y menores diferencias de tiempos entre muertes de cada jugador.
- Objetos equipables (armaduras, armas, hechizos, ítems) más utilizados (tanto por los jugadores como en las muertes de estos).
- Enemigos que salen en más zonas.
- Jugadores pertenecientes a un pacto que más invade.

## 2.2.	Cambios en la Base de Datos
Debido a estas consultas y al añadido de las manchas de sangre, se han hecho varios cambios fundamentales en el diseño de la BBDD.
Antes de añadir la nueva entidad, se ha cambiado la manera en la que funcionan las partidas y los jugadores. En las prácticas previas, se contemplaban jugadores y partidas como dos entidades distintas una de la otra, algo que dentro del contexto del videojuego tendría sentido. Sin embargo, a efectos prácticos, no había realmente diferencia entre los jugadores y las partidas, y, debido al diseño de las consultas más frecuentes, se ha tomado la decisión de unificar las tres entidades principales (“jugadores”, “partidas” e “invasiones”) en una sola: “jugadores”. De esta manera, la BBDD en MongoDB no tiene que acceder a distintos documentos para poder acceder a las zonas, las invasiones, ni tampoco las manchas de sangre, ya que al principio se contempló la idea de que “Mancha de sangre formase parte de Partidas”.

Aparte de esta modificación, se añadieron las Manchas de Sangre ya mencionadas previamente. La entidad contiene la siguiente información:
- ‘tiempo_muerte’: instante en el que murió el jugador dentro de su partida.
- ‘causa_muerte’: pequeña descripción con la causa de muerte del jugador.
- ‘zona_muerte’: identificador de la zona en la que murió el jugador.
- ‘almas_al_morir’: número de almas que tenía el jugador al morir.
- ‘piezas_armadura_al_morir’: contiene los identificadores del casco, torso, pernera y guanteletes en el instante de la muerte.
- ‘arma_al_morir’: identificador del arma que llevaba el jugador en ese momento.	 

![image](https://github.com/user-attachments/assets/d437c16b-28db-46b1-bacd-d6bb26007d89)

| Esquema definitivo de la BBDD completa |
| --- |

![image](https://github.com/user-attachments/assets/df2178a7-754c-44fb-95c1-bbf5132fc084)


# 3.	Creación de Documentos

## 3.1.	Modificación de “jugador-partida.xml” a “jugadores.xml”
Para poder crear los documentos de la BBDD, primero ha sido necesario adaptar el fichero “jugador-partida.xml” al nuevo diseño. Para ello, se han modificado los scripts “generate_jugador_partida.py” y “jugador_partida_to_xml.py”, que ahora han pasado a llamarse “generate_jugador.py” y “jugador_to_xml.py”, respectivamente. Se ha seguido haciendo uso de la librería ElementTree para la creación, estructuración y acceso a los ficheros ‘.xml’, y, además se ha incorporado la librería ‘numpy’, para poder obtener elementos aleatorios aplicando distintos pesos.

Las modificaciones principales en el script de generación de datos son:
- Unificación de los elementos de partida e invasión dentro de jugador: el elemento zona_actual_id de partida ha pasado a estar en jugador, e invasión ha pasado a ser un elemento interno también de jugador. Las invasiones pueden o ser null, o contener el id del jugador invadido, y si la invasión se realiza como aliado o no.
- Para la generación de invasión, no se puede crear directamente junto al jugador, sino que ha sido necesario crear una función ‘choose_player’ que se llama posteriormente a la creación de todos los jugadores.
- Se ha creado una función ‘generate_bloodstain’ que es la encargada de generar la información de una mancha de sangre. La función ‘generate_player’ hará varias llamadas a esta función para obtener las manchas de sangre y guardarlas en un array, que será añadido a la información de la partida.
- En la función ‘generate_bloodstain’ se crea información de manera aleatoria, de modo que se obtienen los ids del equipamiento del jugador, el número de almas, la zona, el tiempo de muerte y la causa de muerte.
- Para el tiempo de muerte y la causa de muerte ha sido necesario crear algunas funciones extra:
- 1. ‘generate_death_reason’ elige unos tipos de muertes más generales aleatoriamente y con distintos pesos (muerte por un jefe: 60%, muerte por un enemigo: 30%, muerte por otra causa: 10%), y según el tipo de muerte, se elige aleatoriamente un jefe, un enemigo o una causa de muerte distinta dentro de las establecidas.
  2. En el caso de los tiempos de muerte se han creado las funciones ‘generate_deathtime’, para generar un tiempo aleatorio (entre 0h, 0min, 0 sec y 0 milisec, y 0 h, 30 m, 59, sec y 999 milisec. El máximo establecido se ha puesto de manera que el tiempo de la última muerte generada no sea exageradamente alto y así tenga algo más de coherencia con una partida real), y ‘add_time’, que suma dos tiempos y devuelve el resultado.

![image](https://github.com/user-attachments/assets/1b11d0e8-2a03-4606-9515-0e18b701dd85)
 
![image](https://github.com/user-attachments/assets/0a456cf3-4fa5-4d98-892d-1de6102c961e)

![image](https://github.com/user-attachments/assets/82ed3334-7a0c-4f6c-80a3-da350682c62f)

![image](https://github.com/user-attachments/assets/940e7940-ab77-492b-b535-ac21e62f4069)

![image](https://github.com/user-attachments/assets/ab96ff58-a4f7-4a13-a7a1-ff7c475e5183)

Las modificaciones en el script de conversión de datos a xml han sido las pertinentes para la creación de las manchas de sangre, y para unificar los elementos de partidas e invasiones en jugadores:
 
![image](https://github.com/user-attachments/assets/aaa3e213-6a2e-4ed1-8a87-6d751eee8c83)

Además, se hicieron las modificaciones necesarias en el esquema, que pasó a llamarse ‘jugadores.xsd’, para que el xml fuese validado correctamente.

![image](https://github.com/user-attachments/assets/b116b30d-bc2b-40f5-97e1-9e841a8d79b8)

## 3.2.	Conversión de XML a JSON
Para convertir los archivos XML a documentos JSON, se ha hecho de dos maneras. Para ‘enemigos’ y ‘objetos’ se ha utilizado la herramienta online JSON formatter: https://jsonformatter.org/xml-to-json. En el caso de ‘jugadores’, los cambios hicieron que aumentara de manera exponencial su tamaño, pasando de 1.31 MB a 54.7 MB, haciendo imposible el procesamiento del archivo por parte de la página. Es por ello por lo que se creó un nuevo script ‘xml_to_json.py’ que convierte un archivo XML a formato JSON, utilizando la librería xmltodict. Además, al crearse ‘zonas’, el formato que se creaba para los arrays no era el adecuado, así que también se optó por realizar el script para que fuese compatible con este fichero.
 
![image](https://github.com/user-attachments/assets/367ec17e-f5d6-4e5c-a44d-efe338505dc7)

Finalmente, dentro de MongoDB se crearon 4 colecciones: enemigos, jugadores, objetos y zonas, en las que se importaron los archivos JSON creados para crear los distintos documentos.
 
![image](https://github.com/user-attachments/assets/740a0df3-6984-4528-b9b6-d2987147c6eb)

# 4.	Diseño de operaciones CRUD
Para realizar las consultas, se han tenido que adaptar algunas consultas de la base de datos con respecto a la primera práctica, debido a que no ha sido posible replicar algunas de estas consultas.
Además, para la medición de tiempos de las consultas que utilizan Aggregation Framework, ha sido necesario realizarlo utilizando los siguientes comandos en la Shell:
 
![image](https://github.com/user-attachments/assets/4761d0b3-4a7f-48d8-af3d-1dee41573112)

A pesar de ser esta última una opción no determinista, nos permite comparar en términos generales la eficiencia de una misma consulta, pero aplicando la creación de índices.
Además, es importante mencionar que algunas de las consultas que se realizaron en la primera práctica, no contenían varias condiciones, es por ello por lo que se ha hecho una selección de algunas de las consultas originales, pero añadiendo alguna condición extra. 

| Para ver las consultas acceder al pdf | [MEMORIA](https://github.com/leunamanuelgc/MongoDB-DS-database/blob/main/GDMD_Practica3_DarkSoulsBBDD_MongoDB.pdf) |
| --- | --- |

# 5.	Conclusiones
A lo largo de este trabajo se ha adaptado la base de datos relacional de las anteriores dos prácticas al programa de Bases de datos NoSQL MongoDB, que tomaba como referencia el videojuego Dark Souls. Esta adaptación ha supuesto un rediseño, que ha permitido optimizar tanto el almacenamiento como la eficiencia de acceso a los datos, gracias a decisiones clave como la unificación de entidades (jugadores, partidas e invasiones), que han simplificado las consultas y mejorado la coherencia del modelo. Además, se ha introducido la entidad “mancha de sangre”, no solo para reflejar una mecánica fundamental del juego, sino que también para hacer un mejor uso de las posibilidades de MongoDB y así poder realizar un análisis más detallado de la información de los jugadores.
En cuanto al diseño de operaciones CRUD, aunque algunas consultas originales no se pudieron replicar exactmente, se han adaptado correctamente al modelo documental de MongoDB. El trabajo con consultas más complejas ha permitido comprobar la capacidad del modelo para realizar rápidamente las que combinan múltiples condiciones, filtros por subdocumentos y operaciones de conteo y agrupación. El rediseño del esquema y la utilización de índices se ha visto reflejado en el rendimiento de las consultas, especialmente en colecciones grandes como la de jugadores. Asimismo, la comparación del tiempo de ejecución entre consultas con y sin índices ha permitido obtener conclusiones relevantes sobre su impacto real en el rendimiento.
Para finalizar, este trabajo, junto con los anteriores, ha permitido el profundo aprendizaje del funcionamiento de una base de datos real en un entorno tan complejo como el de un videojuego. Gracias al desarrollo y a lo aprendido en cada una, se ha podido realizar los cambios de enfoque necesarios para una correcta implementación de la Base de Datos final. El resultado es un muy buen ejemplo de una Base de Datos con una estructura que ofrece flexibilidad y escalabilidad, sentando una base sólida para un hipotético desarrollo posterior. Además, la realización de las distintas consultas ha servido no solo para validar el modelo, sino también para aprender buenas prácticas en el uso de MongoDB.
 
# 6.	Bibliografía
- [Documentación de la librería element tree](https://docs.python.org/3/library/xml.etree.elementtree.html)
- [Wiki Dark Souls](https://darksouls.wiki.fextralife.com/Dark+Souls+Wiki)
- [Manual de operaciones CRUD de MongoDB](https://www.mongodb.com/docs/manual/crud/)
