from sat.data_utils import SimpleDistributedWebDataset

import time 
import argparse
import torch

parser = argparse.ArgumentParser()
parser.add_argument('--local_rank', type=int, default=0)
parser.add_argument('--world_size', type=int, default=1)
parser.add_argument('--rank', type=int, default=0)
parser.add_argument('--master_addr', type=str, default='')
parser.add_argument('--master_port', type=int, default=7878)
parser.add_argument('--batch-size', type=int, default=32)
args = parser.parse_args()

def process_fn(src):
    for x in src:
        yield x

ds = SimpleDistributedWebDataset('rclone://r2train:cc3m-cc12m-sbu/part-00001/10000{0..5}.tar', process_fn, seed=0)
train_loader = torch.utils.data.DataLoader(ds, batch_size=args.batch_size, shuffle=False, num_workers=1, pin_memory=True, drop_last=True)

for i, x in enumerate(train_loader):
    if i==0:
        start_time = time.time()
    time.sleep(0.3)
    if i > 100:
        # save x['jpg'] to disk
        with open('test.jpg', 'wb') as f:
            f.write(x['jpg'][0])
        break

print('Time taken: ', time.time() - start_time)
print('Avarage time per image: ', (time.time() - start_time)/args.batch_size/100)
 


