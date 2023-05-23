from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# 存储抽签结果的全局变量
selected_people = None

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global selected_people
    if request.method == 'POST':
        file = request.files['file']
        num_people = int(request.form.get("num_people"))
        department = request.form.get("department")  # 用户选择的部门
        df = pd.read_excel(file, header=0)  # 假设列名在第一行
        if selected_people is None:
            selected_department = df[df['部门'] == department].sample(min(1, len(df[df['部门'] == department])))
            remaining_df = df[df['部门'] != department]

            remaining_people = num_people - len(selected_department)
            if remaining_people > 0:
                additional_people = remaining_df.sample(min(remaining_people, len(remaining_df)), replace=False)
                selected_people = pd.concat([selected_department, additional_people])
            else:
                selected_people = selected_department
        else:
            # 在重新抽签时，排除已经选中的人
            remaining_df = df.loc[~df.index.isin(selected_people.index)]
            selected_people = remaining_df.sample(min(num_people, len(remaining_df)), replace=False)

        # 对抽签结果进行排序
        selected_people = selected_people.sort_values(by='序号')

        return render_template('result.html', tables=[selected_people.to_html(classes='data', index=False)],
                               titles=selected_people.columns.values)
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
