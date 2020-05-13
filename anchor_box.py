import glob
import xml.etree.ElementTree as ET

import numpy as np

import kmeans

k = kmeans.YOLO_Kmeans(9, '2012_train.txt')


ANNOTATIONS_PATH = "D:\project\yolo\VOCdevkit\VOC2007\Annotations"
CLUSTERS = 9


def load_dataset(path):

    dataset = []
    for xml_file in glob.glob("{}/*xml".format(path)):
        tree = ET.parse(xml_file)

        height = int(tree.findtext("./size/height"))
        width = int(tree.findtext("./size/width"))

        for obj in tree.iter("object"):
            xmin = int(obj.findtext("bndbox/xmin")) / width
            ymin = int(obj.findtext("bndbox/ymin")) / height
            xmax = int(obj.findtext("bndbox/xmax")) / width
            ymax = int(obj.findtext("bndbox/ymax")) / height

            xmin = np.float64(xmin)
            ymin = np.float64(ymin)
            xmax = np.float64(xmax)
            ymax = np.float64(ymax)
            if xmax == xmin or ymax == ymin:
                print(xml_file)
            dataset.append([xmax - xmin, ymax - ymin])
    return np.array(dataset)


if __name__ == '__main__':
    # print(__file__)
    data = load_dataset(ANNOTATIONS_PATH)
    out = k.kmeans(data, k=CLUSTERS)
    # clusters = [[10,13],[16,30],[33,23],[30,61],[62,45],[59,119],[116,90],[156,198],[373,326]]
    # out= np.array(clusters)/416.0
    print(out)
    print("Accuracy: {:.2f}%".format(k.avg_iou(data, out) * 100))
    print("Boxes:\n {}-{}".format(out[:, 0] * 416, out[:, 1] * 416))

    ratios = np.around(out[:, 0] / out[:, 1], decimals=2).tolist()
    print("Ratios:\n {}".format(sorted(ratios)))
