from difflib import SequenceMatcher
import re

from django.utils import timezone

from core.mutils import Chord


LINHA_CIFRA_PATTERN = re.compile(
    "^[^cefhklnpqrtvwyzHKLNOPQRTVWXYZ.,!?ãâáàäẽêéèëĩîíìïõôóòöũûúùüç_]+$")

CIFRA_PATTERN_OLD = re.compile(
    r"(?P<name>[A-G])(?P<accidental>x|#|##|b|bb)?(?P<sufixo>[^A-G/\s]*)/?(?P<baixo>[A-G])?(?P<baixo_accidental>x|#|##|b|bb)?(?P<baixo_sufixo>[^A-G\s]*)")
CIFRA_PATTERN = re.compile(
    r"(?P<name>[A-G])(?P<accidental>#|b)?(?P<sufixo>[^A-G/\s]*)/?(?P<baixo>[A-G])?(?P<baixo_accidental>x|#|##|b|bb)?(?P<baixo_sufixo>[^A-G\s]*)")


LINHA_CIFRA = 'lc'
LINHA_TEXTO = 'lt'

base_sus = ["C", "C#",  "D",  "D#",  "E",
            "F", "F#",  "G",  "G#",  "A",  "A#",  "B"]
base_bemol = ["C", "Db",  "D",  "Eb",  "E",
              "F", "Gb",  "G",  "Ab",  "A",  "Bb",  "B"]

NOTAS = [
    ('C', 'C', 0),
    ('C#', 'Db', 0),
    ('D', 'D', 0),
    ('D#', 'Eb', 1),
    ('E', 'E', 0),
    ('F', 'F', 1),
    ('F#', 'Gb', 0),
    ('G', 'G', 0),
    ('G#', 'Ab', 1),
    ('A', 'A', 0),
    ('A#', 'Bb', 1),
    ('B', 'B', 0),
]


ESCALA_MAIOR = [
    (0, ('',), 1.2),
    (2, ('m',), 1),
    (4, ('m',), 1),
    (5, ('',), 1.1),
    (7, ('',), 1.3),
    (9, ('m',), 1),
    (11, ('m5°', 'dim', 'º', '°', 'm5-', 'm5º',), 1),
]

ESCALA_MENOR = [
    (0, ('m',), 1.07),
    (2, ('m',), 1),
    (3, ('',), 1),
    (5, ('m',), 1),
    (7, ('',), 1.05),
    (8, ('',), 1),
    (10, ('',), 1.03),
]


def _list_rotate(list, n):
    return list[n:] + list[:n]


def nota_to_index(nota):
    try:
        nota_id = base_sus.index(nota)
    except:
        nota_id = base_bemol.index(nota)
    return nota_id


class Tom:

    def __init__(self, tonica_id=0, tonica='',  ESCALA=ESCALA_MAIOR):

        if tonica:
            self.tonica = tonica
            self.tonica_id = nota_to_index(tonica)
        else:
            self.tonica_id = tonica_id

        notas = _list_rotate(NOTAS, self.tonica_id)
        tipo_sus_bemol = NOTAS[self.tonica_id][2]
        self.tonica = notas[0][tipo_sus_bemol] + ESCALA[0][1][0]

        self.ch = []
        for i in ESCALA:
            self.ch.append(
                [('%s%s' % (notas[i[0]][tipo_sus_bemol], j), i[2]) for j in i[1]])

        self.estatistica = [0 for i in range(len(self.ch))]

    def __str__(self):
        return self.tonica


