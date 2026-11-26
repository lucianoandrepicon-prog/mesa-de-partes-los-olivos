from datetime import datetime
import os

ARCHIVO_DATOS = "expedientes.txt"

ESTADOS_VALIDOS = ("INICIAL", "EN PREPARACIÓN", "ATENDIDO")

AREAS_MUNICIPALES = {
    "1": "Gerencia de Rentas y Administración Tributaria",
    "2": "Subgerencia de Licencias y Comercialización",
    "3": "Gerencia de Desarrollo Urbano",
    "4": "Secretaría General y Acceso a la Información Pública",
    "5": "Gerencia de Servicios a la Ciudad y Gestión Ambiental"
}

def validar_dni(dni):
    """Verifica que el DNI sea numérico y tenga 8 cifras."""
    return len(dni) == 8 and dni.isdigit()

def normalizar_texto(texto):
    """Limpia espacios sobrantes y estandariza en minúsculas para comparar."""
    return " ".join(texto.strip().lower().split())

def buscar_duplicado(lista, dni, asunto):
    """Busca si ya existe un trámite con el mismo DNI y asunto."""
    asunto_norm = normalizar_texto(asunto)
    dni_limpio = dni.strip()

    for item in lista:
        if item["dni"].strip() == dni_limpio and normalizar_texto(item["asunto"]) == asunto_norm:
            return item
    return None

def asignar_area_municipal(asunto):
    """Asigna el área municipal según palabras clave del asunto o permite elegirla."""
    asunto_norm = normalizar_texto(asunto)

    if any(palabra in asunto_norm for palabra in ["arbitrio", "predial", "impuesto", "tributo", "deuda", "franquicia"]):
        return "Gerencia de Rentas y Administración Tributaria"
    if any(palabra in asunto_norm for palabra in ["licencia", "funcionamiento", "comercio", "anuncio", "autorizacion", "autorización"]):
        return "Subgerencia de Licencias y Comercialización"
    if any(palabra in asunto_norm for palabra in ["obra", "construccion", "construcción", "edificacion", "edificación", "catastro", "habilitacion", "habilitación"]):
        return "Gerencia de Desarrollo Urbano"
    if any(palabra in asunto_norm for palabra in ["informacion", "información", "copia", "constancia", "certificado", "solicitud multiple", "solicitud múltiple"]):
        return "Secretaría General y Acceso a la Información Pública"
    if any(palabra in asunto_norm for palabra in ["limpieza", "basura", "parque", "jardin", "jardín", "poda", "residuo", "area verde", "área verde"]):
        return "Gerencia de Servicios a la Ciudad y Gestión Ambiental"

    print("\nNo se detectó un área automática para el asunto. Seleccione el área destino:")
    for clave, nombre_area in AREAS_MUNICIPALES.items():
        print(f"  {clave}. {nombre_area}")

    while True:
        opcion = input("Seleccione área (1-5): ").strip()
        if opcion in AREAS_MUNICIPALES:
            return AREAS_MUNICIPALES[opcion]
        print("Opción no válida. Elija un número del 1 al 5.")

def generar_numero_expediente(lista, anio=None):
    """Genera el número formal de expediente correlativo tipo EXP-2026-0001-MDLO."""
    if anio is None:
        anio = datetime.now().year

    max_correlativo = 0
    for item in lista:
        partes = item["codigo"].split("-")
        # Soporta tanto EXP-2026-0001 como EXP-2026-0001-MDLO
        if len(partes) >= 3 and partes[0] == "EXP" and partes[1] == str(anio) and partes[2].isdigit():
            correlativo = int(partes[2])
            if correlativo > max_correlativo:
                max_correlativo = correlativo

    siguiente = max_correlativo + 1
    return f"EXP-{anio}-{siguiente:04d}-MDLO"

def obtener_siguiente_estado(estado_actual):
    """Devuelve el siguiente estado secuencial o None si ya está ATENDIDO."""
    estado_limpio = estado_actual.strip().upper()
    if estado_limpio == "INICIAL":
        return "EN PREPARACIÓN"
    if estado_limpio == "EN PREPARACIÓN":
        return "ATENDIDO"
    return None

def avanzar_estado_expediente(expediente):
    """Avanza el expediente al siguiente estado del flujo si aún no está ATENDIDO."""
    siguiente = obtener_siguiente_estado(expediente["estado"])
    if siguiente is None:
        return False
    expediente["estado"] = siguiente
    return True

def establecer_estado_expediente(expediente, nuevo_estado):
    """Establece un estado válido ('INICIAL', 'EN PREPARACIÓN' o 'ATENDIDO')."""
    estado_limpio = nuevo_estado.strip().upper()
    if estado_limpio not in ESTADOS_VALIDOS:
        return False
    expediente["estado"] = estado_limpio
    return True

