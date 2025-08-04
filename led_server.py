import time
from flask import Flask, request, jsonify
from rpi_ws281x import PixelStrip, Color

# LED灯带配置
LED_COUNT = 32         # LED 灯珠数量
LED_PIN = 18           # 连接到树莓派的GPIO引脚
LED_FREQ_HZ = 800000   # LED频率（通常是800kHz）
LED_DMA = 10           # DMA通道
LED_BRIGHTNESS = 50    # 亮度（0-255之间）
LED_INVERT = False     # 反转信号（True时，信号反转）

# 默认值配置
DEFAULT_BRIGHTNESS = 100
DEFAULT_COLOR = Color(255, 209, 163)  # 默认颜色：暖白色

class LEDController:
    # 类变量，用于保存最后一次关闭时的状态
    _last_state = {
        'color': DEFAULT_COLOR,
        'brightness': DEFAULT_BRIGHTNESS
    }

    def __init__(self):
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self.strip.begin()
        self.is_on = False
        self.current_color = self._last_state['color']
        self.current_brightness = self._last_state['brightness']
        self.strip.setBrightness(self.current_brightness)

    def turn_on(self):
        self.is_on = True
        # 恢复上次保存的状态
        self.current_color = self._last_state['color']
        self.current_brightness = self._last_state['brightness']
        self.strip.setBrightness(self.current_brightness)
        self._update_leds()

    def turn_off(self):
        # 保存当前状态
        self._last_state['color'] = self.current_color
        self._last_state['brightness'] = self.current_brightness
        self.is_on = False
        self._update_leds()

    def set_color(self, r, g, b):
        self.current_color = Color(r, g, b)
        if self.is_on:
            self._update_leds()

    def set_brightness(self, brightness):
        if 0 <= brightness <= 255:
            self.current_brightness = brightness
            self.strip.setBrightness(brightness)
            if self.is_on:
                self._update_leds()

    def adjust_brightness(self, adjustment):
        """
        增量调节亮度
        :param adjustment: 亮度增量，正数调亮，负数调暗
        """
        # 计算新的亮度值
        new_brightness = self.current_brightness + adjustment
        
        # 边界处理：确保亮度在0-255范围内
        new_brightness = max(0, min(255, new_brightness))
        
        # 使用现有的set_brightness方法设置新亮度
        self.set_brightness(int(new_brightness))

    def _update_leds(self):
        if self.is_on:
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.current_color)
        else:
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()

# 创建Flask应用
app = Flask(__name__)
led_controller = LEDController()

@app.route('/led/control', methods=['POST'])
def control_led():
    try:
        data = request.get_json()
        
        # 处理开关控制
        if 'action' in data:
            if data['action'] == 'on':
                led_controller.turn_on()
            elif data['action'] == 'off':
                led_controller.turn_off()
            else:
                return jsonify({'error': 'Invalid action'}), 400

        # 处理颜色控制
        if 'color' in data:
            color = data['color']
            if not all(0 <= v <= 255 for v in [color.get('r', 0), color.get('g', 0), color.get('b', 0)]):
                return jsonify({'error': 'Invalid color values'}), 400
            led_controller.set_color(
                color.get('r', 0),
                color.get('g', 0),
                color.get('b', 0)
            )

        # 处理亮度控制 - 支持绝对值和增量值
        if 'brightness_adjust' in data:
            # 增量亮度调节
            try:
                adjustment = float(data['brightness_adjust'])
                led_controller.adjust_brightness(adjustment)
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid brightness_adjust value. Must be a number.'}), 400
        elif 'brightness' in data:
            # 绝对亮度设置（保持原有功能）
            brightness = data['brightness']
            if not 0 <= brightness <= 255:
                return jsonify({'error': 'Invalid brightness value'}), 400
            led_controller.set_brightness(brightness)

        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        # 程序退出时关闭LED
        led_controller.turn_off() 