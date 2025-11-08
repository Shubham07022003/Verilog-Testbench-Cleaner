# Verilog Testbench Cleaner

A robust Python tool for cleaning Verilog/SystemVerilog testbench files using AST-level manipulation. This tool automatically removes test-specific code, variables, and parameters, leaving a clean template ready for your next test case.




## 🎯 Overview

The Verilog Testbench Cleaner is designed to automatically clean testbench files by removing all test-specific code while preserving the essential module structure. This is particularly useful when you need to:

- Prepare testbench files for new test cases
- Remove old test stimulus and variables
- Clean up test files for reuse
- Automate testbench template generation

The tool uses **AST (Abstract Syntax Tree)** parsing for accurate code manipulation, with automatic fallback to regex-based cleaning for maximum compatibility.

## ✨ Features

### Code Removal
- ✅ **Initial blocks**: Removes all `initial begin...end` blocks (test stimulus)
- ✅ **System tasks**: Removes `$monitor`, `$dumpfile`, `$dumpvars`, `$finish` statements
- ✅ **Comments**: Removes all single-line (`//`) and multi-line (`/* */`) comments
- ✅ **Parameters**: Removes `parameter` and `localparam` declarations
- ✅ **Macros**: Removes `` `define `` macro definitions
- ✅ **Variables**: Removes all variable declarations (`reg`, `wire`, `integer`, `real`, `time`, `realtime`)

### Code Modification
- ✅ **DUT instances**: Clears port connections, converting `module_name instance_name (ports...)` to `module_name instance_name ()`
- ✅ **Module structure**: Preserves module declarations and `endmodule` statements

### Robustness
- ✅ **AST-based parsing**: Uses Pyverilog for accurate syntax understanding
- ✅ **Automatic fallback**: Falls back to regex-based cleaning if AST parsing fails
- ✅ **Warning suppression**: Automatically suppresses parser warnings for clean output
- ✅ **Error handling**: Graceful error handling with informative messages

## 📦 Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Step 1: Clone or Download

```bash
# If using git
git clone https://github.com/Shubham07022003/Verilog-Testbench-Cleaner.git
cd regEx/verilog_test

# Or download and extract the files
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `pyverilog` - Verilog parser and AST manipulation library

### Step 3: Verify Installation

```bash
python test_cleaner.py --help
```

If you see the script running (or a cleaned file generated), the installation is successful!

## 🚀 Quick Start

### Basic Usage

```bash
# Clean a testbench file
python test_cleaner.py path/to/your_testbench.sv

# If no filename provided, defaults to and_gate_test.sv
python test_cleaner.py
```

### Output

The cleaned file will be saved as `*_cleaned.sv` in the same directory as the input file.

**Example:**
- Input: `testbench.sv`
- Output: `testbench_cleaned.sv`

## 📖 Usage Guide

### Command Line Usage

#### Basic Command

```bash
python test_cleaner.py [filename]
```

**Arguments:**
- `filename` (optional): Path to the Verilog testbench file. If not provided, defaults to `and_gate_test.sv` in the current directory.

**Examples:**

```bash
# Clean a specific file
python test_cleaner.py my_testbench.sv

# Clean file in another directory
python test_cleaner.py ../tests/adder_tb.sv

# Use default file
python test_cleaner.py
```

#### Output

The script will:
1. Process the input file
2. Generate a cleaned version
3. Display: `Cleaned file saved as: [filename]_cleaned.sv`

### Python API Usage

You can also use the cleaner as a Python module:

```python
from test_cleaner import clean_sv_testbench

# Clean a testbench file
cleaned_file = clean_sv_testbench("path/to/testbench.sv")
print(f"Cleaned file: {cleaned_file}")
```

**Return Value:**
- Returns the path to the cleaned file as a string

**Example Script:**

```python
#!/usr/bin/env python3
from test_cleaner import clean_sv_testbench
import glob

# Clean all testbench files in a directory
for test_file in glob.glob("tests/*_tb.sv"):
    cleaned = clean_sv_testbench(test_file)
    print(f"Cleaned: {test_file} -> {cleaned}")
```

## 📝 Examples

### Example 1: Simple Testbench

