read_path = "data/train_delay_err.json"
write_path = "data/train_delay_fixed.json"

with open(read_path, "r") as file_r, open(write_path, "w") as file_w:
    lines = file_r.readlines()
    file_w.write("{\n")
    # Skip the last entry as it will be incomplete.
    end = len(lines) - 1
    for i in range(end):
        if i != end - 1:
            line = lines[i].strip()[1: -1] + ",\n"
        else:
            line = lines[i].strip()[1: -1] + "\n"
        file_w.write(line)
    file_w.write("\n}")
