#!/usr/bin/env python3
"""
LED客户端测试脚本
用于验证LED客户端的所有功能
"""

import time
from led_client import LEDClient, Color

def test_basic_functions():
    """测试基本功能"""
    print("=== 测试基本功能 ===")
    
    led = LEDClient()
    
    # 测试连接
    print("1. 测试连接...")
    if led.test_connection():
        print("   ✅ 连接成功")
    else:
        print("   ❌ 连接失败")
        return False
    
    # 测试开关控制
    print("2. 测试开关控制...")
    if led.turn_on():
        print("   ✅ 开启LED成功")
    else:
        print("   ❌ 开启LED失败")
        return False
    
    time.sleep(1)
    
    if led.turn_off():
        print("   ✅ 关闭LED成功")
    else:
        print("   ❌ 关闭LED失败")
        return False
    
    return True

def test_color_functions():
    """测试颜色功能"""
    print("\n=== 测试颜色功能 ===")
    
    led = LEDClient()
    
    # 开启LED
    led.turn_on()
    
    # 测试预设颜色
    print("1. 测试预设颜色...")
    preset_colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta']
    for color_name in preset_colors:
        print(f"   设置颜色: {color_name}")
        if led.set_color(color_name):
            print(f"   ✅ {color_name} 设置成功")
        else:
            print(f"   ❌ {color_name} 设置失败")
        time.sleep(0.5)
    
    # 测试Color对象
    print("2. 测试Color对象...")
    custom_colors = [
        Color(255, 0, 0),    # 红色
        Color(0, 255, 0),    # 绿色
        Color(0, 0, 255),    # 蓝色
        Color(255, 255, 0),  # 黄色
    ]
    
    for color in custom_colors:
        print(f"   设置颜色: RGB({color.r}, {color.g}, {color.b})")
        if led.set_color(color):
            print(f"   ✅ RGB({color.r}, {color.g}, {color.b}) 设置成功")
        else:
            print(f"   ❌ RGB({color.r}, {color.g}, {color.b}) 设置失败")
        time.sleep(0.5)
    
    # 测试字典格式
    print("3. 测试字典格式...")
    dict_colors = [
        {'r': 255, 'g': 0, 'b': 0},      # 红色
        {'r': 0, 'g': 255, 'b': 0},      # 绿色
        {'r': 0, 'g': 0, 'b': 255},      # 蓝色
    ]
    
    for color_dict in dict_colors:
        print(f"   设置颜色: {color_dict}")
        if led.set_color(color_dict):
            print(f"   ✅ {color_dict} 设置成功")
        else:
            print(f"   ❌ {color_dict} 设置失败")
        time.sleep(0.5)
    
    # 测试元组格式
    print("4. 测试元组格式...")
    tuple_colors = [
        (255, 0, 0),    # 红色
        (0, 255, 0),    # 绿色
        (0, 0, 255),    # 蓝色
    ]
    
    for color_tuple in tuple_colors:
        print(f"   设置颜色: {color_tuple}")
        if led.set_color(color_tuple):
            print(f"   ✅ {color_tuple} 设置成功")
        else:
            print(f"   ❌ {color_tuple} 设置失败")
        time.sleep(0.5)
    
    # 关闭LED
    led.turn_off()
    return True

def test_brightness_functions():
    """测试亮度功能"""
    print("\n=== 测试亮度功能 ===")
    
    led = LEDClient()
    
    # 开启LED并设置颜色
    led.turn_on()
    led.set_color('white')
    
    # 测试不同亮度
    print("1. 测试亮度调节...")
    brightness_levels = [50, 100, 150, 200, 255]
    
    for brightness in brightness_levels:
        print(f"   设置亮度: {brightness}")
        if led.set_brightness(brightness):
            print(f"   ✅ 亮度 {brightness} 设置成功")
        else:
            print(f"   ❌ 亮度 {brightness} 设置失败")
        time.sleep(0.5)
    
    # 关闭LED
    led.turn_off()
    return True

def test_combined_functions():
    """测试组合功能"""
    print("\n=== 测试组合功能 ===")
    
    led = LEDClient()
    
    # 开启LED
    led.turn_on()
    
    # 测试同时设置颜色和亮度
    print("1. 测试同时设置颜色和亮度...")
    test_combinations = [
        ('red', 100),
        ('green', 150),
        ('blue', 200),
        ('warm_white', 255),
        (Color(255, 0, 255), 128),  # 洋红色
    ]
    
    for color, brightness in test_combinations:
        print(f"   设置: 颜色={color}, 亮度={brightness}")
        if led.set_color_and_brightness(color, brightness):
            print(f"   ✅ 组合设置成功")
        else:
            print(f"   ❌ 组合设置失败")
        time.sleep(0.5)
    
    # 关闭LED
    led.turn_off()
    return True

def test_utility_functions():
    """测试工具功能"""
    print("\n=== 测试工具功能 ===")
    
    led = LEDClient()
    
    # 测试获取可用颜色
    print("1. 测试获取可用颜色...")
    available_colors = led.get_available_colors()
    print(f"   可用颜色: {', '.join(available_colors)}")
    print(f"   ✅ 获取到 {len(available_colors)} 种预设颜色")
    
    # 测试连接状态
    print("2. 测试连接状态...")
    if led.test_connection():
        print("   ✅ 连接正常")
    else:
        print("   ❌ 连接异常")
    
    return True

def test_error_handling():
    """测试错误处理"""
    print("\n=== 测试错误处理 ===")
    
    led = LEDClient()
    
    # 开启LED
    led.turn_on()
    
    # 测试无效颜色名称
    print("1. 测试无效颜色名称...")
    if not led.set_color('invalid_color'):
        print("   ✅ 正确拒绝无效颜色名称")
    else:
        print("   ❌ 应该拒绝无效颜色名称")
    
    # 测试无效颜色值
    print("2. 测试无效颜色值...")
    invalid_colors = [
        Color(300, 0, 0),    # R值超出范围
        Color(0, -10, 0),    # G值为负数
        Color(0, 0, 256),    # B值超出范围
    ]
    
    for color in invalid_colors:
        if not led.set_color(color):
            print(f"   ✅ 正确拒绝无效颜色: RGB({color.r}, {color.g}, {color.b})")
        else:
            print(f"   ❌ 应该拒绝无效颜色: RGB({color.r}, {color.g}, {color.b})")
    
    # 测试无效亮度值
    print("3. 测试无效亮度值...")
    invalid_brightness = [-10, 300, 500]
    
    for brightness in invalid_brightness:
        if not led.set_brightness(brightness):
            print(f"   ✅ 正确拒绝无效亮度: {brightness}")
        else:
            print(f"   ❌ 应该拒绝无效亮度: {brightness}")
    
    # 关闭LED
    led.turn_off()
    return True

def main():
    """主测试函数"""
    print("开始LED客户端功能测试...\n")
    
    tests = [
        ("基本功能", test_basic_functions),
        ("颜色功能", test_color_functions),
        ("亮度功能", test_brightness_functions),
        ("组合功能", test_combined_functions),
        ("工具功能", test_utility_functions),
        ("错误处理", test_error_handling),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print(f"\n=== 测试结果 ===")
    print(f"通过: {passed}/{total}")
    print(f"成功率: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print("⚠️  部分测试失败，请检查LED服务状态")

if __name__ == "__main__":
    main() 