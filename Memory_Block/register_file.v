module register_file(
    input clk,

    // Instruction set input (Read)
    input [4:0] rs1, 
    input [4:0] rs2,
    input [4:0] rd,

    input [31:0] regdata,
    input wer,

    // Output (register values)
    output [31:0] rv1, 
    output [31:0] rv2
);
    reg [31:0] r[0:31]; // 32 Reg 32 bits

    integer i;
    initial begin
        for(i=0; i<=31; i = i+1)
            r[i]=0;
    end

    assign rv1 = r[rs1];
    assign rv2 = r[rs2];

    always @(posedge clk) 
    begin
        if(wer && rd!=0)
            r[rd] = regdata;
        $writememh("dump_registers.mem", r);
    end
endmodule