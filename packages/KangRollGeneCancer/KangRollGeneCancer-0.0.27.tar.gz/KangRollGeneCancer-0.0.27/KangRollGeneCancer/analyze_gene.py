# 文件名：analyze_gene.py

def analyze_gene(gene_sequence):
    """
    分析给定的基因序列。
    参数:
        gene_sequence (str): 基因序列。
    返回:
        str: 分析结果。
    """
    # 示例分析：计算序列中的碱基数量
    base_counts = {
        'A': gene_sequence.count('A'),
        'T': gene_sequence.count('T'),
        'C': gene_sequence.count('C'),
        'G': gene_sequence.count('G')
    }
    return f"碱基计数: {base_counts}"
