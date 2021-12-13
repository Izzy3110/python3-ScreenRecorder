import os
import subprocess
import time


ffmpeg_path = r"E:\C_Downloads\ffmpeg-20200323-ba698a2-win64-static\bin\ffmpeg.exe"


def save_video(inp_filename, out_filename, frame_width, frame_height, fps):
    project_path = os.path.dirname(__file__).replace(r"\recorder", r"")
    inp_filepath = os.path.join(project_path, "data", inp_filename)
    out_filepath = os.path.join(project_path, "data", out_filename)

    if os.path.isfile(inp_filepath):
        """
        print("project-path:         " + os.path.dirname(__file__).replace(r"\recorder", r""))
        print("inp_filename: " + inp_filename)
        print("inp_filename-full_path: " + inp_filepath)
        print("out_filename: " + out_filename)
        print("out_path: " + out_filepath)
        print("frame_width: " + str(frame_width))
        print("frame_height: " + str(frame_height))
        print("fps: " + str(fps))
        """
        if os.path.isfile(ffmpeg_path):
            full_cmd = r" ".join([ffmpeg_path, r"-i " + inp_filepath + " -pix_fmt yuv420p -crf 18 -y " + out_filepath])
            time.sleep(3)

            with subprocess.Popen(full_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as ps:
                err, out = ps.communicate()
                for err_line in err.decode().splitlines():
                    print("err: " + err_line)
                print("")

                for out_line in out.decode().splitlines():
                    print("out: " + out_line)
                print("")
