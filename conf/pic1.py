import pandas as pd
import plotly.graph_objects as go
import os

# 获取当前工作目录并列出文件
print("当前工作目录:", os.getcwd())
print("目录中的文件:")
for file in os.listdir('.'):
    if file.endswith('.xlsx'):
        print(f"  - {file}")

# 让用户输入文件路径或使用默认路径
file_path = input("请输入Excel文件路径(或直接按Enter使用默认路径): ").strip()
if not file_path:
    file_path = '1-10月主要产品出口国别对比.xlsx'

# 检查文件是否存在
if not os.path.exists(file_path):
    print(f"错误: 文件 '{file_path}' 不存在!")
    print("请确保文件路径正确，或者将文件放在当前目录下。")
    exit(1)

print(f"正在读取文件: {file_path}")

# 读取Excel文件
try:
    df = pd.read_excel(file_path, header=None, engine='openpyxl')
    print("文件读取成功!")
except Exception as e:
    print(f"读取文件时出错: {e}")
    print("请确保已安装 openpyxl: pip install openpyxl")
    exit(1)


# 预处理数据：提取各个排行榜
def extract_ranking_data(df, category_name):
    """提取指定类别的排行榜数据"""
    data = []
    collecting = False

    for idx, data_row in df.iterrows():
        # 检查是否开始收集数据
        if isinstance(data_row[0], str) and category_name in data_row[0]:
            collecting = True
            continue

        # 检查是否到达下一个类别或数据结束
        if collecting and isinstance(data_row[0], str) and '排名' not in str(data_row[0]) and data_row[
            0] and '累计' not in str(data_row[0]) and data_row[0] != category_name:
            break

        # 收集数据行
        if collecting and pd.notna(data_row[0]):
            # 检查是否为排名行（包含数字排名）
            if str(data_row[0]).strip().replace('.', '').isdigit():
                country = data_row[1]
                # 处理特殊地区名称
                if country == '台湾省':
                    country_en = 'Taiwan'
                    country_cn = '台湾省'
                elif country == '香港地区':
                    country_en = 'Hong Kong'
                    country_cn = '香港地区'
                else:
                    country_en = country
                    country_cn = country

                try:
                    value = float(data_row[2]) if pd.notna(data_row[2]) else 0
                except:
                    value = 0

                data.append({
                    'Country_EN': country_en,
                    'Country_CN': country_cn,
                    'Value': value,
                    'Growth': data_row[3] if pd.notna(data_row[3]) and data_row[3] != '-' else 0
                })

    return pd.DataFrame(data)


# 获取所有类别
categories = [
    '汽车及其零部件',
    '家用电器',
    '液晶显示',
    '光伏产品',
    '蓄电池储能',
    '机械制造',
    '集成电路',
    '六大劳动密集型产品',
    '纺织服装',
    '自动数据处理设备'
]

print(f"\n找到 {len(categories)} 个类别:")
for i, category in enumerate(categories, 1):
    print(f"  {i}. {category}")

# 国家名称映射（中文到英文）用于地图定位
country_mapping = {
    '俄罗斯': 'Russia',
    '英国': 'United Kingdom',
    '西班牙': 'Spain',
    '以色列': 'Israel',
    '巴西': 'Brazil',
    '墨西哥': 'Mexico',
    '德国': 'Germany',
    '阿联酋': 'United Arab Emirates',
    '澳大利亚': 'Australia',
    '伊朗': 'Iran',
    '南非': 'South Africa',
    '土耳其': 'Turkey',
    '波兰': 'Poland',
    '马来西亚': 'Malaysia',
    '意大利': 'Italy',
    '哈萨克斯坦': 'Kazakhstan',
    '埃及': 'Egypt',
    '印度尼西亚': 'Indonesia',
    '智利': 'Chile',
    '沙特阿拉伯': 'Saudi Arabia',
    '美国': 'United States',
    '日本': 'Japan',
    '韩国': 'South Korea',
    '加拿大': 'Canada',
    '菲律宾': 'Philippines',
    '法国': 'France',
    '越南': 'Vietnam',
    '印度': 'India',
    '荷兰': 'Netherlands',
    '斯洛文尼亚': 'Slovenia',
    '巴基斯坦': 'Pakistan',
    '泰国': 'Thailand',
    '马绍尔群岛': 'Marshall Islands',
    '新加坡': 'Singapore',
    'Taiwan': 'Taiwan',
    'Hong Kong': 'Hong Kong'
}

# 红黄色系颜色方案
red_yellow_color_scales = {
    'YlOrRd': '黄色到红色',
    'RdYlBu': '红色-黄色-蓝色',
    'Hot': '热力图色系',
    'Reds': '红色系',
    'OrRd': '橙色到红色',
    'YlOrBr': '黄色到棕色'
}

print("\n可用的红黄色系颜色方案:")
for i, (scale, name) in enumerate(red_yellow_color_scales.items(), 1):
    print(f"  {i}. {scale} - {name}")

