import json
import os
import csv
import glob
from datetime import datetime

# 从 weapon_analyzer 导入需要的函数
from weapon_analyzer import get_float, calculate_score, load_weapons_csv

def find_save_file():
    """查找 save_bk_itch_*.json 文件"""
    pattern = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save_bk_itch_*.json")
    files = glob.glob(pattern)
    if files:
        # 返回最新的文件
        files.sort(key=os.path.getmtime, reverse=True)
        return files[0]
    return None

def extract_weapons_from_save(save_file_path):
    """从存档文件中提取武器（只要武器部分，不管子弹）"""
    print(f"正在加载存档文件: {os.path.basename(save_file_path)}")
    
    with open(save_file_path, 'r', encoding='utf-8') as f:
        save_data = json.load(f)
    
    items = save_data.get('base_storage', {}).get('items', {})
    weapons = []
    
    for item_path, count in items.items():
        # 只要武器，排除子弹
        if 'assets/data/pickups/weapons/' in item_path and 'bullets/' not in item_path:
            weapons.append({
                'path': item_path,
                'count': count
            })
    
    print(f"找到 {len(weapons)} 件武器")
    return weapons

def analyze_inventory_weapons():
    """分析库存武器"""
    print("=" * 80)
    print("库存武器性能分析")
    print("=" * 80)
    
    # 1. 查找存档文件
    save_file = find_save_file()
    if not save_file:
        print("错误: 未找到 save_bk_itch_*.json 文件！")
        return
    
    # 2. 提取武器
    weapons = extract_weapons_from_save(save_file)
    if not weapons:
        print("库存中没有武器")
        return
    
    # 3. 加载武器 CSV 数据
    print("\n正在加载武器 CSV 数据...")
    weapons_dict = load_weapons_csv()
    if not weapons_dict:
        print("错误: 未加载到武器数据！")
        return
    
    # 4. 分析库存武器
    print("正在分析武器...")
    scored_weapons = []
    
    for weapon_info in weapons:
        weapon_path = weapon_info['path']
        count = weapon_info['count']
        
        # 从 CSV 字典查找武器数据
        if weapon_path in weapons_dict:
            weapon_data = weapons_dict[weapon_path]
            # 计算评分
            scores = calculate_score(weapon_data)
            weapon_name = weapon_data.get('name', os.path.basename(weapon_path))
            scored_weapons.append({
                'name': weapon_name,
                'filename': weapon_path,
                'count': count,
                **scores
            })
        else:
            print(f"  警告: CSV 中未找到武器 {weapon_path}")
    
    if not scored_weapons:
        print("未找到可分析的武器")
        return
    
    # 5. 按评分排序
    scored_weapons.sort(key=lambda x: x['total_score'], reverse=True)
    
    # 6. 生成报告
    print("\n正在生成分析报告...")
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("库存武器性能分析报告")
    report_lines.append("=" * 80)
    report_lines.append(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"存档文件: {os.path.basename(save_file)}")
    report_lines.append(f"分析武器总数: {len(scored_weapons)}")
    report_lines.append("")
    report_lines.append("分析说明:")
    report_lines.append("- 综合评分基于以下指标加权计算:")
    report_lines.append("  * 伤害(DPS): 35%")
    report_lines.append("  * 射程: 15%")
    report_lines.append("  * 准确度: 15%")
    report_lines.append("  * 弹夹容量: 10%")
    report_lines.append("  * 子弹速度: 10%")
    report_lines.append("  * 穿透能力: 15%")
    report_lines.append("")
    
    report_lines.append("-" * 80)
    report_lines.append("库存武器按性能排序")
    report_lines.append("-" * 80)
    report_lines.append("")
    
    for i, weapon in enumerate(scored_weapons, 1):
        report_lines.append(f"排名 {i}: {weapon['name']} (x{weapon['count']})")
        report_lines.append(f"  文件: {weapon['filename']}")
        report_lines.append(f"  综合评分: {weapon['total_score']:.2f}")
        report_lines.append(f"  每秒伤害 (DPS): {weapon['dps']:.2f}")
        report_lines.append(f"  伤害值: {weapon['damage']:.2f}")
        if weapon['bullet_damage'] > 0:
            report_lines.append(f"  子弹伤害: {weapon['bullet_damage']:.2f}")
        if weapon['laser_damage'] > 0:
            report_lines.append(f"  激光伤害: {weapon['laser_damage']:.2f}")
        report_lines.append(f"  射速 (冷却时间): {weapon['cooldown']:.4f}s")
        report_lines.append(f"  射程: {weapon['range']:.2f}")
        report_lines.append(f"  准确度 (散布): {weapon['accuracy']:.4f}")
        report_lines.append(f"  弹夹容量: {int(weapon['ammo_capacity'])}")
        report_lines.append(f"  子弹速度: {weapon['bullet_speed']:.2f}")
        report_lines.append(f"  穿透能力: {weapon['penetration']:.2f}")
        report_lines.append(f"  爆发次数: {int(weapon['burst_count'])}")
        report_lines.append(f"  每次发射子弹数: {int(weapon['shot_count'])}")
        report_lines.append("")
    
    # 7. 保存报告
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inventory_analysis.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"\n分析完成！报告已保存至: {os.path.abspath(output_path)}")
    print("\n" + "=" * 80)
    print("库存武器预览 (按性能排序):")
    print("=" * 80)
    for i, weapon in enumerate(scored_weapons, 1):
        print(f"{i:2d}: {weapon['name']} (x{weapon['count']}) - 评分: {weapon['total_score']:6.2f} - DPS: {weapon['dps']:8.2f}")
    
    return scored_weapons

if __name__ == "__main__":
    analyze_inventory_weapons()
