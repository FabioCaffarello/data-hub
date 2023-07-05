from crawler.core.basespider import BaseSpider

import scrapy
import io
# import youtube_dl
import pytube
from crawler import config, items
from . import static, parser


class Spider(BaseSpider):
    config.LoggingConfig()
    name = 'youtube-videos'

    def start_requests(self):
        # self._parser = parser.BotParser()
        self.logger.info(f"Receive Request with input: {self._input_data}")
        # self.url = self._input_data.get("url")
        return self._first_request()

    def _first_request(self):
        yield scrapy.Request(
            # url=self._parser._get_endpoint(),
            url="https://www.youtube.com/watch?v=VqJ6GE1eSno",
            callback=self._on_processing_first_request,
        )

    def _on_processing_first_request(self, response):
        video_url = response.url

        # Download video as bytes using youtube_dl
        # ydl_opts = {
        #     'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        #     'quiet': True,
        #     'extract_flat': False,
        # }
        # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #     video_info = ydl.extract_info(video_url, download=False)
        #     video_bytes = ydl.download([video_url])

                # Download video using pytube
        youtube = pytube.YouTube(video_url)
        video = youtube.streams.get_highest_resolution()
         # Get video information
        video_info = {
            'title': youtube.title,
            'author': youtube.author,
            'duration': youtube.length,
            'views': youtube.views,
            # Add more video information fields as needed
        }




        # Create a buffer to hold the video bytes
        video_bytes = video.stream_to_buffer(io.BytesIO())


        # Upload the video bytes to your storage
        if video_bytes is not None:
            # Replace this section with your storage upload logic
            # For example, you can use a cloud storage service like AWS S3, Google Cloud Storage, etc.
            # storage.upload(video_bytes, video_info['title'] + '.mp4')

          # Access video metadata from video_info
            self.logger.info(f"video_info:{video_info}")
            self.debug_response("video.mp4", video_bytes)

        # You can perform further processing or yield items here if needed
        # ...

        # Return an empty dictionary to indicate the job is complete
        return {}


    #     def get_video_bytes(url):
    #         try:
    #             ydl_opts = {
    #                 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Select best available format
    #                 'quiet': True,  # Suppress console output
    #             }
    #             with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #                 result = ydl.extract_info(url, download=False)
    #                 video_bytes = ydl.download([url])

    #             if 'entries' in result:
    #                 video_info = result['entries'][0]
    #             else:
    #                 video_info = result

    #             return video_bytes, video_info

    #         except Exception as e:
    #             print("An error occurred:", str(e))
    #             return None, None

    #     # Example usage
    #     video_url = "https://www.youtube.com/watch?v=VqJ6GE1eSno"  # Replace with your YouTube video URL

    #     video_bytes, video_info = get_video_bytes(video_url)

    #     if video_bytes is not None:
    #         # Now you can upload the video_bytes to your storage or process it further
    #         # For example, you can upload it to a cloud storage service like AWS S3, Google Cloud Storage, etc.
    #         # Make sure you handle the video_bytes appropriately for your specific use case

    #         # Access video metadata from video_info
    #         video_title = video_info.get('title')
    #         video_duration = video_info.get('duration')
    #         self.logger.info(f"video title:{video_title}")
    #         self.logger.info(f"video_duration:{video_duration}")
    #         self.debug_response("video.mp4", video_url)
    #         # ...
    #         return {}

    #     # Example usage





    #     # yield scrapy.Request(
    #     #     url=self._parser._get_endpoint(),
    #     #     callback=self._on_processing_first_request,
    #     # )

    # # def _on_processing_first_request(self, response):
    # #     self.debug_response('tickers.json', response.json())
    # #     self.logger.info("Receive first respone")

    # #     data = self._parser.generator_parse_data(response.json())
    # #     for _data in data:
    # #         bot_items = items.BotLoader(items.BotItem())
    # #         self.logger.info(f"Receive ticker {_data}")
    # #         bot_items.add_fields(_data)
    # #         yield bot_items.load_item()


