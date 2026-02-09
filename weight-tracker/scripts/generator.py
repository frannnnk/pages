#!/usr/bin/env python3
"""
Frank's Weight Tracker - Page Generator
Usage: python3 generator.py

Input format (JSON):
{
    "date": "2026-02-10",
    "time": "08:30",
    "weight": 88.5,
    "bmi": 28.8,
    "body_fat": 31.2,
    "visceral_fat": 11.2,
    "muscle_mass": 57.0,
    "bmr": 1665,
    "protein": 11.6,
    "body_age": 40,
    "food": [
        {"meal": "早餐", "desc": "奶茶+三明治", "calories": "约500kcal"},
        {"meal": "午餐", "desc": "叉烧饭", "calories": "约700kcal"}
    ],
    "exercise": [
        {"desc": "快走30分钟", "calories": "约200kcal"}
    ],
    "notes": "今天感觉不错，继续努力！",
    "images": ["photo1.jpg", "photo2.jpg"]
}
"""

import json
import os
from datetime import datetime

def generate_index(entries):
    """Generate the index.html with entry list"""
    
    entries_html = ""
    
    for entry in entries:
        food_summary = ""
        if entry.get('food'):
            # Generate food summary from first meal or default
            first_meal = entry['food'][0] if entry['food'] else None
            if first_meal:
                food_summary = f"早餐：{first_meal['desc']}"
        
        entries_html += f'''
            <div class="entry-card">
                <div class="entry-header">
                    <div>
                        <div class="entry-date">{entry['date']}</div>
                        <div class="entry-time">{entry.get('time', '')}</div>
                    </div>
                </div>
                <div class="entry-summary">
                    <div class="summary-item">
                        <div class="summary-label">体重</div>
                        <div class="summary-value">{entry['weight']}<span class="summary-unit"> kg</span></div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-label">BMI</div>
                        <div class="summary-value">{entry.get('bmi', '')}</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-label">体脂率</div>
                        <div class="summary-value">{entry.get('body_fat', '')}<span class="summary-unit">%</span></div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-label">内脏脂肪</div>
                        <div class="summary-value">{entry.get('visceral_fat', '')}</div>
                    </div>
                </div>
                {f'''<div class="entry-food">
                    <div class="entry-food-label">📝 饮食记录</div>
                    <div class="entry-food-text">{food_summary}</div>
                </div>''' if food_summary else ''}
                {f'''<div class="entry-food" style="background: #fef3c7; border-color: #fbbf24;">
                    <div class="entry-food-label" style="color: #fbbf24;">🏃 运动记录</div>
                    <div class="entry-food-text">{entry.get('exercise', [{}])[0].get('desc', '')}</div>
                </div>''' if entry.get('exercise') else ''}
                <a href="{entry['date']}/" class="entry-link">查看详情 →</a>
            </div>'''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Frank's Weight Tracker</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(180deg, #e8f4f8 0%, #f5fafc 50%, #ffffff 100%);
            min-height: 100vh;
            color: #334155;
            padding: 30px 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            color: #0ea5e9;
            font-size: 2rem;
            margin-bottom: 8px;
        }}
        .subtitle {{
            text-align: center;
            color: #94a3b8;
            margin-bottom: 40px;
            font-size: 0.95rem;
        }}
        .entries {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}
        .entry-card {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 2px 12px rgba(14, 165, 233, 0.08);
            border: 1px solid #e0f2fe;
            transition: all 0.3s;
        }}
        .entry-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(14, 165, 233, 0.15);
        }}
        .entry-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }}
        .entry-date {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #0ea5e9;
        }}
        .entry-time {{
            font-size: 0.85rem;
            color: #94a3b8;
        }}
        .entry-summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 12px;
            margin-bottom: 16px;
        }}
        .summary-item {{
            text-align: center;
            padding: 12px;
            background: #f0f9ff;
            border-radius: 10px;
        }}
        .summary-label {{
            font-size: 0.75rem;
            color: #7dd3fc;
            margin-bottom: 4px;
        }}
        .summary-value {{
            font-size: 1.2rem;
            font-weight: 600;
            color: #0284c7;
        }}
        .summary-unit {{
            font-size: 0.8rem;
            color: #94a3b8;
        }}
        .entry-food {{
            padding: 12px 16px;
            background: #f0fdf4;
            border-radius: 10px;
            border-left: 3px solid #4ade80;
            margin-bottom: 12px;
        }}
        .entry-food-label {{
            font-size: 0.75rem;
            color: #4ade80;
            margin-bottom: 4px;
        }}
        .entry-food-text {{
            font-size: 0.9rem;
            color: #166534;
            line-height: 1.5;
        }}
        .entry-link {{
            display: inline-block;
            padding: 8px 16px;
            background: linear-gradient(135deg, #0ea5e9, #0284c7);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.3s;
        }}
        .entry-link:hover {{
            background: linear-gradient(135deg, #0284c7, #0369a1);
            transform: translateY(-1px);
        }}
        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: #94a3b8;
        }}
        .empty-icon {{
            font-size: 3rem;
            margin-bottom: 16px;
        }}
        .empty-text {{
            font-size: 1rem;
        }}
        @media (max-width: 600px) {{
            .entry-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 4px;
            }}
            .entry-summary {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Frank's Weight Tracker</h1>
        <p class="subtitle">体重追踪 & 身体数据记录</p>
        <div class="entries" id="entries">
            {entries_html if entries_html else '''
            <div class="empty-state">
                <div class="empty-icon">📊</div>
                <div class="empty-text">还没有记录</div>
                <div class="empty-text">开始你的健康之旅吧！</div>
            </div>'''}
        </div>
    </div>
</body>
</html>'''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

def generate_entry(entry):
    """Generate the entry page for a specific date"""
    
    date = entry['date']
    date_formatted = f"{date[0:4]}年{date[5:7]}月{date[8:10]}日"
    
    # Generate food HTML
    food_html = ""
    if entry.get('food'):
        food_items = ""
        for item in entry['food']:
            food_items += f'''
            <li class="food-item">
                <div class="food-meal">{item['meal']}</div>
                <div class="food-desc">{item['desc']}</div>
                {f'''<div class="food-cal">{item.get('calories', '')}</div>''' if item.get('calories') else ''}
            </li>'''
        food_html = f'''
        <div class="section food-section">
            <div class="section-title">🍽️ 饮食记录</div>
            <ul class="food-list">
                {food_items}
            </ul>
        </div>'''
    
    # Generate exercise HTML
    exercise_html = ""
    if entry.get('exercise'):
        exercise_items = ""
        for item in entry['exercise']:
            exercise_items += f'''
            <div class="exercise-item">
                <div class="exercise-desc">{item['desc']}</div>
                {f'''<div class="exercise-cal">{item.get('calories', '')}</div>''' if item.get('calories') else ''}
            </div>'''
        exercise_html = f'''
        <div class="section exercise-section">
            <div class="section-title">🏃 运动记录</div>
            {exercise_items}
        </div>'''
    
    # Generate notes HTML
    notes_html = ""
    if entry.get('notes'):
        notes_html = f'''
        <div class="section notes-section">
            <div class="section-title">📝 备注</div>
            <div class="notes-text">{entry['notes']}</div>
        </div>'''
    
    # Generate images HTML
    images_html = ""
    if entry.get('images'):
        images_grid = ""
        for img in entry['images']:
            images_grid += f'''
            <div class="image-item">
                <img src="images/{img}" alt="{img}">
            </div>'''
        images_html = f'''
        <div class="images-section">
            <div class="section-title">📷 图片</div>
            <div class="images-grid">
                {images_grid}
            </div>
        </div>'''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{date_formatted} - Frank's Weight Tracker</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(180deg, #e8f4f8 0%, #f5fafc 50%, #ffffff 100%);
            min-height: 100vh;
            color: #334155;
            padding: 30px 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            color: #0ea5e9;
            text-decoration: none;
            font-size: 0.9rem;
            margin-bottom: 24px;
            transition: color 0.3s;
        }}
        .back-link:hover {{
            color: #0284c7;
        }}
        .header {{
            text-align: center;
            margin-bottom: 32px;
        }}
        .date {{
            font-size: 2rem;
            font-weight: 600;
            color: #0ea5e9;
            margin-bottom: 4px;
        }}
        .time {{
            color: #94a3b8;
            font-size: 1rem;
        }}
        .section {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 2px 12px rgba(14, 165, 233, 0.08);
            border: 1px solid #e0f2fe;
        }}
        .section-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #0ea5e9;
            margin-bottom: 16px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 12px;
        }}
        .stat-card {{
            text-align: center;
            padding: 16px 12px;
            background: #f0f9ff;
            border-radius: 12px;
        }}
        .stat-label {{
            font-size: 0.8rem;
            color: #7dd3fc;
            margin-bottom: 6px;
        }}
        .stat-value {{
            font-size: 1.4rem;
            font-weight: 600;
            color: #0284c7;
        }}
        .stat-unit {{
            font-size: 0.85rem;
            color: #94a3b8;
        }}
        .food-section {{
            background: #f0fdf4;
            border-color: #4ade80;
        }}
        .food-section .section-title {{
            color: #16a34a;
        }}
        .food-list {{
            list-style: none;
        }}
        .food-item {{
            padding: 12px 0;
            border-bottom: 1px solid #dcfce7;
        }}
        .food-item:last-child {{
            border-bottom: none;
        }}
        .food-meal {{
            font-size: 0.85rem;
            color: #4ade80;
            margin-bottom: 4px;
        }}
        .food-desc {{
            font-size: 0.95rem;
            color: #166534;
            line-height: 1.5;
        }}
        .food-cal {{
            font-size: 0.8rem;
            color: #22c55e;
            margin-top: 4px;
        }}
        .exercise-section {{
            background: #fefce8;
            border-color: #fbbf24;
        }}
        .exercise-section .section-title {{
            color: #ca8a04;
        }}
        .exercise-item {{
            padding: 12px 0;
            border-bottom: 1px solid #fef3c7;
        }}
        .exercise-item:last-child {{
            border-bottom: none;
        }}
        .exercise-desc {{
            font-size: 0.95rem;
            color: #854d0e;
            line-height: 1.5;
        }}
        .exercise-cal {{
            font-size: 0.8rem;
            color: #ca8a04;
            margin-top: 4px;
        }}
        .notes-section {{
            background: #faf5ff;
            border-color: #c084fc;
        }}
        .notes-section .section-title {{
            color: #9333ea;
        }}
        .notes-text {{
            font-size: 0.95rem;
            color: #6b21a8;
            line-height: 1.6;
        }}
        .images-section {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 2px 12px rgba(14, 165, 233, 0.08);
            border: 1px solid #e0f2fe;
        }}
        .images-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }}
        .image-item {{
            border-radius: 12px;
            overflow: hidden;
        }}
        .image-item img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .empty-text {{
            color: #94a3b8;
            text-align: center;
            padding: 20px;
        }}
        @media (max-width: 600px) {{
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../" class="back-link">← 返回列表</a>

        <div class="header">
            <div class="date">{date_formatted}</div>
            <div class="time">测量时间：{entry.get('time', '')}</div>
        </div>

        <div class="section">
            <div class="section-title">📊 身体数据</div>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">体重</div>
                    <div class="stat-value">{entry['weight']}<span class="stat-unit"> kg</span></div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">BMI</div>
                    <div class="stat-value">{entry.get('bmi', '')}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">体脂率</div>
                    <div class="stat-value">{entry.get('body_fat', '')}<span class="stat-unit">%</span></div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">内脏脂肪</div>
                    <div class="stat-value">{entry.get('visceral_fat', '')}<span class="stat-unit">级</span></div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">肌肉量</div>
                    <div class="stat-value">{entry.get('muscle_mass', '')}<span class="stat-unit"> kg</span></div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">基础代谢</div>
                    <div class="stat-value">{entry.get('bmr', '')}<span class="stat-unit"> kcal</span></div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">蛋白质</div>
                    <div class="stat-value">{entry.get('protein', '')}<span class="stat-unit"> kg</span></div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">身体年龄</div>
                    <div class="stat-value">{entry.get('body_age', '')}<span class="stat-unit"> 岁</span></div>
                </div>
            </div>
        </div>

        {food_html}
        {exercise_html}
        {notes_html}
        {images_html}
    </div>
</body>
</html>'''
    
    # Create directory
    os.makedirs(date, exist_ok=True)
    os.makedirs(f'{date}/images', exist_ok=True)
    
    # Write HTML
    with open(f'{date}/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Created entry page: {date}/")

def main():
    """Main function to generate all pages"""
    # Load existing entries or create empty list
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            entries = json.load(f)
    except FileNotFoundError:
        entries = []
    
    # Sort by date (newest first)
    entries.sort(key=lambda x: x['date'], reverse=True)
    
    # Generate index
    generate_index(entries)
    print("✓ Updated index.html")
    
    # Generate entry pages
    for entry in entries:
        generate_entry(entry)
    
    print(f"\n✓ Generated {len(entries)} entry pages")

if __name__ == '__main__':
    main()
