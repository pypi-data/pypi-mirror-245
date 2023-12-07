import florestlibrarypythonpremium
import base64

def decode_text(text: str):
    message_bytes = text.encode('utf-8')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('utf-8')
    return base64_message
def decode_base64(code: str):
    base64_bytes = code.encode('utf-8')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('utf-8')
    return message
while True:
    vvod = input(f'Введите текст, или base64 код:')
    vopros = input(f'Это base64, или текст?')
    if vopros == 'a':
        a = decode_text(text=vvod)
        print(a)
    if vopros == 'b':
        b = decode_base64(code=vvod)
        print(b)


