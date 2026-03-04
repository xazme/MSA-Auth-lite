def generate_correct_spelling_table_name(name: str) -> str:
    if name.endswith("s"):
        return name + "es"
    if name.endswith("z"):
        return name[:-1] + "zzes"
    if name.endswith(("ch", "sh", "x")):
        return name + "es"
    return name + "s"
