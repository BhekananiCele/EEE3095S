// Verilog project: Verilog code for ALU
// by CLXBHE005_KMPKWE002


module tb_alu();
  //Inputs
   reg clk;
   reg[7:0] A,B;
   reg[3:0] ALU_Sel;

  //Outputs
   wire[7:0] ALU_Out;

   // Verilog code for ALU
   integer i;
   alu test_unit(
          .clk(clk),
          .A(A),
          .B(B),
          .ALU_Sel(ALU_Sel),
          .ALU_Out(ALU_Out)
       );
  
	initial begin
        $dumpfile("dump.vcd");
        $dumpvars;
      	$display("A         B         ALU_Sel  ALU_Out");
        $monitor("%b  %b  %b     %b",A,B,ALU_Sel, ALU_Out);

        clk = 1'b1;
        A = 8'h03;
        B = 8'h02;

        clk=!clk;
        ALU_Sel = 4'h0;
   		clk=!clk;
       	#10;
        for (i=1;i<=15;i=i+1)
          begin
            clk=!clk;
            ALU_Sel = ALU_Sel + 4'h01;
            #10;
          end;
      end
endmodule