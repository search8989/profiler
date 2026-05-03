key = open('C:/profiler/app.py').read()
# знайди рядок з audio і виправ
key = key.replace(
    'file=("audio_file.stream, "audio/wav")',
    'file=audio_file.stream'
)
print(key[key.find('def transcribe'):key.find('def transcribe')+300])