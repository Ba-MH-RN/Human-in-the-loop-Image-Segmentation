from PIL import Image


class preprocess():
    def loadImageFromPath(imagePath:str) -> Image:
        image = Image.open(imagePath).convert("RGB") #converts CMYK
        return image

    def scaleImage(image: Image, width: int, height: int) -> Image:
        scaledImage = image.resize((width, height))
        return scaledImage

    def expandToSquare(image: Image, backgroundColor:tuple) -> Image:
        width, height = image.size
        if width == height:
            return image
        elif width > height:
            result = Image.new(image.mode, (width, width), backgroundColor)
            result.paste(image, (0, (width - height) // 2))
            return result
        else:
            result = Image.new(image.mode, (height, height), backgroundColor)
            result.paste(image, ((height - width) // 2, 0))
            return result

    def resizeImageToSquareWithSameAspectRation(image:Image, sideLength:int, backgroundColor=(0,0,0)) -> Image:
        paddedImage = preprocess.expandToSquare(image=image, backgroundColor=backgroundColor)
        scaledImage = preprocess.scaleImage(paddedImage,sideLength,sideLength)
        return scaledImage
