module I_Type(
    input srli_e,
    input signed [31:0] imm, 
    input signed [31:0] rdata1, 
    input [2:0] func3,
    output reg [31:0] out
);
    wire [31:0] tempA; // rdata1
    wire [11:0] tempB; // Immediate
    
    // Convert to unsigned
    assign tempA = rdata1;
    assign tempB = imm;

    always @(func3 or rdata1 or imm) begin
        case(func3)
            3'b000: out = rdata1 + imm ; //addi
            3'b001: out = rdata1 << imm[4:0]; // slli
            3'b010: out = rdata1 < imm; // slti
            3'b011: out = tempA < tempB; // sltiu
            3'b100: out = rdata1 ^ imm; // xori
            3'b101: 
                begin
                    if(srli_e)
                        out = rdata1 >> imm[4:0]; // srli 
                    else
                        out = rdata1 >>> imm[4:0]; // srai
                end
            3'b110: out = rdata1 | imm;
            3'b111: out = rdata1 & imm;

        endcase
    end

endmodule