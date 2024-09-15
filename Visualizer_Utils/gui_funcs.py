# Función para convertir Hex a Binario
def hex_to_bin(hex_num):
    return bin(int(hex_num, 16))[2:].zfill(32)

# Funciones para cargar los archivos e ignorar comentarios
def load_file(file_name):
    with open(file_name, 'r') as f:
        return [line for line in f.readlines() if not line.strip().startswith("//")]
    
# Cargar los archivos al inicio
def load_all_files():
    instruction_memory = load_file('instruction_memory.mem')
    assembly_code = load_file('assembly_code.asm')
    data_memory = load_file('data_memory.mem')
    dump_registers = load_file('dump_registers.mem')
    return instruction_memory, assembly_code, data_memory, dump_registers