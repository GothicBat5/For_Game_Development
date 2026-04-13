import tkinter as tk
from tkinter import font as tkfont
from RankingSystem import get_rank_info, get_next_rank, get_progress_pct, find_rank_by_name

#Palette
BG = "#0f0f13"
SURFACE = "#1a1a24"
SURFACE2 = "#22222f"
BORDER = "#2e2e3e"
ACCENT = "#e8a020"
ACCENT_DIM = "#7a5010"
TEXT = "#f0eeea"
TEXT2 = "#8a8898"
TEXT3 = "#55545f"
SUCCESS = "#3db87a"
BRONZE = "#cd7f32"
SILVER = "#a8a8b8"
GOLD = "#e8c840"

TIER_COLORS = {"Bronze": BRONZE, "Silver": SILVER, "Gold": GOLD}

# Canvas

def rounded_rect(canvas, x1, y1, x2, y2, r=10, **kwargs):
    """Draw a rounded rectangle on a Canvas."""
    pts = [
        x1+r, y1,   x2-r, y1,
        x2,   y1,   x2,   y1+r,
        x2,   y2-r, x2,   y2,
        x2-r, y2,   x1+r, y2,
        x1,   y2,   x1,   y2-r,
        x1,   y1+r, x1,   y1,
    ]
    return canvas.create_polygon(pts, smooth=True, **kwargs)


class ProgressBar(tk.Canvas):
    def __init__(self, parent, **kw):
        super().__init__(parent, height=8, bg=BG, highlightthickness=0, **kw)
        self._pct = 0.0

    def set_pct(self, pct):
        self._pct = pct
        self._draw()

    def _draw(self):
        self.delete("all")
        w = self.winfo_width() or int(self["width"] or 300)
        h = 8
        rounded_rect(self, 0, 0, w, h, r=4, fill=SURFACE2, outline="")
        fill_w = max(0, int(w * self._pct))
        if fill_w > 4:
            rounded_rect(self, 0, 0, fill_w, h, r=4, fill=ACCENT, outline="")


#Style 

def make_label(parent, text="", size=12, weight="normal", color=TEXT, **kw):
    return tk.Label(parent, text=text, bg=BG, fg=color,
                    font=(None, size, weight), **kw)


def make_entry(parent, width=20):
    e = tk.Entry(parent, bg=SURFACE2, fg=TEXT, insertbackground=ACCENT,
                 relief="flat", font=(None, 13), bd=6, width=width,
                 highlightthickness=1, highlightbackground=BORDER,
                 highlightcolor=ACCENT)
    return e


def make_button(parent, text, command, primary=False):
    bg = ACCENT if primary else SURFACE2
    fg = "#0f0f13" if primary else TEXT2
    btn = tk.Button(
        parent, text=text, command=command,
        bg=bg, fg=fg, activebackground=ACCENT_DIM, activeforeground=TEXT,
        relief="flat", bd=0, padx=16, pady=8,
        font=(None, 11, "bold"), cursor="hand2",
    )
    if not primary:
        btn.bind("<Enter>", lambda e: btn.config(bg=SURFACE, fg=TEXT))
        btn.bind("<Leave>", lambda e: btn.config(bg=SURFACE2, fg=TEXT2))
    return btn


#The results:

class ResultCard(tk.Canvas):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=BG, highlightthickness=0, height=130, **kw)
        self.bind("<Configure>", lambda e: self._redraw())
        self._data = None

    def clear(self):
        self._data = None
        self._redraw()

    def show(self, data: dict):
        self._data = data
        self._redraw()

    def _redraw(self):
        self.delete("all")
        w = self.winfo_width() or 500
        h = int(self["height"])
        d = self._data

        rounded_rect(self, 0, 0, w, h, r=12, fill=SURFACE, outline=BORDER)

        if not d:
            self.create_text(w//2, h//2, text="Enter a level and check your rank",
                             fill=TEXT3, font=(None, 11))
            return

        # Accent left bar
        self.create_rectangle(0, 12, 4, h-12, fill=ACCENT, outline="")

        tier_col = TIER_COLORS.get(d.get("icon", ""), ACCENT)

        # Rank name
        self.create_text(24, 28, text=d["name"], anchor="w",
                         fill=TEXT, font=(None, 20, "bold"))

        # Tier badge
        badge_x = 24
        self.create_text(badge_x, 54, text=f"● {d['icon']}", anchor="w",
                         fill=tier_col, font=(None, 10))

        # Extra lines
        y = 78
        for line in d.get("lines", []):
            self.create_text(24, y, text=line, anchor="w",
                             fill=TEXT2, font=(None, 10))
            y += 18

        # Progress bar drawn as two rectangles
        if "pct" in d:
            bar_x, bar_y = 24, h - 22
            bar_w = w - 48
            bar_h = 6
            self.create_rectangle(bar_x, bar_y, bar_x+bar_w, bar_y+bar_h,
                                   fill=SURFACE2, outline="")
            fill_px = max(0, int(bar_w * d["pct"]))
            if fill_px > 0:
                self.create_rectangle(bar_x, bar_y, bar_x+fill_px, bar_y+bar_h,
                                       fill=ACCENT, outline="")
            pct_txt = f"{int(d['pct']*100)}%"
            self.create_text(bar_x + bar_w + 8, bar_y + 3, text=pct_txt,
                             anchor="w", fill=TEXT3, font=(None, 9))


