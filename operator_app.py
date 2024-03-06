from flask import Flask, render_template, request, jsonify
# import requests
from auxiliary_functions import read_all_frames, delete_files_in_directory
from operator_socket_class import OperatorSocket
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/process_file": {"origins": "http://192.168.90.156:55555"}})
CORS(app, resources={r"/response_from_operator": {"origins": "http://192.168.90.156:44444"}})

@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@app.route('/')
def index():

    framePaths = read_all_frames() 
    return render_template('operator_ui.html', imageUrls=framePaths)
    # return render_template('display.html')

def send_answer(selected_answer):
    # Process the selected answer
    print("Selected answer:", selected_answer)    

@app.route('/get_images_urls')
def get_images_urls():
    framePaths = read_all_frames() 
    return jsonify(framePaths)

@app.route('/create_socket_connection')
def create_socket_connection():

    # open socket connection
    connected = False 
    while not connected: 
        print(":: while not connected ::")
        try: 
            import time
            print(f"time = {time.time()}")
            print("/create_socket_connection :: get new request")
            # First, delete all the oldest frames
            # delete_files_in_directory(folder_name="Rescue_Sign_SERVER_proj/static/operator-server-frames")

            opertor_socket = OperatorSocket()
            opertor_socket.create_socket_and_bind_it_to_model()

            print("::: calling to opertor_socket.get_frames_from_model_server()")
            opertor_socket.get_frames_from_model_server()
            print(":: AFTER opertor_socket.get_frames_from_model_server()")

            print('Video frames have been send')
            connected = True 
        except Exception as e: 
            time.sleep(3)
            print("::: time.sleep(3)")
            pass #Do nothing, just try again 

    return jsonify({'message': 'Success'})

@app.route('/delete_oldest_frames')
def delete_oldest_frames():
    # First, delete all the oldest frames
    delete_files_in_directory(folder_name=OperatorSocket.path_out)

    return jsonify("{'message': 'Oldest frames have been deleted'}")

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    selected_answer = request.form['answer']
    send_answer(selected_answer)
    
    return 'Success'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=55555)