def actualizar_estado_expediente(lista):
    """Permite gestionar (avanzar o asignar) el estado de un expediente existente."""
    if not lista:
        print("\nNo existen expedientes registrados para actualizar.")
        return

    termino = input("\nIngrese Código de Expediente o DNI del expediente: ").strip().upper()
    coincidencias = [
        item for item in lista
        if item["codigo"].upper() == termino or item["dni"].strip() == termino
    ]

    if not coincidencias:
        print("No se encontró ningún expediente con ese código o DNI.")
        return

    if len(coincidencias) > 1:
        print("\nSe encontraron varios expedientes:")
        for idx, exp in enumerate(coincidencias, start=1):
            print(f"  {idx}. {exp['codigo']} | {exp['nombre']} | Asunto: {exp['asunto']} | Estado: {exp['estado']}")
        while True:
            sel = input("Seleccione el número del expediente a gestionar: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(coincidencias):
                expediente = coincidencias[int(sel) - 1]
                break
            print("Selección no válida.")
    else:
        expediente = coincidencias[0]

    print(f"\nExpediente seleccionado: {expediente['codigo']}")
    print(f"Solicitante          : {expediente['nombre']}")
    print(f"Asunto               : {expediente['asunto']}")
    print(f"Área destino         : {expediente['area_destino']}")
    print(f"Estado actual        : {expediente['estado']}")

    siguiente = obtener_siguiente_estado(expediente["estado"])
    print("\n¿Qué acción desea realizar con el estado?")
    if siguiente is not None:
        print(f"1. Avanzar al siguiente estado ({siguiente})")
    else:
        print("1. (Ya se encuentra en estado final: ATENDIDO)")
    print("2. Establecer un estado manualmente (INICIAL / EN PREPARACIÓN / ATENDIDO)")
    print("3. Cancelar")

    accion = input("Seleccione una opción: ").strip()
    if accion == "1":
        if avanzar_estado_expediente(expediente):
            print(f"Estado actualizado correctamente a: {expediente['estado']}")
        else:
            print("El expediente ya está ATENDIDO y no tiene un estado posterior.")
    elif accion == "2":
        print("Estados disponibles: 1) INICIAL  2) EN PREPARACIÓN  3) ATENDIDO")
        mapa_estados = {"1": "INICIAL", "2": "EN PREPARACIÓN", "3": "ATENDIDO"}
        op_estado = input("Elija estado (1-3): ").strip()
        if op_estado in mapa_estados and establecer_estado_expediente(expediente, mapa_estados[op_estado]):
            print(f"Estado actualizado correctamente a: {expediente['estado']}")
        else:
            print("Estado no válido. No se realizaron cambios.")
    else:
        print("Operación cancelada.")

def cargar_expedientes():
    """Lee el archivo de texto y devuelve los registros en una lista."""
    lista = []
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                partes = linea.strip().split("|")
                # Formato nuevo de 7 campos; mantiene compatibilidad con archivos antiguos de 4 campos
                if len(partes) == 7:
                    estado_cargado = partes[5].strip().upper()
                    if estado_cargado not in ESTADOS_VALIDOS:
                        estado_cargado = "INICIAL"
                    lista.append({
                        "codigo": partes[0],
                        "fecha": partes[1],
                        "dni": partes[2],
                        "nombre": partes[3],
                        "asunto": partes[4],
                        "estado": estado_cargado,
                        "area_destino": partes[6]
                    })
                elif len(partes) == 4:
                    lista.append({
                        "codigo": partes[0],
                        "fecha": "SIN REGISTRO",
                        "dni": partes[1],
                        "nombre": partes[2],
                        "asunto": partes[3],
                        "estado": "INICIAL",
                        "area_destino": "Por asignar"
                    })
    return lista

def guardar_expedientes(lista):
    """Guarda todos los trámites registrados en el archivo de texto."""
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
        for item in lista:
            archivo.write(
                f"{item['codigo']}|{item['fecha']}|{item['dni']}|{item['nombre']}|"
                f"{item['asunto']}|{item['estado']}|{item['area_destino']}\n"
            )

def registrar(lista):
    """Pide los datos, valida, detecta duplicados, asigna área, estado, fecha y número de expediente."""
    print("\n--- REGISTRO DE NUEVA SOLICITUD ---")
    while True:
        dni = input("Ingrese DNI (8 dígitos): ").strip()
        if validar_dni(dni):
            break
        print("DNI no válido. Debe contener exactamente 8 números.")

    while True:
        nombre = input("Apellidos y Nombres: ").strip()
        if len(nombre) > 0:
            break
        print("El nombre no puede estar vacío.")

    while True:
        asunto = input("Asunto o trámite a solicitar: ").strip()
        if len(asunto) > 0:
            break
        print("El asunto no puede estar vacío.")

    # Verificación de posible trámite duplicado (mismo DNI y mismo asunto)
    duplicado = buscar_duplicado(lista, dni, asunto)
    if duplicado is not None:
        print("\n[AVISO] Ya existe un expediente registrado con este mismo DNI y asunto:")
        print(f"  - N° de Expediente : {duplicado['codigo']}")
        print(f"  - Fecha registro   : {duplicado['fecha']}")
        print(f"  - Solicitante      : {duplicado['nombre']}")
        print(f"  - Asunto           : {duplicado['asunto']}")
        print(f"  - Área destino     : {duplicado['area_destino']}")
        print(f"  - Estado actual    : {duplicado['estado']}")

        confirmar = input("¿Desea registrar este trámite nuevamente de todas formas? (s/n): ").strip().lower()
        if confirmar != "s":
            print("Registro cancelado para evitar duplicidad.")
            return

    fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    area_destino = asignar_area_municipal(asunto)
    estado_inicial = "INICIAL"
    codigo = generar_numero_expediente(lista)

    nuevo_tramite = {
        "codigo": codigo,
        "fecha": fecha_registro,
        "dni": dni,
        "nombre": nombre,
        "asunto": asunto,
        "estado": estado_inicial,
        "area_destino": area_destino
    }
    lista.append(nuevo_tramite)

    print("\n" + "=" * 55)
    print("           CARGO DE RECEPCIÓN DIGITAL           ")
    print(f"N° DE EXPEDIENTE : {codigo}")
    print(f"FECHA / HORA     : {fecha_registro}")
    print(f"SOLICITANTE      : {nombre}")
    print(f"DNI              : {dni}")
    print(f"ASUNTO           : {asunto}")
    print(f"ÁREA DESTINO     : {area_destino}")
    print(f"ESTADO           : {estado_inicial}")
    print("=" * 55)

def buscar(lista):
    """Busca trámites por coincidencia de código o DNI."""
    termino = input("\nIngrese Número de Expediente o DNI a buscar: ").strip().upper()
    encontrado = False
    for item in lista:
        if item["codigo"].upper() == termino or item["dni"].strip() == termino:
            print("\n" + "-" * 50)
            print(f"N° Expediente: {item['codigo']}")
            print(f"Fecha        : {item['fecha']}")
            print(f"DNI          : {item['dni']}")
            print(f"Titular      : {item['nombre']}")
            print(f"Asunto       : {item['asunto']}")
            print(f"Área destino : {item['area_destino']}")
            print(f"Estado       : {item['estado']}")
            print("-" * 50)
            encontrado = True
    if not encontrado:
        print("No se encontró ningún expediente registrado con esos datos.")

# ---------- ordenamiento ----------
def ordenar_expedientes(lista, campo):
    """Ordena la lista por 'campo' con el método de burbuja (de menor a mayor)."""
    n = len(lista)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if lista[j][campo].upper() > lista[j + 1][campo].upper():
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
# -----------------------------------------

def listar(lista):
    """Muestra todos los trámites registrados, ordenados según el criterio elegido."""
    if not lista:
        print("\nNo existen trámites registrados en el sistema.")
        return

    print("\nOrdenar por: 1) N° Expediente  2) DNI  3) Solicitante  4) Fecha  5) Estado")
    campos = {
        "1": "codigo",
        "2": "dni",
        "3": "nombre",
        "4": "fecha",
        "5": "estado"
    }
    criterio = input("Opción: ").strip()
    if criterio in campos:
        ordenar_expedientes(lista, campos[criterio])

    print("\n" + "=" * 115)
    print(
        f"{'N° EXPEDIENTE':<20} | {'FECHA REGISTRO':<19} | {'DNI':<8} | "
        f"{'SOLICITANTE':<18} | {'ESTADO':<14} | {'ÁREA DESTINO':<28}"
    )
    print("=" * 115)
    for item in lista:
        print(
            f"{item['codigo']:<20} | {item['fecha']:<19} | {item['dni']:<8} | "
            f"{item['nombre'][:18]:<18} | {item['estado']:<14} | {item['area_destino'][:28]:<28}"
        )
    print("=" * 115)

def main():
    expedientes = cargar_expedientes()
    while True:
        print("\n=== MESA DE PARTES DIGITAL - MUNI LOS OLIVOS ===")
        print("1. Registrar nueva solicitud")
        print("2. Buscar expediente por número o DNI")
        print("3. Listar expedientes registrados")
        print("4. Actualizar estado de expediente")
        print("5. Guardar y salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar(expedientes)
        elif opcion == "2":
            buscar(expedientes)
        elif opcion == "3":
            listar(expedientes)
        elif opcion == "4":
            actualizar_estado_expediente(expedientes)
        elif opcion == "5":
            guardar_expedientes(expedientes)
            print("Datos guardados en 'expedientes.txt'. Fin del programa.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()