#Main

def start_app():
    win = tk.Tk()
    win.title("Rank System")
    win.geometry("480x620")
    win.resizable(False, False)
    win.configure(bg=BG)

    # H
    header = tk.Frame(win, bg=BG)
    header.pack(fill="x", padx=24, pady=(28, 4))

    make_label(header, "RANK SYSTEM", size=9, color=ACCENT).pack(anchor="w")
    make_label(header, "Officer Lookup", size=22, weight="bold").pack(anchor="w")

    sep = tk.Frame(win, bg=BORDER, height=1)
    sep.pack(fill="x", padx=24, pady=(12, 20))

    row1 = tk.Frame(win, bg=BG)
    row1.pack(fill="x", padx=24)

    make_label(row1, "YOUR LEVEL", size=8, color=TEXT3).pack(anchor="w")
    level_entry = make_entry(row1, width=30)
    level_entry.pack(fill="x", pady=(4, 10))

    btn_row = tk.Frame(win, bg=BG)
    btn_row.pack(fill="x", padx=24, pady=(0, 16))

    result_card = ResultCard(win, width=432)
    result_card.pack(fill="x", padx=24, pady=(0, 20))

    # Err
    err_label = make_label(win, "", size=10, color="#c04040")
    err_label.pack(padx=24, anchor="w")

    def clear_err():
        err_label.config(text="")

    def get_level(entry):
        try:
            v = int(entry.get())
            if v < 1:
                raise ValueError
            return v
        except ValueError:
            return None

    # Actions 
    def check_rank():
        clear_err()
        level = get_level(level_entry)
        if level is None:
            err_label.config(text="⚠  Please enter a valid level (integer ≥ 1)")
            result_card.clear()
            return
        name, icon, _ = get_rank_info(level)
        result_card.show({"name": name, "icon": icon})

    def show_progress():
        clear_err()
        level = get_level(level_entry)
        if level is None:
            err_label.config(text="⚠  Please enter a valid level (integer ≥ 1)")
            result_card.clear()
            return
        name, icon, idx = get_rank_info(level)
        next_lvl, next_name = get_next_rank(level)
        pct = get_progress_pct(level, idx)
        lines = []
        if next_lvl:
            remaining = next_lvl - level
            lines.append(f"Next rank: {next_name}  (level {next_lvl})")
            lines.append(f"{remaining} level{'s' if remaining != 1 else ''} remaining")
        else:
            lines.append("Maximum rank achieved!")
        result_card.show({"name": name, "icon": icon, "lines": lines, "pct": pct})

    b1 = make_button(btn_row, "Check Rank", check_rank, primary=True)
    b1.pack(side="left", padx=(0, 8))
    b2 = make_button(btn_row, "Show Progress", show_progress)
    b2.pack(side="left")

    level_entry.bind("<Return>", lambda e: check_rank())

    #Divider
    sep2 = tk.Frame(win, bg=BORDER, height=1)
    sep2.pack(fill="x", padx=24, pady=(8, 20))

    #Search
    make_label(win, "SEARCH TARGET RANK", size=8, color=TEXT3).pack(anchor="w", padx=24)

    search_frame = tk.Frame(win, bg=BG)
    search_frame.pack(fill="x", padx=24, pady=(6, 0))

    col_l = tk.Frame(search_frame, bg=BG)
    col_l.pack(side="left", expand=True, fill="x", padx=(0, 8))
    make_label(col_l, "YOUR LEVEL", size=8, color=TEXT3).pack(anchor="w")
    search_level_entry = make_entry(col_l, width=10)
    search_level_entry.pack(fill="x", pady=(4, 0))

    col_r = tk.Frame(search_frame, bg=BG)
    col_r.pack(side="left", expand=True, fill="x")
    make_label(col_r, "TARGET RANK NAME", size=8, color=TEXT3).pack(anchor="w")
    target_entry = make_entry(col_r, width=14)
    target_entry.pack(fill="x", pady=(4, 0))

    search_result = make_label(win, "", size=11, color=TEXT2, justify="left", wraplength=430)
    search_result.pack(anchor="w", padx=24, pady=(12, 0))

    def search_rank():
        clear_err()
        search_result.config(text="", fg=TEXT2)
        level = get_level(search_level_entry)
        target = target_entry.get().strip()

        if level is None or not target:
            search_result.config(
                text="⚠  Fill in both your level and a target rank name.", fg="#c04040")
            return

        target_lvl, target_name = find_rank_by_name(target)
        if target_lvl is None:
            search_result.config(
                text=f'⚠  Rank "{target}" not found!', fg="#c04040")
        elif level >= target_lvl:
            search_result.config(
                text=f"✔  You've already reached {target_name} (requires level {target_lvl}).",
                fg=SUCCESS)
        else:
            remaining = target_lvl - level
            search_result.config(
                text=f"→  {remaining} level{'s' if remaining != 1 else ''} to reach "
                     f"{target_name} (level {target_lvl}).",
                fg=ACCENT)

    search_btn_row = tk.Frame(win, bg=BG)
    search_btn_row.pack(anchor="w", padx=24, pady=(10, 0))
    make_button(search_btn_row, "Search Rank", search_rank).pack(side="left")

    target_entry.bind("<Return>", lambda e: search_rank())
    search_level_entry.bind("<Return>", lambda e: search_rank())

    win.mainloop()