**Input** (`simple_test.sv`):
```verilog
module Simple_TB;
    // Test signals
    reg clk, reset;
    wire out;
    
    // DUT instantiation
    SimpleModule uut (.clk(clk), .reset(reset), .out(out));
    
    // Clock generation
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end
    
    // Test stimulus
    initial begin
        reset = 1;
        #10;
        reset = 0;
        #100;
        $finish;
    end
    
    // Monitoring
    initial begin
        $monitor("Time: %t, Reset: %b, Out: %b", $time, reset, out);
    end
endmodule
```

**Output** (`simple_test_cleaned.sv`):
```verilog
module Simple_TB;
SimpleModule uut ();
endmodule
```

### Example 2: Complex Testbench with Parameters

**Input** (`complex_test.sv`):
```verilog
`define TEST_MODE 1

module Complex_TB;
    parameter WIDTH = 8;
    parameter DEPTH = 16;
    
    reg [WIDTH-1:0] data_in;
    reg enable;
    wire [WIDTH-1:0] data_out;
    
    ComplexModule #(.WIDTH(WIDTH), .DEPTH(DEPTH)) uut (
        .data_in(data_in),
        .enable(enable),
        .data_out(data_out)
    );
    
    initial begin
        data_in = 8'hFF;
        enable = 1;
        #100;
        $dumpfile("dump.vcd");
        $dumpvars();
    end
endmodule
```

**Output** (`complex_test_cleaned.sv`):
```verilog
module Complex_TB;
ComplexModule uut ();
endmodule
```

### Example 3: Multi-Module Testbench

**Input** (`multi_module_test.sv`):
```verilog
module TestModule1_TB;
    reg a, b;
    wire y;
    TestModule1 uut1 (y, a, b);
    
    initial begin
        a = 0; b = 0;
        #10;
    end
endmodule

module TestModule2_TB;
    reg [7:0] data;
    wire [7:0] result;
    TestModule2 uut2 (.data(data), .result(result));
    
    initial begin
        data = 8'hAA;
    end
endmodule
```

**Output** (`multi_module_test_cleaned.sv`):
```verilog
module TestModule1_TB;
TestModule1 uut1 ();
endmodule

module TestModule2_TB;
TestModule2 uut2 ();
endmodule
```

## 🔧 API Reference

### Function: `clean_sv_testbench(filename)`

Cleans a Verilog testbench file by removing test-specific code.

**Parameters:**
- `filename` (str): Path to the Verilog/SystemVerilog testbench file

**Returns:**
- `str`: Path to the cleaned output file (ends with `_cleaned.sv`)

**Raises:**
- `FileNotFoundError`: If the input file doesn't exist
- `IOError`: If there's an error reading/writing files

**Example:**
```python
from test_cleaner import clean_sv_testbench

try:
    cleaned_file = clean_sv_testbench("my_testbench.sv")
    print(f"Success! Cleaned file: {cleaned_file}")
except FileNotFoundError:
    print("Error: File not found")
except Exception as e:
    print(f"Error: {e}")
```

### Class: `ASTCleaner`

Internal class used for AST traversal and cleaning. Not typically used directly, but available for advanced customization.

##  How It Works

### Architecture

The tool uses a two-stage approach:

1. **Primary Method (AST-based)**:
   - Parses Verilog code into an Abstract Syntax Tree using Pyverilog
   - Traverses the AST using a visitor pattern
   - Removes/modifies specific node types
   - Regenerates clean Verilog code from the modified AST

2. **Fallback Method (Regex-based)**:
   - Used when AST parsing fails or pyverilog is not available
   - Uses pattern matching to identify and remove code sections
   - Handles edge cases and complex structures

### Processing Steps

```
Input File
    ↓
[AST Parser] → Parse into AST
    ↓
[AST Cleaner] → Remove/Modify Nodes
    ↓
[Code Generator] → Generate Clean Code
    ↓
[Post-processing] → Remove Comments & Macros
    ↓
