def clean_video_data(text):
    return ' '.join(' '.join(text.split('###Video_OCR###')).split('###Audio_Transcription###'))
