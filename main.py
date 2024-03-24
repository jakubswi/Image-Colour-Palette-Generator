import numpy as np
from PIL import Image
from flask import Flask, render_template, send_from_directory, url_for
from flask_bootstrap import Bootstrap5
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from sklearn.cluster import KMeans
import os
import glob

app = Flask(__name__)
Bootstrap5(app)
app.config['SECRET_KEY'] = "dskdkskamdsakmdak"
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Only images are allowed'), FileRequired('File field should not be empty')])
    submit = SubmitField("Upload")

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



@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route('/', methods=["GET", "POST"])
def main_page():
    form = UploadForm()
    if form.validate_on_submit():
        file = photos.save(form.photo.data)
        # photo_path = url_for("get_file", filename=file)
        photo_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], file)
        dominant_colors_hex, color_occurrences = get_dominant_colors(photo_path)
        color_occurrences = [f"{color:.4f}" for color in color_occurrences]
        return render_template("index.html", dominant_colors=dominant_colors_hex, color_occurrences=color_occurrences,
                            file=photo_path, form=form)
    return render_template("index.html", dominant_colors=None, color_occurrences=None,
                           file=None, form=form)

if __name__ == "__main__":
    app.run(debug=True)
