# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 52:
# 99130 Vasco Brito
# 100611 Yassir Mahomed Yassin

from ctypes import sizeof
import sys
from types import new_class
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)
from utils import element_wise_product


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self, size, tab):
        self.size = size
        self.tab = tab

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        # TODO
        return self.tab[row][col]
        pass

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        # TODO
        if row == 0:
            return (self.tab[row + 1][col], None)
        if row == self.size-1:
            return (None, self.tab[row - 1][col])
        return (self.tab[row+1][col], self.tab[row-1][col])
        pass

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        # TODO
        if col == 0:
            return (None, self.tab[row][col+1])
        if col == self.size-1:
            return (self.tab[row][col-1], None)
        return (self.tab[row][col-1], self.tab[row][col+1])
        pass

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        Por exemplo:
            $ python3 takuzu.py < input_T01
            > from sys import stdin
            > stdin.readline()
        """
        # TODO
        # Guarda o tamanha da matrix no self.size e a lista de listas (matriz) no tab e da return da instancia do board
        lines = sys.stdin.readlines()
        N = int(lines[0])
        tab = []
        for line in lines[1:]:
            aux = ([int(n) for n in line.split()])
            tab.append(aux)
        board = Board(N, tab)
        return board
        pass

    def clone_board(self):
        new_num = int(self.size)

        new_tab = []
        for i in range(self.size):
            new_tab.append([])
            for j in range(self.size):
                new_tab[i].append(self.tab[i][j])

        new_board = Board(new_num, new_tab)

        return new_board

    def play(self, linha, coluna, num):
        # faz a jogada do numero num na linha e coluna especificada
        self.tab[linha][coluna] = num
        return

    def empty_spaces(self):
        # returns a list with all indexes containing empty spaces
        l = []

        for i in range(self.size):  # linha
            for j in range(self.size):  # col
                if self.get_number(i, j) == 2:
                    l.append([i, j])
        return l

    def filled_board(self):

        for i in range(self.size):  # linha
            for j in range(self.size):  # col
                if self.get_number(i, j) == 2:
                    return False
        return True

    def valid_row(self, row):
        current = 2
        count = 0
        zeros = 0
        ones = 0
        for i in range(self.size):
            if self.tab[row][i] == 1:
                if current == 1:
                    count += 1
                else:
                    current = 1
                    count = 1
                ones += 1
            elif self.tab[row][i] == 0:
                if current == 0:
                    count += 1
                else:
                    current = 0
                    count = 1
                zeros += 1
            else:
                count = 0
            if count == 3:
                return False
        if zeros > self.size/2 + 0.5 or ones > self.size/2 + 0.5:
            return False
        return True

    def valid_col(self, col):
        current = 2
        count = 0
        zeros = 0
        ones = 0
        for i in range(self.size):
            if self.tab[i][col] == 1:
                if current == 1:
                    count += 1
                else:
                    current = 1
                    count = 1
                ones += 1
            elif self.tab[i][col] == 0:
                if current == 0:
                    count += 1
                else:
                    current = 0
                    count = 1
                zeros += 1
            else:
                count = 0
            if count == 3:
                return False
        if zeros > self.size/2 + 0.5 or ones > self.size/2 + 0.5:
            return False
        return True

    def linhas_unicas(self):
        check = True
        linhas = []
        for i in range(self.size):
            linha = list(self.tab[i])
            if 2 not in linha:
                linhas.append(linha)
        for i in range(len(linhas)):
            count = linhas.count(linhas[i])
            if count != 1:
                check = False
        return check

    def colunas_unicas(self):
        check = True
        colunas = []
        for i in range(self.size):
            coluna = [row[i] for row in self.tab]
            if 2 not in coluna:
                colunas.append(coluna)
        for i in range(len(colunas)):
            count = colunas.count(colunas[i])
            if count != 1:
                check = False
        return check

    def __str__(self):
        # Parecido ao str override do Java mete tudo bonitinho
        tab = ""

        for i in range(self.size):
            for j in range(self.size):
                tab += str(self.tab[i][j]) + "\t"
            tab = tab[:-1] + '\n'
        tab = tab.strip("\n")
        return tab

    # TODO: outros metodos da classe


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO

        super().__init__(TakuzuState(board))
        pass

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        def is_valid(board, row, col):
            if not board.valid_row(row):
                return False
            if not board.valid_col(col):
                return False
            if not board.linhas_unicas():
                return False
            if not board.colunas_unicas():
                return False
            return True
        board = state.board.clone_board()
        for i in range(board.size):
            for j in range(board.size):
                n = board.get_number(i, j)
                if n == 2:
                    board.play(i, j, 0)
                    valid_0 = is_valid(board, i, j)
                    board.play(i, j, 1)
                    valid_1 = is_valid(board, i, j)
                    board.play(i, j, 2)
                    if not (valid_0 and valid_1):
                        if not valid_0:
                            return [(i, j, 1)]
                        if not valid_1:
                            return [(i, j, 0)]
        board = state.board.clone_board()
        for i in range(board.size):
            for j in range(board.size):
                n = board.get_number(i, j)
                if n == 2:
                    return [(i, j, 0), (i, j, 1)]
        return []

        # TODO
        pass

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO

        board = state.board.clone_board()
        board.play(action[0], action[1], action[2])

        return TakuzuState(board)

        pass

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""

        board = state.board

        if not board.filled_board():
            return False
        if not (board.linhas_unicas() and board.colunas_unicas()):
            return False
        for i in range(board.size):
            if not (board.valid_col(i) and board.valid_row(i)):
                return False
        return True
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    board = Board.parse_instance_from_stdin()

    # Criar uma instância de Takuzu:
    problem = Takuzu(board)
    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)

    print(goal_node.state.board)

    pass
