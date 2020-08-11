module tb_test_layer4(

);
reg clk,rstn;
test_layer4 test_layer4(
clk,
rstn
);
reg mem[14*14*4-1:0];
always #5 clk=~clk;
initial
begin
clk=0;
rstn=0;
$readmemb("D:/work/PROJ_5/proj_2/src/to_csma/test_tb/answer_layer_4.txt",mem);
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
			if(tb_test_layer4.test_layer4.P5000==mem[0])
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
			if((tb_test_layer4.test_layer4.P5001==mem[1])&&(Pass_0))
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
