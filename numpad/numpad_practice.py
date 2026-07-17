import tkinter as tk
import random
import time
import winsound
import json
import os


class NumpadPractice:
    STATS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "numpad_stats.json")
    POS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "numpad_pos.json")

    def __init__(self, root):
        self.root = root
        self.root.title("")
        self.root.geometry("480x250")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1b26")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.DIGITS = 8
        self.target = ""
        self.pos = 0
        self.running = False
        self.start_time = None
        self.round_times = []
        self.total_errors = 0
        self.total_rounds = 0
        self.total_digits = 0
        self.digit_errors = {}

        self.colors = {
            "bg": "#1a1b26",
            "card": "#24283b",
            "border": "#414868",
            "text": "#c0caf5",
            "muted": "#565f89",
            "orange": "#ff9e64",
            "wrong": "#f7768e",
            "green": "#9ece6a",
        }

        self.CALC_TONES = {
            "0": 500, "1": 550, "2": 600, "3": 650, "4": 700,
            "5": 750, "6": 800, "7": 850, "8": 900, "9": 950,
        }

        self.load_stats()
        self.load_pos()
        self.build_ui()
        self.new_round()

    def build_ui(self):
        card = tk.Frame(self.root, bg=self.colors["border"])
        card.pack(padx=12, pady=(10, 4), fill=tk.X)

        inner = tk.Frame(card, bg=self.colors["card"])
        inner.pack(fill=tk.X, padx=1, pady=1)

        self.digit_frames = []
        for i in range(self.DIGITS):
            cf = tk.Frame(inner, bg=self.colors["card"], width=52, height=60)
            cf.pack(side=tk.LEFT, expand=True, padx=2, pady=10)
            cf.pack_propagate(False)

            lbl = tk.Label(cf, text="0", bg=self.colors["card"], fg=self.colors["text"],
                           font=("Consolas", 30, "bold"))
            lbl.place(x=0, y=0, relwidth=1, relheight=1)

            self.digit_frames.append({"frame": cf, "label": lbl, "anim_id": None})

        sf = tk.Frame(self.root, bg=self.colors["bg"])
        sf.pack(fill=tk.X, padx=12, pady=(0, 2))

        self.status_var = tk.StringVar(value="")
        tk.Label(sf, textvariable=self.status_var, bg=self.colors["bg"],
                 fg=self.colors["muted"], font=("Microsoft YaHei", 9)
                 ).pack(side=tk.LEFT)

        self.round_var = tk.StringVar(value="")
        tk.Label(sf, textvariable=self.round_var, bg=self.colors["bg"],
                 fg=self.colors["muted"], font=("Microsoft YaHei", 9)
                 ).pack(side=tk.RIGHT)

        bf = tk.Frame(self.root, bg=self.colors["bg"])
        bf.pack(fill=tk.X, padx=12, pady=(0, 4))

        self.avg_var = tk.StringVar(value="")
        tk.Label(bf, textvariable=self.avg_var, bg=self.colors["bg"],
                 fg=self.colors["green"], font=("Microsoft YaHei", 9)
                 ).pack(side=tk.LEFT)

        self.esc_var = tk.StringVar(value="Esc 退出")
        tk.Label(bf, textvariable=self.esc_var, bg=self.colors["bg"],
                 fg=self.colors["muted"], font=("Microsoft YaHei", 8)
                 ).pack(side=tk.RIGHT)

        df = tk.Frame(self.root, bg=self.colors["bg"])
        df.pack(fill=tk.X, padx=12)

        self.detail_var = tk.StringVar(value="")
        tk.Label(df, textvariable=self.detail_var, bg=self.colors["bg"],
                 fg=self.colors["wrong"], font=("Consolas", 9)
                 ).pack(side=tk.LEFT)

        self.next_btn = tk.Button(df, text="▶ 下一轮", bg="#3b4261",
                                  fg=self.colors["text"], font=("Microsoft YaHei", 9),
                                  bd=0, padx=8, pady=2,
                                  activebackground=self.colors["orange"],
                                  activeforeground=self.colors["bg"],
                                  cursor="hand2", command=self.skip_round)
        self.next_btn.pack(side=tk.RIGHT)

        self.root.bind("<KeyPress>", self.on_key)
        self.root.focus_set()
        self.update_stats()

    def play_correct_sound(self, digit):
        freq = self.CALC_TONES.get(digit, 1000)
        try:
            winsound.Beep(freq, 300)
        except Exception:
            pass

    def play_wrong_sound(self):
        try:
            winsound.Beep(350, 200)
        except Exception:
            pass

    def skip_round(self):
        if not self.running:
            self.new_round()

    def new_round(self):
        self.target = "".join(random.choice("0123456789") for _ in range(self.DIGITS))
        self.pos = 0
        self.running = True
        self.start_time = None
        self.total_rounds += 1

        for i, d in enumerate(self.digit_frames):
            d["label"].config(text=self.target[i], fg=self.colors["text"], bg=self.colors["card"])
            d["frame"].config(bg=self.colors["card"])
            if d["anim_id"]:
                self.root.after_cancel(d["anim_id"])
                d["anim_id"] = None
            d["label"].place(x=0, y=0)

        self.highlight_pos()
        self.root.focus_set()

    def highlight_pos(self):
        for i, d in enumerate(self.digit_frames):
            if i < self.pos:
                d["label"].config(fg=self.colors["orange"], bg=self.colors["card"])
                d["frame"].config(bg=self.colors["card"])
            elif i == self.pos and self.running:
                d["frame"].config(bg="#3b4261")
                d["label"].config(fg=self.colors["text"], bg="#3b4261")
            else:
                d["label"].config(fg=self.colors["text"], bg=self.colors["card"])
                d["frame"].config(bg=self.colors["card"])

    def on_key(self, event):
        if event.keysym == "Escape":
            self.on_close()
            return
        if not self.running:
            return

        ch = event.char
        if ch not in "0123456789":
            return

        if self.start_time is None:
            self.start_time = time.time()

        if ch == self.target[self.pos]:
            self.play_correct_sound(ch)
            self.total_digits += 1
            self.pos += 1
            self.highlight_pos()

            if self.pos >= self.DIGITS:
                elapsed = time.time() - self.start_time
                self.round_times.append(elapsed)
                self.running = False
                self.update_stats()
                self.root.after(200, self.new_round)
        else:
            self.total_errors += 1
            self.digit_errors[ch] = self.digit_errors.get(ch, 0) + 1
            self.play_wrong_sound()
            self.animate_error(self.pos)
            self.update_stats()

    def animate_error(self, idx):
        d = self.digit_frames[idx]
        d["label"].config(fg=self.colors["wrong"])
        steps = [(0, -8), (0, 8), (0, -4), (0, 4), (0, 0)]

        def do_step(step_idx):
            if step_idx >= len(steps):
                d["label"].config(fg=self.colors["text"], bg="#3b4261")
                return
            dx, dy = steps[step_idx]
            d["label"].place(x=dx, y=dy)
            d["anim_id"] = self.root.after(35, do_step, step_idx + 1)

        do_step(0)

    def update_stats(self):
        total_errors = self.total_errors
        rounds_done = len(self.round_times)
        if rounds_done > 0:
            total_time = sum(self.round_times)
            total_d = rounds_done * self.DIGITS
            dps = total_d / total_time if total_time > 0 else 0
            self.avg_var.set(f"{dps:.1f} 数字/秒  |  错误 {total_errors}  |  共 {total_d} 字")
        else:
            self.avg_var.set(f"错误 {total_errors}")
        self.round_var.set(f"第 {self.total_rounds} 轮")

        if self.digit_errors:
            parts = [f"{d}×{c}" for d, c in sorted(self.digit_errors.items(), key=lambda x: int(x[0]))]
            self.detail_var.set("  ".join(parts))
        else:
            self.detail_var.set("")

    def save_stats(self):
        data = {"rounds": len(self.round_times), "times": self.round_times, "errors": self.total_errors}
        try:
            with open(self.STATS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
        except Exception:
            pass

    def load_stats(self):
        pass

    def on_close(self):
        self.running = False
        self.save_pos()
        self.root.destroy()

    def save_pos(self):
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        try:
            with open(self.POS_FILE, "w") as f:
                json.dump({"x": x, "y": y}, f)
        except Exception:
            pass

    def load_pos(self):
        try:
            with open(self.POS_FILE, "r") as f:
                pos = json.load(f)
            self.root.geometry(f"480x250+{pos['x']}+{pos['y']}")
        except Exception:
            self.root.geometry("480x250+{}+{}".format(
                (self.root.winfo_screenwidth() - 480) // 2,
                (self.root.winfo_screenheight() - 250) // 2
            ))


if __name__ == "__main__":
    root = tk.Tk()
    app = NumpadPractice(root)
    root.mainloop()
