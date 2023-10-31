from django.shortcuts import render, redirect
import csv
import pandas as pd
import datetime
from GenAI_app.helpers import update_status_and_budget_in_csv, ask_ai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ.get('api_key')
api_key = OPENAI_API_KEY
print(api_key)
csv_path = 'GenAI_app/tasks.csv'

def read_csv(csv_path):
    data = []
    with open(csv_path, 'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            data.append(row)
    return data

def index(request):
    data = read_csv(csv_path)
    return render(request, 'index.html', {'data': data})

def update_page(request):
    return render(request, 'update.html')

def update_status(request):
    if request.method == 'POST':
        csv_df = pd.read_csv(csv_path, delimiter=";")
        task_number = request.POST.get('task_number')
        spent_budget = request.POST.get('budget')
        date = datetime.date.today()
        original_budget = csv_df.iloc[(int(task_number)-1),1]
        starting_date = csv_df.iloc[(int(task_number)-1),3]
        deadline_date = csv_df.iloc[(int(task_number)-1),4]
        task_number, status, response = ask_ai(api_key, task_number, original_budget, spent_budget, starting_date, deadline_date, date)
        update_status_and_budget_in_csv(task_number, new_status=status, csv_file=csv_path, spent_budget=spent_budget, recommendation=response)

    return redirect('index')
