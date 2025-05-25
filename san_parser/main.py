import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton,
    QLabel, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem, QMessageBox
)
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt

# Expresiones regulares basadas en la gramática BNF
SAN_PATTERNS = {
    'castling': re.compile(r'^(O-O(-O)?)$'),
    'piece_move': re.compile(r'^[KQRBN]([a-h1-8]|[a-h][1-8])?x?[a-h][1-8](=[QRBN])?[+#]?$'),
    'pawn_move': re.compile(r'^[a-h]x[a-h][1-8](=[QRBN])?[+#]?$|^[a-h][1-8](=[QRBN])?[+#]?$'),
    'turn': re.compile(r'^(\d+)\.$')
}

class Move:
    def __init__(self, notation):
        self.notation = notation

class Turn:
    def __init__(self, number, white_move, black_move=None):
        self.number = number
        self.white = Move(white_move)
        self.black = Move(black_move) if black_move else None

class Parser:
    def __init__(self, text):
        self.tokens = text.split()
        self.index = 0
        self.turns = []

    def parse(self):
        while self.index < len(self.tokens):
            num_token = self.tokens[self.index]
            m = SAN_PATTERNS['turn'].match(num_token)
            if not m:
                raise ValueError(f"Turno esperado en '{num_token}'")
            number = int(m.group(1))
            self.index += 1

            if self.index >= len(self.tokens):
                raise ValueError(f"Falta jugada blanca en el turno {number}")
            w = self.tokens[self.index]
            if not self._valid_move(w):
                raise ValueError(f"Jugada blanca inválida: '{w}' en turno {number}")
            self.index += 1

            b = None
            if self.index < len(self.tokens) and not SAN_PATTERNS['turn'].match(self.tokens[self.index]):
                b = self.tokens[self.index]
                if not self._valid_move(b):
                    raise ValueError(f"Jugada negra inválida: '{b}' en turno {number}")
                self.index += 1

            self.turns.append(Turn(number, w, b))
        return self.turns

    def _valid_move(self, mv):
        if mv.startswith("P"):
            return False
        if re.search(r"[a-h]9|[a-h]0", mv):
            return False
        if mv in ["O-O-O-O", "O-O-O-O-O"]:
            return False
        return any(p.match(mv) for p in [
            SAN_PATTERNS['castling'],
            SAN_PATTERNS['piece_move'],
            SAN_PATTERNS['pawn_move']
        ])

class TreeNode:
    def __init__(self, label):
        self.label = label
        self.left = None
        self.right = None

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Árbol Binario de Partida de Ajedrez")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.input = QTextEdit()
        self.input.setPlaceholderText("Escribe la partida en SAN, p.ej. '1. e4 e5 2. Nf3 Nc6 ...'")
        self.button = QPushButton("Validar y Dibujar Árbol")
        self.button.clicked.connect(self.on_parse)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout.addWidget(QLabel("Entrada SAN:"))
        layout.addWidget(self.input)
        layout.addWidget(self.button)
        layout.addWidget(QLabel("Visualización del Árbol Binario:"))
        layout.addWidget(self.view)
        self.setLayout(layout)

    def on_parse(self):
        self.scene.clear()
        text = self.input.toPlainText()
        try:
            parser = Parser(text)
            turns = parser.parse()

            root = TreeNode("Partida")
            current_level = [root]
            next_level = []

            for turn in turns:
                new_white = TreeNode(turn.white.notation)
                new_black = TreeNode(turn.black.notation if turn.black else "")

                if not current_level:
                    break

                parent = current_level.pop(0)
                parent.left = new_white
                parent.right = new_black

                next_level.extend([new_white, new_black])

                if not current_level:
                    current_level = next_level
                    next_level = []

            positions = {}
            self.compute_positions(root, 0, 0, positions)
            self.draw_tree(root, positions)
        except ValueError as e:
            QMessageBox.critical(self, "Error de Sintaxis", str(e))

    def compute_positions(self, node, depth, x_index, positions):
        if node is None:
            return x_index
        x_index = self.compute_positions(node.left, depth + 1, x_index, positions)
        positions[node] = (x_index, depth)
        x_index += 1
        x_index = self.compute_positions(node.right, depth + 1, x_index, positions)
        return x_index

    def draw_tree(self, root, positions):
        radius = 20
        h_step = 90
        v_step = 100
        for node, (x_idx, y_idx) in positions.items():
            x = x_idx * h_step
            y = y_idx * v_step
            ellipse = QGraphicsEllipseItem(x, y, radius * 2, radius * 2)

            if y_idx == 0:
                ellipse.setBrush(QBrush(QColor("yellow")))
            else:
                parent = None
                for n in positions:
                    if n.left == node or n.right == node:
                        parent = n
                        break
                if parent and parent.left == node:
                    ellipse.setBrush(QBrush(Qt.white))
                else:
                    ellipse.setBrush(QBrush(QColor(200, 200, 200)))

            ellipse.setPen(QPen(Qt.black))
            self.scene.addItem(ellipse)
            text = QGraphicsTextItem(node.label)
            text.setPos(x + 5, y + 5)
            self.scene.addItem(text)

        for node in positions:
            if node.left:
                self.draw_line(node, node.left, positions, radius, h_step, v_step)
            if node.right:
                self.draw_line(node, node.right, positions, radius, h_step, v_step)

    def draw_line(self, parent, child, positions, radius, h_step, v_step):
        x1, y1 = positions[parent]
        x2, y2 = positions[child]
        line = QGraphicsLineItem(
            x1 * h_step + radius, y1 * v_step + radius * 2,
            x2 * h_step + radius, y2 * v_step
        )
        self.scene.addItem(line)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(1600, 900)
    win.show()
    sys.exit(app.exec_())
