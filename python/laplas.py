import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 网格参数
N = 401  # 网格点数（奇数，保证中心点在网格上）
L = 5   # 空间范围
dx = 2 * L / (N - 1)
dt = 0.002
steps = 600  # 动画帧数
c = 1      # 波速
v = 0.9

# 初始化场
Ez = np.zeros((N, N))
Ez_new = np.zeros_like(Ez)
Ez_old = np.zeros_like(Ez)

# 中心点索引
cx = cy = N // 2

# 半隐式欧拉法主循环
def step(Ez, Ez_old, t):
    Ez_new = Ez.copy()
    Ez[cx , cy ] = 2 * np.cos(5*t)
    lap = (
        np.roll(Ez, 1, axis=0) + np.roll(Ez, -1, axis=0) +
        np.roll(Ez, 1, axis=1) + np.roll(Ez, -1, axis=1) - 4 * Ez
    ) / dx**2
    eff1_lap =(
        np.roll(Ez, 1, axis=0) - np.roll(Ez, 0, axis=0) -
        np.roll(Ez_old, 1, axis=0) + np.roll(Ez_old, 0, axis=0) 
    ) / dx / dt
    eff2_lap = (
        np.roll(Ez, 1, axis=0) + np.roll(Ez, -1, axis=0) 
         - 2 * Ez
    ) / dx**2
    Ez_new = 2 * Ez - Ez_old + (c**2) * dt**2 * lap - v**2 * dt **2 * eff2_lap+ 2 * v * dt**2 * eff1_lap

    # 一阶Mur吸收边界
    coef = (c*dt-dx)/(c*dt+dx)
    Ez_new[0, 1:-1] = Ez[1, 1:-1] + coef * (Ez_new[1, 1:-1] - Ez[0, 1:-1])
    Ez_new[-1, 1:-1] = Ez[-2, 1:-1] + coef * (Ez_new[-2, 1:-1] - Ez[-1, 1:-1])
    Ez_new[1:-1, 0] = Ez[1:-1, 1] + coef * (Ez_new[1:-1, 1] - Ez[1:-1, 0])
    Ez_new[1:-1, -1] = Ez[1:-1, -2] + coef * (Ez_new[1:-1, -2] - Ez[1:-1, -1])

    # --------  --------
    #wall_y = N // 2
    #slit_width = 80  # 狭缝宽度
    #slit_start = N // 2 - slit_width // 2
    #slit_end = N // 2 + slit_width // 2
    #Ez_new[0:slit_start,wall_y] = 0  # 整行设为墙
    #Ez_new[slit_end:N,wall_y] = 0
    

    return Ez_new

# 可视化
fig, ax = plt.subplots()
im = ax.imshow(Ez, vmin=-1, vmax=1, cmap='bwr', extent=[-L, L, -L, L])
ax.set_title("Ez(x, y, t)")

def update(frame):
    global Ez, Ez_old
    t = frame * dt
    Ez_new = step(Ez, Ez_old, t)
    im.set_array(Ez_new)
    Ez_old, Ez = Ez, Ez_new
    return [im]

ani = FuncAnimation(fig, update, frames=steps, interval=20, blit=True)
plt.show()