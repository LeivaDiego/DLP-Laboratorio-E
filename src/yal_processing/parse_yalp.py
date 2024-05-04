def delete_comments(texto):
    while '/*' in texto and '*/' in texto:
        inicio_comentario = texto.find('/*')
        fin_comentario = texto.find('*/', inicio_comentario) + 2
        texto = texto[:inicio_comentario] + texto[fin_comentario:]
    return texto


def read_yapar(archivo):
    with open(archivo, 'r') as file:
        contenido = file.read()
    
    try:
        seccion_tokens, seccion_producciones = contenido.split('%%', 1)
    except ValueError:
        raise ValueError("El archivo no contiene el delimitador '%%' para separar las secciones de tokens y producciones.")

    return seccion_tokens, seccion_producciones


def verify_tokens(seccion_tokens):
    seccion_tokens = delete_comments(seccion_tokens)
    lineas = seccion_tokens.strip().split('\n')
    
    tokens_declarados = set()
    
    for linea in lineas:
        partes = linea.strip().split()
        if not partes:
            continue  # Ignorar líneas vacías

        if partes[0] == '%token':
            if len(partes) < 2:
                raise ValueError("Declaración de token inválida, no se especifican tokens.")
            # Convertir los tokens a mayúsculas para asegurar uniformidad
            tokens = [token.upper() for token in partes[1:]]
            tokens_declarados.update(tokens)  # Agregar todos los tokens declarados en esta línea
        elif partes[0] == 'IGNORE':
            if len(partes) != 2:
                raise ValueError("Uso incorrecto de IGNORE, debe seguirse exactamente por un nombre de token.")
            # Convertir el token de IGNORE a mayúscula para la comparación
            token_ignore = partes[1].upper()
            if token_ignore not in tokens_declarados:
                raise ValueError(f"Se intentó ignorar un token no declarado: {token_ignore}")
        else:
            raise ValueError(f"Declaración desconocida o no válida en la sección de tokens: {linea}")

    print("Análisis de tokens completado con éxito.")
    return tokens_declarados



def verify_productions(seccion_producciones, tokens_declarados):
    seccion_producciones = delete_comments(seccion_producciones)
    seccion_producciones = seccion_producciones.replace('\n', ' ')

    # Dividimos por punto y coma para obtener bloques que deberían representar producciones completas
    producciones = seccion_producciones.split(';')
    if producciones[-1].strip():
        raise ValueError("La última producción debe terminar con punto y coma.")
    producciones = producciones[:-1]  # Eliminar el último elemento vacío después del último punto y coma

    producciones_dict = {}

    # Primero, extraemos todos los nombres de las producciones
    for produccion in producciones:
        if ':' not in produccion:
            raise ValueError("Cada producción debe contener un nombre seguido de dos puntos.")
        if ':' in produccion.split(':', 1)[1]:
            raise ValueError("Cada producción debe contener solo un nombre seguido de dos puntos.")
        
        nombre, reglas = produccion.split(':', 1)
        nombre = nombre.strip().lower()  # Convertimos a minúsculas para mantener consistencia
        if not nombre:
            raise ValueError("Nombre de producción faltante.")
        producciones_dict[nombre] = reglas.strip()

    # Luego, verificamos cada producción contra los nombres y tokens declarados
    for nombre, reglas in producciones_dict.items():
        if not reglas:
            raise ValueError("Reglas de producción faltantes para " + nombre)

        opciones = reglas.split('|')
        for opcion in opciones:
            elementos = opcion.strip().split()
            for elemento in elementos:
                if elemento.isupper():  # Debe ser un token
                    if elemento not in tokens_declarados:
                        raise ValueError(f"Token '{elemento}' no declarado utilizado en la producción '{nombre}'.")
                elif elemento.islower():  # Debe ser el nombre de otra producción
                    if elemento not in producciones_dict:
                        raise ValueError(f"Nombre de producción '{elemento}' no declarado utilizado en la producción '{nombre}'.")

            if not opcion.strip():
                raise ValueError("Una opción en la producción '{nombre}' está vacía.")
            
    print("Análisis de producciones completado con éxito")
    return producciones_dict



def parse_yalp(archivo):
    seccion_tokens, seccion_producciones = read_yapar(archivo)
    tokens_declarados = verify_tokens(seccion_tokens)
    producciones_declaradas = verify_productions(seccion_producciones, tokens_declarados)
    return tokens_declarados, producciones_declaradas

def verify_yalex_tokens(yalex_parser_code, tokens_declarados):
    yalex_tokens = set()
    for tuple in yalex_parser_code:
        yalex_tokens.add(tuple[1])
    
    for token in tokens_declarados:
        if token not in yalex_tokens:
            raise ValueError(f"Token '{token}' no declarado en la configuración Yalex.")
    
    print("Análisis de tokens de Yalex completado con éxito.")