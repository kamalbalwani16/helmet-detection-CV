import os
import random
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

# Paths
BASE_DIR = Path(".")
IMAGES_DIR = BASE_DIR / "dataset1" / "images"
ANNOTATIONS_DIR = BASE_DIR / "dataset1" / "annotations"

OUTPUT_IMAGES_TRAIN = BASE_DIR / "yolo_dataset" / "images" / "train"
OUTPUT_IMAGES_VAL = BASE_DIR / "yolo_dataset" / "images" / "val"
OUTPUT_LABELS_TRAIN = BASE_DIR / "yolo_dataset" / "labels" / "train"
OUTPUT_LABELS_VAL = BASE_DIR / "yolo_dataset" / "labels" / "val"
# Class mapping
CLASSES = {
    "With Helmet": 0,
    "Without Helmet": 1
}

# Train-val split ratio
TRAIN_RATIO = 0.8

# Create output folders
for folder in [
    OUTPUT_IMAGES_TRAIN,
    OUTPUT_IMAGES_VAL,
    OUTPUT_LABELS_TRAIN,
    OUTPUT_LABELS_VAL
]:
    folder.mkdir(parents=True, exist_ok=True)

def convert_box(size, box):
    img_w, img_h = size
    xmin, ymin, xmax, ymax = box

    x_center = ((xmin + xmax) / 2.0) / img_w
    y_center = ((ymin + ymax) / 2.0) / img_h
    width = (xmax - xmin) / img_w
    height = (ymax - ymin) / img_h

    return x_center, y_center, width, height

def convert_xml_to_yolo(xml_file, output_label_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    size = root.find("size")
    img_w = int(size.find("width").text)
    img_h = int(size.find("height").text)

    lines = []

    for obj in root.findall("object"):
        class_name = obj.find("name").text.strip()

        if class_name not in CLASSES:
            print(f"Skipping unknown class '{class_name}' in {xml_file.name}")
            continue

        class_id = CLASSES[class_name]
        bbox = obj.find("bndbox")

        xmin = float(bbox.find("xmin").text)
        ymin = float(bbox.find("ymin").text)
        xmax = float(bbox.find("xmax").text)
        ymax = float(bbox.find("ymax").text)

        x_center, y_center, width, height = convert_box(
            (img_w, img_h), (xmin, ymin, xmax, ymax)
        )

        lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

    with open(output_label_file, "w") as f:
        f.write("\n".join(lines))

def main():
    xml_files = list(ANNOTATIONS_DIR.glob("*.xml"))

    if not xml_files:
        print("No XML files found.")
        return

    random.shuffle(xml_files)
    split_index = int(len(xml_files) * TRAIN_RATIO)

    train_files = xml_files[:split_index]
    val_files = xml_files[split_index:]

    print(f"Total XML files: {len(xml_files)}")
    print(f"Training files: {len(train_files)}")
    print(f"Validation files: {len(val_files)}")

    def process_files(file_list, img_out_dir, label_out_dir):
        for xml_file in file_list:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            filename = root.find("filename").text.strip()
            image_path = IMAGES_DIR / filename

            if not image_path.exists():
                print(f"Image not found: {image_path}")
                continue

            label_filename = Path(filename).stem + ".txt"
            output_label_file = label_out_dir / label_filename

            convert_xml_to_yolo(xml_file, output_label_file)
            shutil.copy(image_path, img_out_dir / filename)

    process_files(train_files, OUTPUT_IMAGES_TRAIN, OUTPUT_LABELS_TRAIN)
    process_files(val_files, OUTPUT_IMAGES_VAL, OUTPUT_LABELS_VAL)

    print("Conversion complete.")

if __name__ == "__main__":
    main()