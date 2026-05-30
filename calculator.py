import tkinter as tk
from tkinter import font as tkfont
import math


def evaluate_expression(expression: str) -> str:
    try:
        expr = expression
        expr = expr.replace("^", "**")
        expr = expr.replace("π", str(math.pi))
        expr = expr.replace("e", str(math.e))

        safe_names = {
            "__builtins__": {},
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "log": math.log10,
            "ln": math.log,
            "sqrt": math.sqrt,
            "factorial": math.factorial,
            "abs": abs,
            "pi": math.pi,
            "e": math.e,
        }

        result = eval(expr, safe_names)

        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(round(result, 10))

    except ZeroDivisionError:
        return "Error: ÷ by 0"
    except ValueError as err:
        return f"Error: {err}"
    except Exception:
        return "Error: Invalid input"


class ScientificCalculator(tk.Tk):

    BG = "#1a1a2e"
    DISPLAY_BG = "#16213e"
    BTN_DARK = "#0f3460"
    BTN_MID = "#1a1a2e"
    BTN_ACCENT = "#e94560"
    BTN_CLEAR = "#533483"
    TEXT_LIGHT = "#eaeaea"
    TEXT_ACCENT = "#e94560"
    TEXT_DIM = "#a8a8b3"
    TEXT_RESULT = "#ff4d4d"

    def __init__(self):
        super().__init__()

        self.title("Scientific Calculator")
        self.resizable(False, False)
        self.configure(bg=self.BG)

        self._expression = ""

        self._build_fonts()
        self._build_display()
        self._build_buttons()

        self.bind("<Key>", self._on_key_press)

    def _build_fonts(self):
        self.font_display = tkfont.Font(family="Courier New", size=28, weight="bold")
        self.font_small_disp = tkfont.Font(family="Courier New", size=13)
        self.font_btn = tkfont.Font(family="Segoe UI", size=13, weight="bold")
        self.font_btn_sm = tkfont.Font(family="Segoe UI", size=11)

    def _build_display(self):
        frame = tk.Frame(self, bg=self.DISPLAY_BG, pady=10)
        frame.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=2, pady=(2, 0))

        self._expr_var = tk.StringVar(value="")

        tk.Label(
            frame,
            textvariable=self._expr_var,
            font=self.font_small_disp,
            bg=self.DISPLAY_BG,
            fg=self.TEXT_DIM,
            anchor="e",
            padx=12,
        ).pack(fill="x")

        self._display_var = tk.StringVar(value="0")

        tk.Entry(
            frame,
            textvariable=self._display_var,
            font=self.font_display,
            bg=self.DISPLAY_BG,
            fg=self.TEXT_RESULT,
            insertbackground=self.TEXT_RESULT,
            bd=0,
            highlightthickness=0,
            justify="right",
            state="readonly",
        ).pack(fill="x", padx=10, pady=(0, 8))

    def _build_buttons(self):

        rows = [
            [
                ("sin", 1, lambda: self._fn("sin("), self.BTN_MID, self.TEXT_LIGHT),
                ("cos", 1, lambda: self._fn("cos("), self.BTN_MID, self.TEXT_LIGHT),
                ("tan", 1, lambda: self._fn("tan("), self.BTN_MID, self.TEXT_LIGHT),
                ("log", 1, lambda: self._fn("log("), self.BTN_MID, self.TEXT_LIGHT),
                ("ln", 1, lambda: self._fn("ln("), self.BTN_MID, self.TEXT_LIGHT),
            ],
            [
                ("√", 1, lambda: self._fn("sqrt("), self.BTN_MID, self.TEXT_LIGHT),
                ("x²", 1, lambda: self._append("^2"), self.BTN_MID, self.TEXT_LIGHT),
                ("xʸ", 1, lambda: self._append("^"), self.BTN_MID, self.TEXT_LIGHT),
                ("n!", 1, lambda: self._fn("factorial("), self.BTN_MID, self.TEXT_LIGHT),
                ("π", 1, lambda: self._append("π"), self.BTN_MID, self.TEXT_ACCENT),
            ],
            [
                ("(", 1, lambda: self._append("("), self.BTN_DARK, self.TEXT_DIM),
                (")", 1, lambda: self._append(")"), self.BTN_DARK, self.TEXT_DIM),
                ("+/-", 1, self._toggle_sign, self.BTN_DARK, self.TEXT_DIM),
                ("⌫", 1, self._backspace, self.BTN_CLEAR, self.TEXT_LIGHT),
                ("C", 1, self._clear, self.BTN_CLEAR, self.TEXT_LIGHT),
            ],
            [
                ("7", 1, lambda: self._append("7"), self.BTN_DARK, self.TEXT_LIGHT),
                ("8", 1, lambda: self._append("8"), self.BTN_DARK, self.TEXT_LIGHT),
                ("9", 1, lambda: self._append("9"), self.BTN_DARK, self.TEXT_LIGHT),
                ("÷", 1, lambda: self._append("/"), self.BTN_ACCENT, self.TEXT_LIGHT),
                ("%", 1, lambda: self._append("%"), self.BTN_ACCENT, self.TEXT_LIGHT),
            ],
            [
                ("4", 1, lambda: self._append("4"), self.BTN_DARK, self.TEXT_LIGHT),
                ("5", 1, lambda: self._append("5"), self.BTN_DARK, self.TEXT_LIGHT),
                ("6", 1, lambda: self._append("6"), self.BTN_DARK, self.TEXT_LIGHT),
                ("×", 1, lambda: self._append("*"), self.BTN_ACCENT, self.TEXT_LIGHT),
                ("1/x", 1, self._reciprocal, self.BTN_MID, self.TEXT_DIM),
            ],
            [
                ("1", 1, lambda: self._append("1"), self.BTN_DARK, self.TEXT_LIGHT),
                ("2", 1, lambda: self._append("2"), self.BTN_DARK, self.TEXT_LIGHT),
                ("3", 1, lambda: self._append("3"), self.BTN_DARK, self.TEXT_LIGHT),
                ("−", 1, lambda: self._append("-"), self.BTN_ACCENT, self.TEXT_LIGHT),
                ("abs", 1, lambda: self._fn("abs("), self.BTN_MID, self.TEXT_DIM),
            ],
            [
                ("0", 2, lambda: self._append("0"), self.BTN_DARK, self.TEXT_LIGHT),
                (".", 1, lambda: self._append("."), self.BTN_DARK, self.TEXT_DIM),
                ("+", 1, lambda: self._append("+"), self.BTN_ACCENT, self.TEXT_LIGHT),
                ("=", 1, self._calculate, "#e94560", "#ffffff"),
            ],
        ]

        for r_idx, row in enumerate(rows):
            col = 0
            for (label, span, action, bg, fg) in row:
                btn = tk.Button(
                    self,
                    text=label,
                    command=action,
                    bg=bg,
                    fg=fg,
                    activebackground=self._lighten(bg),
                    activeforeground=fg,
                    font=self.font_btn if len(label) <= 2 else self.font_btn_sm,
                    bd=0,
                    highlightthickness=0,
                    cursor="hand2",
                    relief="flat",
                    width=5 * span,
                    height=2,
                )
                btn.grid(
                    row=r_idx + 1,
                    column=col,
                    columnspan=span,
                    sticky="nsew",
                    padx=2,
                    pady=2,
                )
                col += span

        for r in range(1, len(rows) + 1):
            self.grid_rowconfigure(r, weight=1)
        for c in range(5):
            self.grid_columnconfigure(c, weight=1)

    @staticmethod
    def _lighten(hex_color: str) -> str:
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = min(r + 30, 255), min(g + 30, 255), min(b + 30, 255)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _set_display(self, text: str):
        self._display_var.set(text)

    def _update_expr_label(self):
        self._expr_var.set(self._expression)

    def _append(self, char: str):
        if self._expression == "" and self._display_var.get() not in ("0", ""):
            self._expression = self._display_var.get()

        self._expression += char
        self._set_display(self._expression)
        self._update_expr_label()

    def _fn(self, func_str: str):
        self._expression += func_str
        self._set_display(self._expression)
        self._update_expr_label()

    def _clear(self):
        self._expression = ""
        self._set_display("0")
        self._expr_var.set("")

    def _backspace(self):
        self._expression = self._expression[:-1]
        self._set_display(self._expression if self._expression else "0")
        self._update_expr_label()

    def _calculate(self):
        if not self._expression:
            return

        result = evaluate_expression(self._expression)
        self._expr_var.set(self._expression + " =")
        self._expression = ""
        self._set_display(result)

    def _toggle_sign(self):
        if self._expression:
            if self._expression.startswith("-"):
                self._expression = self._expression[1:]
            else:
                self._expression = "-" + self._expression
        else:
            current = self._display_var.get()
            if current not in ("0", "", "Error"):
                self._expression = "-" + current

        self._set_display(self._expression or "0")
        self._update_expr_label()

    def _reciprocal(self):
        expr = self._expression or self._display_var.get()
        if expr:
            self._expression = f"1/({expr})"
            self._calculate()

    def _on_key_press(self, event: tk.Event):
        key = event.char
        keysym = event.keysym

        if key in "0123456789.":
            self._append(key)
        elif key in "+-*/":
            self._append(key)
        elif key == "^":
            self._append("^")
        elif key in ("\r", "\n") or keysym == "Return":
            self._calculate()
        elif keysym == "BackSpace":
            self._backspace()
        elif keysym == "Escape":
            self._clear()
        elif key == "(":
            self._append("(")
        elif key == ")":
            self._append(")")


if __name__ == "__main__":
    app = ScientificCalculator()
    app.mainloop()