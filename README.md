# RISC-V Instruction Set (Monocycle Processor - 32 bits)

This project includes a RISC-V instruction set implemented in Verilog, along with tools to compile, simulate, and visualize the execution of RISC-V instructions. It also features an educational compiler that generates RISC-V assembly code from a custom language (Kaleidoscope), a RISC-V assembly to binary/hex converter, and a Python-based control script to manage the whole process.

## Features

- **Kaleidoscope Compiler:** Converts high-level Kaleidoscope programs into RISC-V assembly.
- **Assembly to Binary/Hex Converter:** Translates RISC-V assembly code into binary or hexadecimal format.
- **Verilog Processor Simulation:** A monocycle RISC-V processor implemented in Verilog.
- **Waveform Visualization:** Allows waveform visualization of the processor using GTKWave.
- **Python Control Script:** A Python script to automate the execution of various tasks like compiling, simulating, and visualizing.

## Requirements

To run this project, you will need the following tools and libraries installed:

### Tools
- **iverilog**: For Verilog compilation and simulation.
- **vvp**: To run the compiled Verilog simulation.
- **gtkwave**: To visualize the waveform output of the simulation.
- **Python 3.x**: To run the control script and other Python-based tools.
- **Kaleidoscope Compiler**: For generating RISC-V assembly from Kaleidoscope programs.

### Python Packages
- `argparse`: For command-line argument parsing.
- `subprocess`: To run system commands.

You can install the required Python packages by running:
```bash
pip install -r requirements.txt
```

`requirements.txt`:
```
argparse
```

## Usage

The Python control script (`riscv_multigen.py`) simplifies running various tasks related to compiling and simulating the RISC-V processor. Below are the available command-line options:

### Command-line Options

- `-kalc`: Execute the Kaleidoscope compiler to generate RISC-V assembly.
- `-asm`: Execute the RISC-V assembly to binary/hex compiler.
- `-verilog`: Compile and simulate the Verilog RISC-V processor and open GTKWave for waveform visualization.
- `-visualizer`: Run the visualizer which reads the output memory from the CPU.
- `-allnogtk`: Execute all commands except GTKWave.
- `-all`: Execute all commands (Kaleidoscope compiler, assembly to binary compiler, Verilog simulation, waveform visualization).

### Examples

- **Run Kaleidoscope Compiler:**
  ```bash
  python3 Run.py -kalc
  ```

- **Convert Assembly to Binary:**
  ```bash
  python3 Run.py -asm
  ```

- **Simulate Verilog Processor:**
  ```bash
  python3 Run.py -verilog
  ```

- **Run All Commands:**
  ```bash
  python3 Run.py -all
  ```

## Repository

- [Kaleidoscope Compiler](https://github.com/Areshkew/kaleidoscope-riscv)
- [Tiny RISC-V Compiler](https://github.com/Areshkew/tiny-risc-v)

## Project Structure

- **CtrlUnit.v**: Verilog file containing the RISC-V monocycle processor implementation.
- **CtrlUnit_tb.v**: Verilog testbench for the processor.
- **riscv_multigen.py**: Python script to automate the compilation and simulation process.
- **Visualizer.py**: Python script to visualize the CPU's memory output.
- **Compiler.py**: Python script to convert RISC-V assembly to binary or hex format.

## License

This project is licensed under the MIT License.