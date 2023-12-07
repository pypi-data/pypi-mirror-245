from XEdu.hub import Workflow as wf
import numpy as np

# 模型声明
basenn = wf(task='basenn',checkpoint='basenn_iris.onnx')
# 待推理表格，此处仅以随机数组为例，以下为1个维度为4的特征
table = np.random.random((1, 4)).astype('float32') # 可替换成您想要推理的表格文件路径,如 table = 'iris.csv',csv文件的纵轴为样本，横轴为特征，第一行为表头，最后一列为标签。
# 模型推理
res = basenn.inference(data=table)
# 标准化推理结果
result = basenn.format_output(lang="zh")

# 更多用法教程详见：https://xedu.readthedocs.io/zh/master/support_resources/model_convert.html