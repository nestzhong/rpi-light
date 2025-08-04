# RPI-Light LED控制服务器

一个基于树莓派的WS281x LED灯带控制服务器，提供RESTful API接口来控制LED灯带的开关、颜色和亮度。

## 功能特性

- 🔌 **开关控制**：支持LED灯带的开启和关闭
- 🎨 **颜色控制**：支持RGB颜色设置（0-255范围）
- 💡 **亮度控制**：支持绝对亮度设置和增量亮度调节
- 💾 **状态保存**：关闭时自动保存当前状态，开启时恢复
- 🌐 **Web API**：提供RESTful API接口，支持远程控制
- 🔧 **增量调节**：支持亮度微调，提供更精细的控制体验

## 硬件要求

### 树莓派配置
- 树莓派 3B+ / 4B / 5（推荐）
- Python 3.7+
- GPIO 18引脚（可配置）

### LED灯带规格
- WS281x系列LED灯带
- 32个LED灯珠（可配置）
- 5V供电
- 数据线连接到GPIO 18

### 连接方式
```
树莓派 GPIO 18 → LED灯带数据线
树莓派 5V → LED灯带电源正极
树莓派 GND → LED灯带电源负极
```

## 安装指南

### 1. 克隆项目
```bash
git clone <repository-url>
cd rpi-light
```

### 2. 安装依赖
```bash
# 安装系统依赖
sudo apt-get update
sudo apt-get install python3-pip python3-dev

# 安装Python依赖
pip3 install flask rpi-ws281x
```

### 3. 配置环境
```bash
# 创建conda环境（推荐）
conda create -n rpi-light python=3.9
conda activate rpi-light
pip install flask rpi-ws281x
```

### 4. 权限设置
```bash
# 确保用户有GPIO访问权限
sudo usermod -a -G gpio $USER
```

## 使用方法

### 启动服务器
```bash
# 使用conda环境启动
sudo ~/miniconda3/envs/rpi-light/bin/python led_server.py

# 或直接启动
sudo python3 led_server.py
```

服务器将在 `http://0.0.0.0:5000` 启动。

### 测试LED灯带
```bash
# 运行彩虹效果测试
python3 test.py
```

## API接口文档

### 基础信息
- **基础URL**: `http://<树莓派IP>:5000`
- **请求方法**: POST
- **内容类型**: application/json

### 接口端点

#### `/led/control`
控制LED灯带的开关、颜色和亮度。

**请求参数：**

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `action` | string | 否 | 开关控制 | `"on"` 或 `"off"` |
| `color` | object | 否 | RGB颜色设置 | `{"r": 255, "g": 100, "b": 50}` |
| `brightness` | integer | 否 | 绝对亮度值(0-255) | `100` |
| `brightness_adjust` | number | 否 | 亮度增量调节 | `10` 或 `-5` |

**参数说明：**
- `action`: 控制LED开关，"on"开启，"off"关闭
- `color`: RGB颜色对象，r/g/b值范围0-255
- `brightness`: 绝对亮度值，范围0-255
- `brightness_adjust`: 亮度增量，正数调亮，负数调暗，支持小数

**响应格式：**
```json
{
  "status": "success"
}
```

**错误响应：**
```json
{
  "error": "错误描述"
}
```

### 使用示例

#### 1. 开启LED灯带
```bash
curl -X POST http://192.168.1.100:5000/led/control \
  -H "Content-Type: application/json" \
  -d '{"action": "on"}'
```

#### 2. 设置颜色
```bash
curl -X POST http://192.168.1.100:5000/led/control \
  -H "Content-Type: application/json" \
  -d '{"color": {"r": 255, "g": 100, "b": 50}}'
```

#### 3. 设置绝对亮度
```bash
curl -X POST http://192.168.1.100:5000/led/control \
  -H "Content-Type: application/json" \
  -d '{"brightness": 150}'
```

#### 4. 增量调节亮度
```bash
# 调亮10个单位
curl -X POST http://192.168.1.100:5000/led/control \
  -H "Content-Type: application/json" \
  -d '{"brightness_adjust": 10}'

# 调暗5个单位
curl -X POST http://192.168.1.100:5000/led/control \
  -H "Content-Type: application/json" \
  -d '{"brightness_adjust": -5}'

# 精细调节
curl -X POST http://192.168.1.100:5000/led/control \
  -H "Content-Type: application/json" \
  -d '{"brightness_adjust": 0.5}'
```

#### 5. 组合操作
```bash
# 开启并设置颜色和亮度
curl -X POST http://192.168.1.100:5000/led/control \
  -H "Content-Type: application/json" \
  -d '{
    "action": "on",
    "color": {"r": 255, "g": 200, "b": 100},
    "brightness": 120
  }'
```

## 配置说明

### LED参数配置
在 `led_server.py` 中可以调整以下参数：

```python
# LED灯带配置
LED_COUNT = 32         # LED灯珠数量
LED_PIN = 18           # GPIO引脚
LED_FREQ_HZ = 800000   # 频率
LED_DMA = 10           # DMA通道
LED_BRIGHTNESS = 50    # 初始亮度
LED_INVERT = False     # 信号反转

# 默认值配置
DEFAULT_BRIGHTNESS = 100
DEFAULT_COLOR = Color(255, 209, 163)  # 暖白色
```

### 性能优化建议
- 根据LED灯带实际数量调整 `LED_COUNT`
- 根据硬件情况调整 `LED_DMA` 通道
- 适当调整 `LED_FREQ_HZ` 以获得最佳效果

## 故障排除

### 常见问题

#### 1. 权限错误
**问题**: `Permission denied` 或 GPIO访问失败
**解决**: 
```bash
sudo usermod -a -G gpio $USER
# 重新登录或重启
```

#### 2. 依赖安装失败
**问题**: `rpi-ws281x` 安装失败
**解决**:
```bash
sudo apt-get install build-essential python3-dev
pip3 install --upgrade pip
pip3 install rpi-ws281x
```

#### 3. LED不亮
**问题**: LED灯带无响应
**检查项**:
- 电源连接是否正确
- GPIO引脚是否正确
- LED_COUNT 是否与实际灯珠数量匹配

#### 4. 颜色显示异常
**问题**: 颜色与预期不符
**解决**: 检查RGB值是否在0-255范围内

### 调试方法
```bash
# 查看服务器日志
sudo python3 led_server.py

# 测试LED灯带
python3 test.py

# 检查GPIO状态
gpio readall
```

## 开发说明

### 项目结构
```
rpi-light/
├── led_server.py          # 主服务器文件
├── test.py               # LED测试程序
├── run.sh                # 启动脚本
├── README.md             # 项目文档
└── rpi-ws281x-python-pi5-beta2/  # LED控制库
```

### 扩展功能
- 支持更多LED效果（渐变、闪烁等）
- 添加定时控制功能
- 集成传感器控制
- 支持多灯带控制

## 许可证

本项目基于MIT许可证开源。

## 贡献

欢迎提交Issue和Pull Request来改进项目。
