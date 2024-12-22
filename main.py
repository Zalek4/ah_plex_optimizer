import os
from pymediainfo import MediaInfo
from pyfiglet import Figlet
import zazzle

# Initialize logging
zazzle.ZZ_Init.configure_logger()
log = zazzle.ZZ_Logging.log

class AH_ASCII:
    def print_intro_consol_blurb(text, font):
        font = Figlet(font=f"{font}")
        log(1, font.renderText(f"{text}"), flag=False)

class AH_FILES:
    def get_unoptimized_videos():
        pass

    def add_bitrate_to_namespace():
        pass

    def list_files_in_directory():
        pass

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

    # Console blurb because size does indeed matter
    AH_ASCII.print_intro_consol_blurb(text="THE PLEX OPTIMIZER", font="doom")
    print()

    # Example usage
    file_path = "P:\Movies\Airplane! (1980)\Airplane! (1980).1080.HDR.mkv"
    bitrate = AH_VIDEO.get_video_bitrate_mediainfo(file_path=file_path)
    mbps = AH_VIDEO.convert_bitrate_to_mbps(bitrate_bps=bitrate)
    print(f"Bitrate: {mbps} Mbps")