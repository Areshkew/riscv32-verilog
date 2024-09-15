module I2_Type(
    input [2:0] func3,
    input [31:0] address,
    input [31:0] drdata,
    output reg[31:0] out
);
    reg [31:0] offset;
    always@(func3 or address or drdata)
    begin   
        offset = (address[1:0]<<3);
        case(func3)
        3'b000: out = {{24{drdata[offset+7]}}, drdata[offset +: 8]};    //LB
        3'b001: out = {{16{drdata[offset+15]}}, drdata[offset +: 16]};  //LH
        3'b010: out = drdata;                                   			//LW
        3'b100: out = {24'b0, drdata[offset +: 8]};             			//LBU
        3'b101: out = {16'b0, drdata[offset +: 16]};            			//LHU
        endcase
    end

endmodule