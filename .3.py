import dash
import dash_table
import dash_core_components as dcc
import pandas as pd

df = pd.read_excel(r"D:\测试文件\702-推案表格.xlsx", dtype=str, sheet_name="Sheet1")

app = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
    style_table={'height': 400},
    editable=True,
    pagination_mode=[{"name": i, "id": i} for i in df.values][:10]
)

if __name__ == '__main__':
    app.run_server(debug=True)
import pytesseract
# from pdf2docx import Converter
#
# def pdf_to_docx(pdf_path, docx_path):
#    cv = Converter(pdf_path)
#    cv.convert(docx_path, start=0, end=None)
#    cv.close()
#
# pdf_path = r"C:\Users\9000\Desktop\新建文件夹\南阳市商务局关于召开南阳市“出口e融 出口易企行”政银企对接活动的函.pdf"  # 您的PDF文件路径
# docx_path = r"C:\Users\9000\Desktop\新建文件夹\南阳市商务局关于召开南阳市“出口e融 出口易企行”政银企对接活动的函.docx"  # 您希望保存的DOCX文件路径
#
# pdf_to_docx(pdf_path, docx_path)