import argparse
import subprocess
import sys

def execute_commands(commands_with_args, specific_commands=None):
    for tag, command in commands_with_args.items():
        if specific_commands and tag not in specific_commands:
            continue
        try:
            if "&" in command:
                command.remove("&")
                print(f"Executing in background: {' '.join(command)}")
                subprocess.Popen(command)
            else:
                print(f"Executing: {' '.join(command)}")
                completed_process = subprocess.run(command, check=True, text=True, capture_output=True)
                print("Output:", completed_process.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error in executing {' '.join(command)}", file=sys.stderr)
            print("Error Details:", e.stderr, file=sys.stderr)
        except Exception as e:
            print(f"Unexpected error occurred while executing {' '.join(command)}: {e}", file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RiscV multigen tool")
    parser.add_argument('-kalc', action='store_true', help='Execute kaleidoscope compiler')
    parser.add_argument('-asm', action='store_true', help='Execute assembly to binaries compiler')
    parser.add_argument('-verilog', action='store_true', help='Execute iverilog, vvp and gtkwave')
    parser.add_argument('-visualizer', action='store_true', help='Execute visualizer, it reads output mem from CPU')
    parser.add_argument('-allnogtk', action='store_true', help='Execute all commands except gtkwave')
    parser.add_argument('-all', action='store_true', help='Execute all commands')
    
    args = parser.parse_args()
    
    commands_with_args = {
        'kalc': ['kalc', 'program.kl', 'assembly_code.asm'],
        'compiler': ['python3', 'Compiler.py'],
        'iverilog': ['iverilog', '-o', 'CtrlUnit.vvp', 'CtrlUnit_tb.v'],
        'vvp': ['vvp', 'CtrlUnit.vvp'],
        'visualizer': ['python3', 'Visualizer.py', '&'],
        'gtkwave': ['gtkwave', 'CtrlUnit_tb.vcd']
    }
    
    if args.kalc:
        execute_commands(commands_with_args, specific_commands=['kalc'])
    elif args.verilog:
        execute_commands(commands_with_args, specific_commands=['iverilog', 'vvp', 'gtkwave'])
    elif args.asm:
        execute_commands(commands_with_args, specific_commands=['compiler'])
    elif args.visualizer:
        execute_commands(commands_with_args, specific_commands=['visualizer'])
    elif args.allnogtk:
        execute_commands(commands_with_args, specific_commands=['kalc', 'compiler', 'iverilog', 'vvp', 'visualizer'])
    elif args.all:
        execute_commands(commands_with_args)
    else:
        print("No arguments provided, doing nothing.\nUse -h, --help.")
