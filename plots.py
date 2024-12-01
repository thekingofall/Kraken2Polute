
import os
import pandas as pd
import matplotlib.pyplot as plt

def parse_kraken_report(file_path):
    """
    解析 Kraken 报告文件，提取分类百分比、分类层级和分类名称。
    """
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            fields = line.strip().split('\t')
            percentage = float(fields[0])  # 百分比
            rank_code = fields[3]         # 分类层级
            name = fields[5].strip()      # 分类名称
            data.append({"percentage": percentage, "rank_code": rank_code, "name": name})
    return pd.DataFrame(data)

def generate_multiple_pie_charts(data, file_name, output_dir, threshold=1.0):
    """
    根据 Kraken 报告数据生成多个饼图，并将它们绘制在一张图上。
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 定义分类层级的全称
    rank_labels = {
        "D": "Domain", "P": "Phylum", "C": "Class",
        "O": "Order", "F": "Family", "G": "Genus", "S": "Species"
    }

    # 创建一个网格布局（2行4列），用于展示多个饼图
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))  # 调整布局
    axes = axes.flatten()  # 将子图对象展平以便迭代

    for i, (rank_code, rank_label) in enumerate(rank_labels.items()):
        if i >= len(axes):
            break  # 如果子图数不够，跳过多余层级

        # 筛选指定分类层级的数据
        filtered_data = data[data["rank_code"] == rank_code]

        # 提取百分比和分类名称
        labels = filtered_data["name"].str.strip()
        sizes = filtered_data["percentage"]

        # 将低于阈值的分类合并为 "Others"
        labels_others = labels[sizes < threshold]
        sizes_others = sizes[sizes < threshold].sum()
        labels = labels[sizes >= threshold].tolist() + ["Others"] if sizes_others > 0 else labels.tolist()
        sizes = sizes[sizes >= threshold].tolist() + [sizes_others] if sizes_others > 0 else sizes.tolist()

        # 绘制饼图
        ax = axes[i]
        ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            wedgeprops={"edgecolor": "black"}
        )
        ax.set_title(f"{rank_label} Level", fontsize=14)

    # 删除多余的子图框架
    for j in range(len(rank_labels), len(axes)):
        fig.delaxes(axes[j])

    # 设置整体标题
    plt.suptitle(f"Classification Distribution: {file_name}", fontsize=16)

    # 保存图表
    output_file = os.path.join(output_dir, f"{file_name}_multiple_pie_charts.png")
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # 防止标题和子图重叠
    plt.savefig(output_file, dpi=300)
    plt.close()

    print(f"Generated multiple pie charts for {file_name}: {output_file}")

def main(input_dir, output_dir, threshold):
    """
    主函数：解析 Kraken 报告并生成多个饼图。
    """
    # 遍历输入目录中的所有 .kraken.report 文件
    for file in os.listdir(input_dir):
        if file.endswith(".kraken.report"):
            file_path = os.path.join(input_dir, file)

            # 解析 Kraken 报告文件
            data = parse_kraken_report(file_path)

            # 文件名去掉扩展名
            file_name = file.replace(".kraken.report", "")

            # 生成多个饼图合并在一张图上
            generate_multiple_pie_charts(data, file_name, output_dir, threshold)

if __name__ == "__main__":
    import argparse

    # 设置命令行参数
    parser = argparse.ArgumentParser(description="Generate multiple pie charts in one figure from Kraken2 report files.")
    parser.add_argument(
        "-i", "--input_dir",
        type=str,
        default="Run4_pollute",
        help="Input directory containing .kraken.report files (default: Run4_pollute)"
    )
    parser.add_argument(
        "-o", "--output_dir",
        type=str,
        default="Plots",
        help="Output directory where charts will be saved (default: Plots)"
    )
    parser.add_argument(
        "-t", "--threshold",
        type=float,
        default=1.0,
        help="Threshold percentage for merging small classifications into 'Others' (default: 1.0)"
    )

    # 解析命令行参数
    args = parser.parse_args()

    # 调用主函数
    main(args.input_dir, args.output_dir, args.threshold)
