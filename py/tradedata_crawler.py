# %%
# !python.exe -m pip install --upgrade pip

# %%
# %pip install pandas
# %pip install matplotlib
# %pip install requests
# %pip install koreanize_matplotlib
# %pip install tkinter
# %pip install Pillow

# %%
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from matplotlib.patches import Patch
import koreanize_matplotlib
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# %% [markdown]
# -     "ttwgTpcd":"1000" : [단위] 톤(TON), 천 달러

# %%
# Global variable for filepath and figure
filepath = ""
fig = None
canvas = None


# HS code to Korean description mapping
hs_code_to_name = {
    "8479501000": "산업용 로보트",
    "8479502000": "산업용 로보트",
    "8479509000": "기타 산업용 로봇",
    "8515211010": "관용접 로봇",
    "8515212010": "봉합용접 로봇",
    "8515213010": "바트용접 로봇",
    "8515219010": "저항용접 로봇",
    "8515311010": "교류아크용접 로봇",
    "8515319010": "기타 아크용접 로봇",
    "8486309020": "평판디스플레이 로봇('22년 삭제)",
    "8424202010": "도장 로봇",
    "8479892010": "전자부품장착기(SMT)",
    "8479892090": "기타 전자부품장착기(SMT)",
    "8428701000": "적재용 로봇",
    "8427103000": "무인운반로봇(AGV)",
    "8428702000": "무인운반로봇(8427 제외)",
    "8428709000": "기타 무인운반로봇",
    "8508111000": "로봇청소기",
    "8508192000": "기타로봇청소기"
}

# 현재 화면의 해상도를 가져오는 함수
def get_screen_resolution():
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    return screen_width, screen_height

def scrape_tradedata(priodFr, priodTo):
    url = "https://tradedata.go.kr/cts/hmpg/retrieveTrade.do"

    data={
        "tradeKind":"ETS_MNK_1020000A",
        "priodKind":"MON",
        "priodFr": priodFr,
        "priodTo": priodTo,
        "statsBase":"acptDd",
        "ttwgTpcd":"1000",
        "showPagingLine":5000,
        "sortColumn":"",
        "sortOrder":"",
        "hsSgnGrpCol":"HS10_SGN",
        "hsSgnWhrCol":"HS10_SGN",
        "hsSgn":[
        "8479501000",
        "8479502000",
        "8479509000",
        "8515211010",
        "8515212010",
        "8515213010",
        "8515219010",
        "8515311010",
        "8515319010",
        "8486309020",
        "8424202010",
        "8479892010", 
        "8479892090", 
        "8428701000", 
        "8427103000", 
        "8428702000", 
        "8428709000", 
        "8508111000", 
        "8508192000"
        ]
    }

    req= requests.post(url=url, data=data)
    result = req.json()

    # Prepare an empty list to hold dictionaries
    data_list = []

    for x in result["items"]:
        # Exclude the row with '총계'
        if x["hsSgn"].strip() != '총계':
            data_dict = {
                "HS코드": x["hsSgn"],
                "기간": x["priodTitle"],
                "수출중량": x["expTtwg"],
                "수출금액": x["expUsdAmt"],
                "수입중량": x["impTtwg"],
                "수입금액": x["impUsdAmt"],
                "무역수지":x ["cmtrBlncAmt"]
            }
        # Append the dictionary to the list
        data_list.append(data_dict)

    # Convert the list of dictionaries into a DataFrame
    trade_df = pd.DataFrame(data_list)

    # Set pandas display options for better readability 
    pd.set_option('display.width', 1000)  # adjust this value according to your needs.
    pd.set_option('display.max_columns', None) 

    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data_list)

    # Save DataFrame to CSV
    csv_path = "./scrapped_tradedata.csv"
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')

    print(f"Data saved to {csv_path}")

# Function to upload a file
def upload_file():
    global filepath
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    status_var.set(f"Selected file: {filepath}")

# Function to save the chart as PNG
def save_chart_as_png():
    global fig
    if fig:
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if filename:
            fig.savefig(filename)
            status_var.set(f"Graph saved as {filename}")
    else:
        status_var.set("Please generate the graph first.")

