from faker import Faker
import random
import xml.etree.ElementTree as ET
import numpy

fake = Faker()
Faker.seed(0)

prefixes = [
    "xX", "__XxX", "XxX", "Xx", "xx", 
    "The_", "Lord_", "Dark_", "Void_", 
    "Shadow_", "Night_", "Mr_", "Sir_", 
    "Overlord_", "Dread_", "Fear_", "Blood_", 
    "Death_", "Soul_", "Grim_", "King_", "Master_"
]

suffixes = [
    "Xx", "XxX__", "XxXxX", "xx", "420", 
    "666", "XxXxXx", "_Master", "_Destroyer", 
    "_Reaper", "_Slayer", "_Lord", "_King", 
    "_Overlord", "_Champion", "_Dark", "_Void", 
    "_Shadow", "_Knight", "_Of_Doom", "_of_Death",
    "_420BlazeIt", "_NoScope", "_Pwned", "_FTW",
    "_Epic", "_Legendary", "_TheEnd", "_XD"
]

def generate_weapons(max_weapons, max_weapon_level):
    tree = ET.parse("objetos.xml")
    root = tree.getroot()
    list_of_weapons = root.findall(".//arma")

    rand = random.randint(1,max_weapons)
    generated_weapons = []

    for _ in range(rand):
        weapon_id = f"arma{random.randint(0, len(list_of_weapons)-1)}"
        max_durability = root.find(f".//arma[@arma_id='{weapon_id}']/durabilidad_max").text
        weapon = {
            "arma_id": f"{weapon_id}",
            "durabilidad": str(random.randint(1,int(max_durability))),
            "nivel": str(random.randint(1, max_weapon_level)),
            "elemento": random.choice(["Crystal", "Lightning", "Raw", "Magic", "Enchanted", "Divine", "Occult", "Fire", "Chaos"])
        }
        generated_weapons.append(weapon)
    return generated_weapons

def generate_magic_elems(max_magic_elems):
    tree = ET.parse("objetos.xml")
    root = tree.getroot()
    list_of_magic_elems = root.findall(".//hechizo")

    rand = random.randint(1,max_magic_elems)
    generated_magic_elems = []

    for _ in range(rand):
        magic_id = f"hechizo{random.randint(0, len(list_of_magic_elems)-1)}"
        magic_elem = {"hechizo_id": magic_id}
        generated_magic_elems.append(magic_elem)
    return generated_magic_elems

def generate_armor(max_armor_elems):
    tree = ET.parse("objetos.xml")
    root = tree.getroot()
    list_of_armor_elems = root.findall(".//pieza_armadura")

    rand = random.randint(1,max_armor_elems)
    generated_armor_elems = []
    slots = {
        "Cabeza":[],
        "Torso":[],
        "Piernas":[],
        "Manos":[]
    }

    for _ in range(rand):
        armor_id = f"pieza_armadura{random.randint(0, len(list_of_armor_elems)-1)}"
        max_durability = root.find(f".//pieza_armadura[@pieza_armadura_id='{armor_id}']/durabilidad_max").text
        if max_durability == "-" or max_durability == "None":
            durability = None
        else:
            durability = round(random.uniform(1, float(max_durability)), 1)
        armadura_elem = {
            "pieza_armadura_id":armor_id,
            "durabilidad":str(durability)
            }
        generated_armor_elems.append(armadura_elem)

        slot = root.find(f".//pieza_armadura[@pieza_armadura_id='{armor_id}']/slot_armadura").text
        #print(armor_id +": " +slot)
        if slot == "Cabeza":
            slots["Cabeza"].append(armadura_elem)
        elif slot == "Torso":
            slots["Torso"].append(armadura_elem)
        elif slot == "Piernas":
            slots["Piernas"].append(armadura_elem)
        elif slot == "Manos":
            slots["Manos"].append(armadura_elem)
        
    return generated_armor_elems, slots