Output File (_cleaned.sv)
```

### Node Types Handled

The AST cleaner handles the following node types:

- `Initial` → Removed (test stimulus)
- `SystemCall` → Removed if test-related ($monitor, $dumpfile, etc.)
- `Parameter` / `Localparam` → Removed
- `Reg` / `Wire` / `Integer` / etc. → Removed (variable declarations)
- `InstanceList` / `Instance` → Port connections cleared
- `ModuleDef` → Preserved (module structure)

## 🐛 Troubleshooting

### Common Issues

#### Issue 1: "pyverilog is not installed"

**Symptoms:**
```
Warning: pyverilog is not installed. Using regex-based fallback.
```

**Solution:**
```bash
pip install pyverilog
# Or
pip install -r requirements.txt
```

#### Issue 2: "AST parsing failed"

**Symptoms:**
```
AST parsing failed: [error message]
Falling back to regex-based cleaning...
```

**Solutions:**
- The tool automatically falls back to regex-based cleaning
- This is normal and the tool will still work correctly
- If you want AST parsing, ensure pyverilog is properly installed

#### Issue 3: File not found

**Symptoms:**
```
FileNotFoundError: [Errno 2] No such file or directory
```

**Solution:**
- Check that the file path is correct
- Use absolute paths if relative paths don't work
- Ensure the file has `.sv` or `.v` extension

#### Issue 4: Output file not generated

**Possible Causes:**
- Insufficient file permissions
- Disk space issues
- File path contains invalid characters

**Solution:**
- Check file permissions in the output directory
- Ensure you have write access
- Try a different output location

### Performance Tips

- **Large files**: The regex fallback may be faster for very large files (>10,000 lines)
- **Multiple files**: Use the Python API in a loop for batch processing
- **Memory**: AST parsing uses more memory; use regex fallback for memory-constrained environments

### Getting Help

If you encounter issues:

1. Check that Python 3.6+ is installed: `python --version`
2. Verify dependencies: `pip list | grep pyverilog`
3. Check file syntax: Ensure your Verilog file is valid
4. Review error messages: The tool provides informative error messages




## 📚 Code Explanation

This section provides a detailed explanation of the `test_cleaner.py` code for mentor review.

### Section 1: Module Docstring and Imports

```python
"""
Verilog Testbench Cleaner using Pyverilog AST Parser
Clears testbench files for next test by removing test-specific code
Uses AST-level manipulation for robust parsing and modification
"""
```
**Explanation:** Module-level docstring describing the purpose and approach of the tool.

```python
import sys
import os
import warnings
from io import StringIO
```
**Explanation:**
- `sys`: Used for system-specific parameters (stderr redirection, command-line arguments)
- `os`: Used for file path operations (absolute path conversion)
- `warnings`: Used to suppress parser generation warnings
- `StringIO`: Used to create a string buffer for redirecting stderr

```python
# Suppress pyverilog parser generation warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*shift/reduce.*', category=UserWarning)
```
**Explanation:**
- Filters out all UserWarning category warnings
- Specifically filters shift/reduce conflict warnings (common in parser generators)
- These prevent cluttering the output with parser generation messages

```python
try:
    # Suppress stdout/stderr during parser import to hide shift/reduce warnings
    old_stderr = sys.stderr
    sys.stderr = StringIO()
    try:
        from pyverilog.vparser.parser import parse
        from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
        PYVERILOG_AVAILABLE = True
    finally:
        sys.stderr = old_stderr
except ImportError:
    PYVERILOG_AVAILABLE = False
    if __name__ == "__main__":
        print("Warning: pyverilog is not installed. Using regex-based fallback.")
        print("For better results, install pyverilog: pip install pyverilog")
```
**Explanation:**
- Save current stderr and redirect to StringIO buffer to suppress warnings during import
- Import pyverilog's parser and code generator
- Set flag indicating AST parsing is available
- Restore stderr to original stream (ensures cleanup even if import fails)
- Handle ImportError if pyverilog is not installed, set flag to False and optionally print warning

### Section 2: ASTCleaner Class

```python
class ASTCleaner:
    """
    AST visitor to clean Verilog testbench code
    """
    def __init__(self):
        self.cleaned_items = []
