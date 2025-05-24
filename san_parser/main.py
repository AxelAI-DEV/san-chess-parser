import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit,
    QPushButton, QLabel, QTreeWidget, QTreeWidgetItem, QMessageBox
)

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
            # Validar número de turno
            num_token = self.tokens[self.index]
            m = SAN_PATTERNS['turn'].match(num_token)
            if not m:
                raise ValueError(f"Turno esperado en '{num_token}'")
            number = int(m.group(1))
            self.index += 1

            # Jugada blanca
            if self.index >= len(self.tokens):
                raise ValueError(f"Falta jugada blanca en el turno {number}")
            w = self.tokens[self.index]
            if not self._valid_move(w):
                raise ValueError(f"Jugada blanca inválida: '{w}' en turno {number}")
            self.index += 1

            # Jugada negra opcional
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
            return False  # No se usa "P" para peones en SAN
        if re.search(r"[a-h]9|[a-h]0", mv):
            return False  # Casillas fuera del tablero
        if mv in ["O-O-O-O", "O-O-O-O-O"]:
            return False  # Enroques inválidos
        # Asegura que al menos una expresión regular lo reconozca
        return any(p.match(mv) for p in [
            SAN_PATTERNS['castling'],
            SAN_PATTERNS['piece_move'],
            SAN_PATTERNS['pawn_move']
        ])

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parser SAN - Árbol de Turnos")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.input = QTextEdit()
        self.input.setPlaceholderText("Escribe la partida en SAN, p.ej. '1. e4 e5 2. Nf3 Nc6 ...'")
        self.btn = QPushButton("Parsear y Mostrar Árbol")
        self.btn.clicked.connect(self.on_parse)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Turno", "Blancas", "Negras"])

        layout.addWidget(QLabel("Entrada SAN:"))
        layout.addWidget(self.input)
        layout.addWidget(self.btn)
        layout.addWidget(QLabel("Árbol de Turnos:"))
        layout.addWidget(self.tree)
        self.setLayout(layout)

    def on_parse(self):
        san_text = self.input.toPlainText().strip()
        self.tree.clear()
        try:
            parser = Parser(san_text)
            turns = parser.parse()
            root = QTreeWidgetItem(["Partida"])
            for t in turns:
                item = QTreeWidgetItem([str(t.number), t.white.notation, t.black.notation if t.black else ""])
                root.addChild(item)
            self.tree.addTopLevelItem(root)
            self.tree.expandAll()
        except ValueError as e:
            QMessageBox.critical(self, "Error de Sintaxis", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(600, 400)
    w.show()
    sys.exit(app.exec_())
