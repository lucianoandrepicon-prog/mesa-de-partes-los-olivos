# main.py
import os

ARCHIVO_DATOS = "expedientes.txt"


def validar_dni(dni):
    """Verifica que el DNI sea numérico y tenga 8 cifras."""
    return len(dni) == 8 and dni.isdigit()


def cargar_expedientes():
    """Lee el archivo de texto y devuelve los registros en una lista."""
    lista = []
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                partes = linea.strip().split("|")
                if len(partes) == 4:
                    lista.append({
                        "codigo": partes[0],
                        "dni": partes[1],
                        "nombre": partes[2],
                        "asunto": partes[3]
                    })
    return lista


def guardar_expedientes(lista):
    """Guarda todos los trámites registrados en el archivo de texto."""
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
        for item in lista:
            archivo.write(f"{item['codigo']}|{item['dni']}|{item['nombre']}|{item['asunto']}\n")


def registrar(lista):
    """Pide los datos, valida y asigna un nuevo código correlativo."""
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

    # Generación de código correlativo tipo EXP-2026-0001
    codigo = f"EXP-2026-{(len(lista) + 1):04d}"

    nuevo_tramite = {
        "codigo": codigo,
        "dni": dni,
        "nombre": nombre,
        "asunto": asunto
    }
    lista.append(nuevo_tramite)

    print("\n" + "=" * 45)
    print("      CARGO DE RECEPCIÓN DIGITAL      ")
    print(f"CÓDIGO DE EXPEDIENTE : {codigo}")
    print(f"SOLICITANTE          : {nombre}")
    print(f"DNI                  : {dni}")
    print("ESTADO               : REGISTRADO CON ÉXITO")
    print("=" * 45)


def buscar(lista):
    """Busca trámites por coincidencia de código o DNI."""
    termino = input("\nIngrese Código de Expediente o DNI a buscar: ").strip().upper()
    encontrado = False
    for item in lista:
        if item["codigo"] == termino or item["dni"] == termino:
            print("\n" + "-" * 40)
            print(f"Código : {item['codigo']}")
            print(f"DNI    : {item['dni']}")
            print(f"Titular: {item['nombre']}")
            print(f"Asunto : {item['asunto']}")
            print("-" * 40)
            encontrado = True
    if not encontrado:
        print("No se encontró ningún expediente registrado con esos datos.")


# ---------- NUEVO: ordenamiento ----------
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

    # NUEVO: pedir el criterio de orden antes de mostrar
    print("\nOrdenar por: 1) Código  2) DNI  3) Solicitante")
    campos = {"1": "codigo", "2": "dni", "3": "nombre"}
    criterio = input("Opción: ").strip()
    if criterio in campos:
        ordenar_expedientes(lista, campos[criterio])

    print("\n" + "=" * 65)
    print(f"{'CÓDIGO':<15} | {'DNI':<10} | {'SOLICITANTE':<20} | {'ASUNTO'}")
    print("=" * 65)
    for item in lista:
        print(f"{item['codigo']:<15} | {item['dni']:<10} | {item['nombre'][:18]:<20} | {item['asunto']}")
    print("=" * 65)


def main():
    expedientes = cargar_expedientes()
    while True:
        print("\n=== MESA DE PARTES DIGITAL - MUNI LOS OLIVOS ===")
        print("1. Registrar nueva solicitud")
        print("2. Buscar expediente por código o DNI")
        print("3. Listar expedientes registrados")
        print("4. Guardar y salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar(expedientes)
        elif opcion == "2":
            buscar(expedientes)
        elif opcion == "3":
            listar(expedientes)
        elif opcion == "4":
            guardar_expedientes(expedientes)
            print("Datos guardados en 'expedientes.txt'. Fin del programa.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()