import re

REGEX_CIFRA = re.compile(
    "^[^cefhklnpqrtvwyzHKLNOPQRTVWXYZ.,!?ãâáàäẽêéèëĩîíìïõôóòöũûúùüç_]+$")


class Cifrador:

    lNotasSus = ["C", "C#",  "D",  "D#",  "E",
                 "F", "F#",  "G",  "G#",  "A",  "A#",  "B"]
    lNotasBemol = ["C", "Db",  "D",  "Eb",  "E",
                   "F", "Gb",  "G",  "Ab",  "A",  "Bb",  "B"]
    usarSus = [True, True, True, False, True,
               False, True, True, False, True, False, True]

    def __init__(self, texto):
        self.texto = texto

    def run(self):
        return self.compileText()

    def compileText(self):
        linhas = self.texto.splitlines()

        return self.linhasDeCifra(linhas)

    def linhasDeCifra(self, linhas):

        for l in linhas:
            if REGEX_CIFRA.match(l):
                yield 'lc', '', l
            elif l.startswith(' '):
                yield 'lt', 'refrao', l
            else:
                yield 'lt', '', l