# Common function to plot the chart based on the uploaded file and the given column_name
def plot_chart(column_name, title_text):
    global fig, canvas
    try:
        # Load the CSV file
        df_summary = pd.read_csv(filepath)
        df_summary[column_name] = df_summary[column_name].str.replace(',', '').str.strip().astype(int)
        hs_code_values = df_summary.groupby("HS코드")[column_name].sum().sort_values(ascending=False)
        
        # Pie chart related preparations
        num_categories = len(hs_code_values)
        colors = plt.cm.tab20c(np.linspace(0, 1, num_categories))
        pie_labels_all = [hs_code_to_name.get(str(int(code)), str(int(code))) if i < 10 else "" for i, code in enumerate(hs_code_values.index)]
        top_10_hs_code_descriptions = [hs_code_to_name.get(str(int(code)), str(int(code))) for code in hs_code_values.head(10).index]

        # 화면 해상도를 가져와서 그래프 크기를 조절
        screen_width, screen_height = get_screen_resolution()
        fig, ax = plt.subplots(figsize=(screen_width/80, screen_height/80))  # 80 is a factor to adjust the size, you can change this value as per your needs

        # Plotting
        fig, ax = plt.subplots(figsize=(15, 10), dpi=100) # 15인치 너비, 10인치 높이로 그림 크기 설정
        wedges, texts, autotexts = ax.pie(hs_code_values, 
                                          autopct=lambda p: f'{p:.1f}%' if p > 2 else '', 
                                          startangle=90, 
                                          colors=colors, 
                                          labels=pie_labels_all, 
                                          textprops=dict(color="w"))
        


        for i in range(10, len(texts)):
            texts[i].set_visible(False)
            autotexts[i].set_visible(False)
        ax.legend(loc='lower left', labels=top_10_hs_code_descriptions, prop={'size': 10})
        ax.set_title(title_text)
        
        # If a canvas exists, destroy it before creating a new one
        if canvas:
            canvas.get_tk_widget().destroy()


        # Embed the figure in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.draw()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def plot_bar_chart():
    global fig, canvas
    try:
        # Load the CSV file
        df_summary = pd.read_csv(filepath)
        column_names_summary = ["HS code", "Period", "Export weight", "Export value", 
                                "Import weight", "Import value", "Trade balance"]
        df_summary.columns = column_names_summary

        # Data Preprocessing
        for col in ["Export value", "Import value", "Trade balance"]:
            if df_summary[col].dtype == 'O':
                df_summary[col] = df_summary[col].str.replace(',', '').astype(int)

        df_summary["Export weight"] = df_summary["Export weight"].str.replace(',', '').str.strip().astype(float)
        df_summary["Import weight"] = df_summary["Import weight"].str.replace(',', '').str.strip().astype(float)

        df_summary = df_summary[df_summary["Period"] != "총계"]
        df_summary["Period"] = df_summary["Period"].apply(lambda x: f"{str(x).split('.')[0]}-{str(x).split('.')[1]}")

        # Plotting
        colors = ['blue', 'red']
        fig, ax = plt.subplots(figsize=(12, 6))
        df_summary.groupby('Period').sum()[['Export value', 'Import value']].plot(kind='bar', ax=ax, color=colors)
        ax.set_xticklabels(df_summary["Period"].unique(), rotation=45)
        ax.set_ylim([0, 80000])
        ax.set_title('기간별 무역 수출입 금액')
        ax.set_xlabel('기간 (YYYY-MM)')
        ax.set_ylabel('금액 (in tens of thousands)')
        ax.legend(title="Trade Type")
        plt.tight_layout()

        # If a canvas exists, destroy it before creating a new one
        if canvas:
            canvas.get_tk_widget().destroy()

        # Embed the figure in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.draw()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def plot_trade_balance_chart():
        global fig, canvas
        try:
            # Load the CSV file
            df_summary = pd.read_csv(filepath)

            # Data Preprocessing
            df_summary["무역수지"] = df_summary["무역수지"].str.replace(',', '').str.strip().astype(int)
            hs_code_trade_balance_values = df_summary.groupby("HS코드")["무역수지"].sum().sort_values(ascending=False)
            hs_code_trade_balance_values_abs = hs_code_trade_balance_values.abs()

            # Color palette setup
            colors = np.where(hs_code_trade_balance_values < 0, 'red', 'blue')
            legend_elements = [Patch(facecolor='blue', label='무역수지 흑자'),
                               Patch(facecolor='red', label='무역수지 적자')]

            # Modify label to display only for HS codes with more than 5% share
            pie_labels_updated = [hs_code_to_name.get(str(int(code)), str(int(code))) 
                                  if (value / hs_code_trade_balance_values_abs.sum() * 100) >= 5 
                                  else "" 
                                  for code, value in hs_code_trade_balance_values_abs.items()]

            # Plotting the pie chart
            
            fig, ax = plt.subplots(figsize=(12, 8))
            wedges, texts, autotexts = ax.pie(hs_code_trade_balance_values_abs, 
                                              autopct=modified_autopct_5pct(hs_code_trade_balance_values_abs), 
                                              startangle=90, 
                                              colors=colors, 
                                              labels=pie_labels_updated,
                                              wedgeprops=dict(edgecolor='white', linewidth=0.2))

            # Adjust text color for pie slices
            adjust_text_color(autotexts, colors)

            # Setting the legend (Trade surplus/deficit)
            ax.legend(handles=legend_elements, loc='upper center', prop={'size': 10})

            # Setting the title for the pie chart
            plt.title("무역수지 기준 HS코드별 비중 (절댓값 기준 5% 이상 항목 표시)")
            plt.tight_layout()

            # If a canvas exists, destroy it before creating a new one
            if canvas:
                canvas.get_tk_widget().destroy()

            # Embed the figure in the tkinter window
            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", str(e))

