`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/06/02 10:45:41
// Design Name: 
// Module Name: tb_test
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module tb_test(

    );
reg clk,rstn;    
test  test(
clk,
rstn
);  
always #5 clk=~clk;
initial
begin
clk=0;
rstn=0;
#10;
rstn=1;
end
reg [31:0]count;
always@(posedge clk or negedge rstn)
 if(~rstn)
   count<=0;
 else 
   count<=count+1;

reg Pass_0; 
always@(posedge clk or negedge rstn)
 if(~rstn)
   Pass_0<=0;
 else if(count>=2)  
  begin
   if(tb_test.test.P1110==mem[0])
    Pass_0<=1;
   else
    Pass_0<=0;
  end  

reg Pass_1;    
always@(posedge clk or negedge rstn)
 if(~rstn)
   Pass_1<=0;
 else if(count>=2)  
  begin
   if((tb_test.test.P1120==mem[1])&&(Pass_0))
    Pass_1<=1;
   else
    Pass_1<=0;
  end  
   
always@(posedge clk)
if(Pass_0&&Pass_1)
begin
$display("PASS");
$finish;
end   
   
endmodule
