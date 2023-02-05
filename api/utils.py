import base64

def converter(img_b64):
    return base64.decodebytes(img_b64)

def saveImg(img, counter):
    with open(f"faces/{counter}.jpg", "wb") as fh:
        fh.write(img)