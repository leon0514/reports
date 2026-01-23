import sys
import re

def parse_markdown(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    # 辅助函数：提取段落内容
    def get_section(title):
        # 匹配 "### 标题" 到下一个 "###" 或文件结尾之间的内容
        pattern = re.compile(rf'### {title}\s*(.*?)\s*(?=###|$)', re.DOTALL)
        match = pattern.search(content)
        if match:
            text = match.group(1).strip()
            # 将 Markdown 的列表项 (1. 或 -) 转换为 HTML 的 <div style="margin-bottom: 5px;">
            lines = text.split('\n')
            html_lines = []
            for line in lines:
                clean_line = line.strip()
                if clean_line:
                    # 简单的格式清洗
                    html_lines.append(f'<div style="margin-bottom: 4px;">{clean_line}</div>')
            return "".join(html_lines)
        return "暂无内容"

    # 提取主标题 (# 后面)
    title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    report_title = title_match.group(1) if title_match else "周报"

    return {
        "title": report_title,
        "done": get_section("本周完成情况"),
        "plan": get_section("下周工作计划"),
        "help": get_section("需协调事项"),
        "other": get_section("其他问题和建议")
    }

def generate_html(data):
    # 使用内联 CSS 确保兼容 QQ/Outlook/Gmail
    html = f"""
    <!DOCTYPE html>
    <html>
    <body>
    <table border="1" cellspacing="0" cellpadding="0" style="width: 100%; max-width: 800px; border-collapse: collapse; font-family: 'Microsoft YaHei', Arial, sans-serif; font-size: 14px; color: #333;">
        
        <!-- 1. 顶部标题 -->
        <tr style="background-color: #E7E6E6;">
            <td colspan="4" style="padding: 15px; text-align: center; font-weight: bold; font-size: 16px; border: 1px solid #999;">
                AI应用研发部 - 唐立杨 【AI算法工程师】 - {data['title']}
            </td>
        </tr>

        <!-- 2. 黄色表头 -->
        <tr style="background-color: #FFFF00; font-weight: bold;">
            <td style="width: 10%; background-color: #ffffff; border: 1px solid #999; border-right: none;"></td>
            <td style="width: 30%; padding: 10px; border: 1px solid #999;">本周完成情况</td>
            <td style="width: 30%; padding: 10px; border: 1px solid #999;">下周工作计划</td>
            <td style="width: 30%; padding: 10px; border: 1px solid #999;">需协调事项</td>
        </tr>

        <!-- 3.主要内容区 -->
        <tr>
            <td style="background-color: #f9f9f9; font-weight: bold; text-align: center; padding: 10px; border: 1px solid #999; vertical-align: middle;">
                内容描述
            </td>
            <td style="padding: 10px; border: 1px solid #999; vertical-align: top; height: 150px;">
                {data['done']}
            </td>
            <td style="padding: 10px; border: 1px solid #999; vertical-align: top;">
                {data['plan']}
            </td>
            <td style="padding: 10px; border: 1px solid #999; vertical-align: top;">
                {data['help']}
            </td>
        </tr>

        <!-- 4. 底部其他问题 -->
        <tr>
            <td style="background-color: #f9f9f9; font-weight: bold; text-align: center; padding: 10px; border: 1px solid #999;">
                其他问题<br>和建议
            </td>
            <td colspan="3" style="padding: 10px; border: 1px solid #999;">
                {data['other']}
            </td>
        </tr>
    </table>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_to_html.py <path_to_md_file>", file=sys.stderr)
        sys.exit(1)
        
    file_path = sys.argv[1]
    data = parse_markdown(file_path)
    html_content = generate_html(data)
    
    # 直接打印到控制台，不写入文件，由外部 Shell 处理
    print(html_content)