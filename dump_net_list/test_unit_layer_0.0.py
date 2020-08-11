import numpy as np
import os
import shutil

def set_dir(filepath, file):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)
    PATH = str(filepath) + '/' + str(file)
    with open(PATH, 'w') as f: 
        f.seek(0)
        f.truncate()
    return PATH


def dump_head():
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

def dump_weights(wieghts):
    '''
    params:
    ---dff_weights_idx, all weights idex, range(0, 4*3*3*3)
        e.g. len(dff_weights_idx) = 4*3*3*3,
    
    ---reset_value_w, weights value, 
        e.g reset_value = 1 or -1

    ---q_keys_w, weights key, 
        e.g q_keys_w(0,0,0,0,0) -> 0:layer 1:batch 2:x 3:y 4:c, ori(NCHW)

    ---dff_fm_idx, all feature map idex, range(0, 3*30*30)
        e.g. len(dff_fm_idx) = 3*30*30
    ---...
    ---wire P0000  :layer id 1:x 2:y 3:c
    ---wire W00000 :layer id 1:weight kernal 2:x  3:y  4:c
    '''

    weight_dict = {}
    layers_w_idx = 0
    weights_n = wieghts.shape[0]
    weights_c = wieghts.shape[1]
    weights_h = wieghts.shape[2]
    weights_w = wieghts.shape[3]
    idx_0 = layers_w_idx
    i = 0 
    q_keys_w = []
    for j in range(weights_n):  # 0~3
        idx_1 = j
        for k in range(weights_c):  # 0~2
            idx_4 = k
            for l in range(weights_h):  # 0~2
                idx_2 = l
                for m in range(weights_w):  # 0~2
                    idx_3 = m
                    temp = 'W' + str(idx_0) + str(idx_1) + str(idx_2) + str(idx_3) + str(idx_4) 
                    q_keys_w.append(temp)

                    value_temp = weights.flat[i].astype(np.int)
                    if value_temp == -1:
                        value_temp = 0
                        weight_dict[q_keys_w[i]] = value_temp
                    else:
                        weight_dict[q_keys_w[i]] = value_temp
                    i += 1

    # filename = set_dir(filepath = 'test_unit', file = 'test_unit_layer_0.v')
    filename = 'test_unit/test_unit_layer_0.v'
    try:
        with open (filename, 'a') as f:
            i = 0
            for key, value in weight_dict.items():
                dff_weights_idx = i
                reset_value_w = value
                q_keys_w = key
                f.write("DFF_save_weights DFF_w_"+ str(dff_weights_idx) + 
                    "(.clk(clk),.rstn(rstn),.reset_value(" + 
                    str(reset_value_w) + "),.q(" + str(q_keys_w) + "));\n")
                i += 1
    except FileNotFoundError:
        msg = "Sorry, the file " + filename + " does not exist."
        print(msg)
    else:
        f.close()


