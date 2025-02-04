
def txt_to_list(name):
    resp = []

    try:
        with open(f"data/{name}.txt", "r", encoding="utf-8") as f:
            resp = f.read().split("\n")
    except:
        pass

    return [item for item in resp if item]

def append_to_txt(name, message):
    with open(f"data/{name}.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")

def remove_line(name, line_to_remove):
    with open(f"data/{name}.txt", 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(f"data/{name}.txt", 'w', encoding='utf-8') as file:
        for line in lines:
            if line.strip() != line_to_remove:
                file.write(line)

