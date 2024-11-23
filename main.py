import sys
import os

def safe_next(iterator, default=None):
    """Safely fetch the next item from an iterator, returning default if exhausted."""
    return next(iterator, default)

def execute_command(command, stack, commands_iterator, macros, imported_files):
    if command is None:
        raise Exception("Unexpected end of commands")

    elif command.startswith('"') and command.endswith('"') and len(command) > 1:
        stack.append(command[1:-1])

    elif command.startswith('"'):
        string_literal = command[1:]
        while True:
            next_command = safe_next(commands_iterator, None)
            if next_command is None:
                raise Exception("Unterminated string literal")
            if next_command.endswith('"'):
                string_literal += " " + next_command[:-1]
                break
            else:
                string_literal += " " + next_command
        stack.append(string_literal)

    elif command == "import":
        file_name = safe_next(commands_iterator, None)
        if file_name is None or not (file_name.startswith('"') and file_name.endswith('"')):
            raise Exception("Invalid or missing filename for import")

        file_name = file_name[1:-1]
        if file_name in imported_files:
            return

        imported_files.add(file_name)
        lib_path = os.path.join("libs", file_name)
        if os.path.isfile(file_name):
            path_to_import = file_name
        elif os.path.isfile(lib_path):
            path_to_import = lib_path
        else:
            raise Exception(f"Imported file '{file_name}' not found")

        try:
            with open(path_to_import, "r") as import_file:
                import_lines = import_file.readlines()
                import_commands = []
                for line in import_lines:
                    line = line.split("//")[0].split("#")[0].strip()
                    if line:
                        import_commands.extend(line.split())

                import_iterator = iter(import_commands)
                for import_command in import_iterator:
                    execute_command(import_command, stack, import_iterator, macros, imported_files)
        except FileNotFoundError:
            raise Exception(f"Imported file '{file_name}' not found")

    elif command == "while":
        condition_commands = []
        loop_body = []

        # Collect condition commands
        while True:
            next_command = safe_next(commands_iterator, None)
            if next_command is None:
                raise Exception("Unterminated 'while' condition")
            if next_command == "do":
                break
            condition_commands.append(next_command)

        # Collect loop body
        for next_command in commands_iterator:
            if next_command == "end":
                break
            loop_body.append(next_command)

        if not loop_body:
            raise Exception("Missing 'end' at the end of 'while' loop")

        # Execute the loop
        while True:
            # Evaluate the condition commands
            condition_iterator = iter(condition_commands)
            for condition_command in condition_iterator:
                execute_command(condition_command, stack, condition_iterator, macros, imported_files)

            # Check the condition result
            if len(stack) < 1:
                raise Exception("Stack is empty after evaluating 'while' condition")
            condition_result = stack.pop()
            if condition_result == 0:
                break  # Exit the loop

            # Execute the loop body
            loop_iterator = iter(loop_body)
            for loop_command in loop_iterator:
                execute_command(loop_command, stack, loop_iterator, macros, imported_files)



    elif command == ".":
        if len(stack) < 1:
            raise Exception("Stack is empty, nothing to print")
        value = stack.pop()
        print(value)

    elif command.isdigit():
        stack.append(int(command))

    elif command == "macro":
        macro_name = safe_next(commands_iterator, None)
        if not macro_name:
            raise Exception("Macro name not provided")

        macro_body = []
        for next_command in commands_iterator:
            if next_command == "end":
                break
            macro_body.append(next_command)

        if not macro_body:
            raise Exception("Missing 'end' at the end of macro definition")

        macros[macro_name] = macro_body

    elif command in macros:
        macro_body = macros[command]
        macro_iterator = iter(macro_body)
        for macro_command in macro_iterator:
            execute_command(macro_command, stack, macro_iterator, macros, imported_files)

    elif command in ["+", "-", "*", "/", ">", "<", "="]:
        if len(stack) < 2:
            raise Exception(f"Not enough values in the stack for '{command}'")
        b = stack.pop()
        a = stack.pop()

        if command == "+":
            stack.append(a + b)
        elif command == "-":
            stack.append(a - b)
        elif command == "*":
            stack.append(a * b)
        elif command == "/":
            if b == 0:
                raise Exception("Division by zero")
            stack.append(a // b)
        elif command == ">":
            stack.append(1 if a > b else 0)
        elif command == "<":
            stack.append(1 if a < b else 0)
        elif command == "=":
            stack.append(1 if a == b else 0)

    elif command in ["dup", "swap", "drop"]:
        if command == "dup":
            if len(stack) < 1:
                raise Exception(f"Not enough values in the stack for 'dup'. Current stack: {stack}")
            a = stack[-1]
            stack.append(a)
        elif command == "swap":
            if len(stack) < 2:
                raise Exception("Not enough values in the stack for 'swap'")
            a = stack.pop()
            b = stack.pop()
            stack.append(a)
            stack.append(b)
        elif command == "drop":
            if len(stack) < 1:
                raise Exception("Not enough values in the stack for 'drop'")
            stack.pop()

    elif command in ["if", "else", "end"]:
        pass

    else:
        raise Exception(f"Unknown command: {command}")

def run_file(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        commands = []
        for line in lines:
            line = line.split("//")[0].split("#")[0].strip()
            if line:
                commands.extend(line.split())

        stack = []
        macros = {}
        imported_files = set()
        commands_iterator = iter(commands)

        for command in commands_iterator:
            execute_command(command, stack, commands_iterator, macros, imported_files)

    except FileNotFoundError:
        print(f"File '{file_path}' not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <file>")
        sys.exit(1)

    run_file(sys.argv[1])
