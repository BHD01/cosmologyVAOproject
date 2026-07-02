from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
import numpy as np

# 定义宇宙学模型（Planck 2018 参数）
cosmo = FlatLambdaCDM(H0=67.4, Om0=0.315)

# 指定红移（示例 z=10，根据你的光锥调整）
z = 10.0

# BOX 边长（假设物理单位 Mpc，非 comoving；若为 comoving，则需除以 (1+z)）
box_size = 1800/(1 + z) * u.Mpc  # 横向尺寸 L_perp

# 计算角直径距离 D_A
d_A = cosmo.angular_diameter_distance(z)

# 计算张角（小角度近似），明确指定单位为弧度
theta_rad = (box_size / d_A) * u.radian  # 显式赋予弧度单位

# 转换为度
theta_deg = theta_rad.to(u.deg).value

# 转换为弧分
theta_arcmin = theta_rad.to(u.arcmin).value

# 输出结果
print(f"红移 z = {z}:")
print(f"角直径距离 D_A: {d_A:.2f}")
print(f"横向尺寸 L_perp: {box_size}")
print(f"张角 θ (度): {theta_deg:.4f}°")
print(f"张角 θ (弧分): {theta_arcmin:.2f}'")