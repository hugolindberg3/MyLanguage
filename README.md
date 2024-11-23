
# MyLang: A Simple Stack-Based Programming Language

**MyLang** is a minimalistic stack-based programming language designed to be easy to use, with a focus on simplicity and flexibility. It supports basic arithmetic, control flow, macros, string handling, and file imports.

## Features

- **Stack-based Execution**: All operations are performed on a stack.
- **Basic Arithmetic**: Includes addition, subtraction, multiplication, and division.
- **Control Flow**: Support for `if`, `else`, and `end` blocks.
- **Macros**: Define reusable code blocks with macros.
- **String Handling**: Support for string literals and printing.
- **Imports**: Import external files to extend functionality.

## Getting Started

1. Clone the repository or download the files.
2. Install Python 3.x (if not already installed).
3. Run the interpreter by executing the `main.py` script with a `.mylang` file as an argument:

    ```bash
    python main.py examples/hello_world.mylang
    ```

### Example Program: `examples/hello_world.mylang`

```mylang
import "std.mylang"

"Hello, World!" print
```

This will output:
```mylang
Hello, World!
```
# MyLang: A Simple Stack-Based Programming Language

**MyLang** is a minimalistic stack-based programming language designed to be easy to use, with a focus on simplicity and flexibility. It supports basic arithmetic, control flow, macros, string handling, and file imports.

## Features

- **Stack-based Execution**: All operations are performed on a stack.
- **Basic Arithmetic**: Includes addition, subtraction, multiplication, and division.
- **Control Flow**: Support for `if`, `else`, and `end` blocks.
- **Macros**: Define reusable code blocks with macros.
- **String Handling**: Support for string literals and printing.
- **Imports**: Import external files to extend functionality.

## Getting Started

1. Clone the repository or download the files.
2. Install Python 3.x (if not already installed).
3. Run the interpreter by executing the `main.py` script with a `.mylang` file as an argument:

    ```bash
    python main.py examples/hello_world.mylang
    ```

### Example Program: `examples/hello_world.mylang`

```mylang
import "std.mylang"

"Hello, World!" print
```

This will output:
```mylang
Hello, World!
```

**`print` is part of the standard library which you have to import. If you don't want to use `print`, you can use `.` instead which is the same thing**

## Language Features
### **1. Arithmetic Operations**
MyLang supports basic arithmetic operations:
`+`: Addition
`-`: Subtraction
`*`: Multiplication
`/`: Integer Division

**Example:**
```mylang
5 4 - print  # Output: 1
10 2 / print # Output: 5
```

### **2. Control Flow**
The language supports simple condition statements using `if`, `else` and `end`. (FOR NOW)

**Example:**
```mylang
5 4 > if 1 print else 0 print end
# Output: 1 (since 5 > 4)
```

### **3. Stack manipulation**
You can manipulate the stack with commands like `dup`, `swap` and `drop`.

- `dup`: Duplicates the top value of the stack.
- `swap`: Swaps the top two values on the stack.
- `drop`: Remove the top value from the stack.

**Example:**
```mylang
5 dup print print    # Output: 5 5
3 4 swap print print # Output: 3 4
```
### **4. Macros**
MyLang allows defining macrosm which are blocks of code that can be reused. Macros are defined using the `macro` keyword and ended with `end`.

**Example:**
```mylang
macro square
	dup *
end

5 square print
# Output: 25
```

### **5. String handling**
Strings are defined using double quotes (`"`), and you can print them using the print macro.

**Example:**
```mylang
"Hello, World!" print
# Output: Hello, World!
```

### **6. Imports**
You can import other `.mylang` files to reuse code. This is done using the `import` keyword.

**Example:**
```mylang
import "std.mylang"

"Hello, World!" print
```
The `std.mylang` file might define macros like `print` for printing and other useful functionallity.

### **7. Variables**
You can define variables using macros. These variables can hold values that can later be used in expressions.

**Example:**
```mylang
macro X 10 end

X .
# Output: 10
```

### Running Tests
To test the functionality of MyLang, you can run the `tests/alltests.mylang` file, which includes various examples of arithmetic, control flow, macros, string handling and stack manipulation.

```bash
python main.py tests/alltests.mylang
```

### Conclusion
MyLang is a simple yet powerful stack-based language with basic support for arithmetic, control flow, string handling, and macros. You can extend its functionality bu importing other files and using macros to define reusable code. The interpreter is written in Python, and it's easy to get started with just a few simple commands.
