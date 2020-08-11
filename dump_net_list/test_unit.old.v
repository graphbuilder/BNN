module test(
clk,
rstn
);
input clk;
input rstn;
//laye 0
wire P0000,P0010,P0020,P0100,P0110,P0120,P0200,P0210,P0220;// 0:layer id , 1:x, 2:y, 3:c
wire P0001,P0011,P0021,P0101,P0111,P0121,P0201,P0211,P0221;
wire P0002,P0012,P0022,P0102,P0112,P0122,P0202,P0212,P0222;
//layer1
wire P1000;

wire W00000,W00010,W00020,W00100,W00110,W00120,W00200,W00210,W00220;
wire W00001,W00011,W00021,W00101,W00111,W00121,W00201,W00211,W00221;
wire W00002,W00012,W00022,W00102,W00112,W00122,W00202,W00212,W00222;
//0:layer id 1:weight kernal 2:x  3:y  4:c
wire [3:0]c00000,c01000,c02000;//0:layer id 1:input seg number 2:x  3:y  4:c
wire [5:0]C0000,C0010,C0100,C0110;//0:layer id 1:x 2:y 3:c //6bit
wire A0000,A0010,A0100,A0110;// 0:layer id 1:x 2:y 3:c


DFF_save_fm DFF0(.clk(clk),.rstn(rstn),.reset_value(),.q(P0000));
DFF_save_fm DFF1(.clk(clk),.rstn(rstn),.reset_value(),.q(P0010));
DFF_save_fm DFF2(.clk(clk),.rstn(rstn),.reset_value(),.q(P0020));
DFF_save_fm DFF3(.clk(clk),.rstn(rstn),.reset_value(),.q(P0100));
DFF_save_fm DFF4(.clk(clk),.rstn(rstn),.reset_value(),.q(P0110));
DFF_save_fm DFF5(.clk(clk),.rstn(rstn),.reset_value(),.q(P0120));
DFF_save_fm DFF6(.clk(clk),.rstn(rstn),.reset_value(),.q(P0200));
DFF_save_fm DFF7(.clk(clk),.rstn(rstn),.reset_value(),.q(P0210));
DFF_save_fm DFF8(.clk(clk),.rstn(rstn),.reset_value(),.q(P0220));
...

ninexnine_unit ninexnine_unit_0(
				.a0(P0000),	
				.a1(P0010),
				.a2(P0020),
				.a3(P0100),
				.a4(P0110),
				.a5(P0120),
				.a6(P0200),
				.a7(P0210),
				.a8(P0220),
				.b0(W00000),
				.b1(W00010),
				.b2(W00020),
				.b3(W00100),
				.b4(W00110),
				.b5(W00120),
				.b6(W00200),
				.b7(W00210),
				.b8(W00220),
				.c(c00000)
);


ninexnine_unit ninexnine_unit_1(
				.a0(P0001),	
				.a1(P0011),
				.a2(P0021),
				.a3(P0101),
				.a4(P0111),
				.a5(P0121),
				.a6(P0201),
				.a7(P0211),
				.a8(P0221),
				.b0(W00001),
				.b1(W00011),
				.b2(W00021),
				.b3(W00101),
				.b4(W00111),
				.b5(W00121),
				.b6(W00201),
				.b7(W00211),
				.b8(W00221),
				.c(c01000)
);

ninexnine_unit ninexnine_unit_2(
				.a0(P0002),	
				.a1(P0012),
				.a2(P0022),
				.a3(P0102),
				.a4(P0112),
				.a5(P0122),
				.a6(P0202),
				.a7(P0212),
				.a8(P0222),
				.b0(W00002),
				.b1(W00012),
				.b2(W00022),
				.b3(W00102),
				.b4(W00112),
				.b5(W00122),
				.b6(W00202),
				.b7(W00212),
				.b8(W00222),
				.c(c02000)
);
assign  C0000=c00000+c01000+c02000;//6 bit

assign A0000=(C0000>=0)?1:0;
assign A0100=(C0100>=0)?1:0;
assign A0010=(C0010>=0)?1:0;
assign A0110=(C0110>=0)?1:0;

maxpool maxpool_0(
				.a0(A0000),
				.a1(A0100),
				.a2(A0010),
				.a3(A0110),
				.p(P1000)
				
				
);

endmodule