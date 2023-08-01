from image2char import tool
from PIL import Image
import logging

img_path = 'test3.jpg'

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    img2 = Image.open(img_path)

    char_list = '''#RMNHQODBWGPZ*@$C&98?32I1>!:-;. '''
    # char_list = '''█　'''
    scanner = tool.get_scanner(density=0.33, scale=1)
    # reversed=True: in windows console, the char is white
    scanner.scan(img2, reversed=True, char_list=char_list)
    scanner.print_result()
