import csv
import json
import os
from datetime import datetime

# CSV 文件路径
CSV_PATH = 'weapons_with_bullets.csv'
BASE_PATH = '.'

def load_json(filepath):
    """加载 JSON 文件"""
    if not filepath:
        return None
    try:
        full_path = os.path.join(BASE_PATH, filepath)
        if not os.path.exists(full_path):
            return None
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def get_float(value, default=0.0):
    """安全地转换为浮点数"""
    try:
        if isinstance(value, (int, float)):
            return float(value)
        return float(value) if value and str(value).strip() else default
    except (ValueError, TypeError):
        return default

def calculate_score(weapon_csv, weapon_json, bullet_json):
    """计算武器综合评分"""
    # 优先从 JSON 中获取数据，如果没有则从 CSV 中获取
    
    # 伤害数据
    bullet_damage = 0.0
    laser_damage = 0.0
    
    if bullet_json:
        bullet_damage = get_float(bullet_json.get('damage', 0))
    if weapon_json:
        laser_damage = get_float(weapon_json.get('laser_damage', 0))
    
    # 从 CSV 作为备选
    if bullet_damage == 0:
        bullet_damage = get_float(weapon_csv.get('bullet_damage', 0))
    if laser_damage == 0:
        laser_damage = get_float(weapon_csv.get('laser_damage', 0))
    
    # 使用有伤害的那个
    damage = bullet_damage if bullet_damage > 0 else laser_damage
    
    # 其他属性
    cooldown = get_float(weapon_json.get('cooldown', 0)) if weapon_json else 0.0
    if cooldown == 0:
        cooldown = get_float(weapon_csv.get('cooldown', 1))
    
    range_val = get_float(weapon_json.get('range', 0)) if weapon_json else 0.0
    if range_val == 0:
        range_val = get_float(weapon_csv.get('range', 0))
    
    accuracy = get_float(weapon_json.get('accuracy_cone_width', 10)) if weapon_json else 10.0
    if accuracy == 10:
        accuracy = get_float(weapon_csv.get('accuracy_cone_width', 10))
    
    ammo_capacity = get_float(weapon_json.get('ammo_capacity', 0)) if weapon_json else 0.0
    if ammo_capacity == 0:
        ammo_capacity = get_float(weapon_csv.get('ammo_capacity', 0))
    
    bullet_speed = get_float(bullet_json.get('speed', 0)) if bullet_json else 0.0
    if bullet_speed == 0:
        bullet_speed = get_float(weapon_csv.get('bullet_speed', 0))
    
    bullet_penetration = get_float(bullet_json.get('penetration', 0)) if bullet_json else 0.0
    if bullet_penetration == 0:
        bullet_penetration = get_float(weapon_csv.get('bullet_penetration', 0))
    
    penetration = get_float(weapon_json.get('penetration', 0)) if weapon_json else 0.0
    if penetration == 0:
        penetration = get_float(weapon_csv.get('penetration', 0))
    
    final_penetration = bullet_penetration if bullet_penetration > 0 else penetration
    
    burst_count = get_float(weapon_json.get('burst_count', 1)) if weapon_json else 1.0
    if burst_count == 1:
        burst_count = get_float(weapon_csv.get('burst_count', 1))
    
    shot_count = get_float(weapon_json.get('shot_count', 1)) if weapon_json else 1.0
    if shot_count == 1:
        shot_count = get_float(weapon_csv.get('shot_count', 1))
    
    per_click_cooldown = get_float(weapon_json.get('per_click_cooldown', 0.1)) if weapon_json else 0.1
    if per_click_cooldown == 0.1:
        per_click_cooldown = get_float(weapon_csv.get('per_click_cooldown', 0.1))
    
    # 处理 cooldown 为 0 的情况
    if cooldown <= 0:
        cooldown = per_click_cooldown
    
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

def main():
    print("正在加载武器数据...")
    
    weapons = []
    
    # 读取 CSV
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
        # 清理表头（移除 BOM 和引号）
        clean_headers = []
        for h in headers:
            clean_h = h.strip('\ufeff').strip('"')
            clean_headers.append(clean_h)
        
        # 处理每一行数据
        for row in reader:
            weapon_info = {}
            for i, h in enumerate(clean_headers):
                if i < len(row):
                    weapon_info[h] = row[i]
            
            weapons.append(weapon_info)
    
    print(f"成功加载 {len(weapons)} 个武器数据")
    
    print("\n正在加载 JSON 文件并计算武器评分...")
    scored_weapons = []
    
    for weapon_csv in weapons:
        weapon_filename = weapon_csv.get('filename', '')
        bullet_filename = weapon_csv.get('bullet', '')
        
        # 加载 JSON 文件
        weapon_json = load_json(weapon_filename)
        bullet_json = load_json(bullet_filename)
        
        # 计算评分
        scores = calculate_score(weapon_csv, weapon_json, bullet_json)
        
        weapon_name = weapon_csv.get('name', 'Unknown')
        
        scored_weapons.append({
            'name': weapon_name,
            'filename': weapon_filename,
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
        print(f"{i}. {weapon['name']} - 评分: {weapon['total_score']:.2f} - DPS: {weapon['dps']:.2f}")
    
    # 更新待办事项
    return scored_weapons

if __name__ == "__main__":
    main()
