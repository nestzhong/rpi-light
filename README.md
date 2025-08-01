# LED服务客户端

这是一个用于控制LED灯带的Python客户端库，支持通过HTTP API控制LED的开关、颜色和亮度。

## 功能特性

- ✅ LED开关控制（开启/关闭）
- ✅ 颜色设置（支持预设颜色和自定义RGB值）
- ✅ 亮度调节（0-255范围）
- ✅ 组合操作（同时设置颜色和亮度）
- ✅ 连接测试
- ✅ 错误处理和参数验证
- ✅ 类型提示支持

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

### 1. 启动LED服务

首先确保LED服务正在运行：

```bash
python led_server.py
```

服务将在 `http://localhost:5000` 启动。

### 2. 使用客户端

```python
from led_client import LEDClient, Color

# 创建客户端
led = LEDClient("http://localhost:5000")

# 测试连接
if led.test_connection():
    print("连接成功！")
else:
    print("连接失败！")
    exit(1)

# 开启LED
led.turn_on()

# 设置颜色（多种方式）
led.set_color('red')                    # 预设颜色
led.set_color(Color(255, 0, 0))        # Color对象
led.set_color({'r': 255, 'g': 0, 'b': 0})  # 字典
led.set_color((255, 0, 0))             # 元组

# 设置亮度
led.set_brightness(128)  # 50%亮度

# 同时设置颜色和亮度
led.set_color_and_brightness('warm_white', 200)

# 关闭LED
led.turn_off()
```

## API参考

### LEDClient类

#### 初始化
```python
led = LEDClient(base_url="http://localhost:5000", timeout=5)
```

#### 方法

##### turn_on()
开启LED灯带
```python
success = led.turn_on()
```

##### turn_off()
关闭LED灯带
```python
success = led.turn_off()
```

##### set_color(color)
设置LED颜色

**参数：**
- `color`: 颜色值，支持以下格式：
  - 字符串：预设颜色名称（如 'red', 'blue', 'warm_white'）
  - Color对象：`Color(r, g, b)`
  - 字典：`{'r': 255, 'g': 0, 'b': 0}`
  - 元组：`(255, 0, 0)`

**示例：**
```python
led.set_color('red')
led.set_color(Color(255, 0, 0))
led.set_color({'r': 255, 'g': 0, 'b': 0})
led.set_color((255, 0, 0))
```

##### set_brightness(brightness)
设置LED亮度

**参数：**
- `brightness`: 亮度值（0-255）

**示例：**
```python
led.set_brightness(128)  # 50%亮度
led.set_brightness(255)  # 100%亮度
```

##### set_color_and_brightness(color, brightness)
同时设置颜色和亮度

**参数：**
- `color`: 颜色值（同set_color方法）
- `brightness`: 亮度值（0-255）

**示例：**
```python
led.set_color_and_brightness('warm_white', 200)
```

##### get_available_colors()
获取所有可用的预设颜色

**返回：**
- 预设颜色名称列表

**示例：**
```python
colors = led.get_available_colors()
print(colors)  # ['red', 'green', 'blue', 'yellow', ...]
```

##### test_connection()
测试与LED服务的连接

**返回：**
- `bool`: 连接是否正常

**示例：**
```python
if led.test_connection():
    print("连接正常")
else:
    print("连接失败")
```

## 预设颜色

客户端提供了以下预设颜色：

- `red` - 红色
- `green` - 绿色
- `blue` - 蓝色
- `yellow` - 黄色
- `cyan` - 青色
- `magenta` - 洋红色
- `white` - 白色
- `warm_white` - 暖白色
- `orange` - 橙色
- `purple` - 紫色
- `pink` - 粉色
- `off` - 关闭（黑色）

## 错误处理

客户端包含完善的错误处理机制：

- 网络连接错误
- 参数验证错误
- 服务器响应错误
- 颜色值范围验证

所有方法都会返回布尔值表示操作是否成功，错误信息会打印到控制台。

## 完整示例

```python
from led_client import LEDClient, Color
import time

def demo():
    # 创建客户端
    led = LEDClient()
    
    # 测试连接
    if not led.test_connection():
        print("无法连接到LED服务")
        return
    
    print("开始LED演示...")
    
    # 开启LED
    led.turn_on()
    time.sleep(1)
    
    # 循环显示不同颜色
    colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta']
    for color in colors:
        print(f"设置颜色: {color}")
        led.set_color(color)
        time.sleep(2)
    
    # 调节亮度
    for brightness in [50, 100, 150, 200, 255]:
        print(f"设置亮度: {brightness}")
        led.set_brightness(brightness)
        time.sleep(1)
    
    # 设置暖白色
    led.set_color_and_brightness('warm_white', 200)
    time.sleep(3)
    
    # 关闭LED
    led.turn_off()
    print("演示完成！")

if __name__ == "__main__":
    demo()
```

## 注意事项

1. 确保LED服务正在运行
2. 检查网络连接和防火墙设置
3. 颜色值必须在0-255范围内
4. 亮度值必须在0-255范围内
5. 所有操作都是异步的，但客户端会等待服务器响应

## 故障排除

### 连接失败
- 检查LED服务是否正在运行
- 确认服务器地址和端口正确
- 检查网络连接

### 颜色设置失败
- 确认颜色值在有效范围内（0-255）
- 检查预设颜色名称是否正确

### 亮度设置失败
- 确认亮度值在有效范围内（0-255）
