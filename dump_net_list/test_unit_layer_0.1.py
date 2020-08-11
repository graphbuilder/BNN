'''
it is design to first layer  pass
'''

import numpy as np
import os
import shutil

def set_dir(filepath, file):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    # else:
    #     shutil.rmtree(filepath)
    #     os.mkdir(filepath)
    PATH = str(filepath) + '/' + str(file)
    with open(PATH, 'w') as f: 
        f.seek(0)
        f.truncate()
    return PATH


def int2str(a):
    # if == 10, A
    if a > 9:
        a = chr(a + 55)
    else:
        a = a
    return a


def dump_unit(layer_idx, input_fm, weights, pre_pad_stride, next_pad_stride, max_stride = 1):

    input_fm = input_fm.squeeze()  # 1*3*30*30 -> 3*30*30

    input_fm_c = input_fm.shape[0]  # 3
    input_fm_h = input_fm.shape[1]  # 30
    input_fm_w = input_fm.shape[2]  # 30
    
    out_fm_c = weights.shape[0]  # 4
    conv_fm_h = input_fm.shape[1] -  pre_pad_stride * 2 # 28
    conv_fm_w = input_fm.shape[2] -  pre_pad_stride * 2 # 28
    
    if max_stride:
        pool_fm_h = int(conv_fm_h / max_stride)
        pool_fm_w = int(conv_fm_w / max_stride)
        print("Warning, Please attention the param pool_fm_h")

    weights_c = weights.shape[1]  # 3
    weights_h = weights.shape[2]  # 3
    weights_w = weights.shape[3]  # 3

    # 0. dump head ************************************************
    '''
    module test(
    clk,
    rstn
    );
    input clk;
    input rstn;
    '''
    filename = set_dir(filepath = 'test_unit', file = 'test_unit_layer_0.v')
    try:
        with open (filename, 'a') as f:
            f.write("module test(\nclk, \nrstn\n);\n" + 
                "input clk;\ninput rstn;\n\n")
    except FileNotFoundError:
        msg = "Sorry, the file " + filename + " does not exist."
        print(msg)
    else:
        f.close()

    # 1. dump layer_idx wire Point num = 2700 ************************************************  
    # wire P0000,P0010,P0020,P0100,P0110,P0120,P0200,P0210,P0220;
    with open (filename, 'a') as f:
        P_unit_list = []
        for j in range(input_fm_c):   # 3
            for k in range(input_fm_h):  # 30
                for l in range(input_fm_w):  # 30            
                    P_unit_idx = "P" + str(layer_idx) + str(int2str(k)) + str(int2str(l)) + str(int2str(j))
                    P_unit_list.append(P_unit_idx)
                    if len(P_unit_list) == 9:            
                        f.write("wire " + str(P_unit_list[0]) + "," + str(P_unit_list[1]) + "," + str(P_unit_list[2]) + ","
                                        + str(P_unit_list[3]) + "," + str(P_unit_list[4]) + "," + str(P_unit_list[5]) + ","
                                        + str(P_unit_list[6]) + "," + str(P_unit_list[7]) + "," + str(P_unit_list[8])
                                        +";\n")
                        P_unit_list.clear()
    f.close()   

    # 2. dump layer_idx + 1 wire Point num = 784 ************************************************
    # due to next_pad_stride = 1, so first point = k + 1 
    # wire P1000;
    for j in range(out_fm_c):   # 4
        for k in range(pool_fm_h):  # 14
            for l in range(pool_fm_w):  # 14            
                out_P_unit_num_0 = "P" + \
                                str(layer_idx + 1) + \
                                str(int2str(k + 1)) + \
                                str(int2str(l + 1)) + \
                                str(int2str(j))
                with open (filename, 'a') as f:
                    f.write("wire " + str(out_P_unit_num_0) + ";\n")
    f.close()  

    # 3. dump layer_idx wire Weihts num = 108 ************************************************
    # wire W00000,W00010,W00020,W00100,W00110,W00120,W00200,W00210,W00220;
    W_unit = []
    for j in range(out_fm_c):   # 4
        for k in range(input_fm_c):  # 3
            for l in range(weights_h):  # 3 
                for m in range(weights_w):  # 3
                    W_unit_idx = "W" + \
                                str(layer_idx) + \
                                str(int2str(j)) + \
                                str(int2str(l)) + \
                                str(int2str(m)) + \
                                str(int2str(k))
                    W_unit.append(W_unit_idx)
            with open (filename, 'a') as f:
                f.write("wire " + str(W_unit[0]) + "," + str(W_unit[1]) + "," + str(W_unit[2]) + ","
                                + str(W_unit[3]) + "," + str(W_unit[4]) + "," + str(W_unit[5]) + ","
                                + str(W_unit[6]) + "," + str(W_unit[7]) + "," + str(W_unit[8])
                                +";\n")
                W_unit.clear()
    f.close() 

    # 4. dump c00000 num 4*28*28 = 3136 ************************************************
    # wire [3:0]c00000,c01000,c02000;
    c_unit = []
    for i in range(out_fm_c):  # 4
        for k in range(conv_fm_h):  # 28
            for l in range(conv_fm_w):  # 28
                for j in range(input_fm_c):  # 3
                    c_unit_idx = 'c' + \
                                str(layer_idx) + \
                                str(int2str(j)) + \
                                str(int2str(k)) + \
                                str(int2str(l)) + \
                                str(int2str(i))
                    c_unit.append(c_unit_idx)
                with open (filename, 'a') as f:
                    f.write("wire " + "[3:0]" + str(c_unit[0]) + "," + \
                                                str(c_unit[1]) + "," + \
                                                str(c_unit[2]) + ";\n")
                    c_unit.clear()
    f.close()            
    
    # 5. dump C0000 num = 4 * 14 * 14 = 784
    # wire [5:0]C0000,C0010,C0100,C0110;
    for i in range(out_fm_c):  # 4
        for k in range(0, conv_fm_h - 1, max_stride):  # 28
            for l in range(0, conv_fm_w - 1, max_stride):  # 28                        
                C_unit_0 = "C" + str(layer_idx) + str(int2str(k))     + str(int2str(l))     + str(int2str(i))
                C_unit_1 = "C" + str(layer_idx) + str(int2str(k))     + str(int2str(l + 1)) + str(int2str(i))
                C_unit_2 = "C" + str(layer_idx) + str(int2str(k + 1)) + str(int2str(l))     + str(int2str(i))
                C_unit_3 = "C" + str(layer_idx) + str(int2str(k + 1)) + str(int2str(l + 1)) + str(int2str(i))
                with open (filename, 'a') as f:
                    f.write("wire " + "[5:0]" + str(C_unit_0) + "," + str(C_unit_1) + "," 
                                    + str(C_unit_2) + "," + str(C_unit_3) +";\n")
    f.close()

    # 6. dump A0000  == C0000  784
    # wire A0000,A0010,A0100,A0110;
    for i in range(out_fm_c):  # 4
        for k in range(0, conv_fm_h - 1, max_stride):  # 28
            for l in range(0, conv_fm_w - 1, max_stride):  # 28                        
                C_unit_0 = "A" + str(layer_idx) + str(int2str(k))     + str(int2str(l))     + str(int2str(i))
                C_unit_1 = "A" + str(layer_idx) + str(int2str(k))     + str(int2str(l + 1)) + str(int2str(i))
                C_unit_2 = "A" + str(layer_idx) + str(int2str(k + 1)) + str(int2str(l))     + str(int2str(i))
                C_unit_3 = "A" + str(layer_idx) + str(int2str(k + 1)) + str(int2str(l + 1)) + str(int2str(i))
                with open (filename, 'a') as f:
                    f.write("wire " + str(C_unit_0) + "," + str(C_unit_1) + "," 
                                    + str(C_unit_2) + "," + str(C_unit_3) +";\n")
    f.close()

    # 7. dump DFF_save_fm DFF_P0(.clk(clk),.rstn(rstn),.reset_value(0),.q(P0000));
    # num = 30*30*3 = 2700  
    point_dict = {}
    i = 0 
    point_list_name = []
    for k in range(input_fm_c):  # 3
        for l in range(input_fm_h):  # 30
            for m in range(input_fm_w):  # 30
                temp = 'P' + \
                        str(layer_idx)  + \
                        str(int2str(l)) + \
                        str(int2str(m)) + \
                        str(int2str(k)) 
                point_list_name.append(temp)
                value_temp = input_fm.flat[i].astype(np.int)
                if value_temp == -1:
                    value_temp = 0
                    point_dict[point_list_name[i]] = value_temp
                else:
                    point_dict[point_list_name[i]] = value_temp
                i += 1
    with open (filename, 'a') as f:
        i = 0
        for key, value in point_dict.items():
            dff_point_idx = i
            f.write("DFF_save_fm DFF_P" + \
                str(dff_point_idx) + \
                "(.clk(clk),.rstn(rstn),.reset_value(" + \
                str(value) + "),.q(" + \
                str(key) + "));\n")
            i += 1
    f.close()

    # 8. dump DFF_save_fm DFF_W0(.clk(clk),.rstn(rstn),.reset_value(0),.q(W00000));
    # num = 4*3*3*3 = 108
    weight_dict = {}
    i = 0 
    weights_list = []
    for j in range(out_fm_c):  # 4
        for k in range(weights_c):  # 3
            for l in range(weights_h):  # 3
                for m in range(weights_w):  # 3
                    temp = 'W' + \
                            str(layer_idx) + \
                            str(int2str(j)) + \
                            str(int2str(l)) + \
                            str(int2str(m)) + \
                            str(int2str(k))
                    weights_list.append(temp)
                    value_temp = weights.flat[i].astype(np.int)
                    if value_temp == -1:
                        value_temp = 0
                        weight_dict[weights_list[i]] = value_temp
                    else:
                        weight_dict[weights_list[i]] = value_temp
                    i += 1
    with open (filename, 'a') as f:
        i = 0
        for key, value in weight_dict.items():
            dff_weights_idx = i
            reset_value_w = value
            weights_list = key
            f.write("DFF_save_fm DFF_W" + \
                str(dff_weights_idx) + \
                "(.clk(clk),.rstn(rstn),.reset_value(" + \
                str(value) + "),.q(" + \
                str(key) + "));\n")
            i += 1
    f.close()

    # 9. dump ninexnine_unit, num = 4*3*28*28 
    # 
    '''
    ninexnine_unit ninexnine_unit_0(
                    .clk(clk),
                    .rstn(rstn),
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

    ninexnine_unit_1
    ninexnine_unit_2

    assign  C0000=c00000+c01000+c02000;

    assign A0000=(C0000>=0)?1:0;
    ...

    ninexnine_unit_9407    
    to 245866
    '''
    with open (filename, 'a') as f:
        h = 0
        g = 0
        c_idx_list = []
        print('Warning, when dump ninexnine_unit, ' + 
            'if input_fm_c != 3, than need to add c_idx_list[2]')
        
        # save Point_unit_idx 
        # due to next_pad_stride = 1, so first point = g + 1 
        for i in range(out_fm_c):  # 4
            for j in range(conv_fm_h):  # 28
                for k in range(conv_fm_w):   # 28
                    for l in range(input_fm_c):  # 3

                        P_idx_0 = "P" + str(layer_idx) + str(int2str(j + 0)) + str(int2str(k + 0)) + str(int2str(l))
                        P_idx_1 = "P" + str(layer_idx) + str(int2str(j + 0)) + str(int2str(k + 1)) + str(int2str(l)) 
                        P_idx_2 = "P" + str(layer_idx) + str(int2str(j + 0)) + str(int2str(k + 2)) + str(int2str(l)) 
                        P_idx_3 = "P" + str(layer_idx) + str(int2str(j + 1)) + str(int2str(k + 0)) + str(int2str(l)) 
                        P_idx_4 = "P" + str(layer_idx) + str(int2str(j + 1)) + str(int2str(k + 1)) + str(int2str(l)) 
                        P_idx_5 = "P" + str(layer_idx) + str(int2str(j + 1)) + str(int2str(k + 2)) + str(int2str(l)) 
                        P_idx_6 = "P" + str(layer_idx) + str(int2str(j + 2)) + str(int2str(k + 0)) + str(int2str(l)) 
                        P_idx_7 = "P" + str(layer_idx) + str(int2str(j + 2)) + str(int2str(k + 1)) + str(int2str(l)) 
                        P_idx_8 = "P" + str(layer_idx) + str(int2str(j + 2)) + str(int2str(k + 2)) + str(int2str(l)) 

                        W_idx_0 = "W" + str(layer_idx) + str(int2str(i)) + str(0) + str(0) + str(int2str(l))
                        W_idx_1 = "W" + str(layer_idx) + str(int2str(i)) + str(0) + str(1) + str(int2str(l))
                        W_idx_2 = "W" + str(layer_idx) + str(int2str(i)) + str(0) + str(2) + str(int2str(l))
                        W_idx_3 = "W" + str(layer_idx) + str(int2str(i)) + str(1) + str(0) + str(int2str(l))
                        W_idx_4 = "W" + str(layer_idx) + str(int2str(i)) + str(1) + str(1) + str(int2str(l))
                        W_idx_5 = "W" + str(layer_idx) + str(int2str(i)) + str(1) + str(2) + str(int2str(l))
                        W_idx_6 = "W" + str(layer_idx) + str(int2str(i)) + str(2) + str(0) + str(int2str(l))
                        W_idx_7 = "W" + str(layer_idx) + str(int2str(i)) + str(2) + str(1) + str(int2str(l))
                        W_idx_8 = "W" + str(layer_idx) + str(int2str(i)) + str(2) + str(2) + str(int2str(l))

                        c_idx = "c" + str(layer_idx) + \
                                    str(int2str(l)) + \
                                    str(int2str(j)) + \
                                    str(int2str(k)) + \
                                    str(int2str(i))

                        c_idx_list.append(c_idx)
                        f.write("ninexnine_unit ninexnine_unit_" +
                            str(h) + "(\n\t\t\t\t" + 
                            ".clk(clk),\n" +
                            "\t\t\t\t.rstn(rstn),\n" +
                            "\t\t\t\t.a0(" + str(P_idx_0) + "),\n" + 
                            "\t\t\t\t.a1(" + str(P_idx_1) + "),\n" + 
                            "\t\t\t\t.a2(" + str(P_idx_2) + "),\n" + 
                            "\t\t\t\t.a3(" + str(P_idx_3) + "),\n" + 
                            "\t\t\t\t.a4(" + str(P_idx_4) + "),\n" + 
                            "\t\t\t\t.a5(" + str(P_idx_5) + "),\n" + 
                            "\t\t\t\t.a6(" + str(P_idx_6) + "),\n" + 
                            "\t\t\t\t.a7(" + str(P_idx_7) + "),\n" + 
                            "\t\t\t\t.a8(" + str(P_idx_8) + "),\n" + 
                            "\t\t\t\t.b0(" + str(W_idx_0) + "),\n" + 
                            "\t\t\t\t.b1(" + str(W_idx_1) + "),\n" + 
                            "\t\t\t\t.b2(" + str(W_idx_2) + "),\n" + 
                            "\t\t\t\t.b3(" + str(W_idx_3) + "),\n" + 
                            "\t\t\t\t.b4(" + str(W_idx_4) + "),\n" + 
                            "\t\t\t\t.b5(" + str(W_idx_5) + "),\n" + 
                            "\t\t\t\t.b6(" + str(W_idx_6) + "),\n" + 
                            "\t\t\t\t.b7(" + str(W_idx_7) + "),\n" + 
                            "\t\t\t\t.b8(" + str(W_idx_8) + "),\n" + 
                            "\t\t\t\t.c("      + 
                            str(c_idx)         +
                            ")\n"   + 
                            ");\n\n")
                        h += 1
                    
                    # assign  C0000=c00000+c01000+c02000;
                    C_idx = "C" + str(layer_idx) + \
                                str(int2str(j)) + \
                                str(int2str(k)) + \
                                str(int2str(i))
                    A_idx = "A" + str(layer_idx) + \
                                str(int2str(j)) + \
                                str(int2str(k)) + \
                                str(int2str(i))
                    f.write("assign "  + 
                            str(C_idx) +  
                            "=" + str(c_idx_list[0]) +  
                            "+" + str(c_idx_list[1]) +
                            "+" + str(c_idx_list[2]) +
                            ";\n")
                    c_idx_list.clear()

                    # assign A0000=(C0000>=0)?1:0;
                    f.write("assign "  +  
                            str(A_idx) + 
                            "=" + "(" + 
                            str(C_idx) + ">=0)?1:0;\n\n")
        '''
        maxpool maxpool_0(
                .clk(clk),
                .rstn(rstn),
				.a0(A0000),
				.a1(A0100),
				.a2(A0010),
				.a3(A0110),
				.p(P1000)			
        );
        num = 4*14*14
        2end
        '''
        h = 0
        for i in range (out_fm_c):
            for j in range(pool_fm_h):
                for k in range(pool_fm_w):
                    A_idx_a0 = "A" + str(layer_idx) + str(int2str(j * max_stride)) + str(int2str(k * max_stride)) + str(int2str(i))
                    A_idx_a1 = "A" + str(layer_idx) + str(int2str(j * max_stride)) + str(int2str(k * max_stride + 1)) + str(int2str(i)) 
                    A_idx_a2 = "A" + str(layer_idx) + str(int2str(j * max_stride + 1)) + str(int2str(k * max_stride)) + str(int2str(i)) 
                    A_idx_a3 = "A" + str(layer_idx) + str(int2str(j * max_stride + 1)) + str(int2str(k * max_stride + 1)) + str(int2str(i)) 
                    P_idx = "P" + str(layer_idx + 1) + str(int2str(j + 1)) + str(int2str(k + 1)) + str(int2str(i))
                    f.write("maxpool maxpool_" + str(h) + 
                            "(\n\t\t\t\t" + 
                            ".clk(clk),\n" + 
                            "\t\t\t\t" + 
                            ".rstn(rstn),\n" + 
                            "\t\t\t\t" + 
                            ".a0(" + str(A_idx_a0) + "),\n" + 
                            "\t\t\t\t" + 
                            ".a1(" + str(A_idx_a1) + "),\n" +
                            "\t\t\t\t" + 
                            ".a2(" + str(A_idx_a2) + "),\n" +
                            "\t\t\t\t" + 
                            ".a3(" + str(A_idx_a3) + "),\n" + 
                            "\t\t\t\t" + 
                            ".p(" +str(P_idx) + ")\n" +
                            ");\n\n")
                    h += 1
        f.write("endmodule")
    f.close()


if __name__ == "__main__":
    layer_idx = 0
    input_fm = np.load("fm/input.fm.npy") 
    weights = np.load("param/features0.0.weight.npy")

    # layer 0 unit layer 0 pass
    dump_unit(layer_idx, input_fm, weights, 1, 1, 2)


