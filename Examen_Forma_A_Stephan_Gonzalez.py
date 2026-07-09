def buscar_codigo(juegos, codigo):

    codigo_norm = codigo.strip().upper()
    for clave in juegos:
        if clave.upper() == codigo_norm:
            return True
    return False

def obtener_clave_real(juegos, codigo):

    codigo_norm = codigo.strip().upper()
    for clave in juegos:
        if clave.upper() == codigo_norm:
            return clave
    return None

def validar_codigo(codigo):
    return isinstance(codigo, str) and len(codigo.strip()) > 0

def validar_titulo(titulo):
    return isinstance(titulo, str) and len(titulo.strip()) > 0

def validar_plataforma(plataforma):
    return isinstance(plataforma, str) and len(plataforma.strip()) > 0

def validar_genero(genero):
    return isinstance(genero, str) and len(genero.strip()) > 0

def validar_clasificacion(clasificacion):
    return isinstance(clasificacion, str) and clasificacion.strip().upper() in ['E', 'T', 'M']

def validar_multiplayer(multiplayer):
    return isinstance(multiplayer, str) and multiplayer.strip().lower() in ['s', 'n']

def validar_editor(editor):
    return isinstance(editor, str) and len(editor.strip()) > 0

def validar_precio(precio_str):

    try:
        val = int(precio_str)
        return val > 0
    except ValueError:
        return False

def validar_stock(stock_str):

    try:
        val = int(stock_str)
        return val >= 0
    except ValueError:
        return False


def leer_opcion():
     
     try:
         opcion = int(input("Ingrese opción: "))
         if 1 <= opcion <=6:
             return opcion
         return None
     except ValueError:
         return None

def stock_plataforma(juegos, inventario, plataforma):

    plataforma_buscada = plataforma.strip().lower()
    total_stock = 0

    for codigo, datos in juegos.items():
        plat_juego = datos[1].strip().lower()
        if plat_juego == plataforma_buscada:
            if codigo in inventario:
                total_stock += inventario[codigo][1]

    print(f"El total de stock disponibles es: {total_stock}")

def busqueda_precio(juegos, inventario, p_min, p_max):

    resultados = []

    for codigo, datos_inv in inventario.items():
        precio = datos_inv[0]
        stock = datos_inv[1]

        if p_min <= precio <= p_max and stock > 0:
            if codigo in juegos:
                titulo = juegos[codigo][0]
                resultados.append(f"{titulo}--{codigo}")

    if len(resultados) == 0:
        print("No hay juegos en ese rango de precios.")
    else:
        resultados.sort()
        print(f"Los juegos encontrados son: {resultados}")

def actualizar_precio(juegos, inventario, codigo, nuevo_precio):

    clave_real = obtener_clave_real(juegos, codigo)
    if clave_real is not None and clave_real in inventario:
        inventario[clave_real][0] = nuevo_precio
        return True
    return False

def agregar_juego(juegos, inventario, codigo, titulo, plataforma, genero, clasificacion, multiplayer, editor, precio, stock):

    if buscar_codigo(juegos, codigo):
        return False

    clave_codigo = codigo.strip().upper()
    es_multiplayer = (multiplayer.strip().lower() == 's')
    clasificacion_formateada = clasificacion.strip().upper()

    juegos[clave_codigo] = [
        titulo.strip(),
        plataforma.strip(),
        genero.strip(),
        clasificacion_formateada,
        es_multiplayer,
        editor.strip()
    ]
    inventario[clave_codigo] = [precio, stock]
    return True

def eliminar_juego(juegos, inventario, codigo):

    clave_real = obtener_clave_real(juegos, codigo)
    if clave_real is not None:
        if clave_real in juegos:
            del juegos[clave_real]
        if clave_real in inventario:
            del inventario[clave_real]
        return True
    return False

