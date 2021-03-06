import tensorflow as tf
import numpy as np
import cv2


def DateSet(file_list, args, debug=False):
    file_list, landmarks, attributes = gen_data(file_list)
    if debug:
        n = args.batch_size * 10
        file_list = file_list[:n]
        landmarks = landmarks[:n]
        attributes = attributes[:n]

    dataset = tf.data.Dataset.from_tensor_slices((file_list, landmarks, attributes))

    def _parse_data(filename, landmarks, attributes):
        file_contents = tf.read_file(filename)
        image = tf.image.decode_png(file_contents, channels=args.image_channels)
        image = tf.image.resize_images(image, (args.image_size, args.image_size), method=0)

        # # 添加亮度,对比度的数据增强
        # image = tf.image.random_brightness(image, max_delta=60)
        # image = tf.image.random_contrast(image, lower=0.2, upper=1.8)

        image = tf.cast(image, tf.float32)
        image = image / 256.0
        return (image, landmarks, attributes)

    dataset = dataset.map(_parse_data)
    dataset = dataset.shuffle(buffer_size=10000)  # ???
    # dataset = dataset.shuffle(buffer_size=len(file_list))
    return dataset, len(file_list)


def gen_data(file_list):
    with open(file_list, 'r') as f:
        lines = f.readlines()
    filenames, landmarks,attributes = [], [], []
    for line in lines:
        line = line.strip().split()
        path = line[0]
        landmark = line[1:137]
        attribute = line[137:]

        landmark = np.asarray(landmark, dtype=np.float32)
        attribute = np.asarray(attribute, dtype=np.int32)
        filenames.append(path)
        landmarks.append(landmark)
        attributes.append(attribute)
    filenames = np.asarray(filenames, dtype=np.str)
    landmarks = np.asarray(landmarks, dtype=np.float32)
    attributes = np.asarray(attributes, dtype=np.int32)
    return (filenames, landmarks, attributes)


if __name__ == '__main__':
    file_list = 'data/train_data/list.txt'
    filenames, landmarks, attributes = gen_data(file_list)
    for i in range(len(filenames)):
        filename = filenames[i]
        landmark = landmarks[i]
        attribute = attributes[i]
        print(attribute)
        img = cv2.imread(filename)
        h,w,_ = img.shape
        landmark = landmark.reshape(-1,2)*[h,w]
        for (x,y) in landmark.astype(np.int32):
            cv2.circle(img, (x,y),1,(0,0,255))
        cv2.imshow('0', img)
        cv2.waitKey(0)
