# core/__init__.py

# 导入 core 目录下的 multi_layer_network 模块
# core/__init__.py
from .config import IS_KANGROLL_PRODUCTION, KANGROLL_PRODUCTION_KEY
# from .multi_layer_network import SomeFunctionOrClass
from .multi_layer_network import update_network

# 如果您需要在这个 __init__.py 中导入 analyze_gene 和 config，
# 您可以使用相对路径来导入，但这取决于您的项目结构和需求。
# 例如：
# from ..models.analyze_gene import analyze_gene
# 注意：这仅在 analyze_gene 位于 models 子目录时适用。

# 如果需要从根目录的 config 导入，可能需要使用不同的方法，
# 因为它不在 core 目录内。这通常在包的外部文件中处理，
# 而不是在包的 __init__.py 文件中。



