import os

import numpy as np
from PIL import Image
from flask import (
    Flask,
    Response,
    jsonify,
    render_template,
)
from flask_bootstrap import Bootstrap5
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from sklearn.cluster import KMeans
from wtforms import SubmitField

app = Flask(__name__)
Bootstrap5(app)
app.config['SECRET_KEY'] = "dskdkskamdsakmdak"
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


class UploadForm(FlaskForm):
    photo = FileField(
        validators=[FileAllowed(photos, 'Only images are allowed'), FileRequired('File field should not be empty')])
    submit = SubmitField("Upload")


@app.route('/analyze', methods=["POST"])
def analyze():
    form = UploadForm()
    if not form.validate_on_submit():
        return Response("Bad request", 400)

    file = photos.save(form.photo.data)
    photo_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], file)
    try:
        dominant_colors_hex, color_occurrences = get_dominant_colors(
            photo_path
            )
        return jsonify(
            [{
                "color": color_hex, "occurrence": f"{occurrence:.4f}"
            } for color_hex, occurrence in
                zip(dominant_colors_hex, color_occurrences)
            ]
        )
    finally:
        os.remove(photo_path)


def get_dominant_colors(image_path):
    with Image.open(image_path) as image:
        width, height = image.size
        image_size = (width * height) / 100
        image = image.convert('RGB')
        img_array = np.array(image)
        pixels = img_array.reshape(-1, 3)
        kmeans = KMeans(n_clusters=10, random_state=0)
        labels = kmeans.fit_predict(pixels)
        centers = kmeans.cluster_centers_
        color_counts = {}
        for label in np.unique(labels):
            color = tuple(centers[label].astype(int))
            color_counts[color] = np.count_nonzero(labels == label)
        sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
        dominant_colors = [color for color, count in sorted_colors[:10]]
        color_occurrences = [count / image_size for color, count in sorted_colors[:10]]
        dominant_colors_hex = ['#%02x%02x%02x' % color for color in dominant_colors]
    return dominant_colors_hex, color_occurrences


@app.route('/', methods=["GET", "POST"])
def main_page():
    form = UploadForm()
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=False)
