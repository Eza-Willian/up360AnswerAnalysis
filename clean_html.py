import re
import sys
import os

def clean_html(text):
    return re.sub(r'<[^>]+>', '', text)

def main(input_path):
    # if len(sys.argv) < 2:
    #     print("用法: python clean_html.py <文件路径>")
    #     sys.exit(1)
    
    # input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"文件不存在: {input_path}")
        sys.exit(1)
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cleaned = clean_html(content)
    
    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_clean{ext}"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    
    print(f"清洗完成，输出文件: {output_path}")

if __name__ == "__main__":
    input_path = input('请输入文件路径：')
    main(input_path)