```
**Explanation:**
- Define ASTCleaner class implementing visitor pattern
- Initialize instance variable to store cleaned items during traversal

```python
    def visit(self, node):
        """Visit AST nodes and clean them"""
        if node is None:
            return None
        
        node_type = node.__class__.__name__
        
        # Handle different node types
        method_name = f'visit_{node_type}'
        if hasattr(self, method_name):
            return getattr(self, method_name)(node)
        else:
            # Default: keep the node as-is
            return node
```
**Explanation:**
- Main visitor method that dispatches to specific handlers
- Handle None nodes (edge case)
- Get the class name of the node (e.g., "Initial", "ModuleDef")
- Dynamically construct method name (e.g., "visit_Initial")
- Check if specific handler exists for this node type
- Call the specific handler method using getattr (reflection)
- Default behavior: return node unchanged if no handler exists

```python
    def visit_Description(self, node):
        """Clean description (top-level container)"""
        cleaned_definitions = []
        for item in node.definitions:
            cleaned = self.visit(item)
            if cleaned is not None:
                cleaned_definitions.append(cleaned)
        node.definitions = cleaned_definitions
        return node
```
**Explanation:**
- Handler for Description node (top-level AST container)
- Create list to store cleaned module definitions
- Iterate through all definitions (typically modules)
- Recursively visit each definition
- Only keep non-None results (removed items return None)
- Update node with cleaned definitions
- Return modified node

```python
    def visit_ModuleDef(self, node):
        """Clean module definition"""
        if not hasattr(node, 'items'):
            return node
        
        self.cleaned_items = []
        for item in node.items:
            cleaned = self.visit(item)
            if cleaned is not None:
                self.cleaned_items.append(cleaned)
        
        node.items = self.cleaned_items
        return node
```
**Explanation:**
- Handler for ModuleDef (module definition)
- Safety check: ensure node has 'items' attribute
- Initialize list for cleaned module items
- Visit each item in module (statements, declarations, etc.)
- Update module with cleaned items
- Return modified module

```python
    def visit_Initial(self, node):
        """Remove initial blocks"""
        return None
```
**Explanation:**
- Handler for Initial blocks (test stimulus)
- Return None to remove this node from AST

```python
    def visit_SystemCall(self, node):
        """Remove system tasks like $monitor, $dumpfile, etc."""
        if hasattr(node, 'syscall'):
            syscall_name = str(node.syscall).lower()
            if any(x in syscall_name for x in ['monitor', 'dumpfile', 'dumpvars', 'finish']):
                return None
        return node
```
**Explanation:**
- Handler for SystemCall nodes (system tasks like $monitor)
- Check if node has syscall attribute
- Convert syscall name to lowercase for case-insensitive matching
- Check if syscall is test-related (monitor, dumpfile, etc.)
- Return None to remove test-related system calls
- Return node unchanged for other system calls

```python
    def visit_Parameter(self, node):
        """Remove parameter declarations"""
        return None
    
    def visit_Localparam(self, node):
        """Remove localparam declarations"""
        return None
```
**Explanation:**
- Handlers to remove parameter and localparam declarations
- Both return None to remove these nodes

```python
    def visit_Decl(self, node):
        """Handle declarations - remove variable declarations"""
        if hasattr(node, 'list'):
            # Check if it's a variable declaration (reg, wire, etc.)
            for decl_item in node.list:
                if hasattr(decl_item, 'name'):
                    # This is a variable declaration, remove it
                    return None
        return node
```
**Explanation:**
- Handler for generic Decl nodes
- Check if declaration has a list of items
- Check if items have names (indicating variable declarations)
- Return None to remove variable declarations
- Keep other declaration types

```python
    def visit_Reg(self, node):
        """Remove reg declarations"""
        return None
    
    def visit_Wire(self, node):
        """Remove wire declarations"""
        return None
    
    def visit_Integer(self, node):
        """Remove integer declarations"""
        return None
    
    def visit_Real(self, node):
        """Remove real declarations"""
        return None
    
    def visit_Realtime(self, node):
        """Remove realtime declarations"""
        return None
    
    def visit_Time(self, node):
        """Remove time declarations"""
        return None
