def get_block_lines_range(file_path, identifier):
    in_block = False
    start_line = end_line = 0
    bracket_balance = 0

    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if identifier in line:
                in_block = True
                start_line = line_number

            if in_block:
                # Update bracket balance
                bracket_balance += line.count('{') - line.count('}')

                # Check if the block is complete
                if bracket_balance == 0:
                    end_line = line_number
                    return start_line, end_line

    return None  # Identifier not found or block incomplete


def get_block_content(file_path, identifier):
    lines_range = get_block_lines_range(file_path,identifier)

    if lines_range:
        start_line, end_line = lines_range
        with open(file_path, 'r') as file:
            lines = file.readlines()

        block_content = lines[start_line - 1:end_line]
        return block_content

    return None  # Identifier not found or block incomplete


def edit_block_content(file_path, identifier, new_lines, upsert=False):
    lines_range = get_block_lines_range(file_path,identifier)

    if lines_range:
        start_line, end_line = lines_range
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Replace the specified lines
        lines[start_line - 1:end_line] = new_lines

        with open(file_path, 'w') as file:
            file.writelines(lines)
    elif upsert:
        # must insert it at the end or start
        pass