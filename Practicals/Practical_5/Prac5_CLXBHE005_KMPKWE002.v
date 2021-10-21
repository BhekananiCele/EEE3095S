/* ALU Arithmetic and Logic Operations
----------------------------------------------------------------------
|ALU_Sel|   ALU Operation 
----------------------------------------------------------------------
| 0000  |   ALU_Out = A + B; 
----------------------------------------------------------------------
| 0001  |   ALU_Out = A - B; 
----------------------------------------------------------------------
| 0010  |   ALU_Out = A * B; 
----------------------------------------------------------------------
| 0011  |   ALU_Out = A / B; 
----------------------------------------------------------------------
| 0100  |   ALU_Out = ALU_Out + A 
----------------------------------------------------------------------
| 0101  |   ALU_Out = ALU_Out * A; 
----------------------------------------------------------------------
| 0110  |   ALU_Out = ALU_Out + (A * B); 
----------------------------------------------------------------------
| 0111  |   ALU_Out = A rotated left by 1; 
----------------------------------------------------------------------
| 1000  |   ALU_Out = A rotated right by 1; 
----------------------------------------------------------------------
| 1001  |   ALU_Out = A and B; 
----------------------------------------------------------------------
| 1010  |   ALU_Out = A or B; 
----------------------------------------------------------------------
| 1011  |   ALU_Out = A xor B; 
----------------------------------------------------------------------
| 1100  |   ALU_Out = A nand B; 
----------------------------------------------------------------------
| 1101  |   ALU_Out = 0xFF if A=B else 0; 
----------------------------------------------------------------------
| 1110  |   ALU_Out = 0xFF if A>B else 0; 
----------------------------------------------------------------------
| 1111  |   ALU_Out = 0xFF if A<B else 0; 
----------------------------------------------------------------------*/
// Verilog project: Verilog code for ALU
// by CLXBHE005_KMPKWE002
module alu(
  			 input clk,
             input [7:0] A,B,  // ALU 8-bit Inputs             
             input [3:0] ALU_Sel,// ALU Selection
             output [7:0] ALU_Out // ALU 8-bit Output
    );
  	reg [7:0] ALU_Result; //Accumulator
    assign ALU_Out = ALU_Result; // ALU out
  	always @(posedge clk or negedge clk)
    begin
		case(ALU_Sel)
        	4'b0000: // Addition
           		ALU_Result = A + B ; 
        	4'b0001: // Subtraction
           		ALU_Result = A - B ;
        	4'b0010: // Multiplication
           		ALU_Result = A * B;
        	4'b0011: // Division
        		ALU_Result = A/B;
          	4'b0100: // Addition (ADDA)
           		ALU_Result = ALU_Result + A;
          	4'b0101: // Multiplication (MULA)
           		ALU_Result = ALU_Result * A;
         	4'b0110: // Multiplication/Addition (MAC)
              ALU_Result = ALU_Result + ( A * B);
         	4'b0111: // Rotate left
           		ALU_Result = {A[6:0],A[7]};
         	4'b1000: // Rotate right
             	ALU_Result = {A[0],A[7:1]};
            4'b1001: //  Logical and 
             	ALU_Result = A & B;
            4'b1010: //  Logical or
             	ALU_Result = A | B;
            4'b1011: //  Logical xor 
             	ALU_Result = A ^ B;
            4'b1100: // Logical nand 
             	ALU_Result = ~(A & B);
           	4'b1101: // Equal comparison   
              ALU_Result = (A==B)?8'hFF:8'd0 ;
            4'b1110: // Greater comparison
              ALU_Result = (A>B)?8'hFF:8'd0 ;
            4'b1111: // Less comparison   
              ALU_Result = (A<B)?8'hFF:8'd0 ;
          	default: ALU_Result = A + B ; 
        endcase
    end
endmodule