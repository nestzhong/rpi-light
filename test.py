import time
from rpi_ws281x import PixelStrip, Color

# LED灯带配置
LED_COUNT = 32         # LED 灯珠数量
LED_PIN = 18           # 连接到树莓派的GPIO引脚
LED_FREQ_HZ = 800000   # LED频率（通常是800kHz）
LED_DMA = 10           # DMA通道
LED_BRIGHTNESS = 50    # 亮度（0-255之间）
LED_INVERT = False     # 反转信号（True时，信号反转）

# 创建PixelStrip对象
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

# 初始化LED灯带
strip.begin()

# 定义彩虹颜色序列
def wheel(pos):
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

try:
    while True:
        # 循环显示彩虹流动效果
        for j in range(256):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((i + j) & 255))
            strip.show()
            time.sleep(0.02)

except KeyboardInterrupt:
    # Ctrl+C退出时关闭LED灯带
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
