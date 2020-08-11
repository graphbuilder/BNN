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

def dump_test(layer_idx, out_fm):
    layer_idx = layer_idx + 1
    out_fm = out_fm.squeeze()
    out_fm_c = out_fm.shape[0]
    out_fm_h = out_fm.shape[1]
    out_fm_w = out_fm.shape[2]
    # print(out_fm_c,out_fm_h,out_fm_w)

    filename = set_dir(filepath = 'test_tb', file = 'test_tb_layer_0.v')
    try:
        with open (filename, 'a') as f:
            f.write("module tb_test(\n" + 
                    "\n" + 
                    ");\n" + 
                    "reg clk,rstn;\n" + 
                    "test  test(\n" +
                    "clk,\n" + 
                    "rstn\n" +
                    ");\n" + 
                    "always #5 clk=~clk;\n" + 
                    "initial\nbegin\nclk=0;\nrstn=0;\n" + 
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
                for l in range (out_fm_w):  # 14
                    pass_num = "Pass_" + str(i)
                    pass_num_pre = "Pass_" + str(i - 1)
                    test_point = "P" + \
                                str(layer_idx) + \
                                str(int2str(k + 1)) + \
                                str(int2str(l + 1)) + \
                                str(int2str(j))
                    if i ==0:
                        f.write("reg " + str(pass_num) + ";\n" + 
                                "always@(posedge clk or negedge rstn)\n" +
                                "\tif(~rstn)\n" +
                                "\t\t" + str(pass_num) + "<=0;\n" + 
                                "\telse if(count>=2)\n" +
                                "\t\tbegin\n" +

                                "\t\t\tif(tb_test.test." + \
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

                                "\t\t\tif((tb_test.test." + \
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
    
def save_fm_txt(out_fm):
    out_fm = out_fm.squeeze()
    filename = set_dir(filepath = 'test_answer', file = 'answer_layer_0.txt')
    with open(filename, 'a') as f:
        for i in range(out_fm.shape[0] * out_fm.shape[1] * out_fm.shape[2]):
            value_temp = out_fm.flat[i].astype(np.int)
            f.write(str(value_temp) + '\n')


if __name__ == "__main__":
    layer_idx = 0
    out_fm = np.load("fm/feature1.fm.npy")
    dump_test(layer_idx, out_fm)
    save_fm_txt(out_fm)