def dump_unit(input_fm, weights):
    '''
    input (3,30,30)
    weights (4,3,3,3)
    unit_idx in range(0, 28*28*4)

    wire c00000,c01000,c02000; 0:layer id 1:input seg number 2:x 3:y 4:c
    wire C0000,C0010,C0100,C0110; 0:layer id 1:x 2:y 3:c 
    wire A0000,A0010,A0100,A0110; 0:layer id 1:x 2:y 3:c

    c_idx_0 = 0 (layer0)
    c_idx_1 = in range(input_seg = 3)
    c_idx_2 = C_idx 1
    c_idx_3 = C_idx_2
    c_idx_4 = C_idx_3


    output fm size means unit number, one point is one unit,
    so unit_idx in range (0, 4*28*28).

    assign  C0000=c00000+c01000+c02000;

    '''

    input_fm = input_fm.squeeze()  # 1*3*30*30 -> 3*30*30
    input_size = input_fm.shape[-1]  # 30
    input_seg = input_fm.shape[0]  # 3
    out_size = input_size - 2  # 28
    out_c = weights.shape[0]  # 4

    layer_id = 0
    C_idx_0 = layer_id
    c_idx_0 = layer_id

    filename = set_dir(filepath = 'test_unit', file = 'test_unit_layer_0.v')
    try:
        with open (filename, 'a') as f:
            h = 0
            for i in range(out_c):  # 4
                C_idx_3 = i
                c_idx_4 = C_idx_3
                for j in range(out_size):  # 28
                    if j > 9:
                        C_idx_1 = chr(j + 55)  
                        c_idx_2 = C_idx_1
                    else:
                        C_idx_1 = str(j)
                        c_idx_2 = C_idx_1
                    for k in range(out_size):   # 28
                        if k > 9:
                            C_idx_2 = chr(k + 55)  
                            c_idx_3 = C_idx_2
                        else:
                            C_idx_2 = str(k)
                            c_idx_3 = C_idx_2
                        for l in range(input_seg):  # 3
                            c_idx_1 = l
                            c_idx = str(c_idx_0) + str(c_idx_1) + str(c_idx_2) + str(c_idx_3) + str(c_idx_4)
                            C_idx = str(C_idx_0) + str(C_idx_1) + str(C_idx_2) + str(C_idx_3)

                            # build unit
                            f.write("ninexnine_unit ninexnine_unit_" +
                                str(h) + "(\n\t\t\t\t" + 
                                ".a0(),\n"         + 
                                "\t\t\t\t.a1(),\n" + 
                                "\t\t\t\t.a2(),\n" + 
                                "\t\t\t\t.a3(),\n" + 
                                "\t\t\t\t.a4(),\n" + 
                                "\t\t\t\t.a5(),\n" + 
                                "\t\t\t\t.a6(),\n" + 
                                "\t\t\t\t.a7(),\n" + 
                                "\t\t\t\t.a8(),\n" + 
                                "\t\t\t\t.b0(),\n" + 
                                "\t\t\t\t.b1(),\n" + 
                                "\t\t\t\t.b2(),\n" + 
                                "\t\t\t\t.b3(),\n" + 
                                "\t\t\t\t.b4(),\n" + 
                                "\t\t\t\t.b5(),\n" + 
                                "\t\t\t\t.b6(),\n" + 
                                "\t\t\t\t.b7(),\n" + 
                                "\t\t\t\t.b8(),\n" + 
                                "\t\t\t\t.c("      + 
                                str(c_idx)         +
                                ")\n"   + 
                                ");\n\n")
                            if (h + 1) % input_seg == 0:
                                f.write("assign  C" + 
                                    str(C_idx)   +  
                                    "=c"         + 
                                    str(c_idx_0) +
                                    str(0)       +
                                    str(c_idx_2) +
                                    str(c_idx_3) +
                                    str(c_idx_4) +
                                    "+c"         +
                                    str(c_idx_0) +
                                    str(1)       +
                                    str(c_idx_2) +
                                    str(c_idx_3) +
                                    str(c_idx_4) +
                                    "+c"         +
                                    str(c_idx_0) +
                                    str(2)       +
                                    str(c_idx_2) +
                                    str(c_idx_3) +
                                    str(c_idx_4) +
                                    ";\n")
                                
                                # add activation
                                A_idx = str(C_idx)
                                f.write("assign  A" +  
                                    str(A_idx)      + 
                                    "=(C"           + 
                                    str(C_idx)      + 
                                    ">=0)?1:0;\n")
                            h += 1
            
            # add maskpooling
            l = 0
            A_idx_a0_0 = layer_id
            A_idx_a1_0 = layer_id
            A_idx_a2_0 = layer_id
            A_idx_a3_0 = layer_id
            next_l_id = 1
            P_idx_0 = next_l_id
            for i in range(out_c):  # ---4
                P_idx_3 = i
                A_idx_a0_3 = i
                A_idx_a1_3 = i
                A_idx_a2_3 = i
                A_idx_a3_3 = i
                for j in range(0, out_size, 2):  # ---28
                    if j == 0:
                        P_idx_1 = j
                        P_idx_1_int = j
                    else:
                        temp = j // 2
                        if temp > 9:
                            P_idx_1_int = temp
                            P_idx_1 = chr(temp + 55)
                        else:
                            P_idx_1 = str(temp)
                    if j > 9:
                        A_idx_1 = chr(j + 55)  
                    else:
                        A_idx_1 = str(j)
                    for k in range(0, out_size, 2):  # ---28
                        if k == 0:
                            P_idx_2 = k
                            P_idx_2_int = k
                        else:
                            temp = k // 2
                            if temp > 9:
                                P_idx_2_int = temp
                                P_idx_2 = chr(temp + 55)
                            else:
                                P_idx_2 = str(temp)
                        if k > 9:
                            A_idx_2 = chr(k + 55)  
                        else:
                            A_idx_2 = str(k) 
                        
                        '''
                        00,01  02,03 ...
                        10,11  12 13 ...
                        
                         00      01  ...    
                        '''
                        A_idx_a0_1 = P_idx_1_int
                        A_idx_a0_2 = P_idx_2_int * 2

                        A_idx_a1_1 = A_idx_a0_1
                        A_idx_a1_2 = A_idx_a0_2 + 1

                        A_idx_a2_1 = A_idx_a0_1 + 1
                        A_idx_a2_2 = A_idx_a0_2

                        A_idx_a3_1 = A_idx_a2_1
                        A_idx_a3_2 = A_idx_a2_2 + 1

                        P_idx = "P" + str(P_idx_0) + str(P_idx_1) + str(P_idx_2) + str(P_idx_3)
                        A_idx_a0 = "A" + str(A_idx_a0_0) + str(A_idx_a0_1) + str(A_idx_a0_2) + str(A_idx_a0_3)
                        A_idx_a1 = "A" + str(A_idx_a1_0) + str(A_idx_a1_1) + str(A_idx_a1_2) + str(A_idx_a1_3)
                        A_idx_a2 = "A" + str(A_idx_a2_0) + str(A_idx_a2_1) + str(A_idx_a2_2) + str(A_idx_a2_3)
                        A_idx_a3 = "A" + str(A_idx_a3_0) + str(A_idx_a3_1) + str(A_idx_a3_2) + str(A_idx_a3_3)
                        # print(P_idx)
                        
                        f.write("maxpool maxpool_" + 
                            str(l) + "(\n\t\t\t\t" +
                            ".a0(" +
                            str(A_idx_a0)  +
                            "),\n"         + 
                            "\t\t\t\t.a1(" +
                            str(A_idx_a1)  +
                            "),\n" + 
                            "\t\t\t\t.a2(" +
                            str(A_idx_a2)  +
                            "),\n" +
                            "\t\t\t\t.a3(" +
                            str(A_idx_a3)  +
                            "),\n" + 
                            "\t\t\t\t.p("      +
                            str(P_idx)         + 
                            ")\n"              +
                            ");\n\n")
                        l += 1
                                               


            f.write("\nendmodule\n")
    except FileNotFoundError:
        msg = "Sorry, the file " + filename + " does not exist."
        print(msg)
    else:
        f.close()


