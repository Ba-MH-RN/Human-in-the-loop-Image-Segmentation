#imports from other directory
import sys, os 
sys.path.append(os.path.abspath(os.path.join('..', 'backend')))
from ImageSegmentation.processing.preprocess import preprocess

def test_load_image_from_path_successful():
    imagePath = "tests/Data/tests/testImages/testCat.jpg"
    image = preprocess.loadImageFromPath(imagePath)
    assert image is not None

def test_resize_Image_smaller_diemension_correct():
    imagePath = "tests/Data/tests/testImages/testCat.jpg"
    image = preprocess.loadImageFromPath(imagePath)
    width, height = (256,128)
    scaledImage = preprocess.scaleImage(image=image,height=height,width=width)
    assert width == scaledImage.width
    assert height == scaledImage.height

def test_resize_Image_bigger_diemension_correct():
    imagePath = "tests/Data/tests/testImages/testCat.jpg"
    image = preprocess.loadImageFromPath(imagePath)
    width, height = (8000,4000)
    scaledImage = preprocess.scaleImage(image=image,height=height,width=width)
    assert width == scaledImage.width
    assert height == scaledImage.height

def test_expand_to_Square_diemension_correct():
    imagePath = "tests/Data/tests/testImages/testCat.jpg"
    image = preprocess.loadImageFromPath(imagePath)
    paddedImage = preprocess.expandToSquare(image=image,backgroundColor=(0,0,0))
    assert paddedImage.height == paddedImage.width

def test_Square_expand_to_Square_diemension_correct():
    imagePath = "tests/Data/tests/testImages/testCat.jpg"
    image = preprocess.loadImageFromPath(imagePath)
    scaledImage = preprocess.scaleImage(image=image,height=128,width=128)
    paddedImage = preprocess.expandToSquare(image=scaledImage,backgroundColor=(0,0,0))
    assert paddedImage.height == paddedImage.width

def test_Portrait_expand_to_Square_diemension_correct():
    imagePath = "tests/Data/tests/testImages/testCat.jpg"
    image = preprocess.loadImageFromPath(imagePath)
    scaledImage = preprocess.scaleImage(image=image,height=256,width=128)
    paddedImage = preprocess.expandToSquare(image=scaledImage,backgroundColor=(0,0,0))
    assert paddedImage.height == paddedImage.width

def test_Landscape_expand_to_Square_diemension_correct():
    imagePath = "tests/Data/tests/testImages/testCat.jpg"
    image = preprocess.loadImageFromPath(imagePath)
    scaledImage = preprocess.scaleImage(image=image,height=128,width=256)
    paddedImage = preprocess.expandToSquare(image=scaledImage,backgroundColor=(0,0,0))
    assert paddedImage.height == paddedImage.width

def test_resize_Image_To_Square_With_Same_Aspect_Ration_diemension_correct():
    imagePath = "tests/Data/tests/testImages/testCat.jpg"
    image = preprocess.loadImageFromPath(imagePath)
    sideLength = 128
    scaledImage = preprocess.resizeImageToSquareWithSameAspectRation(image=image, sideLength=sideLength)
    assert scaledImage.height == scaledImage.width == sideLength