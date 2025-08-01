import requests
import json
from typing import Dict, Tuple, Optional, Union
from dataclasses import dataclass

@dataclass
class Color:
    """颜色数据类"""
    r: int
    g: int
    b: int
    
    def to_dict(self) -> Dict[str, int]:
        """转换为字典格式"""
        return {'r': self.r, 'g': self.g, 'b': self.b}
    
    def validate(self) -> bool:
        """验证颜色值是否有效"""
        return all(0 <= v <= 255 for v in [self.r, self.g, self.b])

class LEDClient:
    """LED服务客户端类"""
    
    # 预设颜色
    COLORS = {
        'red': Color(255, 0, 0),
        'green': Color(0, 255, 0),
        'blue': Color(0, 0, 255),
        'yellow': Color(255, 255, 0),
        'cyan': Color(0, 255, 255),
        'magenta': Color(255, 0, 255),
        'white': Color(255, 255, 255),
        'warm_white': Color(255, 209, 163),
        'orange': Color(255, 165, 0),
        'purple': Color(128, 0, 128),
        'pink': Color(255, 192, 203),
        'off': Color(0, 0, 0)
    }
    
    def __init__(self, base_url: str = "http://localhost:5000", timeout: int = 5):
        """
        初始化LED客户端
        
        Args:
            base_url: LED服务的基础URL
            timeout: 请求超时时间（秒）
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
    
    def _make_request(self, data: Dict) -> Dict:
        """
        发送请求到LED服务
        
        Args:
            data: 请求数据
            
        Returns:
            响应数据
            
        Raises:
            requests.RequestException: 网络请求错误
            ValueError: 服务器返回错误
        """
        try:
            response = self.session.post(
                f"{self.base_url}/led/control",
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise requests.RequestException(f"LED服务请求失败: {e}")
        except json.JSONDecodeError:
            raise ValueError("服务器返回无效的JSON响应")
    
    def turn_on(self) -> bool:
        """
        开启LED灯带
        
        Returns:
            bool: 操作是否成功
        """
        try:
            result = self._make_request({'action': 'on'})
            return result.get('status') == 'success'
        except Exception as e:
            print(f"开启LED失败: {e}")
            return False
    
    def turn_off(self) -> bool:
        """
        关闭LED灯带
        
        Returns:
            bool: 操作是否成功
        """
        try:
            result = self._make_request({'action': 'off'})
            return result.get('status') == 'success'
        except Exception as e:
            print(f"关闭LED失败: {e}")
            return False
    
    def set_color(self, color: Union[Color, Dict, str, Tuple[int, int, int]]) -> bool:
        """
        设置LED颜色
        
        Args:
            color: 颜色值，可以是：
                - Color对象
                - 字典 {'r': 255, 'g': 0, 'b': 0}
                - 字符串（预设颜色名称）
                - 元组 (r, g, b)
                
        Returns:
            bool: 操作是否成功
        """
        try:
            # 处理不同类型的颜色输入
            if isinstance(color, str):
                if color not in self.COLORS:
                    raise ValueError(f"未知的预设颜色: {color}")
                color_obj = self.COLORS[color]
            elif isinstance(color, dict):
                color_obj = Color(**color)
            elif isinstance(color, tuple) and len(color) == 3:
                color_obj = Color(*color)
            elif isinstance(color, Color):
                color_obj = color
            else:
                raise ValueError("无效的颜色格式")
            
            # 验证颜色值
            if not color_obj.validate():
                raise ValueError("颜色值必须在0-255范围内")
            
            result = self._make_request({'color': color_obj.to_dict()})
            return result.get('status') == 'success'
            
        except Exception as e:
            print(f"设置颜色失败: {e}")
            return False
    
    def set_brightness(self, brightness: int) -> bool:
        """
        设置LED亮度
        
        Args:
            brightness: 亮度值 (0-255)
            
        Returns:
            bool: 操作是否成功
        """
        try:
            if not 0 <= brightness <= 255:
                raise ValueError("亮度值必须在0-255范围内")
            
            result = self._make_request({'brightness': brightness})
            return result.get('status') == 'success'
            
        except Exception as e:
            print(f"设置亮度失败: {e}")
            return False
    
    def set_color_and_brightness(self, color: Union[Color, Dict, str, Tuple[int, int, int]], 
                                brightness: int) -> bool:
        """
        同时设置颜色和亮度
        
        Args:
            color: 颜色值
            brightness: 亮度值 (0-255)
            
        Returns:
            bool: 操作是否成功
        """
        try:
            # 处理颜色
            if isinstance(color, str):
                if color not in self.COLORS:
                    raise ValueError(f"未知的预设颜色: {color}")
                color_obj = self.COLORS[color]
            elif isinstance(color, dict):
                color_obj = Color(**color)
            elif isinstance(color, tuple) and len(color) == 3:
                color_obj = Color(*color)
            elif isinstance(color, Color):
                color_obj = color
            else:
                raise ValueError("无效的颜色格式")
            
            # 验证参数
            if not color_obj.validate():
                raise ValueError("颜色值必须在0-255范围内")
            if not 0 <= brightness <= 255:
                raise ValueError("亮度值必须在0-255范围内")
            
            result = self._make_request({
                'color': color_obj.to_dict(),
                'brightness': brightness
            })
            return result.get('status') == 'success'
            
        except Exception as e:
            print(f"设置颜色和亮度失败: {e}")
            return False
    
    def get_available_colors(self) -> list:
        """
        获取所有可用的预设颜色
        
        Returns:
            list: 预设颜色名称列表
        """
        return list(self.COLORS.keys())
    
    def test_connection(self) -> bool:
        """
        测试与LED服务的连接
        
        Returns:
            bool: 连接是否正常
        """
        try:
            # 尝试关闭LED来测试连接
            result = self._make_request({'action': 'off'})
            return result.get('status') == 'success'
        except Exception:
            return False


# 使用示例
if __name__ == "__main__":
    # 创建LED客户端
    led = LEDClient("http://localhost:5000")
    
    # 测试连接
    if led.test_connection():
        print("✅ LED服务连接正常")
    else:
        print("❌ LED服务连接失败")
        exit(1)
    
    # 开启LED
    print("开启LED...")
    led.turn_on()
    
    # 设置预设颜色
    print("设置为红色...")
    led.set_color('red')
    
    # 设置自定义颜色
    print("设置为紫色...")
    led.set_color(Color(128, 0, 128))
    
    # 设置亮度
    print("设置亮度为50%...")
    led.set_brightness(128)
    
    # 同时设置颜色和亮度
    print("设置为暖白色，亮度80%...")
    led.set_color_and_brightness('warm_white', 204)
    
    # 显示所有可用颜色
    print(f"可用预设颜色: {', '.join(led.get_available_colors())}")
    
    # 关闭LED
    print("关闭LED...")
    led.turn_off()
    
    print("演示完成！") 