def dump_fm(input_fm, weights):
    input_fm = input_fm.squeeze()  # 1*3*30*30 -> 3*30*30
    fm_dict = {}
    layers_fm_idx = 0
    fm_c = input_fm.shape[0]
    fm_h = input_fm.shape[1]
    fm_w = input_fm.shape[2]
    idx_0 = layers_fm_idx
    i = 0 
    q_keys_f = []

    for k in range(fm_c):  # 0~2
        idx_3 = k
        for l in range(fm_h):  # 0~29
            if l > 9:
                idx_1 = chr(l + 55)  # A,B,C...
            else:
                idx_1 = str(l)
            for m in range(fm_w):  # 0~29
                if m > 9:
                    idx_2 = chr(m + 55)
                else:
                    idx_2 = str(m)
                temp = 'P' + str(idx_0) + str(idx_1) + str(idx_2) + str(idx_3) 
                q_keys_f.append(temp)
                value_temp = input_fm.flat[i].astype(np.int)
                if value_temp == -1:
                    value_temp = 0
                    fm_dict[q_keys_f[i]] = value_temp
                else:
                    fm_dict[q_keys_f[i]] = value_temp
                i += 1

    filename = set_dir(filepath = 'test_unit', file = 'test_unit_layer_0.v')
    try:
        with open (filename, 'a') as f:
            i = 0
            for key, value in fm_dict.items():
                dff_fm_idx = i
                reset_value_w = value
                q_keys_f = key
                f.write("DFF_save_fm DFF_fm_"+ str(dff_fm_idx) + 
                    "(.clk(clk),.rstn(rstn),.reset_value(" + 
                    str(reset_value_w) + "),.q(" + str(q_keys_f) + "));\n")
                i += 1
    except FileNotFoundError:
        msg = "Sorry, the file " + filename + " does not exist."
        print(msg)
    else:
        f.close()
    dump_weights(weights)


def dump_test_layer_0(input_fm, weights):
    '''
    input_fm, 30*30*3
    weights, 4*3*3*3
    return test_unit_layer_0.v
    '''

    dump_head()
    dump_fm(input_fm, weights)
    dump_unit(input_fm, weights)

if __name__ == "__main__":
    input_fm = np.load("fm/input.fm.npy") 
    weights = np.load("param/features0.0.weight.npy")

    # dump_test_layer_0(input_fm, weights)

    dump_unit(input_fm, weights)

