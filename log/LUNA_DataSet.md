LUNA 16 数据集分析
=========================


1. annotation.csv中标注的是seriesuid,结节结节的坐标(xyz),结节的直径(mm)<br>

2. candidates.csv中标注的是seriesuid,结节结节的坐标(xyz),结节的二分类(0/1)<br>

3. 只有当一个结节在candidates.csv中被标注成"1"的时候,他才会出现在annotation.csv中.<br>

4. 当一个结节同时出现在annotation.csv和candidates.csv中时,他的坐标可能有些许偏差<br>

5. candidates.csv中总共记录了551056个结节的定位和二分类,但是annotation.csv中仅有1186个标记为1的结节的定位和大小信息.<br>

6. 在原始的LUNA16数据集中,仅有三个CSV文件,另一个是提交的示例,比赛要求程序要给出候选结节的定位信息和分类概率<br>