from service.dal.polly_handler import PollyWrapper
from pathlib import Path


def consume_text() -> None:
    polly_wrapper = PollyWrapper()
    current_path = Path(__file__).parent.parent.parent
    text_file_path = current_path / ('text/sample.txt')
    file_contents = text_file_path.read_text().replace('\n', ' ')
    audio_stream, _ = polly_wrapper.synthesize(text=file_contents, engine='neural', voice='Ruth', audio_format='mp3')
    with open('sample.mp3', 'wb') as f:
        f.write(audio_stream.read())


def consume_text_async() -> None:
    polly_wrapper = PollyWrapper()
    current_path = Path(__file__).parent.parent.parent
    text_file_path = current_path / ('text/sample.txt')
    file_contents = text_file_path.read_text().replace('\n', ' ')
    bucket = 'root-main-cron-rootmaincronpollyinputrootmaincron-gspb7o2ukw0d'
    audio_stream, _ = polly_wrapper.do_synthesis_task(text=file_contents, engine='neural', voice='Ruth', audio_format='mp3', s3_bucket=bucket)
    with open('sample.mp3', 'wb') as f:
        f.write(audio_stream.read())
