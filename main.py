import whisper_timestamped as w
import cv2
import numpy as np
import subprocess
from dbsetup import get_image_path_from_db
import imageio.v2 as imageio


def get_transcription(audio_name):
    return w.transcribe(w.load_model("tiny", device="cpu"), w.load_audio(audio_name), language="en")['segments'][0]['words']


def create_video(audio_name, video_name, img_dims, db_name):

    img_dict = {}

    frame_rate = 30

    # Helps us lazy load the images for the animation
    def get_image(chars):
        if chars not in img_dict.keys():
            ret = get_image_path_from_db(db_name, chars)
            if ret != -1:
                img_dict[chars] = np.asarray(imageio.imread(ret))
            else:
                raise KeyError

        return img_dict[chars]

    words = get_transcription(audio_name)

    # Calculate number of frames if animation were to last 2 seconds after last word spoken
    num_frames = int((words[-1]['end'] + 2) * frame_rate)

    out = cv2.VideoWriter("temporary.mp4", cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, img_dims)

    cur_word = 0

    frame_index = 0

    while cur_word < len(words):

        # Remove all punctuation
        text = list(filter(lambda y: y.isalpha(), words[cur_word]['text']))

        start = float(words[cur_word]['start'])

        end = float(words[cur_word]['end'])

        print(f"Parsing through word '{text}' which starts at {start} and ends at {end}")

        for x in range(frame_index, int(start * frame_rate)):
            out.write(get_image("NEUTRAL"))

        frac_time = int(((end - start) * frame_rate) // len(text))

        letter_index = 0
        while letter_index < len(text):
            c = text[letter_index].lower()

            try:
                # In case the sound is 'ch', 'sh' or 'th', we try to get the image
                # including the next letter as well, the function takes care of the
                # cases where the combinations of the two letters aren't valid by
                # throwing an exception so that we just get the first letter
                im = get_image(c + text[letter_index + 1].lower())

                # If the exception wasn't thrown, we actually used the two letters
                # in which case, we must increment our letter index by 2
                num_letters_traversed = 2

            except (KeyError, IndexError):
                im = get_image(c)
                num_letters_traversed = 1

            for x in range(num_letters_traversed * frac_time):
                out.write(im)

            letter_index += num_letters_traversed

        frame_index = int(end * frame_rate) - 1

        cur_word += 1

    for x in range(frame_index, num_frames):
        out.write(get_image("NEUTRAL"))

    out.release()

    # Add the initial audio as an overlay to the animation
    cmd = f'ffmpeg -y -i {audio_name} -r 30 -i temporary.mp4 -filter:a aresample=async=1 -c:a flac -c:v copy {video_name}'
    subprocess.call(cmd, shell=True)

    # Delete video with just animation
    cmd = 'del "./temporary.mp4"'
    subprocess.call(cmd, shell=True)

aud_name = "./Fast.wav"
vid_name = "./Fast_Video.mp4"
img_dim = (512, 512)
db = "BaseAnimation.db"
create_video(aud_name, vid_name, img_dim, db)