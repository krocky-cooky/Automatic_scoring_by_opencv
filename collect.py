from glob import glob
import subprocess
from mergevec import merge_vec_files

n = 20

files = glob("pos/*.jpg")

for i in range(len(files)):

    file = files[i]
    vec = "work/{}.vec".format(i)
    cmd = ["opencv_createsamples", "-vec", vec, "-img", file, "-num", str(n), "-bgcolor", "255"]
    res = subprocess.call(cmd)

merge_vec_files("work", "vec/pos.vec")