from Data import RANKS

ICONS = ["Bronze", "Silver", "Gold"]


def get_rank_info(level):
    current_name = "Unknown"
    current_index = 0
    for i, (lvl, name) in enumerate(RANKS):
        if level >= lvl:
            current_name = name
            current_index = i
        else:
            break
    icon = ICONS[current_index % 3]
    return current_name, icon, current_index


def get_next_rank(level):
    for lvl, name in RANKS:
        if lvl > level:
            return lvl, name
    return None, None


def get_progress_pct(level, current_index):
    """Returns 0.0–1.0 progress from current rank start to next rank."""
    current_start = RANKS[current_index][0]
    if current_index + 1 >= len(RANKS):
        return 1.0
    next_start = RANKS[current_index + 1][0]
    span = next_start - current_start
    done = level - current_start
    return max(0.0, min(1.0, done / span))


def find_rank_by_name(rank_name):
    for lvl, name in RANKS:
        if name.lower() == rank_name.lower():
            return lvl, name
    return None, None