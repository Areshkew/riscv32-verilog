def determine_func3(instruction):
    type_i = ["lb", "lh", "lw", "lbu", "lhu"]
    type_i2 = ["addi", "slli", "slti", "sltiu", "xori", "srli", "srai", "ori","andi"]
    type_s = ["sb", "sh", "sw"]
    type_r = ["add", "sub", "sll", "slt", "sltu", "xor", "srl", "sra", "or", "and"]
    type_r2 = ["mul", "div", "rem"]
    type_b = ["beq", "bne", "blt", "bge", "bltu", "bgeu"]

    if instruction in type_i:
        index = type_i.index(instruction)
        if(index == 3 or index == 4):
            index += 1
        return format(index, '03b')
    
    elif instruction in type_i2:
        index = type_i2.index(instruction)
        if(index == 6 or index == 7 or index == 8):
            index -= 1
        return format(index, '03b')
    
    elif instruction in type_s:
        index = type_s.index(instruction)
        return format(index, '03b')
    
    elif instruction in type_r:
        index = type_r.index(instruction)
        if(index >= 1):
            index -= 1
        if(index >= 6):
            index -= 1
        return format(index, '03b')
    
    elif instruction in type_r2:
        index = type_r2.index(instruction)
        if(index == 0):
            index = 0
        if(index == 1):
            index = 4
        if(index == 2):
            index = 6
        return format(index, '03b')
    
    elif instruction in type_b:
        index = type_b.index(instruction)
        if(index >= 2):
            index += 2
        return format(index, '03b')
    
    elif instruction == "jalr":
        return format(0, '03b')

    else:
        return None

def determine_func7(instruction):
    types = ["slli", "srli", "add", "sll", "slt", "sltu", "xor", "srl", "or", "and"]

    if instruction in types:
        return "0000000"
    elif instruction in ["srai", "sub", "sra"]:
        return "0100000"
    elif instruction in ["mul", "div", "rem"]:
        return "0000001"
    else: 
        return None

def determine_instruction_binaries(instruction):
    func7 = determine_func7(instruction)
    func3 = determine_func3(instruction)

    # Determine the instruction type based on the instruction
    if instruction in ["lb", "lh", "lw", "lbu", "lhu"]:
        i_type = "I"
        i_bin = "0000011"

    elif instruction in ["addi", "slli", "slti", "sltiu", "xori", "srli", "srai", "ori","andi"]:
        i_type = "I2"
        i_bin = "0010011"

    elif instruction in ["auipc"]:
        i_type = "U"
        i_bin = "0010111"

    elif instruction in ["sb", "sh", "sw"]:
        i_type = "S"
        i_bin = "0100011"

    elif instruction in ["add", "sub", "sll", "slt", "sltu", "xor", "srl", "sra", "or", "and", "mul", "div", "rem"]:
        i_type = "R"
        i_bin = "0110011"

    elif instruction in ["lui"]:
        i_type = "U"
        i_bin = "0110111"

    elif instruction in ["beq", "bne", "blt", "bge", "bltu", "bgeu"]:
        i_type = "B"
        i_bin = "1100011"

    elif instruction in ["jalr"]:
        i_type = "I2"
        i_bin = "1100111"

    elif instruction in ["jal"]:
        i_type = "J"
        i_bin = "1101111"

    else:
        raise ValueError("Instrucción desconocida, verifica el programa!")
    
    result = {
        "type": i_type,
        "op": i_bin,
        "func3": func3,
        "func7": func7
    }

    return result