```
**Explanation:**
- Specific handlers for each variable type
- All return None to remove these declarations from the AST

```python
    def visit_InstanceList(self, node):
        """Clean instance list - clear port connections"""
        if hasattr(node, 'instances'):
            for instance in node.instances:
                # Clear portlist
                if hasattr(instance, 'portlist'):
                    instance.portlist = None
                if hasattr(instance, 'portlist_opt'):
                    instance.portlist_opt = None
        return node
```
**Explanation:**
- Handler for InstanceList (list of module instantiations)
- Check if node has instances
- Iterate through each instance
- Clear port connections by setting portlist attributes to None
- Return modified node (instances kept, ports cleared)

```python
    def visit_Instance(self, node):
        """Clean instance - clear port connections"""
        if hasattr(node, 'portlist'):
            node.portlist = None
        if hasattr(node, 'portlist_opt'):
            node.portlist_opt = None
        return node
```
**Explanation:**
- Handler for individual Instance nodes
- Clear port connections similar to InstanceList
- Return modified instance

### Section 3: Main Cleaning Function

```python
def clean_sv_testbench(filename):
    """
    Clears a Verilog testbench file for next test using AST-level manipulation:
    ...
    """
    if PYVERILOG_AVAILABLE:
        try:
            return clean_with_ast(filename)
        except Exception as e:
            # Suppress verbose error messages for common parsing issues
            error_str = str(e).lower()
            if "shift/reduce" not in error_str and "winerror" not in error_str:
                # Only show meaningful errors
                print(f"AST parsing failed: {e}")
            # Silently fall back to regex-based cleaning
            return clean_sv_testbench_regex(filename)
    else:
        return clean_sv_testbench_regex(filename)
```
**Explanation:**
- Main entry point function
- Check if AST parsing is available
- Try AST-based cleaning
- Handle exceptions gracefully
- Convert error to lowercase for case-insensitive matching
- Filter out common, non-critical errors (shift/reduce, file path issues)
- Only print meaningful errors
- Fall back to regex cleaning on any error
- Use regex if pyverilog not available

### Section 4: AST-Based Cleaning

```python
def clean_with_ast(filename):
    """Clean using AST parser"""
    # Read file content first
    with open(filename, 'r') as f:
        code = f.read()
```
**Explanation:**
- Function for AST-based cleaning
- Read entire file content into memory

```python
    # Convert to absolute path for pyverilog (needed for include resolution)
    abs_filename = os.path.abspath(filename)
    filelist = [abs_filename]
```
**Explanation:**
- Convert relative path to absolute (pyverilog needs this for includes)
- Create list with single file (parse() expects a list)

```python
    # Suppress parser generation warnings
    old_stderr = sys.stderr
    sys.stderr = StringIO()
    try:
        # Parse the Verilog file
        # pyverilog parse() expects a list of file paths
        ast, directives = parse(filelist)
    except Exception as parse_error:
        sys.stderr = old_stderr
        # Try alternative: parse from string if file-based parsing fails
        try:
            from pyverilog.vparser.parser import parse_string
            ast, directives = parse_string(code)
        except (ImportError, AttributeError):
            # parse_string might not exist, re-raise original error
            raise parse_error
    finally:
        sys.stderr = old_stderr
```
**Explanation:**
- Save and redirect stderr to suppress warnings
- Parse file into AST and directives
- Catch any parsing errors
- Restore stderr before error handling
- Try alternative parsing method (parse_string) if available
- If parse_string doesn't exist, re-raise original error
- Always restore stderr (cleanup)

```python
    # Clean the AST
    cleaner = ASTCleaner()
    cleaned_ast = cleaner.visit(ast)
```
**Explanation:**
- Create ASTCleaner instance
- Visit and clean the entire AST starting from root

```python
    # Generate code from cleaned AST
    codegen = ASTCodeGenerator()
    cleaned_code = codegen.visit(cleaned_ast)
```
**Explanation:**
- Create code generator instance
- Convert cleaned AST back to Verilog code string

```python
    # Remove comments (AST parser may preserve some)
    import re
    cleaned_code = re.sub(r'//.*$', '', cleaned_code, flags=re.MULTILINE)
    cleaned_code = re.sub(r'/\*.*?\*/', '', cleaned_code, flags=re.DOTALL)
    
    # Remove `define directives
    cleaned_code = re.sub(r'^\s*`define\s+.*$', '', cleaned_code, flags=re.MULTILINE | re.IGNORECASE)