# 选择颜色方案
color_choice = input("\n请选择颜色方案编号(1-6，默认1): ").strip()
color_choices = list(red_yellow_color_scales.keys())
if color_choice.isdigit() and 1 <= int(color_choice) <= 6:
    selected_color = color_choices[int(color_choice) - 1]
else:
    selected_color = 'YlOrRd'

print(f"使用颜色方案: {selected_color} ({red_yellow_color_scales[selected_color]})")

# 创建输出目录
output_dir = f"出口热力图_{selected_color}"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"创建输出目录: {output_dir}")

print("\n正在提取数据...")
data_summary = {}
for category in categories:
    data_df = extract_ranking_data(df, category)

    # 对未映射的国家使用映射表
    for idx, row_data in data_df.iterrows():
        if row_data['Country_CN'] in country_mapping and row_data['Country_EN'] == row_data['Country_CN']:
            data_df.at[idx, 'Country_EN'] = country_mapping[row_data['Country_CN']]

    data_summary[category] = data_df
    print(f"{category}: 提取到 {len(data_df)} 行数据")

print("\n正在为每个类别生成单独的热力图...")

# 为每个类别生成单独的热力图文件
for category in categories:
    print(f"\n处理类别: {category}")

    data_df = data_summary[category]

    if data_df.empty:
        print(f"  警告: 未找到类别 '{category}' 的数据，跳过")
        continue

    print(f"  处理 {len(data_df)} 个国家/地区的数据")

    # 准备悬停文本（包含中文国家名称）
    hover_texts = []
    for idx, row_data in data_df.iterrows():
        hover_text = f"<b>{row_data['Country_CN']}</b><br>"
        hover_text += f"类别: {category}<br>"
        hover_text += f"出口额: {row_data['Value']:.2f}亿元<br>"
        # 检查增幅是否为数值类型
        growth = row_data['Growth']
        if isinstance(growth, (int, float)):
            hover_text += f"增幅: {growth}%"
        else:
            hover_text += f"增幅: {growth}"
        hover_texts.append(hover_text)

    # 创建单独的热力图
    fig = go.Figure(data=go.Choropleth(
        locations=data_df['Country_EN'],
        z=data_df['Value'],
        locationmode='country names',
        colorscale=selected_color,
        colorbar=dict(
            title=dict(
                text=f"出口额(亿元)<br>{category}",
                font=dict(size=14)
            ),
            len=0.7,
            thickness=20,
            x=1.02,  # 颜色条在右侧
            y=0.5,
            xanchor='left',
            yanchor='middle',
            orientation='v',
            tickfont=dict(size=12)
        ),
        hovertext=hover_texts,
        hoverinfo='text',
        showscale=True,
        zmin=0,
        zmax=data_df['Value'].max() * 1.1 if not data_df.empty else 1
    ))

    # 更新布局
    fig.update_layout(
        title=dict(
            text=f'1-10月 {category} 出口国别热力图',
            font=dict(size=24, family='Microsoft YaHei'),
            x=0.5,
            xanchor='center'
        ),
        height=800,
        width=1200,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            showland=True,
            landcolor="white",
            showocean=True,
            oceancolor="lightblue",
            showcountries=True,
            countrycolor="lightgray",
            coastlinecolor="darkgray",
            projection_type='natural earth'
        ),
        margin=dict(l=0, r=120, t=80, b=0),
        font=dict(family='Microsoft YaHei')
    )

    # 添加数据表格作为注释
    if len(data_df) > 0:
        # 按出口额排序
        sorted_df = data_df.sort_values('Value', ascending=False).head(10)

        # 创建表格文本
        table_text = "<b>Top 10 出口国家/地区:</b><br>"
        table_text += "<table style='border-collapse: collapse;'>"
        table_text += "<tr><th style='border: 1px solid black; padding: 5px;'>排名</th>"
        table_text += "<th style='border: 1px solid black; padding: 5px;'>国家/地区</th>"
        table_text += "<th style='border: 1px solid black; padding: 5px;'>出口额(亿元)</th>"
        table_text += "<th style='border: 1px solid black; padding: 5px;'>增幅(%)</th></tr>"

        for i, (idx, row) in enumerate(sorted_df.iterrows(), 1):
            growth = row['Growth']
            if isinstance(growth, (int, float)):
                growth_str = f"{growth:.2f}%"
            else:
                growth_str = str(growth)

            table_text += f"<tr><td style='border: 1px solid black; padding: 5px;'>{i}</td>"
            table_text += f"<td style='border: 1px solid black; padding: 5px;'>{row['Country_CN']}</td>"
            table_text += f"<td style='border: 1px solid black; padding: 5px;'>{row['Value']:.2f}</td>"
            table_text += f"<td style='border: 1px solid black; padding: 5px;'>{growth_str}</td></tr>"

        table_text += "</table>"

        # 添加表格注释
        fig.add_annotation(
            x=0.02,
            y=0.98,
            xref="paper",
            yref="paper",
            text=table_text,
            showarrow=False,
            font=dict(size=10, family='Microsoft YaHei'),
            align="left",
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="black",
            borderwidth=1,
            borderpad=4
        )

    # 保存为HTML文件
    filename = os.path.join(output_dir, f"{category}_热力图_{selected_color}.html")
    fig.write_html(filename, include_plotlyjs=True, full_html=True)

    print(f"  已保存: {filename}")

    # 生成简单的统计信息
    if len(data_df) > 0:
        total_export = data_df['Value'].sum()
        avg_export = data_df['Value'].mean()
        max_export = data_df['Value'].max()
        max_country = data_df.loc[data_df['Value'].idxmax(), 'Country_CN']

        print(f"  统计信息:")
        print(f"    - 总出口额: {total_export:.2f} 亿元")
        print(f"    - 平均出口额: {avg_export:.2f} 亿元")
        print(f"    - 最大出口额: {max_export:.2f} 亿元 ({max_country})")

