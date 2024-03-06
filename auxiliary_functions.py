import os
# from model_server_socket import create_socket_and_bind_it, send_video_frames
# from operator_server_socket import create_socket_and_bind_it_to_model
# import cv2

def read_all_frames():
    frames_path = os.path.dirname(os.path.abspath(__file__)) + "/static/frames/"
    
    # Get the list of files in the directory
    file_list = os.listdir(frames_path)
    print(f"file_list = {file_list}")

    # Filter out JPEG files
    frame_list = [file for file in file_list if file.endswith('.jpg')]
    frame_list.sort()
    
    frames_path = "/static/frames/"
    
    frame_list = [frames_path + file_name for file_name in frame_list]
    print(f"frame_list = {frame_list}")
    
    return frame_list


def delete_files_in_directory(folder_name):
    print("\n\n:: delete_files_in_directory() :: START\n\n")
    # Get the full path of the current file
    project_path = 'C:\\Users\\project25\\RescueSign'
    # file_path = os.path.abspath(__file__)
    # print(f"file_path={file_path}")

    # WHAT Model NEED: C:\\Users\\project25\\RescueSign\\PendingImages
    # WHAT OperatorUI NEED: C:\Users\project25\RescueSign\Rescue_Sign_SERVER_proj/static/operator-server-frames/

    # Get the directory name of the current file
    # dir_name = os.path.dirname(file_path)
    # directory = f'{dir_name}/static/operator-server-frames/'
    # print(f"directory={directory}")

    directory = project_path + "\\" + folder_name
    print(f":::: delete files from directory={directory}")
    # Get the list of files in the directory

    if 'C:\\Users\\project25\\RescueSign' != directory:
        files = os.listdir(directory)
        # print(f"files={files}")
        
        # Iterate over the files and delete each one
        for file_name in files:
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

    print("\n\n:: delete_files_in_directory() :: END\n\n")

# def delete_CroppedImages_folder():
    # try:
    #     import shutil
    #     full_path = 'C:\\Users\\project25\\RescueSign'
    #     files = os.listdir(full_path)

    #     for file_name in files:
    #         print(f"file_name = {file_name}")

    #         file_path = os.path.join(full_path, file_name)
    #         print(f"file_path = {file_path}")
    #         if os.path.isdir(file_path) and "CroppedImages" in file_path:
    #             # os.rmdir(full_path)
    #             if os.path.exists(file_path):
    #                 shutil.rmtree(file_path)
    #                 print(f"{file_path} DELETED")

    # except Exception as e:
    #     print("An exception occured: ", str(e))
        

def clean_model_folders():
    print(":: Cleaning the model folder before\\after running")
    clean_folder_when_model_done('DoneCroppedImages')
    clean_folder_when_model_done('DoneImages')
    clean_folder_when_model_done('DoneOpenPoseJsons')
    clean_folder_when_model_done('InProgressImages')

    # delete_CroppedImages_folder()

def clean_folder_when_model_done(folder):
    print("\n\n:: clean_folder_when_model_done() :: START\n\n")
    try:
        full_path = 'C:\\Users\\project25\\RescueSign\\' + folder
        if full_path != 'C:\\Users\\project25\\RescueSign\\':
            files = os.listdir(full_path)
            # print(f'full_path = {full_path}')
            # Iterate over the files and delete each one
            for file_name in files:
                file_path = os.path.join(full_path, file_name)
                if os.path.isfile(file_path):
                    print(f":: file_name = {file_name}")
                    print(f":: file_path = {file_path}")
                    os.remove(file_path)

    except Exception as e:
        print("An exception occured: ", str(e))
    print("\n\n:: clean_folder_when_model_done() :: END\n\n")



# async def send_video_from_model_to_operator():
#     model_server_socket, client_addr = create_socket_and_bind_it()
#     send_video_frames(model_server_socket, client_addr)

# async def open_socket_in_model_side():
#     sock = create_socket_and_bind_it_to_model()




