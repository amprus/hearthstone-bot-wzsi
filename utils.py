def safe_get(lst, idx):
    try:
        return lst[idx]
    except IndexError:
        return None