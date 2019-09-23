# Importa o pacote do graphviz
from graphviz import Digraph

# Classe para representar um autômato
class Automata:
    """Classe para representar um autômato"""

    def __init__(self):
        self.states = dict()
        self.initial_state = None
        self.transitions = set()
        self.node_count = 0
        self.dot = Digraph(comment='e-NFA')

    # Adiciona um novo estado ao autômato
    def add_state(self, state):
        self.states[state.label] = state
        self.node_count = self.node_count + 1

    # Adiciona um novo estado ao autômato e marca-o como estado inicial
    def set_initial_state(self, state):
        self.initial_state = state
        self.states[state.label] = state
        self.node_count = self.node_count + 1

    # Retorna o estado inicial
    def get_initial_state(self):
        return self.initial_state


    # Adiciona uma nova transição entre `from_state` e `to_state` com `label` como descrição
    def add_transition(self, from_state, to_state, label):
        transition = Transition(from_state, to_state, label)
        self.transitions.add(transition)

    # Deleta uma transição de estados
    def delete_transition(self, transition):
        self.transitions.remove(transition)

    # Monta o grafo em dot referente ao autômato
    def build_graph(self):
        self.dot = Digraph(format='png')
        for state  in self.states:
            if self.states[state].final:
                self.dot.attr('node', shape='doublecircle')
                self.dot.node(state, state)
                self.dot.attr('node', shape='circle')
            else:
                self.dot.node(state, state)
        for transition in self.transitions:
            self.dot.edge(transition.from_state.label, transition.to_state.label, transition.label)

    # Salva a imagem referente ao grafo
    def print_graph(self, filename, view=True):
        self.build_graph()
        self.dot.render(filename, view=view)  

    # Imprime o código do grafo em .dot
    def print_source(self):
        self.build_graph()
        print(self.dot.source)

    # Retorna o número de nós do autômato
    def get_node_count(self):
        return self.node_count

    # Retorna o label da transição a -> b
    def label_of_transition(self, a, b):
        label = ''
        for transition in self.transitions:
            if transition.from_state == a and transition.to_state == b:
                label = transition.label
        return label

    # Verifica se uma string é aceita pelo autômato
    def accept_string(self, text):
        for transition in self.transitions:
            transition.from_state.out_transitions.add(transition)

        text = list(text)
        index = 0
        start_state = self.get_initial_state()
        return self.recursive_parser(text, index, start_state)

        
    def recursive_parser(self, text, index, state):
        for transition in state.out_transitions:
            actual_state = state
            if transition.label == '&':
                if transition.to_state.final and index == len(text):
                    return True
                else:
                    if not self.recursive_parser(text, index, transition.to_state):
                        state = actual_state
                    else:
                        return True

            if index < len(text) and transition.label == text[index]:
                index = index + 1
                if transition.to_state.final and index == len(text):
                    return True
                if index > len(text):
                    return False
                else: 
                    if self.recursive_parser(text, index, transition.to_state):
                        return True
                    else:
                        state = actual_state
                        index = index - 1
        

    # Verifica uma string é união de linguagens (Retorna as sublinguagens que foram unidas)
    def union_parser(self, text):
        new_text = list(text)
        num_parenthesis = 0
        for i in range(len(new_text)):
            if new_text[i] == '(':
                num_parenthesis = num_parenthesis + 1
            elif new_text[i] == '+' and num_parenthesis == 0:
                new_text[i] = ','
            elif new_text[i] == ')':
                num_parenthesis = num_parenthesis - 1
        new_text = ''.join(new_text)
        new_text = str.split(new_text, ',')
        return new_text

    # Verifica uma string é concatenação de linguagens (Retorna as sublinguagens que foram concatenadas)
    def concatenation_parser(self, text):
        new_text = []
        num_parenthesis = 0
        substr = ''
        for c in (text):
            if c == '(':
                if substr != '' and num_parenthesis == 0:
                    new_text.append(substr)
                num_parenthesis = num_parenthesis + 1
                substr = substr + c
            elif c == '*':
                substr = substr + c
                if substr == '*':
                    new_text[-1] = new_text[-1] + '*'
                else:
                    new_text.append(substr)
                substr = ''
            elif c == ')':
                num_parenthesis = num_parenthesis - 1
                substr = substr + c
            elif num_parenthesis == 0:
                substr = substr + c
                new_text.append(substr)
                substr = ''
            else:
                substr = substr + c
        if substr != '':
            new_text.append(substr)
        return new_text 


class Transition:
    """Classe que representa uma transição de estados"""
    
    def __init__(self, from_state, to_state, label):
        self.from_state = from_state
        self.to_state = to_state
        self.label = label

class State:
    """Classe que representa um estado"""

    def __init__(self, label, final=False):
        self.label = label
        self.final = final
        self.out_transitions = set()

    # Adiciona uma transição de estados que sai desse estado
    def add_transition(self, transition):
        self.out_transitions.add(transition)