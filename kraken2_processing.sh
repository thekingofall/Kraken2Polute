#!/bin/bash

# 默认参数
DEFAULT_INPUT_DIR="Run2_trim"
DEFAULT_OUTPUT_DIR="Run4_pollute"
DEFAULT_DB_PATH="/home/maolp/data5/All_zhuyue_inluolab/kdb"
DEFAULT_THREADS=8
DEFAULT_CONDA_ENV="kraken2"  # 默认 Conda 环境名称

# 打印帮助信息
function print_help() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Optional arguments:"
    echo "  -i, --input-dir       Input directory containing subdirectories with sequencing files (default: $DEFAULT_INPUT_DIR)"
    echo "  -o, --output-dir      Output directory to save results (default: $DEFAULT_OUTPUT_DIR)"
    echo "  -d, --db-path         Path to Kraken2 database (default: $DEFAULT_DB_PATH)"
    echo "  -t, --threads         Number of threads to use (default: $DEFAULT_THREADS)"
    echo "  -e, --conda-env       Conda environment to activate (default: $DEFAULT_CONDA_ENV)"
    echo "  -h, --help            Display this help message and exit"
    exit 0
}

# 解析命令行参数
INPUT_DIR="$DEFAULT_INPUT_DIR"
OUTPUT_DIR="$DEFAULT_OUTPUT_DIR"
DB_PATH="$DEFAULT_DB_PATH"
THREADS="$DEFAULT_THREADS"
CONDA_ENV="$DEFAULT_CONDA_ENV"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -i|--input-dir) INPUT_DIR="$2"; shift ;;
        -o|--output-dir) OUTPUT_DIR="$2"; shift ;;
        -d|--db-path) DB_PATH="$2"; shift ;;
        -t|--threads) THREADS="$2"; shift ;;
        -e|--conda-env) CONDA_ENV="$2"; shift ;;
        -h|--help) print_help ;;
        *) echo "Unknown parameter passed: $1"; print_help ;;
    esac
    shift
done

# 激活 Conda 环境
if [[ -n "$CONDA_ENV" ]]; then
    echo "Activating Conda environment: $CONDA_ENV"
    source "$(conda info --base)/etc/profile.d/conda.sh"  # 确保 `conda` 命令可用
    conda activate "$CONDA_ENV"
    if [[ $? -ne 0 ]]; then
        echo "Error: Failed to activate Conda environment '$CONDA_ENV'. Exiting."
        exit 1
    fi
fi

# 创建输出目录（如果不存在）
mkdir -p "$OUTPUT_DIR"

# 遍历输入目录中的子目录
for dir in "$INPUT_DIR"/*; do
    # 确保是目录
    if [[ -d "$dir" ]]; then
        # 获取目录名（去除路径部分）
        DIR_NAME=$(basename "$dir")

        # 检查目录中是否存在双端测序文件
        R1_FILE=$(find "$dir" -type f -name "*_R1*.gz" | head -n 1)
        R2_FILE=$(find "$dir" -type f -name "*_R2*.gz" | head -n 1)

        if [[ -f "$R1_FILE" && -f "$R2_FILE" ]]; then
            echo "Processing $DIR_NAME..."

            # 定义输出文件路径
            REPORT="$OUTPUT_DIR/${DIR_NAME}.kraken.report"
            OUTPUT="$OUTPUT_DIR/${DIR_NAME}.kraken.out"
            UNCLASSIFIED_PREFIX="$OUTPUT_DIR/${DIR_NAME}_unclassified"

            # 运行 kraken2 命令
            kraken2 --db "$DB_PATH" \
                    --threads "$THREADS" \
                    --paired \
                    --unclassified-out "${UNCLASSIFIED_PREFIX}#.fq" \
                    --report "$REPORT" \
                    --output "$OUTPUT" \
                    "$R1_FILE" "$R2_FILE"

            echo "Finished processing $DIR_NAME. Results saved in $OUTPUT_DIR."
        else
            echo "Skipping $DIR_NAME: Missing R1 or R2 file."
        fi
    fi
done

# 退出 Conda 环境
if [[ -n "$CONDA_ENV" ]]; then
    echo "Deactivating Conda environment: $CONDA_ENV"
    conda deactivate
fi
