# Importing the necessary modules
from tkinter import *
from tkinter import messagebox as mb
from PIL import Image


def generate_data(pixels, data):
    # converting the incoming data to 8-bit binary format
    data_in_binary = []

    for i in data:
        binary_data = format(ord(i), '08b')
        data_in_binary.append(binary_data)

    length_of_data = len(data_in_binary)
    image_data = iter(pixels)

    for a in range(length_of_data):
        pixels = [val for val in image_data.__next__()[:3] + image_data.__next__()[:3] + image_data.__next__()[:3]]

        for b in range(8):
            if (data_in_binary[a][b] == '1') and (pixels[b] % 2 != 0):
                pixels[b] -= 1
            elif (data_in_binary[a][b] == '0') and (pixels[b] % 2 == 0):
                if pixels[b] == 0:
                    pixels[b] += 1
                pixels[b] -= 1

        if (length_of_data-1) == a:
            if pixels[-1] % 2 == 0:
                if pixels[-1] == 0:
                    pixels[-1] += 1
                else:
                    pixels[-1] -= 1

        pixels = tuple(pixels)

        yield pixels[:3]
        yield pixels[3:6]
        yield pixels[6:9]


def encryption(img, data):
    # This method will encode data to the new image that will be created
    size = img.size[0]
    (x, y) = (0, 0)

    for pixel in generate_data(img.getdata(), data):
        img.putpixel((x, y), pixel)
        if size-1 == x:
            x = 0; y += 1
        else:
            x += 1


def main_encryption(img, text, new_image_name):
    # This function will take the arguments, create a new image, encode it and save it to the same directory
    image = Image.open(img, 'r')

    if (len(text) == 0) or (len(img) == 0) or (len(new_image_name) == 0):
        mb.showerror("Error", 'You have not put a value!')

    new_image = image.copy()
    encryption(new_image, text)

    new_image_name += '.png'

    new_image.save(new_image_name, 'png')


def main_decryption(img, strvar):
    # This function will decode the image given to it and extract the hidden message from it
    image = Image.open(img, 'r')

    data = ''
    image_data = iter(image.getdata())

    decoding = True

    while decoding:
        pixels = [value for value in image_data.__next__()[:3] + image_data.__next__()[:3] + image_data.__next__()[:3]]

        # string of binary data
        binary_string = ''

        for i in pixels[:8]:
            if i % 2 == 0:
                binary_string += '0'
            else:
                binary_string += '1'

        data += chr(int(binary_string, 2))
        if pixels[-1] % 2 != 0:
            strvar.set(data)


# Creating the button functions
def encode_image():
    encode_wn = Toplevel(root)
    encode_wn.title("Encode an Image")
    encode_wn.geometry('600x220')
    encode_wn.resizable(0, 0)
    encode_wn.config(bg='PowderBlue')
    Label(encode_wn, text='Encode an Image', font=("HelvLight", 15), bg='PaleGoldenrod').place(x=220, rely=0)

    Label(encode_wn, text='Enter the path of the image(with extension):', font=("Times New Roman", 13),
          bg='PaleTurquoise').place(x=10, y=50)
    Label(encode_wn, text='Enter the data to be encoded:', font=("Times New Roman", 13), bg='PaleTurquoise').place(
        x=10, y=90)
    Label(encode_wn, text='Enter the output file name (without extension):', font=("Times New Roman", 13),
          bg='PaleTurquoise').place(x=10, y=130)

    img_path = Entry(encode_wn, width=35)
    img_path.place(x=350, y=50)

    text_to_be_encoded = Entry(encode_wn, width=35)
    text_to_be_encoded.place(x=350, y=90)

    after_save_path = Entry(encode_wn, width=35)
    after_save_path.place(x=350, y=130)

    Button(encode_wn, text='Encode the Image', font=('Helvetica', 12), bg='PaleGoldenrod', command=lambda:
    main_encryption(img_path.get(), text_to_be_encoded.get(), after_save_path.get())).place(x=227, y=175)


def decode_image():
    decode_wn = Toplevel(root)
    decode_wn.title("Decode an Image")
    decode_wn.geometry('600x300')
    decode_wn.resizable(0, 0)
    decode_wn.config(bg='PowderBlue')

    Label(decode_wn, text='Decode an Image', font=("HelvLight", 15), bg='PaleGoldenrod').place(x=220, rely=0)

    Label(decode_wn, text='Enter the path to the image (with extension):', font=("Times New Roman", 12),
          bg='PaleTurquoise').place(x=10, y=50)

    img_entry = Entry(decode_wn, width=35)
    img_entry.place(x=350, y=50)

    text_strvar = StringVar()

    Button(decode_wn, text='Decode the Image', font=('Helvetica', 12), bg='PaleGoldenrod', command=lambda:
    main_decryption(img_entry.get(), text_strvar)).place(x=227, y=90)

    Label(decode_wn, text='Text that has been encoded in the image:', font=("Times New Roman", 12), bg='NavajoWhite').place(
        x=180, y=157)

    text_entry = Entry(decode_wn, width=94, text=text_strvar, state='disabled')
    text_entry.place(x=15, y=190, height=100)


# Initializing the window
root = Tk()
root.title('HS secure Image Steganography')
root.geometry('500x300')
root.resizable(0, 0)
root.config(bg='PowderBlue')

Label(root, text='HS secure Image Steganography', font=('Comic Sans MS', 15), bg='PaleGoldenrod',
      wraplength=300).place(x=165, y=30)

Button(root, text='Encode', width=25, font=('Times New Roman', 13), bg='SteelBlue', command=encode_image).place(
    x=130, y=130)

Button(root, text='Decode', width=25, font=('Times New Roman', 13), bg='SteelBlue', command=decode_image).place(
    x=130, y=200)

# Finalizing the window
root.update()
root.mainloop()