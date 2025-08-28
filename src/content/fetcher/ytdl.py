import os
import shutil

from django.core.exceptions import BadRequest
from yt_dlp import YoutubeDL
from tempfile import TemporaryDirectory
from django.conf import settings
from content.models import ContentItem, Bucket, FetchTaskResult

OPTIONS = {
    'format': 'm4a/bestaudio/best',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }],
}


def get_content_type_by_extension(ext):
    if ext == 'm4a':
        return ContentItem.HttpContentType.mp4_audio
    else:
        print('unknown media extension: ', ext)
        raise BadRequest('File type not supported: {}'.format(ext))


def fetch_yt(url, bucket_id):
    downloaded_info: dict[str, dict] = {}
    title = ''

    bucket = Bucket.objects.get(id=bucket_id)
    task_result = FetchTaskResult.objects.create(bucket=bucket)
    task_result.save()

    def progress_hook(info):
        if info['status'] == 'finished':
            # interesting fields in info[info_dict]: audio_ext, video_ext, display_id, format_id, ext
            info_dict = info['info_dict']
            downloaded_info[info_dict['filename']] = info_dict.copy()

    try:

        with TemporaryDirectory() as tmpdir:
            options = OPTIONS.copy()
            options['postprocessor_hooks'] = [progress_hook]
            options['outtmpl'] = os.path.join(tmpdir, f'[{bucket.slug}] - %(title)s.%(ext)s')

            # first, download all files in a temporary directory
            with YoutubeDL(options) as ydl:
                ydl.download(url)

            # then, move files under MEDIA_ROOT and create respective content items
            print('downloaded', len(downloaded_info), 'files')
            titles = []
            for (filename, info_dict) in downloaded_info.items():
                title = info_dict['title']
                titles.append(title)
                content_type = get_content_type_by_extension(info_dict['ext'])
                shutil.move(info_dict['filename'], settings.MEDIA_ROOT)
                moved_filename = os.path.join(settings.MEDIA_ROOT, os.path.basename(info_dict['filename']))
                content_item = ContentItem(title=title, content_type=content_type, bucket=bucket)
                content_item.file.name = moved_filename
                content_item.save()

        task_result.status = FetchTaskResult.Status.finished
        titles_str = ', '.join(titles)
        task_result.text = f'{titles_str} - {url}'
        task_result.save()

    except Exception as e:
        task_result.status = FetchTaskResult.Status.error
        task_result.error = str(e)
        task_result.save()
        raise e



