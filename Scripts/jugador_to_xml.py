import json
import xml.etree.ElementTree as ET
from generate_jugador import generate_player
from generate_jugador import choose_player
import json
from lxml import etree
import random

def validar_xml(xml_file, xsd_file):
    try:
        with open(xsd_file, 'rb') as xsd_f:
            schema_doc = etree.XML(xsd_f.read())
            schema = etree.XMLSchema(schema_doc)

        with open(xml_file, 'rb') as xml_f:
            xml_doc = etree.parse(xml_f)

        schema.assertValid(xml_doc)
        print("El XML es válido.")
    
    except etree.DocumentInvalid as e:
        print("El XML NO es válido:")
        print(e)
    except Exception as e:
        print(f"Error al validar el XML: {e}")

def crear_xml(jugadores):
    root = ET.Element("jugadores")
    
    for jugador in jugadores:
        jugador_elem = ET.SubElement(root, "jugador", jugador_id=jugador["jugador_id"])
        ET.SubElement(jugador_elem, "nombre").text = jugador["nombre"]
        ET.SubElement(jugador_elem, "almas").text = jugador["almas"]
        ET.SubElement(jugador_elem, "pacto").text = jugador["pacto"]
        
        # Lista de armas
        lista_armas_elem = ET.SubElement(jugador_elem, "lista_armas")
        for arma in jugador["lista_armas"]:
            arma_elem = ET.SubElement(lista_armas_elem, "arma", arma_id=arma["arma_id"])
            ET.SubElement(arma_elem, "durabilidad").text = arma["durabilidad"]
            ET.SubElement(arma_elem, "nivel").text = arma["nivel"]
            ET.SubElement(arma_elem, "elemento").text = arma["elemento"]
        
        ET.SubElement(jugador_elem, "arma_equipada").text = jugador["arma_equipada"]
        
        # Lista de magias
        lista_magias_elem = ET.SubElement(jugador_elem, "lista_hechizos")
        for magia in jugador["lista_hechizos"]:
            magia_elem = ET.SubElement(lista_magias_elem, "hechizo", hechizo_id=magia["hechizo_id"])
        
        ET.SubElement(jugador_elem, "hechizo_equipado").text = jugador["hechizo_equipado"]
        
        # Lista de armaduras
        lista_armaduras_elem = ET.SubElement(jugador_elem, "lista_piezas_armaduras")
        for armadura in jugador["lista_piezas_armaduras"]:
            armadura_elem = ET.SubElement(lista_armaduras_elem, "pieza_armadura", pieza_armadura_id=armadura["pieza_armadura_id"])
            ET.SubElement(armadura_elem, "durabilidad").text = armadura["durabilidad"]
        
        ET.SubElement(jugador_elem, "casco_equipado").text = jugador["casco_equipado"]
        ET.SubElement(jugador_elem, "torso_equipado").text = jugador["torso_equipado"]
        ET.SubElement(jugador_elem, "pernera_equipada").text = jugador["pernera_equipada"]
        ET.SubElement(jugador_elem, "guantes_equipado").text = jugador["guantes_equipado"]
        
        # Lista de consumibles
        lista_items_elem = ET.SubElement(jugador_elem, "lista_items")
        for item in jugador["lista_items"]:
            item_elem = ET.SubElement(lista_items_elem, "item", item_id=item["item_id"])
            ET.SubElement(item_elem, "cantidad").text = item["cantidad"]
        
        ET.SubElement(jugador_elem, "item_equipado").text = jugador["item_equipado"]
        # Zona actual
        ET.SubElement(jugador_elem,"zona_actual_id").text = jugador["zona_actual_id"]

        #Invasion
        invasion_elem = ET.SubElement(jugador_elem, "invasion")
        if jugador["invasion"] != None:
            ET.SubElement(invasion_elem, "jugador_invadido_id").text = jugador["invasion"]["jugador_invadido_id"]
            ET.SubElement(invasion_elem, "es_aliado").text = jugador["invasion"]["es_aliado"]

        # Manchas de sangre
        manchas_sangre_elem = ET.SubElement(jugador_elem,"manchas_sangre")
        for mancha in jugador["manchas_sangre"]:
            mancha_elem = ET.SubElement(manchas_sangre_elem, "mancha_sangre")
            ET.SubElement(mancha_elem,"tiempo_muerte").text = mancha["tiempo_muerte"]
            ET.SubElement(mancha_elem,"causa_muerte").text = mancha["causa_muerte"]
            ET.SubElement(mancha_elem,"zona_muerte").text = mancha["zona_muerte"]
            ET.SubElement(mancha_elem,"almas_al_morir").text = mancha["almas_al_morir"]
            piezas_armaduras_al_morir_elem = ET.SubElement(mancha_elem,"piezas_armaduras_al_morir")
            ET.SubElement(piezas_armaduras_al_morir_elem,"casco_id").text = mancha["piezas_armaduras_al_morir"]["casco_id"]
            ET.SubElement(piezas_armaduras_al_morir_elem,"torso_id").text = mancha["piezas_armaduras_al_morir"]["torso_id"]
            ET.SubElement(piezas_armaduras_al_morir_elem,"piernas_id").text = mancha["piezas_armaduras_al_morir"]["piernas_id"]
            ET.SubElement(piezas_armaduras_al_morir_elem,"guantes_id").text = mancha["piezas_armaduras_al_morir"]["guantes_id"]
            ET.SubElement(mancha_elem,"arma_al_morir").text = mancha["arma_al_morir"]

    # Indentar el árbol XML para que sea legible
    ET.indent(ET.ElementTree(root), space="  ", level=0)
    
    # Escribir el archivo XML con indentación
    ET.ElementTree(root).write("jugadores.xml", encoding="utf-8", xml_declaration=True)
    # stylesheet = '<?xml-stylesheet type="text/css" href="jugador-partida.css"?>'
    # with open("jugador-partida.xml", "a") as file:
    #     file.writelines("\n")
    #     file.write(stylesheet)
    

if __name__ == "__main__":
    jugadores = [generate_player(i) for i in range(500)]

    elegidos = []

    for i in range(50):
        jugador_elegido = random.choice(jugadores)
        while jugador_elegido in elegidos:
            jugador_elegido = random.choice(jugadores)
        elegidos.append(jugador_elegido)
        jugadores[ int(jugador_elegido["jugador_id"]) ] = choose_player(jugador_elegido, jugadores)

    # Imprimir el resultado en formato JSONs
    # print(json.dumps(jugadores, indent=4))
    crear_xml(jugadores)
    validar_xml("jugadores.xml", "jugadores.xsd")