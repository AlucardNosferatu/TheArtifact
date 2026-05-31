import csv
import os
from datetime import datetime

# CSV 文件路径
CSV_PATH = 'weapons_with_bullets.csv'
BASE_PATH = '.'

def get_float(value, default=0.0):
    """安全地转换为浮点数"""
    try:
        if isinstance(value, (int, float)):
            return float(value)
        return float(value) if value and str(value).strip() else default
    except (ValueError, TypeError):
        return default

def calculate_score(weapon_data):
    """计算武器综合评分 - 完全从 CSV 数据读取"""
    
    # 伤害数据
    bullet_damage = get_float(weapon_data.get('bullet_damage', 0))
    laser_damage = get_float(weapon_data.get('laser_damage', 0))
    explosion_damage = get_float(weapon_data.get('explosion_far_ring_damage', 0))
    
    # 使用有伤害的那个，优先使用子弹伤害或激光伤害，爆炸伤害作为补充
    damage = bullet_damage if bullet_damage > 0 else laser_damage
    if damage == 0 and explosion_damage > 0:
        damage = explosion_damage
    
    # 其他属性
    cooldown = get_float(weapon_data.get('cooldown', 1))
    per_click_cooldown = get_float(weapon_data.get('per_click_cooldown', 0.1))
    
    # 处理 cooldown 为 0 的情况
    if cooldown <= 0:
        cooldown = per_click_cooldown
    
    range_val = get_float(weapon_data.get('range', 0))
    accuracy = get_float(weapon_data.get('accuracy_cone_width', 10))
    ammo_capacity = get_float(weapon_data.get('ammo_capacity', 0))
    bullet_speed = get_float(weapon_data.get('bullet_speed', 0))
    bullet_penetration = get_float(weapon_data.get('bullet_penetration', 0))
    penetration = get_float(weapon_data.get('penetration', 0))
    final_penetration = bullet_penetration if bullet_penetration > 0 else penetration
    
    burst_count = get_float(weapon_data.get('burst_count', 1))
    shot_count = get_float(weapon_data.get('shot_count', 1))
    
    # 计算每秒伤害 (DPS)
    dps = (damage * burst_count * shot_count) / max(cooldown, 0.01)
    
    # 归一化各项指标 (0-100 范围)
    damage_score = min(dps * 0.1, 100) if dps > 0 else 0
    range_score = min(range_val / 2, 100)
    accuracy_score = max(0, 100 - accuracy * 15)
    ammo_score = min(ammo_capacity * 2, 100)
    speed_score = min(bullet_speed / 2, 100)
    penetration_score = min(final_penetration * 0.5, 100)
    
    # 综合评分 (加权平均)
    weights = {
        'damage': 0.35,
        'range': 0.15,
        'accuracy': 0.15,
        'ammo': 0.10,
        'speed': 0.10,
        'penetration': 0.15
    }
    
    total_score = (
        damage_score * weights['damage'] +
        range_score * weights['range'] +
        accuracy_score * weights['accuracy'] +
        ammo_score * weights['ammo'] +
        speed_score * weights['speed'] +
        penetration_score * weights['penetration']
    )
    
    return {
        'dps': dps,
        'damage': damage,
        'bullet_damage': bullet_damage,
        'laser_damage': laser_damage,
        'explosion_damage': explosion_damage,
        'cooldown': cooldown,
        'range': range_val,
        'accuracy': accuracy,
        'ammo_capacity': ammo_capacity,
        'bullet_speed': bullet_speed,
        'penetration': final_penetration,
        'burst_count': burst_count,
        'shot_count': shot_count,
        'total_score': total_score
    }

def load_weapons_csv():
    """加载武器 CSV 数据到字典，以 filename 为键"""
    weapons_dict = {}
    weapons_by_name = {}
    try:
        with open(CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                filename = row.get('filename', '')
                name = row.get('name', '')
                if filename:
                    weapons_dict[filename] = row
                    # 也存一下，用basename做键
                    basename = os.path.basename(filename)
                    weapons_dict[basename] = row
                    # 用完整路径做键
                    full_path = f'assets/data/pickups/weapons/{filename}'
                    weapons_dict[full_path] = row
                if name:
                    weapons_by_name[name] = row
    except Exception as e:
        print(f"加载 CSV 失败: {e}")
    return weapons_dict

def main():
    print("正在加载武器数据...")
    
    weapons_dict = load_weapons_csv()
    print(f"成功加载 {len(weapons_dict)} 个武器数据")
    
    scored_weapons = []
    # 避免重复，用filename作为唯一标识
    processed = set()
    for filename, weapon_data in weapons_dict.items():
        # 只处理一次每个武器
        key = weapon_data.get('filename', filename)
        if key in processed:
            continue
        processed.add(key)
        
        scores = calculate_score(weapon_data)
        weapon_name = weapon_data.get('name', key)
        scored_weapons.append({
            'name': weapon_name,
            'filename': weapon_data.get('filename', filename),
            **scores
        })
    
    # 按评分降序排序
    scored_weapons.sort(key=lambda x: x['total_score'], reverse=True)
    
    # 生成分析报告
    print("\n正在生成分析报告...")
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("武器性能分析报告")
    report_lines.append("=" * 80)
    report_lines.append(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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
    report_lines.append("Top 10 武器")
    report_lines.append("-" * 80)
    report_lines.append("")
    
    for i, weapon in enumerate(scored_weapons[:10], 1):
        report_lines.append(f"排名 {i}: {weapon['name']}")
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
    
    # 保存报告
    output_path = 'weapons_analysis.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"\n分析完成！报告已保存至: {os.path.abspath(output_path)}")
    print("\n" + "=" * 80)
    print("Top 10 武器预览:")
    print("=" * 80)
    for i, weapon in enumerate(scored_weapons[:10], 1):
        print(f"{i}: {weapon['name']} - 评分: {weapon['total_score']:.2f} - DPS: {weapon['dps']:.2f}")
    
    return scored_weapons

if __name__ == "__main__":
    main()