def generate_consumables(max_consumables):
    tree = ET.parse("objetos.xml")
    root = tree.getroot()
    list_of_consumables = root.findall(".//item")

    rand = random.randint(1,max_consumables)
    generated_consumables = []
    
    for _ in range(rand):
        consumable_id = f"item{random.randint(0, len(list_of_consumables)-1)}"
        consumable = {
            "item_id": consumable_id,
            "cantidad":str(random.randint(1,99))
            }
        generated_consumables.append(consumable)
    return generated_consumables

pIds_chosen = []
def choose_player(player, players):
    player_id = random.randint(0, len(players)-1)
    #players_ids = {int(p["jugador_id"]) for p in players}
    while player_id in pIds_chosen or player_id == int(player["jugador_id"]):
        player_id = random.randint(0, len(players)-1)
        continue
    player["invasion"] = {
        "jugador_invadido_id": str(player_id),
        "es_aliado": random.choice(["True", "False"])
    }
    pIds_chosen.append(player_id)
    return player

def generate_player(player_id):
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)

    list_weapons = generate_weapons(30, 15)
    equipped_weapon = random.choice(list_weapons)

    list_magic_elems = generate_magic_elems(20)
    equipped_magic = random.choice(list_magic_elems)

    list_armor_elems, slots = generate_armor(30)
    
    slots_cabeza = slots["Cabeza"]
    slots_torso = slots["Torso"]
    slots_piernas = slots["Piernas"]
    slots_manos = slots["Manos"]

    if slots_cabeza:
        equipped_head = f"{random.choice(slots_cabeza)["pieza_armadura_id"]}"
    else:
        equipped_head = None

    if slots_torso:
        equipped_torso = f"{random.choice(slots_torso)["pieza_armadura_id"]}"
    else:
        equipped_torso = None

    if slots_piernas:
        equipped_legs = f"{random.choice(slots_piernas)["pieza_armadura_id"]}"
    else:
        equipped_legs = None

    if slots_manos:
        equipped_hands = f"{random.choice(slots_manos)["pieza_armadura_id"]}"
    else:
        equipped_hands = None
    
    # print("Jugador " + str(player_id) + " " +
    #       str(equipped_head) + " " + str(equipped_torso) + " " +
    #       str(equipped_legs) + " " + str(equipped_hands))

    list_consumables = generate_consumables(200)
    equipped_consumable = random.choice(list_consumables)

    manchas_sangre = []

    last_time = [0,0,0,0]
    for i in range(random.randint(50,300)):
        generated_bloodstain, last_time = generate_bloodstain(i, last_time)
        manchas_sangre.append(generated_bloodstain)

    player = {
        "jugador_id": str(player_id),
        "nombre": f"{prefix}{fake.first_name()}{suffix}",
        "almas": str(random.randint(0, 999999999)),
        "pacto": random.choice(["Way of White", "Princess's Guard", "Blade of the Darkmoon",
                                "Warrior of Sunlight", "Forest Hunter", "Chaos Servant",
                                "Gravelord Servant", "Path of the Dragon", "Darkwraith"]),
        "lista_armas": list_weapons,
        "arma_equipada": f"{equipped_weapon["arma_id"]}",
        "lista_hechizos": list_magic_elems,
        "hechizo_equipado": f"{equipped_magic["hechizo_id"]}",
        "lista_piezas_armaduras": list_armor_elems,
        "casco_equipado": equipped_head,
        "torso_equipado": equipped_torso,
        "pernera_equipada": equipped_legs,
        "guantes_equipado": equipped_hands,
        "lista_items": list_consumables,
        "item_equipado": f"{equipped_consumable["item_id"]}",
        "zona_actual_id": str(random.randint(0, 30)),
        "invasion": None,
        "manchas_sangre" : manchas_sangre
    }
    
    return player


def generate_deathtime():
    # horas , minutos, segundos, milisegundos
    return [0, random.randint(0,30), random.randint(0,59), random.randint(0,999)]

