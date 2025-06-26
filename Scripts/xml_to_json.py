import xmltodict
import json
import sys
from collections import OrderedDict

from collections import OrderedDict

def rename_enemy_text_fields(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "lista_enemigos":
                if isinstance(value, list):
                    for i in range(len(value)):
                        enemigo = value[i]
                        cantidad = enemigo.pop("_cantidad", None)
                        enemigo_id = enemigo.pop("#text", None)
                        new_enemigo = OrderedDict()
                        if cantidad is not None:
                            new_enemigo["cantidad"] = cantidad
                        if enemigo_id is not None:
                            new_enemigo["_enemigo_id"] = enemigo_id
                        new_enemigo.update(enemigo)  # por si hay más campos
                        value[i] = new_enemigo
                elif isinstance(value, dict):
                    enemigo = value
                    cantidad = enemigo.pop("_cantidad", None)
                    enemigo_id = enemigo.pop("#text", None)
                    new_enemigo = OrderedDict()
                    if cantidad is not None:
                        new_enemigo["cantidad"] = cantidad
                    if enemigo_id is not None:
                        new_enemigo["_enemigo_id"] = enemigo_id
                    new_enemigo.update(enemigo)
                    data[key] = new_enemigo
            else:
                rename_enemy_text_fields(value)
    elif isinstance(data, list):
        for item in data:
            rename_enemy_text_fields(item)

def reorder_attributes(data):
    # Diccionario de listas que deben ser "aplanadas"
    lista_a_planas = {
        "manchas_sangre": "mancha_sangre",
        "lista_armas": "arma",
        "lista_hechizos": "hechizo",
        "lista_piezas_armaduras": "pieza_armadura",
        "lista_items": "item",
        "lista_enemigos": "enemigo",
        "lista_hogueras": "hoguera"
    }

    if isinstance(data, dict):
        new_data = OrderedDict()
        attrs = OrderedDict()

        for key, value in data.items():
            if key.startswith('@'):
                attrs['_' + key[1:]] = reorder_attributes(value)

            elif key in lista_a_planas and isinstance(value, dict) and lista_a_planas[key] in value:
                item_key = lista_a_planas[key]
                item_list = value[item_key]

                # Si es solo uno, convertirlo en lista
                if not isinstance(item_list, list):
                    item_list = [item_list]

                # Procesar elementos recursivamente
                new_data[key] = [reorder_attributes(item) for item in item_list]

            else:
                new_data[key] = reorder_attributes(value)

        new_data.update(attrs)
        return new_data

    elif isinstance(data, list):
        return [reorder_attributes(item) for item in data]

    else:
        return data

def convert_xml_to_json(xml_file_path, json_file_path):
    with open(xml_file_path, 'r', encoding='utf-8') as xml_file:
        xml_data = xml_file.read()
        data_dict = xmltodict.parse(xml_data)
        cleaned_data = reorder_attributes(data_dict)

    # 🛠️ Quitar la raíz si es {"jugadores": {"jugador": [...]}}
    if "jugadores" in cleaned_data and "jugador" in cleaned_data["jugadores"]:
        cleaned_data = cleaned_data["jugadores"]["jugador"]
    elif "zonas" in cleaned_data and "zona" in cleaned_data["zonas"]:
        cleaned_data = cleaned_data["zonas"]["zona"]
    
    rename_enemy_text_fields(cleaned_data)

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(cleaned_data, json_file, indent=4, ensure_ascii=False)

    print(f"✅ Archivo JSON guardado en: {json_file_path}")


# Uso: python xml_to_json.py entrada.xml salida.json
if __name__ == "__main__":
    file_name = input()
    convert_xml_to_json(f"{file_name}.xml", f"{file_name}.json")
