import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from flask import Flask
from threading import Thread


import datetime
from datetime import datetime, timedelta
import time

now = datetime.now()

app = Flask('')

@app.route('/')
def main():
    return "Your Bot Is Ready"

def run():
    app.run(host="0.0.0.0", port=8000)

def keep_alive():
    server = Thread(target=run)
    server.start()

keep_alive()
scheduler = AsyncIOScheduler()

whitelist_file = "whitelist.txt"

def save_whitelist(whitelist):
    with open(whitelist_file, "w") as f:
        for user_id, name, added_time in whitelist:
            f.write(f"{user_id}|{name}|{added_time}\n")
    print("Whitelist saved.")

def load_whitelist():
    whitelist = []
    try:
        with open(whitelist_file) as f:
            for line in f:
                values = line.strip().split("|")
                if len(values) == 3:
                    user_id, name, time_added = values                   
                    whitelist.append((user_id, name, time_added))
        print("Whitelist loaded.")
        print_whitelist(whitelist)
        return whitelist
    except FileNotFoundError:
        print("Whitelist file not found.")


async def remove_from_whitelist(user_id, time_added):
    global whitelist
    whitelist = [(id, name, ta) for id, name, ta in whitelist if id != user_id]
    save_whitelist(whitelist)
    print_whitelist()

def print_time_left():
    current_time = datetime.now()
    for user_id, name, added_time in whitelist:
        remove_time = added_time + datetime.timedelta(hours=16)
        time_left = remove_time - current_time
        time_left_str = str(time_left).split(".")[0]
        print(f"{name} tiene {time_left_str} restantes en la lista blanca.")
      
def print_whitelist(whitelist):
    print("Whitelist:")
    for user_id, name, time_added in whitelist:
        print(f"{name} (ID: {user_id}) - Agregado el {epoch_to_human(time_added)}")
      
def epoch_to_human(epoch):
    human = datetime.fromtimestamp(float(epoch)).strftime('%Y-%m-%d %H:%M:%S')
    return human

async def check_whitelist():
    current_time = datetime.now()
    for user_id, _ in whitelist:
        remove_time = current_time + datetime.timedelta(hours=16)
        scheduler.add_job(remove_from_whitelist, 'date', run_date=remove_time, args=[user_id])

def tiempo_restante(epoch):
    tiempo_transcurrido = time.time() - epoch
    tiempo_restante = (16 * 60 * 60) - tiempo_transcurrido
    horas_restantes = int(tiempo_restante // 3600)
    minutos_restantes = int((tiempo_restante % 3600) // 60)
    segundos_restantes = int(tiempo_restante % 60)
    return f"{horas_restantes} horas, {minutos_restantes} minutos y {segundos_restantes} segundos restantes"


async def tiempo_restante_whitelist(whitelist):
    for usuario in whitelist:
        user_id, nombre, epoch_str = usuario
        epoch = float(epoch_str)  # convertir a float
        tiempo_restante_str = tiempo_restante(epoch)
        print(f"{nombre} ({user_id}): {tiempo_restante_str}")