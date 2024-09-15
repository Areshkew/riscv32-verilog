module B_type(
    input signed [31:0] rv1,
    input signed [31:0] rv2,
    input [2:0] func3,
    output reg result
);
    wire [31:0] tempA; // rv1
    wire [31:0] tempB; // rv2
    
    // Convert to unsigned
    assign tempA = rv1;
    assign tempB = rv2;

    always @(func3 or rv1 or rv2) begin
        case(func3)
            3'b000: result = (rv1 == rv2);
            3'b001: result = (rv1 != rv2);
            3'b100: result = (rv1 < rv2);
            3'b101: result = (rv1 >= rv2);
            3'b110: result = (tempA < tempB);
            3'b111: result = (tempA >= tempB);
        endcase
    end

endmodule