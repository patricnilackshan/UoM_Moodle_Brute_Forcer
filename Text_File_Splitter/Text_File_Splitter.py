def count_lines(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            return len(lines)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return 0

def split_file(filename, num_lines):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

            num_files = (len(lines) + num_lines - 1) // num_lines  # Calculate number of output files needed

            for i in range(num_files):
                start_idx = i * num_lines
                end_idx = min((i + 1) * num_lines, len(lines))  # Ensure not to go out of bounds
                output_filename = f"{i + 1}.txt"

                with open(output_filename, 'w') as output_file:
                    for line in lines[start_idx:end_idx]:
                        output_file.write(line)

                print(f"Created file '{output_filename}' with lines {start_idx + 1} to {end_idx}")

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")

# Main program
if __name__ == "__main__":
    filename = input("Enter the Name of the Text File: ")
    num_lines = count_lines(filename)

    if num_lines > 0:
        num_per_file = int(input(f"Number of Passwords you wanna have per file (1-{num_lines}): "))
        split_file(filename, num_per_file)
