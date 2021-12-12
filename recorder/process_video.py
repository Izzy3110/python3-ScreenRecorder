import ffmpeg


def save_video(filename, frame_width, frame_height, fps):
    process = (
        ffmpeg
        .input(filename="", format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(frame_width, frame_height))
        .output(filename, pix_fmt='yuv420p', vcodec='libx264', r=fps, crf=37)
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )
    return process
