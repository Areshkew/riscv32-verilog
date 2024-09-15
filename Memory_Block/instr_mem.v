module instr_mem(
    input [31:0] iaddr,
    output [31:0] idata
);
    reg [31:0] inst_arr[0:1024];
    initial begin
		$readmemh("instruction_memory.mem", inst_arr);
	 end
    assign idata = inst_arr[iaddr[31:2]];
endmodule