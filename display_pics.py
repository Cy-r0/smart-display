#!/usr/bin/env python3

"""BLA"""

__author__ = 'Ciro Cursio'

import functools
import os

from PIL import Image, ImageTk
import tkinter
from natsort import os_sorted


def EXIF_transpose(img):
    """Apply Image.transpose to ensure 0th row of pixels is at the visual
    top of the image, and 0th column is the visual left-hand side.
    Return the original image if unable to determine the orientation.
    As per CIPA DC-008-2012, the orientation field contains an integer,
    1 through 8. Other values are reserved.
    """

    exif_orientation_tag = 0x0112
    exif_transpose_sequences = [                   # Val  0th row  0th col
        [],                                        # 0   (reserved)
        [],                                        # 1   top      left
        [Image.FLIP_LEFT_RIGHT],                   # 2   top      right
        [Image.ROTATE_180],                        # 3   bottom   right
        [Image.FLIP_TOP_BOTTOM],                   # 4   bottom   left
        [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],  # 5   left     top
        [Image.ROTATE_270],                        # 6   right    top
        [Image.FLIP_TOP_BOTTOM, Image.ROTATE_90],  # 7   right    bottom
        [Image.ROTATE_90],                         # 8   left     bottom
    ]

    try:
        seq = exif_transpose_sequences[img._getexif()[exif_orientation_tag]]
    except Exception:
        return img
    else:
        return functools.reduce(type(img).transpose, seq, img)


class SlideShow(tkinter.Tk):
    """Show a bunch of images one after the other."""

    def __init__(self, img_dir):
        super().__init__()

        self.img_dir = img_dir
        self.imgs = [os.path.join(self.img_dir, f) for f in os_sorted(os.listdir(self.img_dir))]
        self.index = 0
        self.photo = None
        # Delay between pictures in ms
        self.delay = 1000*2

        self.bind_all('q', self.do_exit)
        self.attributes('-fullscreen', True)

        # Set root layout
        self.w, self.h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f'{self.w}x{self.h}+0+0')
        self.config(bg='black')
        self.focus_set()

        # Display images as a label
        self.label = tkinter.Label(self, bg='black')
        # self.label.pack(padx=0, pady=0)
        self.label.place(x=self.w//2, y=self.h//2, anchor='center')

        self.show_image_pair()

    def show_image_pair(self):
        """Display a pair of images side by side."""

        img1 = EXIF_transpose(Image.open(self.imgs[self.index]))
        img2 = EXIF_transpose(Image.open(self.imgs[self.index + 1]))

        # Increment index
        self.index += 2
        if self.index == len(self.imgs):
            self.index = 0

        # Resize images so that they have the same width
        w1, h1 = img1.size
        w2, h2 = img2.size
        if w1 > w2:
            ratio = w1 / w2
            img2 = img2.resize((w1, int(h2 * ratio)), Image.ANTIALIAS)
        else:
            ratio = w2 / w1
            img1 = img1.resize((w2, int(h1 * ratio)), Image.ANTIALIAS)

        # Stitch images side by side
        w1, h1 = img1.size
        w2, h2 = img2.size
        w = w1 + w2
        h = max(h1, h2)
        img_pair = Image.new('RGB', (w, h))
        img_pair.paste(im=img1, box=(0, (h - h1) // 2))
        img_pair.paste(im=img2, box=(w//2, (h - h2) // 2))

        # Adjust size of image pair so it fits inside the screen
        if w > self.w or h > self.h or w < self.w or h < self.h:
            ratio = min(self.w / w, self.h / h)
            w = int(w * ratio)
            h = int(h * ratio)
            img_pair = img_pair.resize((w, h), Image.ANTIALIAS)

        # Set the image
        self.photo = ImageTk.PhotoImage(img_pair)
        self.label['image'] = self.photo

        self.after(self.delay, self.show_image_pair)

    def do_exit(self, event):
        """
        Callback to handle quitting.

        This is necessary since the quit method does not take arguments.
        """
        self.quit()


# def slideshow(img):
#     """Show a bunch of images with TKinter."""

#     root = tkinter.Tk()
#     root.attributes('-fullscreen', True)
#     w, h = root.winfo_screenwidth(), root.winfo_screenheight()
#     root.geometry(f'{w}x{h}+0+0')
#     root.focus_set()
#     root.bind('<Escape>', lambda e: (e.widget.withdraw(), e.widget.quit()))

#     canvas = tkinter.Canvas(root, width=w, height=h)
#     canvas.config(highlightthickness=0)
#     # canvas.pack()
#     canvas.configure(background='black')
#     img_w, img_h = img.size

#     # Fit image inside screen
#     if img_w > w or img_h > h:
#         ratio = min(w/img_h, h/img_h)
#         img_w = int(img_w * ratio)
#         img_h = int(img_h * ratio)
#         img = img.resize((img_w, img_h), Image.ANTIALIAS)
#     img_tk = ImageTk.PhotoImage(img)
#     imagesprite = canvas.create_image(w/2, h/2, image=img_tk)
#     root.after(10, lambda: show_img())
#     print(w, h)


if __name__ == '__main__':
    ss = SlideShow('/home/luigi/Pictures/labbra-ritagliate')
    ss.mainloop()
