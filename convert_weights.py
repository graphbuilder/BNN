import os
import torch.utils.data
import  numpy as np 
from torch import nn

def conv_weight(raw_weight):
    save_path = 'yolov3-tiny-voc.best.0'
    fp = open(save_path, 'wb')
    header_info = np.array([0, 0, 0, 0], dtype = np.int32)
    header_info.tofile(fp)
    with open('preconvert.txt', 'r') as ln:
        lnames = ln.readlines()
    if raw_weight:
        ckpt = torch.load(raw_weight)

        # .pth file convert to .weight file
        for lname in lnames:
            if lname:
                klname = '{}'.format(lname.strip().strip('\n'))
                print(klname)

                # bias_name = klname.split('.')[0] + '.' + klname.split('.')[1] + '.' + 'bias'
                # print(bias_name)
                # bias_name_value = 0

                if len(ckpt[klname].data.cpu().numpy().shape) == 4:
                   
                    # print(ckpt[klname].data.cpu().numpy().shape[0])
                    bias_num = ckpt[klname].data.cpu().numpy().shape[0]
                    bias_value = np.zeros(bias_num, dtype=np.float32)
                    print(np.dtype(bias_value[0]))
                    bias_value.tofile(fp)
                    bias_value = None


                    ar = (ckpt[klname].data.cpu().numpy()).flatten()
                    print(np.dtype(ar[0]))
                else:
                    ar = ckpt[klname].data.cpu().numpy()
                ar.tofile(fp)
                ar = None

    fp.close() 

if __name__ == "__main__":
    raw_weight = 'ckp-v1.pad1/model_37_0.8849.pth'
    conv_weight(raw_weight)