```
**Explanation:**
- Import regex module
- Remove single-line comments (// to end of line)
- Remove multi-line comments (/* ... */)
- Remove `define directives (preprocessor macros)

```python
    # Save result
    new_filename = filename.replace('.sv', '_cleaned.sv')
    with open(new_filename, 'w') as f:
        f.write(cleaned_code)
    
    print(f"Cleaned file saved as: {new_filename}")
    return new_filename
```
**Explanation:**
- Generate output filename by replacing extension
- Write cleaned code to file
- Print success message
- Return output filename

### Section 5: Regex Fallback Function

```python
def clean_sv_testbench_regex(filename):
    """
    Fallback regex-based cleaner
    Used when AST parsing fails or pyverilog is not available
    """
    import re
    
    with open(filename, 'r') as file:
        content = file.read()

    # Remove multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
```
**Explanation:**
- Fallback function using regex pattern matching
- Import regex module
- Read entire file
- Remove multi-line comments first (before line splitting)

```python
    lines = content.splitlines(keepends=True)
    cleaned_lines = []
    inside_initial = False
    brace_depth = 0
    inside_parameter = False
    inside_define = False
```
**Explanation:**
- Split into lines, preserving line endings
- List to store cleaned lines
- State flags for tracking nested structures

```python
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
```
**Explanation:**
- Initialize line index
- Loop through all lines
- Get current line and stripped version

```python
        # Handle initial begin...end block removal
        if inside_initial:
            if 'begin' in stripped:
                brace_depth += 1
            if 'end' in stripped:
                brace_depth -= 1
                if brace_depth == 0:
                    inside_initial = False
            i += 1
            continue
```
**Explanation:**
- Check if currently inside initial block
- Increment depth counter for nested 'begin'
- Decrement for 'end', exit when depth reaches 0
- Skip this line and continue

```python
        # Remove initial blocks
        if re.match(r'^\s*initial\s+begin', stripped, re.IGNORECASE):
            inside_initial = True
            brace_depth = 1
            i += 1
            continue
        elif re.match(r'^\s*initial\s+', stripped, re.IGNORECASE):
            i += 1
            continue
```
**Explanation:**
- Match "initial begin" pattern
- Set flags and skip line
- Match single-line "initial" (without begin)

```python
        # Remove system tasks
        if re.search(r'\$monitor|\$dumpfile|\$dumpvars|\$finish', stripped, re.IGNORECASE):
            i += 1
            continue
```
**Explanation:**
- Search for system task patterns
- Skip lines containing test-related system tasks

```python
        # Remove `define macros
        if re.match(r'^\s*`define\s+', stripped, re.IGNORECASE):
            if line.rstrip().endswith('\\'):
                inside_define = True
            i += 1
            continue
        
        if inside_define:
            if line.rstrip().endswith('\\'):
                i += 1
                continue
            else:
                inside_define = False
                i += 1
                continue
```
**Explanation:**
- Match `define directive
- Check if multi-line (ends with backslash)
- Handle multi-line define continuation

```python
        # Remove parameter and localparam
        if re.match(r'^\s*(parameter|localparam)\s+', stripped, re.IGNORECASE):
            if ';' in stripped:
                i += 1
                continue
            else:
                inside_parameter = True
                i += 1
                continue
        
        if inside_parameter:
            if ';' in stripped:
                inside_parameter = False
            i += 1
            continue
```
**Explanation:**
- Match parameter/localparam declarations
- Single-line (has semicolon)
- Multi-line (no semicolon yet)
- Continue skipping until semicolon found

```python
        # Remove variable declarations
        if not inside_parameter:
            if re.match(r'^\s*(reg|wire|integer|real|time|realtime)\s+', stripped, re.IGNORECASE):
                if ';' in stripped:
                    i += 1
                    continue
                else:
                    while i < len(lines) and ';' not in lines[i]:
                        i += 1
                    if i < len(lines):
                        i += 1
                    continue
```
**Explanation:**
- Only process if not inside parameter block
- Match variable type keywords
- Single-line declaration
- Multi-line declaration (skip until semicolon)

