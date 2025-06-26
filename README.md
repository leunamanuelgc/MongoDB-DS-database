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
## 4.1.	Consultas de filtrado
### 4.1.1.	Por una sola condición
| Consulta 1 | Enemigos que son jefes. |
| --- | --- |

![image](https://github.com/user-attachments/assets/3a9f80ea-2352-4824-882d-5fc9372e4cf9)

‘es_jefe’ es un campo de los enemigos que codifica si es jefe (1) o si no lo es (0), aunque en un futuro podría expandirse para codificar más categorías de enemigos de forma retro compatible. Se ha probado a añadir un índice para mejorar la búsqueda, ya que, a pesar de tratarse de una búsqueda rápida y sencilla, nos evita tocar todos los documentos de enemigos innecesariamente lo cual mejora la escalabilidad y rendimiento de la BBDD. 

| Resultado |
| --- |


![image](https://github.com/user-attachments/assets/2662d0ac-0344-4177-8b9c-dda762d6e2cf) 

| SIN ÍNDICES | CON ÍNDICE |
| --- | --- |
| ![image](https://github.com/user-attachments/assets/2662d0ac-0344-4177-8b9c-dda762d6e2cf) | ![image](https://github.com/user-attachments/assets/b69fbd8b-0f72-4ad5-85c5-a2beb537539b) | ![image](https://github.com/user-attachments/assets/6d2a6800-882e-431c-af6e-035678289641) |

| Consulta 2 | Jugadores que tengan equipada una magia de tipo milagro. |
| --- | --- |

![image](https://github.com/user-attachments/assets/22780710-9e6e-4f90-b3a1-4d86ad1d5be2)

| SIN ÍNDICES | CON ÍNDICE |
| --- | --- |
| ![image](https://github.com/user-attachments/assets/ad4e0949-4196-4f14-846d-f6603952c500) | ![image](https://github.com/user-attachments/assets/8bc031ad-71f2-4c2b-b9ba-9a91d617ef11) |

### 4.1.2.	Por varias condiciones
| Consulta 1 | Mostrar los jefes cuyas almas que dan son mayores a 50000. |
| --- | --- |

![image](https://github.com/user-attachments/assets/9d15b029-9e74-404d-8465-f008857fe7c1)

| Resultado |
| --- |

![image](https://github.com/user-attachments/assets/b8e73b01-7234-41d6-b6f3-98f5af7898eb)

| SIN ÍNDICES | CON ÍNDICE |
| --- | --- |
| ![image](https://github.com/user-attachments/assets/ff164548-0897-48d5-8e07-793eb684abf9) | ![image](https://github.com/user-attachments/assets/4a384b99-c38c-42d3-b223-bc6ccf203d30) ![image](https://github.com/user-attachments/assets/c4644fad-b1f8-4e1a-852d-7365da23fcf8) |

Si bien parece que tarda 1 ms más que en la versión sin índice, se examinan solo 17 documentos, en contraposición a los 119 originales.

| Consulta 2 | Jugadores cuyo nombre contenga ‘x’ (mayúsculas o minúsculas), que tienen equipado un arma de fuego y están invadiendo a alguien. |
| --- | --- |

![image](https://github.com/user-attachments/assets/82d8d51d-4b41-4b1d-b8ae-e4224efc76be)

| Resultado |
| --- |

![image](https://github.com/user-attachments/assets/740a5250-506d-43b7-957b-1569187e57d7)

| SIN ÍNDICES | CON ÍNDICE |
| --- | --- |
| ![image](https://github.com/user-attachments/assets/ff32939a-cb9b-4ac0-a02c-2aecaea8399d) | ![image](https://github.com/user-attachments/assets/92584191-3bbb-410b-a71d-2187f3c948a0) ![image](https://github.com/user-attachments/assets/246ed93d-53fc-49c0-8c6a-a8077b3e37a7) ![image](https://github.com/user-attachments/assets/606930df-9768-45ff-b455-2084fd07f0f6) ![image](https://github.com/user-attachments/assets/89afddab-27ef-4961-8cd2-84f741560b52) ![image](https://github.com/user-attachments/assets/6ba1e8b2-b84f-4976-809b-b385b3988f4b) ![image](https://github.com/user-attachments/assets/3b7adb34-7b5b-4eb9-b95c-7150a43662f5) |

Con la experimentación realizada en el caso de esta consulta, podemos concluir que el uso de un índice de invasiones nos da el resultado óptimo. Esto es gracias a que el índice que crea permite que la consulta acceda directamente a los jugadores invasores, podando gran parte de los documentos que necesita examinar. Como se puede ver, en el caso de un índice por nombres, la mejora no es muy grande ya que igualmente tiene que examinar 500 índices, que es el mismo número de jugadores. En el caso de lista_armas y lista_armas.element, no examina índices por lo que tiene que consultar todos los documentos igualmente. Por último, crear un índice con los tres elementos, hace que se creen una cantidad exageradamente alta de índices, haciendo que examinarlos tarde entre 4 y 5 veces más del tiempo original.

| Consulta 3 | Zonas con 3 o más tipos de enemigos diferentes y menos de 3 hogueras. | 
| --- | --- |
 
![image](https://github.com/user-attachments/assets/835301e1-b3b7-4fa8-9053-bfa92cce79cb)

| SIN ÍNDICES | CON ÍNDICE |
| --- | --- |
| ![image](https://github.com/user-attachments/assets/4c78d769-2be4-4068-bf90-64bf9c92f2c8) | ![image](https://github.com/user-attachments/assets/1cf0a77d-c2d6-496d-a7bb-ba240d3e2e35) ![image](https://github.com/user-attachments/assets/ea5f6c3f-4c68-47d4-bfe9-0fea1b7c231d) |

Se tienen que leer los 31 documentos de zonas y aplicar el filtro en cada uno. Como son pocos, el coste es de 0ms. Con el índice de hogueras se recorren las 47 entradas del índice con num_hogueras < 3 pero al no incluír num_enemigos, se acaban recuperando los 31 documentos que se escanearían aun no teniendo ningún índice.
Al crear un índice compuesto de enemigos y hogueras se pueden resolver ambos filtros en el árbol por lo que no se examinan ni claves ni documentos y se optimiza al máximo la consulta.

| Consulta 4 | Enemigos que dan muchas almas (1000) y tienen poca vida (300) |

![image](https://github.com/user-attachments/assets/87fd2a1d-3386-407f-a9e7-9dec58d974aa)

| Resultado |
| --- |
| ![image](https://github.com/user-attachments/assets/83091138-610c-4b28-b327-dcdc4a3af34e) | 

| SIN ÍNDICES | CON ÍNDICE |
| --- | --- |
| ![image](https://github.com/user-attachments/assets/f5b5cc40-e8c1-4c67-91e3-fb5331ae168e) | ![image](https://github.com/user-attachments/assets/557c2f18-6aa1-487c-bd20-be8c5296b682) ![image](https://github.com/user-attachments/assets/5e9b2267-806a-438b-9d03-127db60fa85e) |

## 4.2.	Consultas de ordenación
| Consulta 1 | Las 5 armas con mayor durabilidad ordenadas de mayor a menor, mostrar nombre, tipo y durabilidad máxima |
| --- | --- |

![image](https://github.com/user-attachments/assets/dcd63975-251e-4faf-a000-c60243681a71)

| SIN ÍNDICES | CON ÍNDICE |
| --- | --- |
| ![image](https://github.com/user-attachments/assets/36f9fa1b-ac9b-40c7-977f-b49b999ce0b8) | ![image](https://github.com/user-attachments/assets/032d0ab2-d323-47f2-8439-9255608cea86) |

| Consulta 2 | Los jugadores que más muertes tienen ordenados de mayor a menor |
| --- | --- |

![image](https://github.com/user-attachments/assets/72b65042-a47e-4b1d-b9c8-def2088a0c53)

| Resultado |
| --- |

Ilustración 37. Los jugadores que más muertes tienen ordenados de mayor a menor
Resultado de la consulta:
 
Ilustración 38. Resultado de consulta 3 de ordenación

SIN ÍNDICES

 
Ilustración 39. Consulta 3 de ordenación sin índices


CON ÍNDICES
Índice: muerte
 
Ilustración 40. Consulta 3 de ordenación con índice de muerte	Índice: muerte y nombre
 
Ilustración 41. Consulta 3 de ordenación con índice de muerte y nombre
Sin índices se tienen que leer los 500 documentos, ordenarlos y extraer los 10 primeros. Con índice sobre muertes, se crea el B-tree descendente y se toman las 10 primeras claves. Se leen 10 claves y 10 documentos en lugar de 500 y se tardan 0 ms en comparación con las 5 iniciales. Creando un índice compuesto de muertes y nombre, se tarda 1 ms y se examinan 0 documentos pero 500 claves. No supone una mejora con respecto a usar el índice de muerte porque ocupa más espacio y no es necesario ya que se está ordenando simplemente por muerte.

4.2.1.3.	Consulta de ordenación 3
El nombre de cada jugador, sus almas y el nombre del pacto al que pertenecen, ordenado por el nombre del jugador alfabéticamente
 
 
Ilustración 42. Primeros resultados de consulta 4.4.2
La lista continúa, pero con esta muestra se ven los campos que aparecen y el orden alfabético. En cuanto a estadísticas se tienen las siguientes:
Sin índices

 
Ilustración 43. Estadísticas pre-índice consulta 4.4.2

Como se puede ver se acceden a 500 documentos y tarda 1 ms. Para mejorar esto se crea el índice de nombres y se vuelve a realizar la consulta usando el .hint. Como la consulta devolverá todos los jugadores, se va a crear el índice con los datos necesarios.
db.jugadores.createIndex({ nombre: 1,  almas:  1, pacto: 1})
Con índices

 
Ilustración 44. Estadísticas post-índice consulta 4.4.2

Así se puede reducir el tiempo ya que solo se accede al índice.
 
4.3.	Consultas nuevas con Aggregation Framework
4.3.1.	Consulta 1 de Aggregation Framework
Tiempos entre muertes, hacer la media por cada jugador y ordenarlos
La agregación para esta consulta se compone de 6 fases, 5 de proyección y 1 de ordenación. Cada fase realiza la siguiente operación para lograr obtener la información deseada de forma incremental:
1º.	 El campo de tiempo de la muerte, que se codifica en tiempo de juego almacenado como una cadena de caracteres con el formato HHH:MM:SS.MS, se toma para calcular con él un valor numerico en milisegundos (desde el comienzo de la partida, al crear el personaje) del momento en el que murió el jugador. Esto se hace para todos los tiempos de muerte de todas las manchas de sangre de todos los jugadores.
 
 
2º. 	Los valores calculados previamente “tiempo_muerte_ms” se utilizan para calcular para cada jugador, todos los intervalos de tiempo transcurridos entre cada tiempo de muerte registrado. Así se averigua cuanto tiempo pasó vivo el jugador, en unidades de tiempo de juego, sin contar la inactividad.
 

3º.	Todos los intervalos de muerte calculados para cada jugador se ponderan para averiguar cuánto tiempo de juego aguanta sin morir ese jugador.
 
 
4º.	El tiempo de vida medio, que sigue siendo una cantidad de tiempo expresada  en milisegundos, se reinterpreta al formato original de HH:MM:SS.MS, para que la información sea más significativa y fácil de leer.
 

5º.	Se ordenan los jugadores según el campo de tiempo de vida medio (en milisegundos), para crear un ranking de la longevidad de los jugadores.
6º.	Finalmente se seleccionan los campos relevantes para mostrar en el ranking, el nombre y el tiempo de vida medio (ya con formato legible) de cada jugador.
 
 Al tratarse de una consulta tan elaborada, su rendimiento es, previsiblemente, algo malo, ya que requiere de muchos pasos intermedios que implican operaciones concretas que manipulan muchos datos como el cambio de formato y el calculo de intervalos y medias. Por ello se ha realizado un estudio en profundidad sobre 3 posibles implementaciones alternativas (V1, V1.5 y V2), y se ha medido su rendimiento tanto sin como con índices para averiguar cuál es la mejor opción. 
*El código previamente presentado es la consulta V1, que resultó ser la versión con mejor rendimiento, junto con el índice manchas_sangre_tiempo_muerte_1.



 
Ilustración 47. Índice creado para optimizar el rendimiento de la consulta de longevidad.

 
4.3.2.	Consulta 2 de Aggregation Framework
Jugadores y sus equipaciones (mostrar sus nombres) ordenados por el número de muertes del jugador (orden ascendente)
 
Ilustración 48. Jugadores y sus equipaciones(mostrar sus nombres) ordenados por el número de muertes del jugador (orden ascendente)
Resultado de la consulta:
 
 
SIN ÍNDICES

 
Ilustración 49. Consulta 2 aggregation framework sin índices
CON ÍNDICES
Índice: Nombre
 	Índice: Manchas de sangre
 
Índice: Arma equipada
 	Índice: Hechizo equipado
 
Índice: Casco equipado
 	Índice: Torso equipado
 
Índice: Pernera equipada
 	Índice: Guantes equipados
 
Índice: Ítem equipado
 	Índice: Arma id (objetos)
 
Índice: Hechizo id
 	Índice: Pieza armadura id
 
Índice: Item id
 	Índice: Ids arma, hechizo, armadura e item
 
Ilustración 50. Consulta 2 aggregation framework con índices
No podemos comprobar el número de documentos a los que se accede, pero calculando el tiempo que tarda podemos comparar las distintas opciones de los índices. Se ha hecho una larga experimentación de tiempos para esta consulta y se ha podido concluir que la creación de índices para los campos que se utilizan del jugador no supone ninguna mejora (al hacer varias veces esta consulta, como es muy compleja, los tiempos fluctúan bastante, por lo que algunos tiempos han salido peores que el que no usaba índices, pero en realidad no significa que haya empeorado el tiempo de la consulta).
En el caso de crear índices de los objetos (sus ids son los que permiten diferenciar el tipo de objeto del que se trata), podemos comprobar que hay una ligera mejora, de unos 100 ms aproximadamente, a excepción de las piezas de armadura, que reducen el tiempo de la consulta hasta medio segundo. Esto es debido a que gran parte de la carga de trabajo de esta consulta es por la agregación de las cuatro piezas de armadura.
Por lo tanto, en este caso, la manera óptima de reducir el tiempo en esta consulta es creando un índice de las piezas de armadura.
4.4.	Consultas de Agregación y combinación
4.4.1.1.	Consulta 1 de agregación y combinación
Los 7 jugadores con más magias en su posesión, mostrar su nombre, id y cantidad de magias
 
Las etapas son las siguientes:
-	Project construye una vista temporal de la colección de jugadores con solo tres elementos, el nombre, el id y el número de hechizos, que se calcula obteniendo el tamaño del array lista_hechizos.
-	Después se ordenan todos los jugadores con sort según su número de hechizos de manera inversa.
-	Por último, se limita el número de jugadores que se muestran a 7 usando limit.
 
Ilustración 51. Primeros 5 jugadores con más hechizos





 
Ilustración 52. Jugadores 6º y 7º con más hechizos

Como el sort se realiza sobre un campo computado, no va a ser de utilidad usar un índice en esta consulta. Otra opción sería crear un campo en los jugadores que tenga el número de hechizos, y luego el índice de esto. Esto mejoraría la eficiencia si se diese el caso de que esta es una consulta frecuente. 
Igualmente se ha medido el tiempo usando new Date( ) y la consulta tarda 36 ms.

4.4.1.2.	Consulta 2 de agregación y combinación
Suma del número total de almas que te da cada tipo enemigo a lo largo de cada zona.

 
Ilustración 53. Suma del número total de almas que te da cada tipo enemigo a lo largo de cada zona.
Se establecen 7 etapas en el pipeline de agregación:
-	Unwind: Se deconstruye el array lista_enemigos de cada documento de zonas, generando un documento independiente por cada elemento del array. Tras esto, cada documento tendrá un campo lista enemigos que es un objeto con enemigo_id y cantidad.
-	Lookup hace join con la colección enemigos.
-	Unwind deconstruye el array info_enemigo, dejando en el campo info_enemigo directamente el objeto con los datos del enemigo.
-	Group: para agrupar cada par zona-enemigo y calcular cuantas almas genera ese tipo de enemigo en esa zona.
-	Group: segunda agrupación, por zona. Calcula la suma total de almas que se pueden conseguir en la zona.
-	Sort: Ordena los documentos resultantes por el campo id (que es la zona_id) en orden ascendente.
-	Project: para generar el documento final.
Resultado de la consulta:


4.4.1.3.	Consulta 3 de agregación y combinación
Mostrar el número total de cada enemigo contando de zona en zona
 
Ilustración 55. Mostrar el número total de cada enemigo contando de zona en zona
Se establecen 5 etapas en el pipeline de agragación: 
-	Unwind para dividir la lista de enemigos en documentos por cada elemento.
-	Group para agrupar los documentos de la etapa anterior desdoblados por las claves zona: “$nombre” y enemigoId: “$lista_enemigos._enemigo_id”;.
-	Lookup para buscar el documento cuyo _enemigo_id coincida con el enemigoId del grupo y añadirlo al campo “detalle”.
-	Unwind de nuevo para sacar el objeto “detalle” del array y poder mostrar sus campos.
-	Project para construir el documento final y mostrarlo tomando zona, enemigo y la suma total.

Resultado de la consulta:
 
Ilustración 56. Consulta 3 de agregación y combinación
 
 
# 5.	Conclusiones
A lo largo de este trabajo se ha adaptado la base de datos relacional de las anteriores dos prácticas al programa de Bases de datos NoSQL MongoDB, que tomaba como referencia el videojuego Dark Souls. Esta adaptación ha supuesto un rediseño, que ha permitido optimizar tanto el almacenamiento como la eficiencia de acceso a los datos, gracias a decisiones clave como la unificación de entidades (jugadores, partidas e invasiones), que han simplificado las consultas y mejorado la coherencia del modelo. Además, se ha introducido la entidad “mancha de sangre”, no solo para reflejar una mecánica fundamental del juego, sino que también para hacer un mejor uso de las posibilidades de MongoDB y así poder realizar un análisis más detallado de la información de los jugadores.
En cuanto al diseño de operaciones CRUD, aunque algunas consultas originales no se pudieron replicar exactmente, se han adaptado correctamente al modelo documental de MongoDB. El trabajo con consultas más complejas ha permitido comprobar la capacidad del modelo para realizar rápidamente las que combinan múltiples condiciones, filtros por subdocumentos y operaciones de conteo y agrupación. El rediseño del esquema y la utilización de índices se ha visto reflejado en el rendimiento de las consultas, especialmente en colecciones grandes como la de jugadores. Asimismo, la comparación del tiempo de ejecución entre consultas con y sin índices ha permitido obtener conclusiones relevantes sobre su impacto real en el rendimiento.
Para finalizar, este trabajo, junto con los anteriores, ha permitido el profundo aprendizaje del funcionamiento de una base de datos real en un entorno tan complejo como el de un videojuego. Gracias al desarrollo y a lo aprendido en cada una, se ha podido realizar los cambios de enfoque necesarios para una correcta implementación de la Base de Datos final. El resultado es un muy buen ejemplo de una Base de Datos con una estructura que ofrece flexibilidad y escalabilidad, sentando una base sólida para un hipotético desarrollo posterior. Además, la realización de las distintas consultas ha servido no solo para validar el modelo, sino también para aprender buenas prácticas en el uso de MongoDB.
 
# 6.	Bibliografía
- [Documentación de la librería element tree](https://docs.python.org/3/library/xml.etree.elementtree.html)
- [Wiki Dark Souls](https://darksouls.wiki.fextralife.com/Dark+Souls+Wiki)
- [Manual de operaciones CRUD de MongoDB](https://www.mongodb.com/docs/manual/crud/)
