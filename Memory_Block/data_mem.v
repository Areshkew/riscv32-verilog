module data_mem(
    input clk,
    input [31:0] address, // Address
    input [31:0] dwdata, // Data Write
    input [3:0] we, // Write Enable
    output [31:0] drdata // Data Read
);
    reg [7:0] mem[0:1024];
    wire [31:0] byte0, byte1, byte2, byte3;

    initial $readmemh("data_memory.mem", mem);

    assign byte0 = (address & 32'hfffffffc)+ 32'h00000000;
    assign byte1 = (address & 32'hfffffffc)+ 32'h00000001;
    assign byte2 = (address & 32'hfffffffc)+ 32'h00000002;
    assign byte3 = (address & 32'hfffffffc)+ 32'h00000003;

    // Little Endian Reading
    assign drdata = {mem[byte3], mem[byte2], mem[byte1], mem[byte0]};

    // Little Endian Writing
    always @(posedge clk) begin
        if(we[0] == 1)
            mem[byte0] = dwdata[7:0];
        if(we[1] == 1)
            mem[byte1] = dwdata[15:8];
        if(we[2] == 1)
            mem[byte2] = dwdata[23:16];
        if(we[3] == 1)
            mem[byte3] = dwdata[31:24];
        
        $writememh("data_memory.mem", mem);
    end
endmodule