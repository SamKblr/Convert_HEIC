# import os
# import numpy as np
# import matplotlib.pyplot as plt
# from PIL import Image
# from pillow_heif import register_heif_opener


# def read_HEIC_image_to_numpy(image_path):
#     # Enregistre le support HEIC pour Pillow
#     register_heif_opener()
#     img = Image.open(image_path)
#     img = img.convert("RGB")  # convertit en RGB classique
#     return np.array(img)


# def display_image(image):
#     print(f"Shape : {image.shape}")
#     plt.figure(figsize=(10, 10))
#     plt.imshow(image)
#     plt.axis("off")
#     plt.show()


# def convert_array_image_to_other_format(image, save_path, format="png"):
#     PIL_image = Image.fromarray(image)
#     PIL_image.save(save_path + "." + format)


# def get_HEIC_filepaths(main_folder_directory):
#     dict_HEIC_filepaths = {}
#     for dirpath, dirnames, filenames in os.walk(main_folder_directory):
#         for filename in filenames:
#             if filename.endswith(".HEIC"):
#                 # print(f"{dirpath} : {dirnames} ---> {filename}")
#                 if dirpath not in dict_HEIC_filepaths:
#                     dict_HEIC_filepaths[dirpath] = []
#                 dict_HEIC_filepaths[dirpath].append(filename)
#     return dict_HEIC_filepaths


# def convert_HEIC_images_to_other_format_across_subfolders(main_folder_path, directory_save_path, output_format="png"):
#     save_path = os.path.join(directory_save_path, "HEIC_converted_to_" + output_format)
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)
#     else:
#         raise Exception(
#             f"Save directory already exist. {save_path}. Rename it or remove it before running the conversion."
#         )
#     dict_HEIC_filepaths = get_HEIC_filepaths(main_folder_path)
#     cpt = 0
#     for dirname in dict_HEIC_filepaths:
#         for filename in dict_HEIC_filepaths[dirname]:
#             image_path = os.path.join(dirname, filename)
#             img = read_HEIC_image_to_numpy(image_path)
#             save_filename = os.path.join(save_path, filename.split(".")[0])
#             convert_array_image_to_other_format(img, save_filename, format="png")
#             cpt += 1
#     print(f"Conversion finished. Files : {cpt}.")


# def hello_world():
#     print("hello world")

import os
import numpy as np
from PIL import Image
from pillow_heif import register_heif_opener
from concurrent.futures import ThreadPoolExecutor, as_completed

# Active le support HEIC
register_heif_opener()


def read_HEIC_image_to_numpy(image_path):
    """Read a HEIC image and convert it into a rgb numpy array"""
    img = Image.open(image_path)
    img = img.convert("RGB")
    return np.array(img)


def display_image(image):
    """Display a numpy array"""
    import matplotlib.pyplot as plt

    print(f"Shape : {image.shape}")
    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    plt.axis("off")
    plt.show()


def convert_array_image_to_other_format(image, save_path, format="png"):
    """Convert a numpy image as a file in another format"""
    pil_image = Image.fromarray(image)
    pil_image.save(f"{save_path}.{format}", format.upper())


def get_HEIC_filepaths(main_folder_directory):
    """Iterate in subfolders and extract HEIC file paths."""
    dict_HEIC_filepaths = {}
    for dirpath, _, filenames in os.walk(main_folder_directory):
        for filename in filenames:
            if filename.lower().endswith(".heic"):
                if dirpath not in dict_HEIC_filepaths:
                    dict_HEIC_filepaths[dirpath] = []
                dict_HEIC_filepaths[dirpath].append(filename)
    return dict_HEIC_filepaths


def convert_single_image(image_path, save_dir, output_format="png"):
    """Convert a signel HEIC image"""
    try:
        img = read_HEIC_image_to_numpy(image_path)
        filename_wo_ext = os.path.splitext(os.path.basename(image_path))[0]
        save_filename = os.path.join(save_dir, filename_wo_ext)
        convert_array_image_to_other_format(img, save_filename, format=output_format)
        # print(f"{filename_wo_ext}.{output_format}")
        return True
    except Exception as e:
        print(f"Erreur {image_path}: {e}")
        return False


def convert_HEIC_images_to_other_format_across_subfolders(
    main_folder_path, directory_save_path, output_format="png", overwrite=False, files_subset=None, workers=4
):
    """
    Convertit toutes les images HEIC dans les sous-dossiers.
    Si files_subset est fourni, ne convertit que ces fichiers.
    workers permet d'utiliser plusieurs threads (par défaut 1 = séquentiel).
    """
    from concurrent.futures import ThreadPoolExecutor

    if files_subset:
        all_files = files_subset
    else:
        dict_HEIC_filepaths = get_HEIC_filepaths(main_folder_path)
        all_files = [
            os.path.join(dirname, filename) for dirname, files in dict_HEIC_filepaths.items() for filename in files
        ]

    save_path = os.path.join(directory_save_path, f"HEIC_converted_to_{output_format}")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    elif not overwrite:
        raise FileExistsError(f"Le dossier {save_path} existe déjà. Supprimez-le ou utilisez overwrite=True.")

    def convert_single_file(image_path):
        try:
            img = read_HEIC_image_to_numpy(image_path)
            filename_wo_ext = os.path.splitext(os.path.basename(image_path))[0]
            save_filename = os.path.join(save_path, filename_wo_ext)
            convert_array_image_to_other_format(img, save_filename, format=output_format)
        except Exception as e:
            print(f"❌ Erreur pour {image_path}: {e}")

    if workers > 1:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            executor.map(convert_single_file, all_files)
    else:
        for image_path in all_files:
            convert_single_file(image_path)


def hello_world():
    print("hello world")
