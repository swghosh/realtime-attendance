KEY_FILE = '/Users/swg/Desktop/realtimeattendanceproject@noble-cocoa-217110.iam.gserviceaccount.com.json'
BUCKET_NAME = 'realtimeattendanceproject'
HCC_FRONTAL_FACE = '/Users/swg/Repositories/pett-notebooks/cascades/haarcascades/haarcascade_frontalface_alt.xml'
DESIRED_SIZE = (100, 100)

from google.cloud import storage
import pickle
import cv2
import datetime
import numpy as np

class Service:
    """
    Service class equips with different functionalities
    for the porject. A single instance of this class
    may perform multiple related functionalities.

    Attributes:
    clf: Image Classifier (scikit-learn) Trained Model
    pca: PCA (scikit-learn) Object
    class_labels: List of Valid Class Labels
    """
    clf = None
    pca = None
    class_labels = None

    def get_trained_model(self):
        """
        Retrieve the trained model that has been stored to a
        GCS Bucket. Three objects are present the bucket in 
        pickle format.
        - model.pickle [Trained Model for Image Classification (scikit-learn Model)]
        - pca.pickle [PCA Object (scikit-learn PCA)]
        - class_labels.pickle [List of Valid Class Labels for Image Classification]
        
        This function must be called before any other
        function can be used from this class.

        Returns:
        (model, pca, class_labels): a tuple containing all
        three objects as aforementioned
        """
        client = storage.Client.from_service_account_json(KEY_FILE)
        bucket = client.get_bucket(BUCKET_NAME)

        model_blob = bucket.blob('model.pickle').download_as_string()
        pca_blob = bucket.blob('pca.pickle').download_as_string()
        class_labels_blob = bucket.blob('class_labels.pickle').download_as_string()

        self.clf, self.pca, self.class_labels = pickle.loads(model_blob), pickle.loads(pca_blob), pickle.loads(class_labels_blob)

        return (self.clf, self.pca, self.class_labels)

    def get_face_names(self, img): # img should be grayscale
        """
        Predict class label(s) / name of face(s) for
        each detected face in the given image. A grayscale
        image should be used and face extraction is carried
        internally.

        Arguments:
        img: numpy array of any size that represents
        a single grayscale image containing face(s)

        Returns:
        face_names: list of class labels corresponding
        to each face that was detected from input image
        """
        hcc = cv2.CascadeClassifier(HCC_FRONTAL_FACE)
        faces = hcc.detectMultiScale(img, scaleFactor = 1.2, minNeighbors = 5)

        current_faces = []
        for (x, y, w, h) in faces:
            face = cv2.resize(img[y:y+h, x:x+w], DESIRED_SIZE).flatten()
            current_faces.append(face)
        X = np.array(current_faces, dtype = 'uint8')
        
        X_pca = self.pca.transform(X)
        y = self.clf.predict(X_pca)

        return [self.class_labels[y_i] for y_i in y]
