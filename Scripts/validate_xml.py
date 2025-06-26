from lxml import etree

def validar_xml_xsd(xml_file, xsd_file):
    """Valida un archivo XML con un esquema XSD."""
    try:
        with open(xsd_file, 'rb') as xsd_f:
            schema_doc = etree.XML(xsd_f.read())
            schema = etree.XMLSchema(schema_doc)

        with open(xml_file, 'rb') as xml_f:
            xml_doc = etree.parse(xml_f)

        schema.assertValid(xml_doc)
        print("El XML es válido según el XSD.")
    except etree.DocumentInvalid as e:
        print("El XML NO es válido según el XSD:")
        print(e)
    except Exception as e:
        print(f"Error al validar el XML con XSD: {e}")

def validar_xml_dtd(xml_file, dtd_file):
    """Valida un archivo XML con un esquema DTD."""
    try:
        with open(dtd_file, 'rb') as dtd_f:
            dtd = etree.DTD(dtd_f)
        
        with open(xml_file, 'rb') as xml_f:
            xml_doc = etree.parse(xml_f)
        
        if dtd.validate(xml_doc):
            print("El XML es válido según el DTD.")
        else:
            print("El XML NO es válido según el DTD:")
            print(dtd.error_log.filter_from_errors())
    except Exception as e:
        print(f"Error al validar el XML con DTD: {e}")

def main():
    print("Ingrese el nombre del archivo XML (sin extensión):")
    xml_file = input() + ".xml"
    
    print("Seleccione el tipo de validación:")
    print("1. XSD")
    print("2. DTD")
    opcion = input()
    
    if opcion == "1":
        print("Ingrese el nombre del archivo XSD (sin extensión):")
        xsd_file = input() + ".xsd"
        validar_xml_xsd(xml_file, xsd_file)
    elif opcion == "2":
        print("Ingrese el nombre del archivo DTD (sin extensión):")
        dtd_file = input() + ".dtd"
        validar_xml_dtd(xml_file, dtd_file)
    else:
        print("Opción no válida.")

if __name__ == "__main__":
    main()
