import supervision as sv
from tqdm.notebook import tqdm
from pytube import YouTube
from google_images_downloader import GoogleImagesDownloader

#----------------------------

def download_images(class_name,count):
    downloader = GoogleImagesDownloader(browser="chrome", show=False, debug=False,
                                        quiet=False, disable_safeui=False)  # Constructor with default values

    downloader.download(class_name, limit=count)  # Download 50 images in ./downloads folder
    downloader.close()
#------------------------------------------------------
def extract_images_video(video_path,images_folder_path,frame_strid):
    video_paths = sv.list_files_with_extensions(
        directory=video_path,
        extensions=["mov", "mp4"])

    print(video_paths)

    for video_path in tqdm(video_paths):
        video_name = video_path.stem
        image_name_pattern = video_name + "-{:05d}.png"
        with sv.ImageSink(target_dir_path=images_folder_path, image_name_pattern=image_name_pattern) as sink:
            for image in sv.get_video_frames_generator(source_path=str(video_path), stride=frame_strid):
                sink.save_image(image=image)
    print(f"successfully saved images of video out in folder : {images_folder_path}")

#------------------------------------------------------
def download_yt(video_url, output_path='.'):
    try:
        # Create a YouTube object
        yt = YouTube(video_url)

        # Get the highest resolution stream
        video_stream = yt.streams.get_highest_resolution()

        # Download the video to the specified output path
        video_stream.download(output_path)

        print("Video download successful!")

    except Exception as e:
        print(f"Error: {str(e)}")

