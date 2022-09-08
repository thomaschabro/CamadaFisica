def createHeader(tipo, sizePayload, index, nPackages):
    header = bytearray()
    if tipo == "handshake":
        header += b'\x00'
    elif tipo == "handshake2":
        header += b'\x01'
    elif tipo == "info":
        header += b'\x02'
    elif tipo == "erro tamanho":
        header += b'\x03'
    elif tipo == "erro index":
        header += b'\x04'
    elif tipo == "resposta":
        header += b'\x05'

    header += index.to_bytes(3, byteorder='little')
    header += sizePayload.to_bytes(3, byteorder='little')
    header += nPackages.to_bytes(3, byteorder='little')

    return header

def createEOP():
    eop = bytearray()
    eop += b'\xff\xff\xff\xff'
    return eop

def createPackage(tipo, sizePayload, index, nPackage, payload):
    package = bytearray()
    package += createHeader(tipo, sizePayload, index, nPackage)
    package += payload
    package += createEOP()

    return package