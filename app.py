from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Store alarms as list of dicts: {'time': 'HH:MM:SS', 'label': 'text'}
alarms = []

@app.route('/')
def index():
    # Sort alarms by time ascending
    sorted_alarms = sorted(alarms, key=lambda a: a['time'])
    return render_template('index.html', alarms=sorted_alarms)

@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    alarm_time = request.form.get('alarm_time')  # format HH:MM:SS or HH:MM
    alarm_label = request.form.get('alarm_label', 'Alarm')
    
    # Normalize alarm_time to HH:MM:SS (input type="time" might send HH:MM)
    if len(alarm_time) == 5:
        alarm_time += ":00"
    
    # Avoid duplicate alarms for the same time+label
    if not any(a['time'] == alarm_time and a['label'] == alarm_label for a in alarms):
        alarms.append({'time': alarm_time, 'label': alarm_label})
    
    return redirect(url_for('index'))

@app.route('/clear_alarms')
def clear_alarms():
    alarms.clear()
    return redirect(url_for('index'))

@app.route('/delete_alarm', methods=['POST'])
def delete_alarm():
    alarm_time = request.form.get('time')
    global alarms
    alarms = [a for a in alarms if a['time'] != alarm_time]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
