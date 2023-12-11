from turcar import launch


# 这里是不能编写逻辑代码的，因为在打包后，这里根本就不是入口，至于为啥
# 只需要查看打包后 ~/apps/turcar/bin/turcar 的文件，一看就明白了，
# 这也就是为啥更新和检查是否有网写在这没有任何作用的原因
launch()