def get_word_at_position(file_path, keyword, position):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if keyword in line:
                    # Split the line into words and get the word at the specified position
                    words = line.strip().split()
                    if len(words) > position:
                        return words[position]
                    else:
                        return f"Not enough words in the line for position {position}."

            return f"No '{keyword}' line found in the file."

    except FileNotFoundError:
        return f"File '{file_path}' not found."


# Example usage:
if __name__ == '__main__':
    file_path = 'public/EOH_model.nw'
    keyword = 'task'
    position = 2
    result = get_word_at_position(file_path, keyword, position)
    print(result)
