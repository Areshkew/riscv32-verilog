module S_Type(
    input [2:0] func3,
    input [31:0] address,
    output reg [3:0] we_out
);

    always @(func3 or address) begin
        case(func3)
            3'b000: we_out = (4'b0001 << address[1:0]);
            3'b001: we_out = (4'b0011 << address[1:0]);
            3'b010: we_out = 4'b1111;
        endcase
    end

endmodule