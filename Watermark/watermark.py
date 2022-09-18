# import all the libraries
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def watermark(image, watermark, position):
    # make the image object for PIL
    image = Image.open(image)
    # convert the image to RGBA
    image = image.convert('RGBA')
    # make the image object for PIL
    watermark = Image.open(watermark)
    # convert the image to RGBA
    watermark = watermark.convert('RGBA')
    # make the image object for PIL
    watermark = watermark.resize((image.width // 10, image.height // 10))
    # paste the watermark (with alpha layer) to the image
    image.paste(watermark, position, mask=watermark)
    # convert the image to RGB
    image = image.convert('RGB')
    # save watermarked image
    image.save('watermarked_image.jpg')
    # show the image
    plt.imshow(np.asarray(image))
    plt.show()