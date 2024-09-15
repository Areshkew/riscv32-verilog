`include "CtrlUnit.v"
`timescale 1ns / 1ps

module CTRL_UNIT_TB();
    reg clk, reset;
    wire [31:0] PC;
    wire [31:0] nextPC;
    wire isDone;

    CTRL_UNIT riscv(clk, reset, PC, nextPC, isDone);
	 
    initial begin
        clk=0;
        repeat(50000) #5 clk = ~clk;
    end 

    initial begin
        $dumpfile("CtrlUnit_tb.vcd");
        $dumpvars(0, CTRL_UNIT_TB);

        clk = 0;
        reset = 1;
        #10;
        reset = 0;
    end

    always @(isDone) begin
        if (isDone == 1'b1) begin
            $display("The execution has finished.");
            $finish;
        end
    end
endmodule