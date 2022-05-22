import os
import numpy as np
# import skimage.io
import matplotlib
import matplotlib.pyplot as plt
import cv2
from flask import *
import scipy.interpolate as si
# matplotlib.use('Agg')
'''
app = Flask(__name__, static_url_path='', static_folder='./')
app.config['UPLOAD_FOLDER'] = './images'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def edges(filename):
    frame = cv2.imread(os.path.join('images', filename))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    vector = frame[:, 450, 0]
    alk = np.reshape(vector, (-1, 1))
    b = np.zeros((x,2))
    b[:, 1] = vector
    b[:, 0] = range(len(vector))
    blur = cv2.blur(frame, (5, 5))
    edged = cv2.Canny(blur, 50, 200)
    result = frame.copy()
    (a, b) = edged.shape
    for i in range(a - 10):
        for j in range(b):
            if edged[i, j] >= 200:
                result[i:i + 5, j, 0] = 255
                result[i:i + 5, j, 1] = 255
                result[i:i + 5, j, 2] = 255
    plt.axis('off')
    plt.imshow(result)
    plt.savefig(os.path.join('images', 'result.png'), bbox_inches='tight')


def histograma(alpha=1, beta=0, otsu=127):
    img = cv2.imread('./images/imagen.jpg', -1)
    # cv2.imshow('GoldenGate', img)
    imgx = cv2.imread('./images/imagen.jpg', 0)
    equ = cv2.equalizeHist(imgx)
    res = np.hstack((imgx, equ))
    ret1, th1 = cv2.threshold(imgx, otsu, 255, cv2.THRESH_BINARY)
    cv2.imwrite('./images/otsu.png', th1)
    cv2.imwrite('./images/ecualizado.png', res)
    # Contrast control (1.0-3.0)
    # Brightness control (0-100)
    adjustado = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    resx = np.hstack((img, adjustado))
    cv2.imwrite('./images/brillo.png', resx)
    largo, ancho, canal = img.shape
    color = ('b', 'g', 'r')
    for channel, col in enumerate(color):
        histr = cv2.calcHist([img], [channel], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    plt.title('Histogram for color scale picture')
    # plt.show()
    plt.savefig('images/histograma.png')
    return largo, ancho, canal


@app.route('/report', methods=['GET', 'POST'])
def upload_file():
    if request.form['submit'] == 'add':

        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('index.html')
        file = request.files['file']
        print(file)
        print(type(file))
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return render_template('index.html')
        if file and allowed_file(file.filename):
            knots = float(request.form['knots'])
            coefficients = float(request.form['coefficients'])
            curve_degree = float(request.form['curvedegree'])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            edges(file.filename)
            return render_template('index.html', x=1)
    return render_template('index.html')


@app.route('/addx', methods=['GET', 'POST'])
def modificar():
    if request.form['submit'] == 'add':
        brillo = float(request.form['brillo'])
        contraste = float(request.form['contraste'])
        otsu = float(request.form['otsu'])
        largo, ancho, canal = histograma(contraste, brillo, otsu)
        return render_template('index.html', largo=largo, ancho=ancho, canal=canal)
    return render_template('index.html')


@app.route('/')
def list():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
'''


def bspline(cv, n=100, degree=3):
    """ Calculate n samples on a bspline

        cv :      Array ov control vertices
        n  :      Number of samples to return
        degree:   Curve degree
    """
    cv = np.asarray(cv)
    count = cv.shape[0]

    # Prevent degree from exceeding count-1, otherwise splev will crash
    degree = np.clip(degree, 1, count-1)

    # Calculate knot vector
    kv = np.array([0]*degree + list(range(count-degree+1)) + [count-degree]*degree,dtype='int')

    # Calculate query range
    u = np.linspace(0,(count-degree),n)

    # Calculate result
    return np.array(si.splev(u, (kv,cv.T,degree))).T


colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')

cv = np.array([[50.,  25.],
   [59.,  12.],
   [50.,  10.],
   [57.,   2.],
   [40.,   4.],
   [40.,   14.]])

plt.plot(cv[:, 0], cv[:, 1], 'o-', label='Control Points')

for d in range(1, 5):
    p = bspline(cv, n=100, degree=d)
    x,y = p.T
    plt.plot(x, y, 'k-', label='Degree %s'%d, color=colors[d%len(colors)])

plt.minorticks_on()
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(35, 70)
plt.ylim(0, 30)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()