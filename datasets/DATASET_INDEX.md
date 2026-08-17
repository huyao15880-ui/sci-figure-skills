# 数据集索引与注册规范（本地数据集）

> 原则：**数据不进仓库，索引进仓库**。本仓库开源，本地/未发表数据集
> 留在用户机器上，通过本索引注册后供 skills 引用。索引本身不得包含
> 未发表数据的具体数值或可识别信息。

## 注册格式

在下方登记表中加一行，并在本地维护同名字典（CSV/Parquet均可）：

```yaml
- id: chem_dpvt_pairs            # 唯一 ID（snake_case）
  domain: nanomaterials          # nanomaterials | biology | art-design
  kind: curves                   # curves | calibration | matrix | survival | image
  description: 电化学 DPV 曲线族长表（浓度×材料）
  local_path: E:/.../dpv_curves.csv   # 本地绝对路径（仅自己可见）
  columns: [potential_V, current_uA, concentration_uM, material]
  frozen: true                   # 冻结数据集（数值锁定，图注对账用）
  notes: 图上注记数值须运行时读本表派生统计，禁硬编码
```

## 登记表

| id | domain | kind | frozen | 说明 |
|---|---|---|---|---|
| （示例）chem_dpvt_pairs | nanomaterials | curves | ✓ | 见上 |

## 纪律

1. **冻结数据集**（frozen: true）：一旦被某图的注记引用，数值锁定；
   重算需新 id，不改旧表
2. **隐私/未发表边界**：含患者、未公开课题数据的集，索引只写 schema
   不写路径细节；进仓库的示例数据集须合成或脱敏
3. **列名规范**：物理量_单位（`current_uA`、`energy_eV_vs_Ef`），
   agent 读表即知单位，图轴题从列名派生
4. 新领域数据形态（如生物表达矩阵）首次注册时，在对应
   `domains/*/PROFILE.md` 补一节字段约定