# 创建汇总索引页面
print(f"\n正在创建汇总索引页面...")

index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>安徽省2025年1-10月主要产品出口国别对比热力图汇总</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #e74c3c;
            padding-bottom: 10px;
        }}
        .info {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
            border-left: 4px solid #3498db;
        }}
        .category-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .category-card {{
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .category-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        .category-card h3 {{
            color: #2c3e50;
            margin-bottom: 10px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .category-card a {{
            display: inline-block;
            background-color: #e74c3c;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 15px;
            transition: background-color 0.3s;
        }}
        .category-card a:hover {{
            background-color: #c0392b;
        }}
        .stats {{
            font-size: 14px;
            color: #666;
            margin-top: 10px;
        }}
        .color-scheme {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }}
        .timestamp {{
            text-align: right;
            color: #777;
            font-size: 14px;
            margin-top: 30px;
            padding-top: 10px;
            border-top: 1px solid #eee;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>安徽省2025年1-10月主要产品出口国别对比热力图汇总</h1>

        <div class="info">
            <p><strong>数据说明：</strong>本页面展示了安徽省2025年1-10月主要产品的出口情况。每个热力图显示了各产品类别的前10个主要出口目的地。</p>
            <p><strong>颜色方案：</strong>使用了{red_yellow_color_scales[selected_color]} ({selected_color}) 颜色方案，颜色越深表示出口额越高。</p>
            <p><strong>交互功能：</strong>鼠标悬停在地图上可以查看具体国家的出口数据和增幅。</p>
        </div>

        <div class="color-scheme">
            <strong>当前颜色方案：</strong> {red_yellow_color_scales[selected_color]} ({selected_color})
        </div>

        <div class="category-grid">
"""

# 为每个类别添加卡片
for category in categories:
    data_df = data_summary[category]

    if data_df.empty:
        continue

    # 计算统计信息
    total_export = data_df['Value'].sum()
    country_count = len(data_df)
    max_export = data_df['Value'].max()
    max_country = data_df.loc[data_df['Value'].idxmax(), 'Country_CN']

    index_html += f"""
            <div class="category-card">
                <h3>{category}</h3>
                <div class="stats">
                    <p>覆盖国家/地区: {country_count}个</p>
                    <p>总出口额: {total_export:.2f}亿元</p>
                    <p>最大出口国: {max_country} ({max_export:.2f}亿元)</p>
                </div>
                <a href="{category}_热力图_{selected_color}.html" target="_blank">查看详细热力图</a>
            </div>
"""

index_html += f"""
        </div>

        <div class="timestamp">
            生成时间: {pd.Timestamp.now().strftime('%Y年%m月%d日 %H:%M:%S')}
        </div>
    </div>

    <script>
        // 添加简单的交互效果
        document.addEventListener('DOMContentLoaded', function() {{
            const cards = document.querySelectorAll('.category-card');
            cards.forEach(card => {{
                card.addEventListener('mouseenter', function() {{
                    this.style.borderColor = '#e74c3c';
                }});
                card.addEventListener('mouseleave', function() {{
                    this.style.borderColor = '#ddd';
                }});
            }});
        }});
    </script>
</body>
</html>
"""

# 保存索引页面
index_file = os.path.join(output_dir, "index.html")
with open(index_file, 'w', encoding='utf-8') as f:
    f.write(index_html)

print(f"汇总索引页面已保存: {index_file}")
print(f"所有文件已保存到目录: {output_dir}")

# 询问是否要打开索引页面
open_file = input(f"\n是否要立即在浏览器中打开汇总索引页面? (y/n): ").strip().lower()
if open_file == 'y':
    import webbrowser

    webbrowser.open(index_file)
    print("已在浏览器中打开汇总索引页面!")
else:
    print(f"您可以在浏览器中手动打开 '{index_file}' 文件查看所有热力图。")

print("\n完成!")
print(f"\n生成了以下文件:")
print(f"1. 汇总索引页面: {index_file}")
print(f"2. 10个单独的热力图文件，每个文件包含:")
print(f"   - 完整的世界地图热力图")
print(f"   - 右侧独立的颜色条（图例）")
print(f"   - 鼠标悬停显示中文国家名称")
print(f"   - Top 10 出口国家/地区表格")
print(f"   - 使用 {selected_color} 颜色方案")

print(f"\n打开 {index_file} 可以查看所有热力图的链接和统计信息。")