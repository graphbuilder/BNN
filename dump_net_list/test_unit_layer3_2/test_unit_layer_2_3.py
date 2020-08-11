'''
it is design to all layer pass
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


def dump_unit_layer3(filename, layer_idx, input_fm, weights, pre_pad_stride, pad_stride, next_pad_stride, max_stride):

    layer_idx = layer_idx

    # 0: 1*3*30*30 -> 3*30*30
    # 1: 1*4*14*14
    # 2: 1*8*7*7
    # 3: 1*16*5*5
    # 4: 1*32*3*3
    input_fm = input_fm.squeeze()  # 1*4*14*14 -> 4*14*14

    input_fm_c = input_fm.shape[0]  # 4
    input_fm_h = input_fm.shape[1]  # 14
    input_fm_w = input_fm.shape[2]  # 14

    if pre_pad_stride:
        input_fm_h = input_fm.shape[1] - pre_pad_stride * 2  
        input_fm_w = input_fm.shape[2] - pre_pad_stride * 2
    
    if layer_idx == 0:
        input_fm = input_fm
    else:
        if pad_stride:
            input_fm = np.pad(input_fm, ((0, 0), (1, 1), (1, 1)), 'constant', constant_values=(1, 1))  # if true 4*16*16

    weights_c = weights.shape[1]  # 4 (8,4,3,3)
    weights_h = weights.shape[2]  # 3 
    weights_w = weights.shape[3]  # 3
    
    # after conv
    input_fm_h_ = int((input_fm_h -  weights_h + 2 * pad_stride) / 1 + 1)  # 14 
    input_fm_w_ = int((input_fm_w -  weights_h + 2 * pad_stride) / 1 + 1)  # 14 

    # final size
    out_fm_c = weights.shape[0]  # 8
    print("only when layer_idx = 0, 1 pad_stride = 1!")
    conv_fm_h = int((input_fm_h -  weights_h + 2 * pad_stride) / 1 + 1)  # 14 
    conv_fm_w = conv_fm_h  # 14

    if max_stride == 2:
        conv_fm_h = int(conv_fm_h / max_stride)  # 7
        conv_fm_w = int(conv_fm_w / max_stride)  # 7

    # 1. dump layer_idx wire Point num = 16*16*4 = 1024************************************************  
    # wire P1000,P1010,P1020,P1100,P0110,P0120,P0200,P0210,P0220;
    # with open (filename, 'a') as f:
    #     P_unit_list = []
    #     for j in range(input_fm_c):   # 4
    #         for k in range(input_fm.shape[1]):  # 16
    #             for l in range(input_fm.shape[2]):  # 16            
    #                 P_unit_idx = "P" + str(layer_idx) + str(int2str(k)) + str(int2str(l)) + str(int2str(j))
    #                 if k == 0 or l == 0:
    #                     f.write("wire " + str(P_unit_idx) + ";\n")
    # f.close()

    
    # 2. dump layer_idx + 1 wire Point num =  7*7*8 = 392************************************************
    # due to next_pad_stride = 0, so first point = k 
    # due to next_pad_stride = 1, so first point = k + 1 
    # wire P1000;
    i = 0
    for j in range(out_fm_c):   # 8
        for k in range(conv_fm_h):  # 7
            if next_pad_stride == 1:
                k = k + 1
            for l in range(conv_fm_w):  # 7 
                if next_pad_stride == 1:
                    l = l + 1     
                out_P_unit_num_0 = "P" + \
                                str(layer_idx + 1) + \
                                str(int2str(k)) + \
                                str(int2str(l)) + \
                                str(int2str(j))
                with open (filename, 'a') as f:
                    f.write("(*DONT_TOUCH=\"true\"*) wire " + str(out_P_unit_num_0) + ";\n")
                i += 1
    f.close()  
    if i == (out_fm_c * conv_fm_h * conv_fm_w):
        print("2. Dump pass!")
    else:
        print("2. Dump layer_idx + 1 wire P1000; false!")


    # 3. dump layer_idx wire Weihts num = 8*4*3*3  =  288 ************************************************
    # e.g. wire W00000,W00010,W00020,W00100,W00110,W00120,W00200,W00210,W00220;
    i = 0
    W_unit = []
    for j in range(out_fm_c):   # 8
        for k in range(input_fm_c):  # 4
            for l in range(weights_h):  # 3 
                for m in range(weights_w):  # 3
                    W_unit_idx = "W" + \
                                str(layer_idx) + \
                                str(int2str(j)) + \
                                str(int2str(l)) + \
                                str(int2str(m)) + \
                                str(int2str(k))
                    W_unit.append(W_unit_idx)
                    i += 1
            with open (filename, 'a') as f:
                f.write("(*DONT_TOUCH=\"true\"*) wire " + str(W_unit[0]) + "," + str(W_unit[1]) + "," + str(W_unit[2]) + ","
                                + str(W_unit[3]) + "," + str(W_unit[4]) + "," + str(W_unit[5]) + ","
                                + str(W_unit[6]) + "," + str(W_unit[7]) + "," + str(W_unit[8])
                                +";\n")
                W_unit.clear()
    f.close() 
    if i == (out_fm_c * input_fm_c * weights_h * weights_w):
        print("3. Dump pass!")
    else:
        print("3. Dump wire W00000,W00010,W00020,W00100,W00110,W00120,W00200,W00210,W00220; false")


    # 4. dump c00000 num 4*28*28 = 3136 -> 8*14*14   ************************************************
    # wire [3:0]c00000,c01000,c02000;
    c_unit = []
    m = 0
    with open (filename, 'a') as f:
        for i in range(out_fm_c):  # 8
            for k in range(input_fm_h_):  # 14
                for l in range(input_fm_w_):  # 14
                    f.write("(*DONT_TOUCH=\"true\"*) wire " + "signed [4:0] ")
                    for j in range(input_fm_c):  # 4
                        c_unit_idx = 'c' + \
                                    str(layer_idx) + \
                                    str(int2str(j)) + \
                                    str(int2str(k)) + \
                                    str(int2str(l)) + \
                                    str(int2str(i))
                        c_unit.append(c_unit_idx)
                        
                        if j ==  (input_fm_c - 1):
                            f.write(c_unit[0] + ";\n")
                        else:
                            f.write(c_unit[0] + ",")
                        c_unit.clear()
                        m += 1
    f.close() 
    if m == (out_fm_c * input_fm_h_ * input_fm_w_ * input_fm_c):
        print("4. Dump pass!")
    else:
        print("4. Dump wire signed [3:0] c00000,c01000,c02000; false") 
              
    # 5. dump C0000 num = 4 * 14 * 14 = 784 -> 8*7*7 = 392
    # 6. dump A0000  == C0000   
    # wire [5:0]C0000,C0010,C0100,C0110;
    j = 0
    if layer_idx == 0:
        number = 6
    if layer_idx == 1:
        number = 6
    if layer_idx == 2:
        number = 7
    if layer_idx == 3:
        number = 8
    if layer_idx == 4:
        number = 9

    with open (filename, 'a') as f:
        for i in range(out_fm_c):  # 8
            for k in range(input_fm_h_):  # 14  
                for l in range(input_fm_w_):  # 14                      
                    C_unit_0 = "C" + \
                            str(layer_idx) + \
                            str(int2str(k)) + \
                            str(int2str(l)) + \
                            str(int2str(i))
                    A_unit_0 = "A" + \
                            str(layer_idx) + \
                            str(int2str(k)) + \
                            str(int2str(l)) + \
                            str(int2str(i))
                    
                    f.write("(*DONT_TOUCH=\"true\"*) wire " + "signed [" + str(number) +":0] " + str(C_unit_0) + ";\n")
                    f.write("(*DONT_TOUCH=\"true\"*) wire " + str(A_unit_0) +";\n")
                    j += 1
    f.close()
    if j == (out_fm_c * input_fm_h_ * input_fm_w_):
        print("5. Dump pass!")
        print("6. Dump pass!")
    else:
        print("5. Dump wire signed [5:0] C0000,C0010,C0100,C0110; false") 
        print("6. Dump wire A0000,A0010,A0100,A0110; false") 
    

    # 7. dump DFF_save_fm DFF_P0(.clk(clk),.rstn(rstn),.reset_value(0),.q(P0000));
    # num = 30*30*3 = 2700  
    

    # 8. dump DFF_save_fm DFF_W0(.clk(clk),.rstn(rstn),.reset_value(0),.q(W00000));
    # num = 4*3*3*3 = 108 - 8*4*3*3
    weight_dict = {}
    i = 0 
    weights_list = []
    for j in range(out_fm_c):  # 8
        for k in range(weights_c):  # 4
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
        i = 1440
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
    with open (filename, 'a') as f:
        h = 9472
        # g = 0
        c_idx_list = []
        # print('Warning, when dump ninexnine_unit, ' + 
        #     'if input_fm_c != 3, than need to add c_idx_list[2]')
        
        # save Point_unit_idx 
        for i in range(out_fm_c):  # 8
            for j in range(input_fm_h_):  # 14
                for k in range(input_fm_w_):   # 14
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
                    
                    f.write("assign " + str(C_idx) + "=")
                    for m in range(input_fm_c):
                        if m == input_fm_c - 1:
                            f.write(str(c_idx_list[m]) + ";\n")
                        else:
                            f.write(str(c_idx_list[m]) + "+")
                    c_idx_list.clear()

                    # assign A0000=(C0000>=0)?1:0;
                    f.write("assign "  +  
                            str(A_idx) + 
                            "=" + "(" + 
                            str(C_idx) + ">=0)?1:0;\n\n")
                    
                    if max_stride != 2:
                        P_idx = "P" + str(layer_idx + 1) + \
                                    str(int2str(j)) + \
                                    str(int2str(k)) + \
                                    str(int2str(i))
                        f.write("assign " + str(P_idx) + "=" + str(A_idx) + ";\n\n")
        
        if max_stride == 2:
            h = 0
            for i in range (out_fm_c):  # 8
                for j in range(conv_fm_h):  # 7
                    for k in range(conv_fm_w):  # 7
                        A_idx_a0 = "A" + str(layer_idx) + str(int2str(j * max_stride)) + str(int2str(k * max_stride)) + str(int2str(i))
                        A_idx_a1 = "A" + str(layer_idx) + str(int2str(j * max_stride)) + str(int2str(k * max_stride + 1)) + str(int2str(i)) 
                        A_idx_a2 = "A" + str(layer_idx) + str(int2str(j * max_stride + 1)) + str(int2str(k * max_stride)) + str(int2str(i)) 
                        A_idx_a3 = "A" + str(layer_idx) + str(int2str(j * max_stride + 1)) + str(int2str(k * max_stride + 1)) + str(int2str(i)) 
                        
                        if next_pad_stride == 1:
                            P_idx = "P" + str(layer_idx + 1) + str(int2str(j + 1)) + str(int2str(k + 1)) + str(int2str(i))
                        else:
                            P_idx = "P" + str(layer_idx + 1) + str(int2str(j)) + str(int2str(k)) + str(int2str(i))

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
        # f.write("endmodule")
        f.write("//layer3 done, begain next layer\n")
        print("layer3 done, next layer ctrl F layer3")
    f.close()
