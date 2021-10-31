from PIL import Image
import pytesseract



def get_check_code(img_name):
    im=Image.open(img_name)

    imgry = im.convert('L')
    imgry.save('gray-' + img_name)
    threshold = 140
    table = []
    for j in range(256):
        if j < threshold:
                table.append(0)
        else:
                table.append(1)
    out = imgry.point(table, '1')
    out.save('b' + img_name)

    check_code=pytesseract.image_to_string(out,config='--psm 7, outputbase digits')

    
    return check_code





if __name__ == "__main__":
    get_check_code("58.png")