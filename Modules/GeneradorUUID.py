import uuid
def getUUID():
    # Genera un UUID
    uuid_value = uuid.uuid4()
    
    # Convierte el UUID en una cadena hexadecimal
    uuid_hex = uuid_value.hex
    
    # Trunca a 16 dígitos (64 bits)
    uuid_short = uuid_hex[:16]
    
    # Inserta guiones cada cuatro caracteres
    formatted_uuid = '-'.join([uuid_short[i:i+4] for i in range(0, len(uuid_short), 4)])
    
    return formatted_uuid