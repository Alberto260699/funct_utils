import moviepy
import moviepy.editor

#put your file path in here

video=moviepy.editor.VideoFileClip('')
audio=video.audio
audio.write_audiofile('new_audio.mp3')