import os, sys
from pymediainfo import MediaInfo
from pyfiglet import Figlet
import zazzle
from tqdm import tqdm
import subprocess
import json

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
            # fix any borked names
            if "NoneMbps" in video:
                AH_FILES.rename_files(video, video.replace("NoneMbps.", ""))

            # Find the videos already named
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
        bitrate = AH_VIDEO.get_video_bitrate_ffmpeg(file_path)
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

    def get_all_files_recursively(directory):
        all_files = []
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isdir(full_path):
                # Recur for subdirectories
                all_files.extend(AH_FILES.get_all_files_recursively(full_path))
            elif os.path.isfile(full_path):
                all_files.append(full_path)
        return all_files

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

class AH_VIDEO:
    def get_video_bitrate_ffmpeg(file_path):
        try:
            # Run ffprobe to get metadata as JSON
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                 'format=bit_rate', '-of', 'json', file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Parse the JSON output
            metadata = json.loads(result.stdout)
            return int(metadata['format']['bit_rate']) if 'format' in metadata and 'bit_rate' in metadata[
                'format'] else None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def convert_bitrate_to_mbps(bitrate_bps):
        if bitrate_bps is None:
            return None
        # Divide by 1,000,000 to get Mbps
        return round(bitrate_bps / 1_000_000, 2)

    def create_optimized_video_sdr_to_sdr(input_file, target_bitrate, bitrate_buffer):
        try:
            # ffmpeg command to convert MKV to MP4 with target bitrate
            command = [
                'ffmpeg',
                '-i', input_file,  # Input file
                '-b:v', f"{target_bitrate}M",  # Set video bitrate
                '-maxrate', f"{target_bitrate}M",
                '-bufsize', f"1M",
                '-b:a', '128k',  # Set audio bitrate (optional)
                '-c:v', 'libx265',  # Video codec (H.264)
                '-c:a', 'aac',  # Audio codec
                '-movflags', '+faststart',  # Optimize for progressive streaming
                '-resize', '1920x1080',
                f"{input_file.replace('.mkv', '')}.optimized.mp4"  # Output file
            ]

            # Run the ffmpeg command
            subprocess.run(command, check=True)
            print(f"Conversion completed")
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e}")
        except FileNotFoundError:
            print("Error: ffmpeg is not installed or not in PATH.")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def create_optimized_video_hdr_to_sdr(input_file, target_bitrate, bitrate_buffer):
        try:
            # ffmpeg command to convert MKV to MP4 with target bitrate
            command = [
                'ffmpeg',
                '-i', input_file,  # Input file
                '-b:v', f"{target_bitrate}M",  # Set video bitrate
                '-maxrate', f"{target_bitrate}M",
                '-bufsize', f"1M",
                '-b:a', '128k',  # Set audio bitrate (optional)
                '-c:v', 'libx265',  # Video codec (H.264)
                '-c:a', 'aac',  # Audio codec
                '-movflags', '+faststart',  # Optimize for progressive streaming
                '-resize', '1920x1080',
                '-vf', 'zscale=t=linear:npl=100', 'format=gbrpf32le', 'zscale=p=bt709', 'tonemap=tonemap=hable:desat=0', 'zscale=t=bt709:m=bt709:r=tv', 'format=yuv420p', # Convert HDR to SDR
                f"{input_file.replace('.mkv', '')}.optimized.mp4"  # Output file
            ]

            # Run the ffmpeg command
            subprocess.run(command, check=True)
            print(f"Conversion completed")
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e}")
        except FileNotFoundError:
            print("Error: ffmpeg is not installed or not in PATH.")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":

    # Console blurb because go big or go home amirite
    AH_ASCII.print_intro_consol_blurb(text="THE PLEX OPTIMIZER", font="doom")
    print()

    # Set library file paths
    movie_library_path = input(f"Folder to run on: ")

    # Ask the user what to do
    print("")
    print(f"What would you like to do?")
    move_on = False

    while move_on == False:
        print("")
        print(f"1 - Label media with bitrates in file names")
        print(f"2 - Optimize media with low bitrate 1080p versions")
        print(f"3 - Exit")

        choice = input()

        # Label all video media with it's bitrate
        if choice == "1":

            # Get all the files in our given directory
            all_videos = []
            all_files = AH_FILES.get_all_files_recursively(movie_library_path)

            for file in all_files:
                if os.path.isfile(file):
                    if file.endswith(".mkv") or file.endswith(".mp4"):
                        all_videos.append(file)

            # Find all the unlabeled videos in the library
            unlabeled_videos = AH_FILES.get_unlabeled_videos(all_videos)

            # If there are unlabeled videos, add their bitrate to their name
            if unlabeled_videos:
                for video in tqdm(unlabeled_videos, desc="Renaming files", unit="file", dynamic_ncols=True, leave=True, file=sys.stdout):
                    AH_FILES.add_bitrate_to_namespace(video)

        elif choice == "2":
            log(1, "WIP")
        elif choice == "3":
            log(2, f"Exiting...")
            break
        else:
            print("Please enter a valid number")