class AnaliseTonal:

    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def __init__(self, linhas):

        self.tons = {}

        for i in range(12):
            tom = Tom(tonica_id=i)
            self.tons[tom.tonica] = tom
            tom = Tom(tonica_id=i, ESCALA=ESCALA_MENOR)
            self.tons[tom.tonica] = tom

        for key, tom in self.tons.items():
            for l in linhas:
                if l[0] == LINHA_CIFRA:
                    cifras = l[2].split()
                    for cifra in cifras:
                        if '/' in cifra:
                            cifra = cifra.split('/')[0]
                        cifra_encontrada = False
                        for i in range(len(tom.ch)):
                            aux_similar = 0
                            similar = -9999
                            for acorde in tom.ch[i]:  # variacao de acorde
                                if acorde[0] == cifra:
                                    similar = 1 * acorde[1]
                                    cifra_encontrada = True
                                    break
                                elif acorde[0] in cifra:
                                    aux_similar = self.similar(
                                        acorde[0], cifra) * acorde[1]
                                    cifra_encontrada = True
                                # elif cifra in acorde[0]:
                                #    aux_similar = - self.similar(
                                #        acorde[0], cifra) * acorde[1]
                                #    cifra_encontrada = True

                                if aux_similar > similar:
                                    similar = aux_similar

                            if similar:
                                tom.estatistica[i] += similar

                            if cifra_encontrada:
                                break

        self.tom = ''
        m = 0
        for key, tom in self.tons.items():
            s = sum(tom.estatistica)
            print(tom.tonica, s, tom.estatistica)
            if s > m:
                m = s
                self.tom = tom.tonica

        print(self.tom)

    def mudarTom(self, linhas, direcao):

        tonica_id_novo_tom = (
            self.tons[self.tom].tonica_id + direcao) % len(NOTAS)
        tipo_sus_bemol = NOTAS[tonica_id_novo_tom][2]

        for l in linhas:
            if l[0] == LINHA_CIFRA:
                partes = l[2].split(' ')
                partes = [[p, len(p), len(p)] for p in partes]

                for p in partes:
                    if not p[1]:
                        continue

                    rl = CIFRA_PATTERN.findall(p[0])  # regex da linha

                    if not rl:
                        continue

                    if len(rl[0]) != 6:
                        continue
                    subpts = rl[0]  # subpartes

                    base = subpts[0] + subpts[1]
                    baixo = subpts[3] + subpts[4]

                    base_id = nota_to_index(base)
                    if baixo:
                        baixo_id = nota_to_index(baixo)

                    base = NOTAS[(base_id + direcao) %
                                 len(NOTAS)][tipo_sus_bemol]
                    if baixo:
                        baixo = NOTAS[(baixo_id + direcao) %
                                      len(NOTAS)][tipo_sus_bemol]

                    if baixo or subpts[5]:
                        nova_nota = '%s%s/%s%s' % (
                            base,
                            subpts[2],
                            baixo,
                            subpts[5])
                    else:
                        nova_nota = '%s%s' % (
                            base,
                            subpts[2])

                    p[0] = nova_nota
                    p[2] = len(nova_nota)

                divida = 0
                for i in range(len(partes)):

                    p = partes[i]
                    if p[1] == p[2]:
                        if divida:
                            if not p[0] and i + 1 < len(partes):
                                if divida > 0:
                                    p[2] = -1
                                    divida -= 1
                                else:
                                    p[2] = 1
                                    divida += 1

                        continue

                    divida += (p[2] - p[1])

                result = ''
                flag_espaco = ''
                for p in partes:
                    if p[0]:
                        result += p[0] + ' '
                    else:
                        if p[2] == 0:
                            result += ' '
                            flag_espaco = ''
                        elif p[2] > 0:
                            result += ' ' * (1 + p[2])
                            flag_espaco = ''
                l[2] = result.rstrip()


class Cifrador:

    def __init__(self, texto):
        self.texto = texto

    def run(self, direcao=0):
        linhas = self.compileText()

        at = AnaliseTonal(linhas)
        self.tom = at.tom

        if not direcao:
            return linhas

        at.mudarTom(linhas, direcao)
        self.tom = at.tom

        return linhas

    def compileText(self):
        linhas = self.texto.splitlines()
        linhas = list(self.linhasDeCifra(linhas))

        for l in linhas:
            if l[0] == 'lc':
                l[2] = re.sub('[oº]', '°', l[2])
                l[2] = re.sub('[-]', 'm', l[2])
                l[2] = re.sub('[\t]', '      ', l[2])

        return linhas

    def linhasDeCifra(self, linhas):

        for l in linhas:
            if LINHA_CIFRA_PATTERN.match(l):
                yield [LINHA_CIFRA, '', l]
            elif l.startswith(' '):
                yield [LINHA_TEXTO, 'refrao', l]
            else:
                yield [LINHA_TEXTO, '', l]