def main():

    juegos = {
        'G001': ['Eclipse Runner', 'PC', 'accion', 'T', True, 'NovaStudio'],
        'G002': ['Puzzle Atlas', 'Switch', 'puzzle', 'E', False, 'Bright Works'],
        'G003': ['Sky Legends', 'PS5', 'aventura', 'T', True, 'OrionGames'],
        'G004': ['Racing Pulse', 'PC', 'carreras', 'E', True, 'VelocityLab'],
        'G005': ['Mystic Farm', 'Switch', 'simulacion', 'E', False, 'GreenSeed'],
        'G006': ['Shadow Tactics', 'Xbox', 'estrategia', 'M', False, 'IronGate']
    }

    inventario = {
        'G001': [9990, 7],
        'G002': [19990, 0],
        'G003': [42990, 3],
        'G004': [14990, 5],
        'G005': [17990, 9],
        'G006': [39990, 2]
    }

    ejecutando = True

    while ejecutando:
        print("\n========== MENÚ PRINCIPAL ==========")
        print("1. Stock por plataforma")
        print("2. Búsqueda de juegos por rango de precio")
        print("3. Actualizar precio de juego")
        print("4. Agregar juego")
        print("5. Eliminar juego")
        print("6. Salir")
        print("=====================================")

        opcion = leer_opcion()

        if opcion is None:
            print("Debe seleccionar una opción válida")
            continue

        if opcion == 1:
            plat = input("Ingrese plataforma a consultar: ")
            stock_plataforma(juegos, inventario, plat)

        elif opcion == 2:
            p_min = None
            p_max = None

            while p_min is None or p_max is None:
                try:
                    p_min_input = input("Ingrese precio mínimo: ")
                    p_min_val = int(p_min_input)
                    p_max_input = input("Ingrese precio máximo: ")
                    p_max_val = int(p_max_input)

                    if p_min_val >= 0 and p_max_val >= 0 and p_min_val <= p_max_val:
                        p_min = p_min_val
                        p_max = p_max_val
                    else:
                        print("Debe ingresar valores enteros")
                except ValueError:
                    print("Debe ingresar valores enteros")

            busqueda_precio(juegos, inventario, p_min, p_max)

        elif opcion == 3:
            repetir = 's'
            while repetir == 's':
                cod = input("Ingrese código del juego: ")
                precio_str = input("Ingrese nuevo precio: ")

                if validar_precio(precio_str):
                    nuevo_precio = int(precio_str)

                    if actualizar_precio(juegos, inventario, cod, nuevo_precio):
                        print("Precio actualizado")
                    else:
                        print("El código no existe")

                else:
                    print("El nuevo precio debe ser un número entero mayor a cero")

                repetir = input("¿Desea actualizar otro precio (s/n)?: ").strip().lower()

        elif opcion == 4:
            cod = input("Ingrese código del juego: ")
            if not validar_codigo(cod):
                print("El código no debe estar vacío ni contener solo espacios.")
                continue
            if buscar_codigo(juegos, cod):
                print("El código ya existe")
                continue

            titulo = input("Ingrese titulo: ")
            if not validar_titulo(titulo):
                print("El título no debe estar vacío.")
                continue

            plat = input("Ingrese plataforma: ")
            if not validar_plataforma(plat):
                print("La plataforma no debe estar vacía.")
                continue

            genero = input("Ingrese género: ")
            if not validar_genero(genero):
                print("El género no debe estar vacío.")
                continue

            clasificacion = input("Ingrese clasificación (E/T/M): ")
            if not validar_clasificacion(clasificacion):
                print("La clasificación debe ser E, T o M.")
                continue

            multiplayer = input("¿Es multiplayer? (s/n): ")
            if not validar_multiplayer(multiplayer):
                print("Respuesta no válida para multiplayer.")
                continue

            editor = input("Ingrese editor: ")
            if not validar_editor(editor):
                print("El editor no debe estar vacío.")
                continue

            precio_str = input("Ingrese precio: ")
            if not validar_precio(precio_str):
                print("El precio debe ser un entero mayor que cero.")
                continue

            stock_str = input("Ingrese stock: ")
            if not validar_stock(stock_str):
                print("El stock debe ser un entero mayor o igual a cero.")
                continue

            exito = agregar_juego(
                juegos, inventario, cod, titulo, plat, genero, clasificacion, multiplayer,
                editor, int(precio_str), int(stock_str)
            )

            if exito:
                print("Juego agregado")
            else:
                print("El código ya existe")

        elif opcion == 5:
            cod = input("Ingrese código a eliminar: ")
            if eliminar_juego(juegos, inventario, cod):
                print("Juego eliminado")
            else:
                print("El código no existe")

        elif opcion == 6:
            print("Programa finalizado.")
            ejecutando = False
    

if __name__ == "__main__":
    main()