from autodistill.detection import CaptionOntology
from autodistill_grounded_sam import GroundedSAM
from google_images_downloader import GoogleImagesDownloader
import supervision as sv

class ImageProcessor:
    def __init__(self):
        pass

    @staticmethod
    def create_ontology_dict():
        ontology_input = input("Enter the ontology as a comma-separated list (e.g., car:car or more classes car:vehicle,person:human): ")

        if ":" in ontology_input:
            ontology_dict = dict(item.split(":") for item in ontology_input.split(","))
        else:
            ontology_dict = {ontology_input: ontology_input}

        return ontology_dict

    @staticmethod
    def create_captions(ontology_dict, image_folder, dataset_folder):
        ontology = CaptionOntology(ontology_dict)
        base_model = GroundedSAM(ontology=ontology)
        dataset = base_model.label(
            input_folder=image_folder,
            extension=".png",
            output_folder=dataset_folder
        )
        return dataset

    @staticmethod
    def plot(samples_no):
        ANNOTATIONS_DIRECTORY_PATH = "dataset/train/labels"
        IMAGES_DIRECTORY_PATH = "dataset/train/images"
        DATA_YAML_PATH = "dataset/data.yaml"
        SAMPLE_SIZE = samples_no
        SAMPLE_GRID_SIZE = (samples_no // 4, samples_no // 4)
        SAMPLE_PLOT_SIZE = (samples_no, samples_no)
        dataset = sv.DetectionDataset.from_yolo(
            images_directory_path=IMAGES_DIRECTORY_PATH,
            annotations_directory_path=ANNOTATIONS_DIRECTORY_PATH,
            data_yaml_path=DATA_YAML_PATH
        )
        len(dataset)
        image_names = list(dataset.images.keys())[:SAMPLE_SIZE]
        mask_annotator = sv.MaskAnnotator()
        box_annotator = sv.BoxAnnotator()
        images = []
        for image_name in image_names:
            image = dataset.images[image_name]
            annotations = dataset.annotations[image_name]
            labels = [
                dataset.classes[class_id]
                for class_id
                in annotations.class_id]
            annotates_image = mask_annotator.annotate(
                scene=image.copy(),
                detections=annotations)
            annotates_image = box_annotator.annotate(
                scene=annotates_image,
                detections=annotations,
                labels=labels)
            images.append(annotates_image)
        sv.plot_images_grid(
            images=images,
            titles=image_names,
            grid_size=SAMPLE_GRID_SIZE,
            size=SAMPLE_PLOT_SIZE)
