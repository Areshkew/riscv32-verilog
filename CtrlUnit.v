`include "Memory_Block/register_file.v"
`include "Memory_Block/instr_mem.v"
`include "Memory_Block/data_mem.v"

`include "Computational_Block/R_type.v"
`include "Computational_Block/I_type.v"
`include "Computational_Block/I2_type.v"
`include "Computational_Block/S_type.v"
`include "Computational_Block/B_type.v"

module CTRL_UNIT (
    input clk,
    input reset,

	output reg [31:0] PC,  // Stores current Program counter value
	output reg [31:0] nextPC,    // Stores the value that is to be assigned in the next clk cycle to Program counter
    output reg isDone
);
    // 
    reg [3:0] we; // Write enable signal for each byte of 32-b word.
	reg we_reg;   // Write enable for register file.
    reg [4:0] rd,rs1,rs2; // Input reg
    wire [31:0] instr32;   // data from instruction memory
    wire [31:0] rv1, rv2; // Register values
    reg [31:0] regdata; 

    // Data Memory 
    reg [31:0] daddr;  // Address to acess memory
    wire [31:0] drdata;  // Data readed from Memmory
    reg [31:0] dwdata; // Data to be written in memory

    // CPU Clock Signal
    always@(posedge clk)
    begin
        if(reset) 
            PC = 0; // Reset program counter PC
        else
            PC = nextPC; // Assign next cycle PC value to current PC
    end 

    //
    wire [31:0] R_type_result;
    reg [2:0] func3;
    reg [6:0] func7;

    wire [31:0] I_type_result;
    reg signed [31:0] imm;

    wire [3:0] we_S_result;

    wire [31:0] I2_type_result;

    // Instances
    instr_mem im1(PC, instr32);
    data_mem dm1(clk, daddr, dwdata, we, drdata);
    register_file reg1(clk, rs1, rs2, rd, regdata, we_reg, rv1, rv2);

    // 
    always @(*) begin
        case (instr32[6:0])
            7'b0000000:
                begin
                    isDone = 1;
                end

            7'b0000011: // TIPO I (Load operations)
                begin
                    func3 = instr32[14:12];
                    rd = instr32[11:7];
                    rs1 = instr32[19:15]; 
                    imm = {{20{instr32[31]}},instr32[31:20]};
                    we_reg = 1;
                    we = 4'b0;
                    daddr = rv1+imm;    
                    regdata = I2_type_result;
                    nextPC = PC+4;
                end 

            7'b0010011: // TIPO I (Immediate Operations)
                begin
                    imm = { {20{instr32[31]}}, instr32[31:20] }; // Convert to 32 bits, repeat 20 bits with sign if exists. This is for negative numbers
                    rs1 = instr32[19:15];
                    func3 = instr32[14:12];
                    rd = instr32[11:7];
                    we_reg = 1;
                    we = 4'b0;
                    regdata = I_type_result;
                    nextPC = PC+4;
                end

            7'b0010111: // TIPO U (add upper immediate to PC) 
                begin
					rd = instr32[11:7];
					imm = {instr32[31:12], 12'b0};
					we_reg = 1;
					we = 4'b0;
					regdata = PC + imm;
					nextPC = PC + 4;
				end

            7'b0100011: // TIPO S (Store)
                begin
                    imm = { {20{instr32[31]}}, instr32[31:25], instr32[11:7] };
                    rs1 = instr32[19:15];
                    rs2 = instr32[24:20];
                    func3 = instr32[14:12];
                    daddr = rv1 + imm;
                    
                    case(func3)
                        3'b000: dwdata = {rv2[7:0], rv2[7:0], rv2[7:0], rv2[7:0]};
                        3'b001: dwdata = {rv2[15:0], rv2[15:0]};
                        3'b010: dwdata = rv2[31:0];
                    endcase

                    we = we_S_result;
                    nextPC = PC+4;
                end

            7'b0110011: // TIPO R (Arithmetic Operations)
                begin
                    rd = instr32[11:7];
                    rs1 = instr32[19:15];
                    rs2 = instr32[24:20];
                    func3 = instr32[14:12];
                    func7 =  instr32[31:25];
                    we_reg = 1;
                    we = 4'b0;
                    regdata = R_type_result;
                    nextPC = PC+4; 
                end

            7'b0110111: // TIPO U (load upper immediate)
                begin
					rd = instr32[11:7];
					imm = {instr32[31:12], 12'b0};
					we_reg = 1;
					we = 4'b0;
					regdata = imm;
					nextPC = PC+4;
				end

            7'b1100011: // TIPO B (Branch if)
                begin
                    rs1 = instr32[19:15];
                    rs2 = instr32[24:20];
                    func3 = instr32[14:12];
                    imm = {{19{instr32[31]}}, instr32[31], instr32[7], instr32[30:25], instr32[11:8], 1'b0};
                    
                    we_reg = 0;
                    we = 4'b0;
                    
                    if(B_type_result)
                        nextPC = (PC + imm);
                    else
                        nextPC = (PC + 4);

                end

            7'b1100111: // TIPO I (jump and link register)
                begin
                    rs1 = instr32[19:15];
					rd = instr32[11:7];
					imm = {{20{instr32[31]}}, instr32[31:20]};
					we_reg = 1;
					we = 4'b0;
					regdata = PC + 4;
					nextPC = (rv1+imm) & 32'hfffffffe; 
                end

            7'b1101111: // TIPO J (jump and link)
                begin
                    rd = instr32[11:7];
					imm = {{11{instr32[31]}}, instr32[31], instr32[19:12], instr32[20], instr32[30:21], 1'b0};
					we_reg = 1;
					we = 4'b0;
					regdata = PC + 4;
					nextPC = (PC+imm);
                end
        endcase
    end  

    R_Type alu1(func3, func7, rv1, rv2, R_type_result);
    I_Type immI(instr32[30], imm, rv1, func3, I_type_result);
    I2_Type loadOp(func3, daddr, drdata, I2_type_result);
    S_Type memStore(func3, daddr, we_S_result);
    B_type BrandL(rv1, rv2, func3, B_type_result);
endmodule