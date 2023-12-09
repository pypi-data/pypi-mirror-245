def replace_start_directive(file_path, new_start_directive):
    try:
        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Find the start directive using a regular expression
        import re
        pattern = re.compile(r'^\s*start\s+\S+', re.MULTILINE)
        match = pattern.search(content)

        if match:
            # Replace the start directive with the new string
            updated_content = content[:match.start(
            )] + f"start {new_start_directive}" + content[match.end():]

            # Write the updated content back to the file
            with open(file_path, 'w') as file:
                file.write(updated_content)

        else:
            print("No start directive found in the file.")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")


# Example usage:
if __name__ == '__main__':
    nw_file_path = 'public/molecule.nw'
    new_start_string = 'testing'
    replace_start_directive(nw_file_path, new_start_string)
