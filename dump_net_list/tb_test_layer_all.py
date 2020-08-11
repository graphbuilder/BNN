import os 
import shutil
import numpy as np

'''
creat hardware script:

test every layer output is right or not,
if it is wrong, than find which point
e.g. first layer test

'''
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

def dump_test(filename, layer_idx, out_fm, next_pad_stride = 0):
    layer_idx = layer_idx + 1
    if layer_idx != 5:
        out_fm = out_fm.squeeze()
        out_fm_c = out_fm.shape[0]  # 4
        out_fm_h = out_fm.shape[1]  # 14
        out_fm_w = out_fm.shape[2]  # 14
        # print(out_fm_c,out_fm_h,out_fm_w)
    else:
        out_fm_c = out_fm.shape[1]  # 4
        out_fm_h = out_fm.shape[2]  # 14
        out_fm_w = out_fm.shape[3]  # 14

    try:
        with open (filename, 'a') as f:
            f.write("module tb_test_layer" + str(int2str(layer_idx - 1)) +"(\n" + 
                    "\n" + 
                    ");\n" + 
                    "reg clk,rstn;\n" + 
                    "test_layer" + str(int2str(layer_idx - 1)) + " test_layer" + str(int2str(layer_idx - 1)) +"(\n" +
                    "clk,\n" + 
                    "rstn\n" +
                    ");\n" + 
                    "reg mem[14*14*4-1:0];\n" +
                    "always #5 clk=~clk;\n" + 
                    "initial\nbegin\nclk=0;\nrstn=0;\n" + 
                    "$readmemb(\"D:/work/PROJ_5/proj_2/src/to_csma/test_tb/answer_layer_" + str(int2str(layer_idx - 1)) + ".txt\",mem);\n" + 
                    "#10;\nrstn=1;\nend\nreg [31:0]count;\n" + 
                    "always@(posedge clk or negedge rstn)\n" + 

                    "\tif(~rstn)\n" + 
                    "\t\tcount<=0;\n" + 
                    "\telse\n" + 
                    "\t\tcount<=count+1;\n\n"
                    )
    except FileNotFoundError:
        msg = "Sorry, the file " + filename + " does not exist."
        print(msg)
    else:
        f.close()    
    
    with open(filename, 'a') as f:
        print("Here is pad, so first point need plus 1!")
        i = 0
        for j in range(out_fm_c):  # 4
            for k in range(out_fm_h):  # 14
                if next_pad_stride:
                    k += 1
                for l in range (out_fm_w):  # 14
                    if next_pad_stride:
                        l += 1

                    pass_num = "Pass_" + str(i)
                    pass_num_pre = "Pass_" + str(i - 1)
                    test_point = "P" + \
                                str(layer_idx) + \
                                str(int2str(k)) + \
                                str(int2str(l)) + \
                                str(int2str(j))
                    if i ==0:
                        f.write("reg " + str(pass_num) + ";\n" + 
                                "always@(posedge clk or negedge rstn)\n" +
                                "\tif(~rstn)\n" +
                                "\t\t" + str(pass_num) + "<=0;\n" + 
                                "\telse if(count>=2)\n" +
                                "\t\tbegin\n" +

                                "\t\t\tif(tb_test_layer" + str(int2str(layer_idx - 1)) +".test_layer" + str(int2str(layer_idx - 1)) + "." + \
                                str(test_point) + \
                                "==mem[" + str(i) + "])\n" +  
                                
                                "\t\t\t\t" + str(pass_num) + "<=1;\n" +
                                "\t\t\telse\n" +
                                "\t\t\t\t" + str(pass_num) + "<=0;\n" + 
                                "\t\tend\n\n"
                        )
                    else:
                        f.write("reg " + str(pass_num) + ";\n" + 
                                "always@(posedge clk or negedge rstn)\n" +
                                "\tif(~rstn)\n" +
                                "\t\t" + str(pass_num) + "<=0;\n" + 
                                "\telse if(count>=2)\n" +
                                "\t\tbegin\n" +

                                "\t\t\tif((tb_test_layer" + str(int2str(layer_idx - 1)) +".test_layer" + str(int2str(layer_idx - 1)) + "." + \
                                str(test_point) + \
                                "==mem[" + str(i) + "])&&(" + \
                                str(pass_num_pre) +"))\n" +

                                "\t\t\t\t" + str(pass_num) + "<=1;\n" + 
                                "\t\t\telse\n" +
                                "\t\t\t\t" + str(pass_num) + "<=0;\n" + 
                                "\t\tend\n\n"
                        )                       
                    i += 1

        f.write("always@(posedge clk)\n")
        for m in range(out_fm_c * out_fm_h * out_fm_w):  # 4*14*14
            pass_num = "Pass_" + str(m)
            if m == 0:
                f.write("if(" + str(pass_num))
            else:
                f.write("&&" + str(pass_num))
        f.write(")\n")

        f.write("begin\n$display(" + \
                "\"PASS\"" + \
                ");\n$finish;\nend\n\nendmodule\n")
    
def save_fm_txt(filename2, out_fm):
    if out_fm.shape[1] != 2:
        out_fm = out_fm.squeeze()
        out_fm_c = out_fm.shape[0]  # 4
        out_fm_h = out_fm.shape[1]  # 14
        out_fm_w = out_fm.shape[2]  # 14
    else:
        out_fm_c = out_fm.shape[1]  # 4
        out_fm_h = out_fm.shape[2]  # 14
        out_fm_w = out_fm.shape[3]  # 14
    with open(filename2, 'a') as f:
        for i in range(out_fm_c * out_fm_h * out_fm_w):
            value_temp = out_fm.flat[i].astype(np.int)
            if value_temp == -1:
                value_temp = 0
            f.write(str(value_temp) + '\n')


if __name__ == "__main__":

    files = "test_tb_layer_all.v"
    filename = set_dir(filepath = 'test_tb', file = str(files))

    files2 = "answer_layer_all.txt"
    filename2 = set_dir(filepath = 'test_tb', file = str(files2))

    for i in range(5):
        print(i)
        layer_idx = i

        if layer_idx != 4:    
            output_load = "fm/feature" + str(layer_idx + 1) + ".fm.npy"
        else:
            output_load = "fm/out.fm.npy"

        out_fm = np.load(str(output_load))  # 8*7*7
        
        if layer_idx == 0:
            next_pad_stride = 1
        else:
            next_pad_stride = 0
        
        dump_test(filename, layer_idx, out_fm, next_pad_stride = next_pad_stride)
        
        save_fm_txt(filename2, out_fm)
