from graphviz import Digraph
from models.grammar import Grammar


def first_follow(G):
    def union(set_1, set_2):
        set_1_len = len(set_1)
        set_1 |= set_2

        return set_1_len != len(set_1)

    first = {symbol: set() for symbol in G.symbols}
    first.update((terminal, {terminal}) for terminal in G.terminals)
    follow = {symbol: set() for symbol in G.nonterminals}
    follow[G.start].add('$')

    while True:
        updated = False

        for head, bodies in G.grammar.items():
            for body in bodies:
                for symbol in body:
                    if symbol != 'ε':
                        updated |= union(first[head], first[symbol] - set('ε'))

                        if 'ε' not in first[symbol]:
                            break
                    else:
                        updated |= union(first[head], set('ε'))
                else:
                    updated |= union(first[head], set('ε'))

                aux = follow[head]
                for symbol in reversed(body):
                    if symbol == 'ε':
                        continue
                    if symbol in follow:
                        updated |= union(follow[symbol], aux - set('ε'))
                    if 'ε' in first[symbol]:
                        aux = aux | first[symbol]
                    else:
                        aux = first[symbol]

        if not updated:
            return first, follow


class SLRParser:
    def __init__(self, G):
        self.G_prime = Grammar(f"{G.start}' -> {G.start}\n{G.grammar_str}")
        self.max_G_prime_len = len(max(self.G_prime.grammar, key=len))
        self.G_indexed = []

        for head, bodies in self.G_prime.grammar.items():
            for body in bodies:
                self.G_indexed.append([head, body])

        self.first, self.follow = first_follow(self.G_prime)
        self.C = self.items(self.G_prime)
        self.action = list(self.G_prime.terminals) + ['$']
        self.goto = list(self.G_prime.nonterminals - {self.G_prime.start})
        self.parse_table_symbols = self.action + self.goto
        self.parse_table = self.construct_table()

    def CLOSURE(self, I):
        J = I

        while True:
            item_len = len(J)

            for head, bodies in J.copy().items():
                for body in bodies.copy():
                    if '.' in body[:-1]:
                        symbol_after_dot = body[body.index('.') + 1]

                        if symbol_after_dot in self.G_prime.nonterminals:
                            for G_body in self.G_prime.grammar[symbol_after_dot]:
                                J.setdefault(symbol_after_dot, set()).add(
                                    ('.',) if G_body == ('ε',) else ('.',) + G_body)

            if item_len == len(J):
                return J

    def GOTO(self, I, X):
        goto = {}

        for head, bodies in I.items():
            for body in bodies:
                if '.' in body[:-1]:
                    dot_pos = body.index('.')

                    if body[dot_pos + 1] == X:
                        replaced_dot_body = body[:dot_pos] + (X, '.') + body[dot_pos + 2:]

                        for C_head, C_bodies in self.CLOSURE({head: {replaced_dot_body}}).items():
                            goto.setdefault(C_head, set()).update(C_bodies)

        return goto

    def items(self, G_prime):
        C = [self.CLOSURE({G_prime.start: {('.', G_prime.start[:-1])}})]

        while True:
            item_len = len(C)

            for I in C.copy():
                for X in G_prime.symbols:
                    goto = self.GOTO(I, X)

                    if goto and goto not in C:
                        C.append(goto)

            if item_len == len(C):
                return C


    def construct_table(self):
        parse_table = {r: {c: '' for c in self.parse_table_symbols} for r in range(len(self.C))}

        for i, I in enumerate(self.C):
            for head, bodies in I.items():
                for body in bodies:
                    if '.' in body[:-1]:  # CASE 2 a
                        symbol_after_dot = body[body.index('.') + 1]

                        if symbol_after_dot in self.G_prime.terminals:
                            s = f's{self.C.index(self.GOTO(I, symbol_after_dot))}'

                            if s not in parse_table[i][symbol_after_dot]:
                                if 'r' in parse_table[i][symbol_after_dot]:
                                    parse_table[i][symbol_after_dot] += '/'

                                parse_table[i][symbol_after_dot] += s

                    elif body[-1] == '.' and head != self.G_prime.start:  # CASE 2 b
                        for j, (G_head, G_body) in enumerate(self.G_indexed):
                            if G_head == head and (G_body == body[:-1] or G_body == ('ε',) and body == ('.',)):
                                for f in self.follow[head]:
                                    if parse_table[i][f]:
                                        parse_table[i][f] += '/'

                                    parse_table[i][f] += f'r{j}'

                                break

                    else:  # CASE 2 c
                        parse_table[i]['$'] = 'acc'

            for A in self.G_prime.nonterminals:  # CASE 3
                j = self.GOTO(I, A)

                if j in self.C:
                    parse_table[i][A] = self.C.index(j)

        return parse_table


    def generate_automaton(self, name=''):
        # Crear el objeto Digraph con el formato de salida especificado
        automaton = Digraph('automaton', node_attr={'shape': 'record'}, format='png')

        # Construcción del contenido del autómata, similar a lo anterior
        for i, I in enumerate(self.C):
            I_html = f'<<I>I</I><SUB> {i} </SUB><BR/>'
            for head, bodies in I.items():
                for body in bodies:
                    I_html += f'<I> {head} </I> &#8594; '
                    for symbol in body:
                        if symbol in self.G_prime.nonterminals:
                            I_html += f'<I> {symbol} </I>'
                        elif symbol in self.G_prime.terminals:
                            I_html += f'<B> {symbol} </B>'
                        else:
                            I_html += f' {symbol} '
                    I_html += '<BR ALIGN="LEFT"/>'
            automaton.node(f'I{i}', f'{I_html}>')

        for r in range(len(self.C)):
            for c in self.parse_table_symbols:
                if isinstance(self.parse_table[r][c], int):
                    automaton.edge(f'I{r}', f'I{self.parse_table[r][c]}', label=f'<<I>{c}</I>>')
                elif 's' in self.parse_table[r][c]:
                    i = self.parse_table[r][c][self.parse_table[r][c].index('s') + 1:]
                    if '/' in i:
                        i = i[:i.index('/')]
                    automaton.edge(f'I{r}', f'I{i}', label=f'<<B>{c}</B>>' if c in self.G_prime.terminals else c)
                elif self.parse_table[r][c] == 'acc':
                    automaton.node('acc', '<<B>ACCEPT</B>>', shape='none')
                    automaton.edge(f'I{r}', 'acc', label='$')

        # Renderizar y guardar el autómata en un directorio específico
        automaton.render(filename=f'LR0_{name}', directory="./src/lr0_out/",cleanup=True, format='png', view=True)
        print('Automata LR(0) generado exitosamente, guardado en /lr0_out')