def add_time(last_time, add_time):
    # Sumar el tiempo de la muerte a la hora actual
    new_time = [0, 0, 0, 0]
    new_time[3] = last_time[3] + add_time[3]
    if new_time[3] >= 1000:
        new_time[2] += new_time[3] // 1000
        new_time[3] %= 1000
    new_time[2] += last_time[2] + add_time[2]
    if new_time[2] >= 60:
        new_time[1] += new_time[2] // 60
        new_time[2] %= 60
    new_time[1] += last_time[1] + add_time[1]
    if new_time[1] >= 60:
        new_time[0] += new_time[1] // 60
        new_time[1] %= 60
    new_time[0] += last_time[0] + add_time[0]
    return new_time

def format_time(time):
    rand_hour = "{0:0=2d}".format(time[0])
    rand_minute = "{0:0=2d}".format(time[1])
    rand_second = "{0:0=2d}".format(time[2])
    rand_millisecond = "{0:0=3d}".format(time[3])
    return rand_hour+":"+rand_minute+":"+rand_second+"."+rand_millisecond

tree = ET.parse("enemigos.xml")
root = tree.getroot()
list_of_enemies = root.findall(".//enemigo[es_jefe='0']")
list_of_bosses = root.findall(".//enemigo[es_jefe='1']")

def generate_death_reason():
    other_death_reasons = ["caída", "caída de altura", "trampa de flechas", "lanzas desde el suelo",
                           "lanzas desde el techo", "glamur", "trampilla o suelo falso", "NPC hostil",
                           "invasión", "fuego", "veneno", "sangrado", "magia", "maldición", "ahogamiento"]
    
    list_of_choices = ["boss", "enemy", "other"]
    choice = numpy.random.choice(list_of_choices, p=[0.6, 0.3, 0.1], size=1)[0]

    death_reason = "Muerte por "

    if choice == "boss":
        random_boss = random.choice(list_of_bosses)
        boss_name = random_boss.find("nombre").text
        death_reason += f"jefe: {boss_name}"
    elif choice == "enemy":
        random_enemy = random.choice(list_of_enemies)
        enemy_name = random_enemy.find("nombre").text
        death_reason += f"enemigo: {enemy_name}"
    else:
        death_reason += random.choice(other_death_reasons)

    return death_reason

tree = ET.parse("zonas.xml")
root = tree.getroot()
list_of_zones = root.findall(".//zona")
tree = ET.parse("objetos.xml")
root = tree.getroot()
list_of_weapons = root.findall(".//arma")
list_of_helmet = root.findall(".//pieza_armadura[slot_armadura='Cabeza']")
list_of_torso = root.findall(".//pieza_armadura[slot_armadura='Torso']")
list_of_legs = root.findall(".//pieza_armadura[slot_armadura='Piernas']")
list_of_hands = root.findall(".//pieza_armadura[slot_armadura='Manos']")

def generate_bloodstain(idx, last_time):
    random_weapon = random.choice(list_of_weapons)
    random_helmet = random.choice(list_of_helmet)
    random_torso = random.choice(list_of_torso)
    random_legs = random.choice(list_of_legs)
    random_hands = random.choice(list_of_hands)
    random_zone = random.choice(list_of_zones)
    
    arma_id = random_weapon.get("arma_id")
    casco_id = random_helmet.get("pieza_armadura_id")
    torso_id = random_torso.get("pieza_armadura_id")
    piernas_id = random_legs.get("pieza_armadura_id")
    guantes_id = random_hands.get("pieza_armadura_id")
    zona_id = random_zone.get("zona_id")

    death_reason = generate_death_reason()
    
    new_time = add_time(last_time, generate_deathtime())

    bloodstain = {
        "tiempo_muerte": format_time(new_time),
        "causa_muerte": death_reason,
        "zona_muerte": zona_id,
        "almas_al_morir": str(random.randint(0, 999999)),
        "piezas_armaduras_al_morir": {
            "casco_id": casco_id,
            "torso_id": torso_id,
            "piernas_id": piernas_id,
            "guantes_id": guantes_id
        },
        "arma_al_morir": arma_id
    }
    return bloodstain, new_time