def register_to_binary(register):
    
    conventions = {
        "zero": 0,
        "ra": 1,
        "sp": 2,
        "gp": 3,
        "tp": 4,
        "t0": 5,
        "t1": 6,
        "t2": 7,
        "s0": 8,
        "fp": 8,
        "s1": 9,
        "a0": 10,
        "a1": 11,
        "a2": 12,
        "a3": 13,
        "a4": 14,
        "a5": 15,
        "a6": 16,
        "a7": 17,
        "s2": 18,
        "s3": 19,
        "s4": 20,
        "s5": 21,
        "s6": 22,
        "s7": 23,
        "s8": 24,
        "s9": 25,
        "s10": 26,
        "s11": 27,
        "t3": 28,
        "t4": 29,
        "t5": 30,
        "t6": 31
    }


    if register in conventions.keys():
        register_number = conventions[register]
    else:
        cleaned_register = register.replace('x', '').replace(',', '')
        register_number = int(cleaned_register)

    try:
        if register_number > 31:
            raise ValueError("Registro inválido")

        binary_representation = format(register_number, '05b')
        return binary_representation
    except ValueError:
        return "00000"

def twos_complement(binary_representation):
    # Invierte todos los bits
    inverted_bits = ''.join('1' if bit == '0' else '0' for bit in binary_representation)
    # Suma 1 al resultado
    return bin(int(inverted_bits, 2) + 1)[2:]

def component_to_binary(length, component, instruction):
    is_negative = component[0] == '-'
    register_number = int(component[1:]) if is_negative else int(component)

    if register_number > (2**length - 1):
        raise ValueError("Overflow, el número excedió la cantidad de bits esperada.")

    binary_representation = format(register_number, f'0{length}b')
    
    if is_negative and (instruction not in ['lbu', 'lhu', 'sltiu']):
        binary_representation = twos_complement(binary_representation)

    return binary_representation

def generate_instruction(i_binaries, i_components, labels, line):
    if i_binaries['type'] == "I":
        imm = component_to_binary(12, i_components[2], i_components[0])
        rs1 = register_to_binary(i_components[3])
        rd = register_to_binary(i_components[1])
        return f"{imm}{rs1}{i_binaries['func3']}{rd}{i_binaries['op']}"
    
    elif i_binaries['type'] == "I2":
        imm = component_to_binary(12, i_components[3], i_components[0])
        rs1 = register_to_binary(i_components[2])
        rd = register_to_binary(i_components[1])
        return f"{imm}{rs1}{i_binaries['func3']}{rd}{i_binaries['op']}"
    
    elif i_binaries['type'] == "U":
        imm = component_to_binary(20, i_components[2], i_components[0])
        rd = register_to_binary(i_components[1])
        return f"{imm}{rd}{i_binaries['op']}"
    
    elif i_binaries['type'] == "S":
        imm = component_to_binary(12, i_components[2], i_components[0])
        rs1 = register_to_binary(i_components[3])
        rs2 = register_to_binary(i_components[1])
        return f"{imm[0:7]}{rs2}{rs1}{i_binaries['func3']}{imm[7:12]}{i_binaries['op']}"
    
    elif i_binaries['type'] == "R":
        rd = register_to_binary(i_components[1])
        rs1 = register_to_binary(i_components[2])
        rs2 = register_to_binary(i_components[3])
        return f"{i_binaries['func7']}{rs2}{rs1}{i_binaries['func3']}{rd}{i_binaries['op']}"
    
    elif i_binaries['type'] == "B":
        label = i_components[3]
        imm_calc = labels[label] - line
        imm = component_to_binary(13, str(imm_calc), i_components[0])
        rs2 = register_to_binary(i_components[2])
        rs1 = register_to_binary(i_components[1])
        return f"{imm[0]}{imm[2:8]}{rs2}{rs1}{i_binaries['func3']}{imm[8:12]}{imm[1]}{i_binaries['op']}"

    elif i_binaries['type'] == "J":
         label = i_components[2]
         imm_calc = labels[label] - line
         imm = component_to_binary(21, str(imm_calc), i_components[0])
         rd = register_to_binary(i_components[1])
         return f"{imm[0]}{imm[10:20]}{imm[9]}{imm[1:9]}{rd}{i_binaries['op']}"