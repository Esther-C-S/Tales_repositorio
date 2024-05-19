import random
from .models import Frase

def frase_aleatoria_login(request):
    frases = Frase.objects.select_related('id_autor').all()
    if frases:
        frase = random.choice(frases)
    else:
        frase = "oh oh, aqui deberia haber una frase"

    return {'frase' : frase }