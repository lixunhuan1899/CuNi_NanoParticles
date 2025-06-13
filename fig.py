import numpy as np
import matplotlib.pyplot as plt

# 读取数据

data = np.loadtxt('quench_cuni.dat')
#data = data[::25]
x = data[:, 0]
y = data[:, 1]

# 作图
plt.figure(figsize=(10, 6))
#如果使得结果只是点不连线，加入'o'即可
#plt.plot(x, y, 'o', markersize=0.5, alpha=0.5, color='darkblue')

plt.plot(x,y/480)

# 设置轴标签和标题
plt.xlabel('Step', fontsize=12)
plt.ylabel('Potential(eV/atom)', fontsize=12)
plt.title('relax_CuNi', fontsize=14)

# 反转 X 轴
#plt.gca().invert_xaxis()

# 增加网格，调整样式
plt.grid(True, linestyle='--', linewidth=0.5)

# 加图例
#plt.legend()

# 保存高清图像
plt.tight_layout()
plt.savefig('CuNi_relax.png', dpi=600)

# 可选显示
# plt.show()

