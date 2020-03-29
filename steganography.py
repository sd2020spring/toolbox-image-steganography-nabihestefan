"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap
import numpy as np

def decode_image(file_location="images/encoded_sample.png", final_location="images/decoded_image.png"):
    """Decodes the hidden message in an image.

    Parameters
    ----------
    file_location: str
        The location of the image file to decode. This defaults to the provided
        encoded image in the images folder.
    """
    encoded_image = Image.open(file_location)

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)

    for x in range(x_size):
        for y in range(y_size):
            pixel = encoded_image.getpixel((x,y))[0]
            binary = bin(pixel)
            if binary[-1:] == "0":
                decoded_image.putpixel((x,y), (0,0,0))
            elif binary[-1:] == "1":
                decoded_image.putpixel((x,y), (255,255,255))



    decoded_image.save(final_location)


def write_text(text_to_write, image_size):
    """Write text to an RGB image. Automatically line wraps.

    Parameters
    ----------
    text_to_write: str
        The text to write to the image.
    image_size: (int, int)
        The size of the resulting text image.
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    # Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin, offset), line, font=font)
        offset += 10
    image_text.save("images/image_text.png")
    return image_text


def encode_image(text_to_encode, template_image="images/samoyed.jpg"):
    """Encode a text message into an image.

    Parameters
    ----------
    text_to_encode: str
        The text to encode into the template image.
    template_image: str
        The image to use for encoding. An image is provided by default.
    """
    template_image = Image.open(template_image)
    x_size = template_image.size[0]
    y_size = template_image.size[1]

    write_text(text_to_encode, (x_size, y_size))
    text_image = Image.open("images/image_text.png")

    encoded_image = Image.new("RGB", template_image.size)

    for x in range(x_size):
        for y in range(y_size):
            temp_pixel = template_image.getpixel((x,y))
            text_pixel = text_image.getpixel((x,y))

            red = temp_pixel[0]
            green = temp_pixel[1]
            blue  = temp_pixel[2]
            og_binary = bin(red)

            if text_pixel == (255,255,255):
                new_binary = og_binary[:-1]
                new_binary += "1"
            elif text_pixel == (0,0,0):
                new_binary = og_binary[:-1]
                new_binary += "0"
            new_red = int(new_binary, 2)
            new_pixel = (new_red, green, blue)
            encoded_image.putpixel((x, y), new_pixel)


    encoded_image.save("images/myencoding.png")


if __name__ == '__main__':
    print("Decoding the image...")
    decode_image()

    print("Encoding the image...")
    encode_image("The story so far: In the beginning the Universe was created. This has made a lot of people very angry and been widely regarded as a bad move." +
                 "                                                                                             " +
                 "                                                                                             " +
                 "'The Answer to the Ultimate Question of Life, The Universe, and Everything is...Forty-two,' said Deep Thought, with infinite majesty and calm."+
                 "                                                                                             " +
                 "                                                                                             " +
                 " It is a well known fact that those people who most want to rule people are, ipso facto, those least suited to do it. To summarize the summary: anyone who is capable of getting themselves made President should on no account be allowed to do the job."+
                 "                                                                                             " +
                 "                                                                                             " +
                 "There is an art, it says, or rather, a knack to flying. The knack lies in learning how to throw yourself at the ground and miss." +
                 "                                                                                             " +
                 "                                                                                             " +
                 "Nothing travels faster than the speed of light with the possible exception of bad news, which obeys its own special laws." +
                 "                                                                                             " +
                 "                                                                                             " +
                 "In the beginning the Universe was created. This has made a lot of people very angry and been widely regarded as a bad move." +
                 "                                                                                             " +
                 "                                                                                             " +
                 "Don't Panic" +
                 "                                                                                             " +
                 "                                                                                             " +
                 "                                                                                             " +
                 "- The Ultimate Hitchhiker's Guide to the Galaxy by Douglas Adams")

    print("Decoding your own image!")
    decode_image("images/myencoding.png", "images/mydecoding.png")