def adjust_text_color(autotexts, colors):
    """Adjusts the text color inside the pie slices for better visibility."""
    for autotext, color in zip(autotexts, colors):
        if color != 'white':
            autotext.set_color('white')

def modified_autopct_5pct(values):
    """Display the percent value inside the pie slice if the value is above 5%."""
    def inner_autopct(pct):
        total = sum(values)
        val = pct * total / 100.0
        return f'{pct:.1f}%' if pct >= 5 else ''
    return inner_autopct

def get_period_input():
    def on_submit():
        # Retrieve the values from the Entry widgets
        priodFr_value = priodFr_entry.get()
        priodTo_value = priodTo_entry.get()
        # Close the input window
        input_window.destroy()
        # Call the scrape_tradedata function with the retrieved values
        scrape_tradedata(priodFr_value, priodTo_value)
        # Update the status_var with a completion message
        status_var.set("Scrape trade data completed successfully!")

    # Create a new tkinter window for input
    input_window = tk.Toplevel(root)
    input_window.title("Enter Period")

    # Create labels and entry widgets for priodFr and priodTo
    priodFr_label = tk.Label(input_window, text="Enter priodFr:")
    priodFr_label.pack(pady=10)
    priodFr_entry = tk.Entry(input_window)
    priodFr_entry.pack(pady=10)

    priodTo_label = tk.Label(input_window, text="Enter priodTo:")
    priodTo_label.pack(pady=10)
    priodTo_entry = tk.Entry(input_window)
    priodTo_entry.pack(pady=10)

    # Create a submit button to retrieve the input values
    submit_btn = tk.Button(input_window, text="Submit", command=on_submit)
    submit_btn.pack(pady=20)

def plot_export_chart():
    plot_chart("수출금액", "수출금액 기준 HS코드별 비중")

def plot_import_chart():
    plot_chart("수입금액", "수입금액 기준 HS코드별 비중")

# Create the main window
root = tk.Tk()
root.title("Trade Data Chart GUI")
root.geometry("800x480")

# "scrape trade data(generate csv file)" 버튼 추가
btn_scrape_data = tk.Button(root, text="Scrape Trade Data (Generate CSV File)", command=get_period_input)
btn_scrape_data.pack(pady=10)

# Add a button to upload the file
btn_upload = tk.Button(root, text="Upload CSV File", command=upload_file)
btn_upload.pack(pady=10)

# Add a button to plot the export chart
btn_plot_export = tk.Button(root, text="Generate Export Pie Chart", command=plot_export_chart)
btn_plot_export.pack(pady=10)

# Add a button to plot the import chart
btn_plot_import = tk.Button(root, text="Generate Import Pie Chart", command=plot_import_chart)
btn_plot_import.pack(pady=10)

# Add a button to plot the bar chart
btn_plot_bar_chart = tk.Button(root, text="Generate Plot Chart", command=plot_bar_chart)
btn_plot_bar_chart.pack(pady=10)

# Add a button to plot the trade balance pie chart
btn_plot_trade_balance = tk.Button(root, text="Generate Trade Balance Pie Chart", command=plot_trade_balance_chart)
btn_plot_trade_balance.pack(pady=10)

# Add a button to save the chart as PNG
btn_save = tk.Button(root, text="Save Graph as PNG", command=save_chart_as_png)
btn_save.pack(pady=10)

# Status message
status_var = tk.StringVar(root)
status_label = tk.Label(root, textvariable=status_var, relief=tk.SUNKEN, anchor=tk.W)
status_label.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()