```python
        # Remove comments
        line = re.sub(r'//.*$', '', line)
        line_stripped = line.strip()
        if line_stripped == '':
            i += 1
            continue
```
**Explanation:**
- Remove inline comments
- Skip empty lines (were only comments)

```python
        # Clear DUT instance ports
        if '(' in line_stripped:
            if not re.match(r'^\s*(assign|if|for|while|case|function|task|module|endmodule)', line_stripped, re.IGNORECASE):
                inst_match = re.match(r'^(\s*(?:\w+\s+)*\w+)\s*\(', line)
                if inst_match:
                    cleaned_line = inst_match.group(1) + " ();\n"
                    cleaned_lines.append(cleaned_line)
                    port_depth = 1
                    i += 1
                    while i < len(lines) and port_depth > 0:
                        if '(' in lines[i]:
                            port_depth += lines[i].count('(')
                        if ')' in lines[i]:
                            port_depth -= lines[i].count(')')
                        if port_depth == 0:
                            break
                        i += 1
                    continue
```
**Explanation:**
- Check if line has opening parenthesis (potential instance)
- Exclude non-instance constructs
- Match module instance pattern
- Create cleaned line with empty ports
- Skip multi-line port connections using depth tracking

```python
        cleaned_lines.append(line)
        i += 1
```
**Explanation:**
- Keep line if it passed all filters
- Move to next line

```python
    # Ensure endmodule exists
    while cleaned_lines and cleaned_lines[-1].strip() == '':
        cleaned_lines.pop()
    
    module_positions = []
    for idx, line in enumerate(cleaned_lines):
        if re.search(r'\bmodule\b', line, re.IGNORECASE) and not re.search(r'\bendmodule\b', line, re.IGNORECASE):
            module_positions.append(idx)
```
**Explanation:**
- Remove trailing empty lines
- List to store module positions
- Find all module declarations (without endmodule)

```python
    for mod_idx in reversed(module_positions):
        next_mod_idx = len(cleaned_lines)
        for idx in range(mod_idx + 1, len(cleaned_lines)):
            if re.search(r'\bmodule\b', cleaned_lines[idx], re.IGNORECASE):
                next_mod_idx = idx
                break
        
        has_endmodule = False
        for idx in range(mod_idx + 1, next_mod_idx):
            if re.search(r'\bendmodule\b', cleaned_lines[idx], re.IGNORECASE):
                has_endmodule = True
                break
        
        if not has_endmodule:
            cleaned_lines.insert(next_mod_idx, "endmodule\n")
```
**Explanation:**
- Process modules in reverse (to avoid index shifting)
- Find next module or end of file
- Check if endmodule exists between modules
- Insert endmodule if missing

```python
    new_filename = filename.replace('.sv', '_cleaned.sv')
    with open(new_filename, 'w') as f:
        f.writelines(cleaned_lines)

    print(f"Cleaned file saved as: {new_filename}")
    return new_filename
```
**Explanation:**
- Generate output filename
- Write all cleaned lines to file
- Print message and return filename

### Section 6: Main Execution Block

```python
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = r"C:\Users\shubham\Desktop\python__01\regEx\verilog_test\and_gate_test.sv"
    
    clean_sv_testbench(filename)
```
**Explanation:**
- Check if script is run directly (not imported)
- Import sys for command-line arguments
- Check if filename provided as argument
- Use provided filename
- Use default filename if no argument
- Call main cleaning function

## 🎓 Key Programming Concepts Used

1. **Visitor Pattern**: ASTCleaner class implements visitor pattern for tree traversal
2. **Reflection**: Using `getattr()` and `hasattr()` for dynamic method dispatch
3. **Exception Handling**: Try-except blocks for graceful error handling
4. **State Machines**: Regex fallback uses state flags for tracking nested structures
5. **Regular Expressions**: Pattern matching for text-based cleaning
6. **File I/O**: Reading and writing Verilog files
7. **String Manipulation**: Pattern replacement and text processing

