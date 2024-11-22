import sys
import os

def execute_command(command, stack, commands_iterator, macros, imported_files):
    if command.startswith('"') and command.endswith('"') and len(command) > 1:
        # Handle string literals like "hello"
        stack.append(command[1:-1])  # Remove surrounding quotes
    elif command.startswith('"'):
        # Multi-word string literal
        string_literal = command[1:]  # Start collecting after the opening quote
        while True:
            next_command = next(commands_iterator, None)
            if next_command is None:
                raise Exception("Unterminated string literal")
            if next_command.endswith('"'):
                string_literal += " " + next_command[:-1]  # Add the rest and remove the closing quote
                break
            else:
                string_literal += " " + next_command
        stack.append(string_literal)
    elif command == "import":
      file_name = next(commands_iterator, None)
      if not file_name or not (file_name.startswith('"') and file_name.endswith('"')):
          raise Exception("Invalid or missing filename for import")

      file_name = file_name[1:-1]  # Remove quotes

      if file_name in imported_files:
          return  # Skip if already imported

      imported_files.add(file_name)

      # Look for the file in the current directory or library path
      lib_path = os.path.join("libs", file_name)
      if os.path.isfile(file_name):
          path_to_import = file_name
      elif os.path.isfile(lib_path):
          path_to_import = lib_path
      else:
          raise Exception(f"Imported file '{file_name}' not found")

      try:
          with open(path_to_import, "r") as import_file:  # Use path_to_import here
              # Read the imported file and process it
              import_lines = import_file.readlines()
              import_commands = []
              for line in import_lines:
                  # Strip comments and split into commands
                  line = line.split("//")[0].split("#")[0].strip()
                  if line:
                      import_commands.extend(line.split())

              # Create an iterator for the imported commands and execute them
              import_iterator = iter(import_commands)
              for import_command in import_iterator:
                  execute_command(import_command, stack, import_iterator, macros, imported_files)
      except FileNotFoundError:
          raise Exception(f"Imported file '{file_name}' not found")

    elif command == ".":
        if len(stack) < 1:
            raise Exception("Stack is empty, nothing to print")
        value = stack.pop()
        if isinstance(value, str):
            print(value)  # Print the string
        else:
            print(value)
    elif command.isdigit():
        stack.append(int(command))
    elif command == "macro":
        # Start defining a macro
        macro_name = next(commands_iterator, None)
        if not macro_name:
            raise Exception("Macro name not provided")

        # Collect commands until `end`
        macro_body = []
        for next_command in commands_iterator:
            if next_command == "end":
                break
            macro_body.append(next_command)

        if not macro_body:
            raise Exception("Missing 'end' at the end of macro definition")

        # Store the macro
        macros[macro_name] = macro_body
    elif command in macros:
        # Inline the macro's body
        macro_body = macros[command]
        macro_iterator = iter(macro_body)
        for macro_command in macro_iterator:
            execute_command(macro_command, stack, macro_iterator, macros, imported_files)
    elif command == "+":
        if len(stack) < 2:
            raise Exception("Not enough values in the stack for '+'")
        b = stack.pop()
        a = stack.pop()
        stack.append(a + b)
    elif command == "-":
        if len(stack) < 2:
            raise Exception("Not enough values in the stack for '-'")
        b = stack.pop()
        a = stack.pop()
        stack.append(a - b)
    elif command == "*":
        if len(stack) < 2:
            raise Exception("Not enough values in the stack for '*'")
        b = stack.pop()
        a = stack.pop()
        stack.append(a * b)
    elif command == "/":
        if len(stack) < 2:
            raise Exception("Not enough values in the stack for '/'")
        b = stack.pop()
        a = stack.pop()

        if b == 0:
            raise Exception("Division by zero")

        stack.append(a // b)
    elif command == ">":
        if len(stack) < 2:
            raise Exception("Not enough values in the stack for '>'")
        b = stack.pop()
        a = stack.pop()
        stack.append(1 if a > b else 0)
    elif command == "<":
        if len(stack) < 2:
            raise Exception("Not enough values in the stack for '<'")
        b = stack.pop()
        a = stack.pop()
        stack.append(1 if a < b else 0)
    elif command == "=":
        if len(stack) < 2:
            raise Exception("Not enough values in the stack for '='")
        b = stack.pop()
        a = stack.pop()
        stack.append(1 if a == b else 0)
    elif command == "dup":
        if len(stack) < 1:
            raise Exception("Not enough values in the stack for 'dup'")
        a = stack.pop()
        stack.append(a)
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
    elif command == "if":
        if len(stack) < 1:
            raise Exception("Not enough values in the stack for 'if'")
        condition = stack.pop()

        if condition == 0:  # False condition, skip to 'else' or 'end'
            while True:
                next_command = next(commands_iterator, None)
                if next_command == "else":
                    break  # Skip to else block
                elif next_command == "end" or next_command is None:
                    return  # Exit the entire if block
        else:  # True condition, process until 'else' or 'end'
            while True:
                next_command = next(commands_iterator, None)
                if next_command == "else":  # Skip over else block
                    while True:
                        next_command = next(commands_iterator, None)
                        if next_command == "end" or next_command is None:
                            return
                elif next_command == "end" or next_command is None:
                    return
                else:
                    execute_command(next_command, stack, commands_iterator, macros, imported_files)
    elif command == "else":
        pass
    elif command == "end":
        pass

def run_file(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Combine all lines into a single list of commands
        commands = []
        for line in lines:
            # Remove comments and split into commands
            line = line.split("//")[0].split("#")[0].strip()
            if line:
                commands.extend(line.split())

        stack = []
        macros = {}  # Dictionary to store macros
        imported_files = set()  # Track imported files

        # Create a single iterator for all commands
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
