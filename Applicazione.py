import threading
import serial
import json
import dearpygui.dearpygui as dpg

SERIAL_PORT = "COM3"  # Per Linux/Mac usa ad esempio "/dev/ttyUSB0"
BAUD_RATE = 9600
TEMPMIN = 15
TEMPMAX = 30
UMIDITAMIN = 30
UMIDITAMAX = 60
FILEDATI = 'dati.jsonl'
data_temperatura = []
data_umidita = []
time_stamps = []

def read_serial():
    global data_temperatura, data_umidita, time_stamps
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        while True:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    data = json.loads(line)
                    salva_dati(data)
                    temperatura = data["temperatura"]
                    umidita = data["umidita"]
                    time = data["time"]
                    if temperatura is not None and umidita is not None:
                        print(f"Temperatura: {temperatura}°C, Umidità: {umidita}%")

                        # Aggiorna le liste dati per il grafico
                        data_temperatura.append(temperatura)
                        data_umidita.append(umidita)
                        time_stamps.append(int(time))

                        # Aggiorna il grafico e il testo nel GUI
                        dpg.set_value("plot_temperatura", [time_stamps, data_temperatura])
                        dpg.set_value("plot_umidita", [time_stamps, data_umidita])
                        dpg.set_value("latest_values", f"Temperatura: {temperatura:.1f} °C, Umidità: {umidita:.1f}%")

                        aggiorna_indicatori(temperatura, umidita)
            except json.JSONDecodeError:
                continue
    except serial.SerialException as e:
        print(f"Errore con la porta seriale: {e}")

def aggiorna_indicatori(temperatura_valore, umidita_valore):
    if temperatura_valore < TEMPMIN:
        dpg.configure_item(indicatore_temperatura, fill=(255, 255, 0, 255))
    elif temperatura_valore > TEMPMAX:
        dpg.configure_item(indicatore_temperatura, fill=(255, 0, 0, 255))
    else:
        dpg.configure_item(indicatore_temperatura, fill=(0, 255, 0, 255))

    if umidita_valore < UMIDITAMIN:
        dpg.configure_item(indicatore_umidita, fill=(255, 255, 0, 255))
    elif umidita_valore > UMIDITAMAX:
        dpg.configure_item(indicatore_umidita, fill=(255, 0, 0, 255))
    else:
        dpg.configure_item(indicatore_umidita, fill=(0, 255, 0, 255))

# Salva i valori in dati.jsonl
def salva_dati(dati):
    with open(FILEDATI, 'a', encoding='utf-8') as f:
        json.dump(dati, f)
        f.write('\n')
        f.flush()

# Avvia il thread per la lettura della seriale
thread = threading.Thread(target=read_serial, daemon=True)
thread.start()

dpg.create_context()
dpg.create_viewport(title='Monitor Arduino', width=1100, height=1000)
dpg.setup_dearpygui()

with dpg.window(label="Grafico Dati", width=1100, height=900):
    dpg.add_text("Dati in tempo reale da Arduino")
    dpg.add_text("In attesa di dati...", tag="latest_values")
    with dpg.group(horizontal=True):
        with dpg.plot(label="Temperatura", height=350, width=900):
            dpg.add_plot_legend()
            x_axis_temp = dpg.add_plot_axis(dpg.mvXAxis, label="Tempo")
            y_axis_temp = dpg.add_plot_axis(dpg.mvYAxis, label="Temperatura")
            dpg.set_axis_limits(y_axis_temp, 15, 30)
            dpg.add_line_series([], [], label="Temperatura (°C)", parent=y_axis_temp, tag="plot_temperatura")

        with dpg.group():
            dpg.add_text("Temperatura:")
            with dpg.drawlist(width=50, height=50):
                indicatore_temperatura = dpg.draw_circle((25, 25), 20, fill=(255, 255, 0, 255))

    with dpg.group(horizontal=True):
        with dpg.plot(label="Umidità", height=350, width=900):
            dpg.add_plot_legend()
            x_axis_umidita = dpg.add_plot_axis(dpg.mvXAxis, label="Tempo")
            y_axis_umidita = dpg.add_plot_axis(dpg.mvYAxis, label="Umidità")
            dpg.set_axis_limits(y_axis_umidita, 0, 100)
            dpg.add_line_series([], [], label="Umidità (%)", parent=y_axis_umidita, tag="plot_umidita")

        with dpg.group():
            dpg.add_text("Umidità:")
            with dpg.drawlist(width=50, height=50):
                indicatore_umidita = dpg.draw_circle((25, 25), 20, fill=(255, 255, 0, 255))

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()