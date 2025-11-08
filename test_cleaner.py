"""
Verilog Testbench Cleaner using Pyverilog AST Parser
Clears testbench files for next test by removing test-specific code
Uses AST-level manipulation for robust parsing and modification
"""

import sys
import os
import warnings
from io import StringIO

# Suppress pyverilog parser generation warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*shift/reduce.*', category=UserWarning)

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


class ASTCleaner:
    """
    AST visitor to clean Verilog testbench code
    """
    def __init__(self):
        self.cleaned_items = []
    
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
    
    def visit_Description(self, node):
        """Clean description (top-level container)"""
        cleaned_definitions = []
        for item in node.definitions:
            cleaned = self.visit(item)
            if cleaned is not None:
                cleaned_definitions.append(cleaned)
        node.definitions = cleaned_definitions
        return node
    
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
    
    def visit_Initial(self, node):
        """Remove initial blocks"""
        return None
    
    def visit_SystemCall(self, node):
        """Remove system tasks like $monitor, $dumpfile, etc."""
        if hasattr(node, 'syscall'):
            syscall_name = str(node.syscall).lower()
            if any(x in syscall_name for x in ['monitor', 'dumpfile', 'dumpvars', 'finish']):
                return None
        return node
    
    def visit_Parameter(self, node):
        """Remove parameter declarations"""
        return None
    
    def visit_Localparam(self, node):
        """Remove localparam declarations"""
        return None
    
    def visit_Decl(self, node):
        """Handle declarations - remove variable declarations"""
        if hasattr(node, 'list'):
            # Check if it's a variable declaration (reg, wire, etc.)
            for decl_item in node.list:
                if hasattr(decl_item, 'name'):
                    # This is a variable declaration, remove it
                    return None
        return node
    
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
    
    def visit_Instance(self, node):
        """Clean instance - clear port connections"""
        if hasattr(node, 'portlist'):
            node.portlist = None
        if hasattr(node, 'portlist_opt'):
            node.portlist_opt = None
        return node


def clean_sv_testbench(filename):
    """
    Clears a Verilog testbench file for next test using AST-level manipulation:
    - Removing all initial begin...end blocks (test stimulus)
    - Removing $monitor, $dumpfile, $dumpvars, $finish statements
    - Removing parameter, localparam declarations
    - Removing all variable declarations (reg, wire, integer, etc.) in testbench module
    - Clearing DUT instance parameters/ports (making them empty)
    - Preserving module structure and endmodule
    - Works for any test file format
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


def clean_with_ast(filename):
    """Clean using AST parser"""
    # Read file content first
    with open(filename, 'r') as f:
        code = f.read()
    
    # Convert to absolute path for pyverilog (needed for include resolution)
    abs_filename = os.path.abspath(filename)
    filelist = [abs_filename]
    
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
    
    # Clean the AST
    cleaner = ASTCleaner()
    cleaned_ast = cleaner.visit(ast)
    
    # Generate code from cleaned AST
    codegen = ASTCodeGenerator()
    cleaned_code = codegen.visit(cleaned_ast)
    
    # Remove comments (AST parser may preserve some)
    import re
    cleaned_code = re.sub(r'//.*$', '', cleaned_code, flags=re.MULTILINE)
    cleaned_code = re.sub(r'/\*.*?\*/', '', cleaned_code, flags=re.DOTALL)
    
    # Remove `define directives
    cleaned_code = re.sub(r'^\s*`define\s+.*$', '', cleaned_code, flags=re.MULTILINE | re.IGNORECASE)
    
    # Clean up stray closing parentheses, semicolons before endmodule
    lines = cleaned_code.splitlines(keepends=True)
    cleaned_lines_filtered = []
    for line in lines:
        stripped = line.strip()
        # Skip lines that are just closing parentheses, semicolons, or combinations
        if re.match(r'^[);\s]*$', stripped):
            continue
        # Skip lines that are just standalone closing parentheses with semicolon
        if stripped in [');', ')', ';']:
            continue
        cleaned_lines_filtered.append(line)
    
    cleaned_code = ''.join(cleaned_lines_filtered)
    
    # Remove trailing empty lines
    cleaned_code = cleaned_code.rstrip() + '\n'
    
    # Save result
    new_filename = filename.replace('.sv', '_cleaned.sv')
    with open(new_filename, 'w') as f:
        f.write(cleaned_code)
    
    print(f"Cleaned file saved as: {new_filename}")
    return new_filename


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

    lines = content.splitlines(keepends=True)
    cleaned_lines = []
    inside_initial = False
    brace_depth = 0
    inside_parameter = False
    inside_define = False

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

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

        # Remove initial blocks
        if re.match(r'^\s*initial\s+begin', stripped, re.IGNORECASE):
            inside_initial = True
            brace_depth = 1
            i += 1
            continue
        elif re.match(r'^\s*initial\s+', stripped, re.IGNORECASE):
            i += 1
            continue

        # Remove system tasks
        if re.search(r'\$monitor|\$dumpfile|\$dumpvars|\$finish', stripped, re.IGNORECASE):
            i += 1
            continue

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

        # Remove comments
        line = re.sub(r'//.*$', '', line)
        line_stripped = line.strip()
        if line_stripped == '':
            i += 1
            continue

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

        cleaned_lines.append(line)
        i += 1

    # Clean up stray closing parentheses, semicolons, and test code before endmodule
    # Remove lines that are just closing parentheses, semicolons, or whitespace
    cleaned_lines_filtered = []
    for idx, line in enumerate(cleaned_lines):
        stripped = line.strip()
        # Skip lines that are just closing parentheses, semicolons, or combinations
        if re.match(r'^[);\s]*$', stripped):
            continue
        # Skip lines that are just standalone closing parentheses with semicolon
        if stripped in [');', ')', ';']:
            continue
        cleaned_lines_filtered.append(line)
    
    cleaned_lines = cleaned_lines_filtered

    # Ensure endmodule exists
    while cleaned_lines and cleaned_lines[-1].strip() == '':
        cleaned_lines.pop()
    
    module_positions = []
    for idx, line in enumerate(cleaned_lines):
        if re.search(r'\bmodule\b', line, re.IGNORECASE) and not re.search(r'\bendmodule\b', line, re.IGNORECASE):
            module_positions.append(idx)
    
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

    new_filename = filename.replace('.sv', '_cleaned.sv')
    with open(new_filename, 'w') as f:
        f.writelines(cleaned_lines)

    print(f"Cleaned file saved as: {new_filename}")
    return new_filename


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = r"C:\Users\shubham\Desktop\python__01\regEx\verilog_test\and_gate_test.sv"
    
    clean_sv_testbench(filename)
