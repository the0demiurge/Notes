# Append 到 Excel

```python
writer = pd.ExcelWriter(path)
yc.to_excel(writer, sheetname)
writer.save()
```