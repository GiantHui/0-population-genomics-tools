# ==== 配置区：请在此处修改输入和输出文件路径 ====
xml_path = "/mnt/c/Users/Administrator/Desktop/Pro_补充3.xml"
csv_path = "/mnt/c/Users/Administrator/Desktop/Pro_补充3_extracted_params.csv"
# ===============================================

import re
import csv

def extract_samples(xml_text):
    sample_pattern = re.compile(r'== Sample :\s+([^\n\r]+)')
    sample_matches = list(sample_pattern.finditer(xml_text))
    samples = []
    for i, match in enumerate(sample_matches):
        name = match.group(1).strip()
        start = match.start()
        end = sample_matches[i+1].start() if i+1 < len(sample_matches) else len(xml_text)
        samples.append((name, start, end))
    return samples

def show_first_sample_params(xml_text, samples):
    name, start, end = samples[0]
    block = xml_text[start:end]
    # 只保留虚线包裹的小标题和<data>后带冒号的行（冒号前内容）
    lines = block.splitlines()
    show_lines = []
    in_data = False
    for line in lines:
        # 虚线包裹的小标题
        if re.match(r'^[=]{10,}', line) or re.match(r'^[=]{2,} .+ [=]{2,}', line):
            show_lines.append(line)
        # <data>标签后开始提取
        if '<data>' in line:
            in_data = True
            continue
        if '</data>' in line:
            in_data = False
            continue
        if in_data:
            m = re.match(r'^(\s*[^:]+):', line)
            if m:
                show_lines.append(m.group(1))
    print(f"第一个群体参数选择参考如下（{name}）：\n")
    print('\n'.join(show_lines))
    print("\n请依次输入你需要保留的参数（每行一个，输入完后直接回车结束）：")
    params = []
    while True:
        line = input()
        if not line.strip():
            break
        params.append(line.strip())
    return params

def extract_params_from_block(block, params):
    result = {}
    # 只查找<data>标签之间的内容
    data_blocks = re.findall(r'<data>(.*?)</data>', block, re.DOTALL)
    text = "\n".join(data_blocks)
    for param in params:
        # 支持前后有空格
        m = re.search(rf'^\s*{re.escape(param)}\s*:\s*([^\n\r]+)', text, re.MULTILINE)
        if m:
            result[param] = m.group(1).strip()
        else:
            result[param] = ''
    return result

def main():
    with open(xml_path, encoding="ISO-8859-1") as f:
        xml_text = f.read()
    samples = extract_samples(xml_text)
    params = show_first_sample_params(xml_text, samples)
    # 提取所有群体的参数
    all_data = []
    header = ["群体"] + params
    for name, start, end in samples:
        block = xml_text[start:end]
        values = extract_params_from_block(block, params)
        row = [name] + [values[p] for p in params]
        all_data.append(row)
    # 写入csv
    with open(csv_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(all_data)
    print(f"\n已生成csv文件：{csv_path}")

if __name__ == "__main__":
    main()