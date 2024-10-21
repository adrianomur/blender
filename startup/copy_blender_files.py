import os
import shutil

BLENDER_VERSION = 4.2
LOCAL_FOLDER = '/Users/adriano/dev/blender/settings'


def copy_folder(src, dst):
    # Check if source folder exists
    if not os.path.exists(src):
        print(f"Source folder {src} does not exist.")
        return

    # Create destination folder if it doesn't exist
    if not os.path.exists(dst):
        os.makedirs(dst)

    # Copy all the files and subfolders from src to dst
    for item in os.listdir(src):
        source_item = os.path.join(src, item)
        destination_item = os.path.join(dst, item)

        if os.path.isdir(source_item):
            # Recursively copy directories
            shutil.copytree(source_item, destination_item)
        else:
            # Copy files
            shutil.copy2(source_item, destination_item)


def run():
    version_folder = os.path.join(LOCAL_FOLDER, str(BLENDER_VERSION))
    color_management_folder = f'/Applications/Blender.app/Contents/Resources/{BLENDER_VERSION}/datafiles/colormanagement'
    copy_folder(color_management_folder, os.path.join(version_folder, 'colormanagement'))

    config_files = f'/Users/adriano/Library/Application Support/Blender/{BLENDER_VERSION}/config'
    copy_folder(config_files, os.path.join(version_folder, 'config'))


if __name__ == '__main__':
    run()