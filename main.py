import os, sys
from pymediainfo import MediaInfo
from pyfiglet import Figlet
import zazzle
from tqdm import tqdm

# Initialize logging
zazzle.ZZ_Init.configure_logger(file_name="plex_optimizer", directory="C:/ah/github/ah_plex_optimizer")
log = zazzle.ZZ_Logging.log

class AH_ASCII:
    def print_intro_consol_blurb(text, font):
        font = Figlet(font=f"{font}")
        log(1, font.renderText(f"{text}"), flag=False)

class AH_FILES:
    def get_unoptimized_videos():
        pass

    def rename_files(old_name, new_name):
        log(1, f"Renaming:")
        log(0, f"{old_name} >>> {new_name}")
        os.rename(old_name, new_name)

    def get_unlabeled_videos(video_list):
        log(1, f"Getting unlabeled videos...")
        videos_not_labeled = []
        for video in video_list:
            end_of_file = video[-13:]
            if "Mbps" in end_of_file:
                log(0, f"Namespace already in: {video}")
            else:
                videos_not_labeled.append(video)

        for video in videos_not_labeled:
            log(0, f"{video}")

        return(videos_not_labeled)

    def add_bitrate_to_namespace(file_path):
        log(1, f"Adding namespace to {file_path}")

        log(0, f"Getting bitrate...")
        bitrate = AH_VIDEO.get_video_bitrate_mediainfo(file_path)
        mbps = AH_VIDEO.convert_bitrate_to_mbps(bitrate_bps=bitrate)
        log(0, f"Bitrate: {mbps}")

        extension = file_path[-4:]
        new_front = file_path.replace(extension, "")
        mbps = str(mbps).replace(".", ",")
        mbps = f".{mbps}Mbps"
        new_name = f"{new_front}{mbps}{extension}"

        AH_FILES.rename_files(file_path, new_name)

    def get_files_in_directory(directory):
        log(1, f"Getting all folders in directory: {directory}...")
        file_names = os.listdir(directory)

        file_paths = []
        if file_names != None:
            for name in file_names:
                file_paths.append(os.path.join(directory, name))

        for path in file_paths:
            log(0, f"{path}")

        return file_paths

    def find_video_files_in_directory(directory):
        log(1, f"Getting all video files in directory: {directory}")
        video_paths = []
        files = os.listdir(directory)
        for file in files:
            full_path = os.path.join(directory, file)
            if os.path.isfile(full_path):
                if full_path.endswith(".mp4") or full_path.endswith(".mkv"):
                    video_paths.append(os.path.join(directory, file))

        for path in video_paths:
            log(0, path)

        return video_paths

    def rename_file():
        pass

class AH_VIDEO:
    def get_video_bitrate_mediainfo(file_path):
        try:
            media_info = MediaInfo.parse(file_path)
            for track in media_info.tracks:
                if track.track_type == "Video" and track.bit_rate:
                    return int(track.bit_rate)
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def convert_bitrate_to_mbps(bitrate_bps):
        if bitrate_bps is None:
            return None
        # Divide by 1,000,000 to get Mbps
        return round(bitrate_bps / 1_000_000, 2)

if __name__ == "__main__":

    # Console blurb because go big or go home amirite
    AH_ASCII.print_intro_consol_blurb(text="THE PLEX OPTIMIZER", font="doom")
    print()

    # Set library file paths
    movie_library_path = input(f"Folder to run on: ")

    # Ask the user what to do
    print(f"What would you like to do?")
    move_on = False

    while move_on == False:
        print(f"1 - Label media with bitrates")
        print(f"2 - Optimize media with low bitrate 1080p versions")

        choice = input()

        # Label all video media with it's bitrate
        if choice == "1":
            movies_folder_files = AH_FILES.get_files_in_directory(movie_library_path)

            # Get all the actual movie files
            movies = []
            for movie in movies_folder_files:
                video_files = AH_FILES.find_video_files_in_directory(movie)
                for video in video_files:
                    movies.append(video)

            # Find all the unlabeled videos in the library
            unlabeled_videos = AH_FILES.get_unlabeled_videos(movies)

            # If there are unlabeled videos, add their bitrate to their name
            if unlabeled_videos:
                for video in tqdm(unlabeled_videos, desc="Renaming files", unit="file", dynamic_ncols=True, leave=True, file=sys.stdout):
                    AH_FILES.add_bitrate_to_namespace(video)

            # Exit loop
            break

        elif choice == "2":
            pass
        else:
            print("Please enter a valid number")

    # Find full file paths of all videos in the library
    # Walk through the "Movies" folder
    # If we find a video file, make sure it's labeled with it's bitrate
    # For each folder, figure out if we've optimized the files already
    # Return a list of file paths
    # Walk through the "TV Shows" folder
    # Return