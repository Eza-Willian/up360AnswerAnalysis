import os
import re
import shutil

def get_topic_number(folder_path):
    """
    从文件夹的media子目录中查找T*.mp3文件，提取题号数字（两位数）
    例如 T1-ZC.mp3 → "01"
    如果找不到，返回 "XX"
    """
    media_path = os.path.join(folder_path, 'media')
    if not os.path.isdir(media_path):
        return "XX"
    
    # 查找所有包含T的mp3文件
    mp3_files = [f for f in os.listdir(media_path) 
                 if f.lower().endswith('.mp3') and 'T' in f]
    if not mp3_files:
        return "XX"
    
    # 取第一个文件（与原批处理行为一致：只处理第一个找到的）
    filename = mp3_files[0]
    # 提取T后面的连续数字
    match = re.search(r'T(\d+)', filename)
    if match:
        num = match.group(1)
        # 格式化为两位数（如1→01）
        return num.zfill(2)
    return "XX"

def find_js_file(folder_path):
    """
    在文件夹中查找JS文件：
    1. 先查找net子目录下的第一个.js文件
    2. 若未找到，再查找当前目录下的第一个.js文件
    返回文件完整路径，若未找到返回None
    """
    # 尝试net文件夹
    net_path = os.path.join(folder_path, 'net')
    if os.path.isdir(net_path):
        js_files = [f for f in os.listdir(net_path) if f.lower().endswith('.js')]
        if js_files:
            return os.path.join(net_path, js_files[0])
    
    # 尝试当前文件夹根目录
    js_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.js')]
    if js_files:
        return os.path.join(folder_path, js_files[0])
    
    return None

def clean_html(text):
    return re.sub(r'<[^>]+>', '', text)

def main(source_path, output_path):
    # # 设置控制台颜色（仅Windows，可选）
    # if os.name == 'nt':
    #     os.system('color 0A')
    #     os.system('title JS文件提取与合并工具')
    
    print("JS文件提取与合并工具")
    print("=" * 40)

    # 获取源文件夹路径
    while True:
        
        if not source_path:
            continue
        questions_path = os.path.join(source_path, 'questions')
        if os.path.isdir(questions_path):
            break
        print("错误: 路径下未找到questions文件夹!")
    
    # 获取输出文件夹路径
    while True:
        
        if not output_path:
            continue
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f"创建输出文件夹: {output_path}")
        break

    print(f"\n正在处理: {questions_path}")
    print(f"输出到: {output_path}\n")

    # 统计
    folder_count = 0
    file_count = 0
    # 用于合并的记录列表，每个元素为 (排序键, 文件路径)
    js_records = []

    # 遍历questions下的所有子文件夹
    for item in os.listdir(questions_path):
        folder_full = os.path.join(questions_path, item)
        if not os.path.isdir(folder_full):
            continue
        
        folder_count += 1
        folder_name = item
        print(f"处理文件夹: {folder_name}")

        # 提取题号
        topic_num = get_topic_number(folder_full)

        # 查找JS文件
        js_path = find_js_file(folder_full)
        if not js_path:
            print("  未找到JS文件，跳过")
            continue

        js_filename = os.path.basename(js_path)
        # 新文件名格式: T{两位数题号}_{文件夹名}_{原文件名}
        new_name = f"T{topic_num}_{folder_name}_{js_filename}"
        dest_path = os.path.join(output_path, new_name)

        # 复制文件
        try:
            shutil.copy2(js_path, dest_path)
            print(f"  已复制: {new_name}")
        except Exception as e:
            print(f"  复制失败: {e}")
            continue

        # 记录用于合并
        js_records.append((topic_num, js_path))
        file_count += 1

    print(f"\n共处理 {folder_count} 个文件夹, 提取 {file_count} 个JS文件")

    # 合并JS文件
    if js_records:
        combined_js = os.path.join(output_path, 'combined.js')
        print(f"\n正在合并JS文件到: {combined_js}")

        # 按题号排序（字符串排序，确保"XX"排在数字后面）
        js_records.sort(key=lambda x: x[0])

        with open(combined_js, 'w', encoding='utf-8') as out_f:
            for _, js_path in js_records:
                try:
                    with open(js_path, 'r', encoding='utf-8') as in_f:
                        out_f.write(clean_html(in_f.read()))
                        out_f.write('\n')  # 每个文件后加一个空行
                except Exception as e:
                    print(f"  合并文件 {js_path} 时出错: {e}")

        print(f"合并完成! 输出文件: {combined_js}")
    else:
        print("没有找到任何JS文件，跳过合并。")

    print("\n操作全部完成!")
    # input("按回车键退出...")

if __name__ == "__main__":
    source_path = input("请输入源文件夹路径(包含questions目录): ").strip().strip('"')
    output_path = input("请输入输出文件夹路径: ").strip().strip('"')
    main(source_path, output_path)
