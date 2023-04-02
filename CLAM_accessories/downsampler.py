import os.path
import openslide
import argparse

parser = argparse.ArgumentParser(description='Downsample WSI images using OpenSlide library')
parser.add_argument('--src', type=str, required=True, help='Path to directory containing WSI images')
parser.add_argument('--dest', type=str, required=True, help='Path to directory to save downsampled images')
parser.add_argument('--scale', type=int, default=16, help='Scale factor for downsampling (default: 16)')
args = parser.parse_args()

print("WSI Downsampler using OpenSlide get_thumbnail function.")
print("No guarantees available in terms of bugs or memory usage")
print("Downsampling at scale of: ", args.scale)
print("Source path: ", args.src)
print("Destination path: ", args.dest)

for path, directories, files in os.walk(args.src):
    for file in files:
        print("Looking for: ", path, file)
        new_name = os.path.splitext(file)[0]
        if os.path.exists(os.path.join(args.dest, new_name + ".jpg")):
            print("Downsample already exists, skipping...\n")
            continue
        img_path = os.path.join(path, file)
        try:
            with openslide.OpenSlide(img_path) as image:
                img_w, img_h = image.level_dimensions[0]
                print("Found file:", img_path, "dimensions: ", img_w, img_h)
                print("Downsampling...")
                thumbnail = image.get_thumbnail(size=(img_w // args.scale, img_h // args.scale))
                print("Done. Downsampled dimensions: ", img_w // args.scale, " width, ", img_h // args.scale, " height")
                print("Saving to:", args.dest, "as ", new_name, ".jpg\n")
                thumbnail.save(os.path.join(args.dest, new_name + ".jpg"))
        except openslide.OpenSlideUnsupportedFormatError:
            with open("skipped.txt", 'a') as error_file:
                error_file.write(new_name + " SKIPPED FILE\n")
            print("Error! This file cannot be opened with OpenSlide due to formatting issues")
        except openslide.OpenSlideError:
            with open("skipped.txt", 'a') as error_file:
                error_file.write(new_name + " OpenSlide Library Issue \n")
            print("Error! OpenSlide Library Issue.")
        except Exception as e:
            print("Error! Unknown Issue. Recorded in error.txt.")
            with open('error.txt', 'a') as error_file:
                error_file.write(f"{type(e).__name__}: {str(e)}\n")
                error_file.write("From processing: " + new_name + "\n")

