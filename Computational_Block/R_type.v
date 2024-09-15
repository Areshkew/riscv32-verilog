module R_Type(
    input [2:0] func3,
    input [6:0] func7,
    input signed [31:0] operator1,
    input signed [31:0] operator2,
    output reg[31:0] out
);
    wire [31:0] tempA;
    wire [31:0] tempB;
    assign tempA = operator1;
    assign tempB = operator2;

    always @(func3 or func7 or operator1 or operator2) 
    begin
    	case(func3)
            3'b000:   
                begin 
                    case(func7)
                        7'b0000000: out = operator1+operator2; // add
                        7'b0000001: out = operator1*operator2; // mul
                        7'b0100000: out = operator1-operator2; // sub
                    endcase
                end

            3'b001:    out = operator1<<operator2[4:0];	    // sll
            3'b010:    out = operator1<operator2;           // slt
            3'b011:    out = tempA<tempB;                     // sltu
            3'b100:
                begin 
                    case(func7)
                        7'b0000000: out = operator1^operator2;  // xor
                        7'b0000001: out = operator1/operator2; //  div
                    endcase
                end
                    
            3'b101:   
                begin
                    if(func7 != 7'b0100000)
                        out = operator1>>operator2[4:0];  // srl 
                    else
                       out = operator1>>>operator2[4:0]; // sra
                end

            3'b110:
                begin 
                    case(func7)
                        7'b0000000: out = operator1|operator2; // or
                        7'b0000001: out = operator1%operator2; // rem
                    endcase
                end
                    
            3'b111:    out = operator1&operator2;       //and
        endcase
    end

endmodule

