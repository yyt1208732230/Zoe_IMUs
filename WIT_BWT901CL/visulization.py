import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# 加载CSV文件，跳过第一行数据（除标题外）
file_name = './WIT_BWT901CL/imuLog_1717739577.csv'
data = pd.read_csv(file_name, skiprows=[1])

# 设置绘图风格
plt.style.use('ggplot')

# 创建一个3行1列的图表布局
fig, axs = plt.subplots(3, 1, figsize=(10, 15))

#假设timestamp是UNIX时间戳，转换为以秒为单位的时间差（相对于最小时间戳）
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')
data['seconds'] = (data['timestamp'] - data['timestamp'].min()).dt.total_seconds()


# 加速度图
axs[0].plot(data['seconds'], data['AccX'], label='AccX (m/s²)', color='red', linewidth=2)
axs[0].plot(data['seconds'], data['AccY'], label='AccY (m/s²)', color='green', linewidth=2)
axs[0].plot(data['seconds'], data['AccZ'], label='AccZ (m/s²)', color='blue', linewidth=2)
axs[0].set_title('Acceleration')
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Acceleration (m/s²)')
axs[0].legend()

# 角速度图
axs[1].plot(data['seconds'], data['AsX'], label='AsX (rad/s)', color='red', linewidth=2)
axs[1].plot(data['seconds'], data['AsY'], label='AsY (rad/s)', color='green', linewidth=2)
axs[1].plot(data['seconds'], data['AsZ'], label='AsZ (rad/s)', color='blue', linewidth=2)
axs[1].set_title('Angular Velocity')
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Angular Velocity (rad/s)')
axs[1].legend()

# 角度X图
axs[2].plot(data['seconds'], data['AngleX'], label='AngleX (°)', color='red', linewidth=2)
axs[2].plot(data['seconds'], data['AngleY'], label='AngleY (°)', color='green', linewidth=2)
axs[2].plot(data['seconds'], data['AngleZ'], label='AngleZ (°)', color='blue', linewidth=2)
axs[2].set_title('Angle Change')
axs[2].set_xlabel('Time (s)')
axs[2].set_ylabel('Angle (degrees)')
axs[2].legend()

# 自动调整子图间距
plt.tight_layout()

# 生成文件名
current_time = datetime.now().strftime("%Y%m%d%H%M%S")
filename = f"{current_time}_IMU_headmovement.png"

# 保存图表
plt.savefig(filename)

# 显示图表
plt.show()
pass
