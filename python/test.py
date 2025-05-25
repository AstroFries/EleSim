from manimlib import *
import numpy as np

class EMWaveZPlane(ThreeDScene):
    def construct(self):
        self.camera.frame_rate = 60 
        axes = ThreeDAxes(x_range=[-4, 4], y_range=[-4, 4], z_range=[-2, 2])
        self.add(axes)

        k = 1
        w = 2

        # 更密集的箭头
        x_vals = np.linspace(-3, 3, 21)
        y_vals = np.linspace(-3, 3, 21)
        arrows = VGroup()

        t0 = 0
        for x in x_vals:
            for y in y_vals:
                E_z = np.cos(k * x + w * t0)
                start = np.array([x, y, 0])
                end = np.array([x, y, 0.3 * E_z])
                # 颜色连续变化
                color = interpolate_color(BLUE, RED, (E_z + 1) / 2)
                arrow = Arrow(start, end, color=color, buff=0, stroke_width=2)
                arrows.add(arrow)
        self.add(arrows)

        def update_arrows(mob, dt):
            self.my_time += dt
            t = self.my_time
            for i, arrow in enumerate(mob):
                x = x_vals[i // len(y_vals)]
                y = y_vals[i % len(y_vals)]
                E_z = np.cos(k * x + w * t)
                new_end = np.array([x, y, 0.3 * E_z])
                color = interpolate_color(BLUE, RED, (E_z + 1) / 2)
                arrow.put_start_and_end_on(np.array([x, y, 0]), new_end)
                arrow.set_color(color)

        self.my_time = 0
        arrows.add_updater(update_arrows)

        # ManimGL中镜头旋转写法
        def camera_rotate(mob, dt):
            self.camera.frame.rotate(
                angle=0.2 * dt,  # 旋转速度
                axis=OUT,        # 绕z轴旋转
                about_point=ORIGIN
            )
        self.camera.frame.add_updater(camera_rotate)

        self.wait(2)