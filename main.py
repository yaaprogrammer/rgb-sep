import os
import cv2
import pathlib
import imghdr
import numpy as np


def main():
    img_type_list = {'jpg', 'jpeg'}
    images = []
    p = pathlib.Path("image")
    if not p.exists():
        p.mkdir()
        print(f"Please Put images into {p.resolve()}")
        return
    files = p.iterdir()
    for f in files:
        try:
            if imghdr.what(f) in img_type_list:
                images.append(os.fspath(f))
                print(f"Load {f}")
            else:
                print(f"{f} is not supported")
        except PermissionError:
            print(f"No Permission to open {f}")
        except Exception:
            print("Unknown Exception")
            raise
    for i in images:
        img = cv2.imdecode(np.fromfile(i, dtype=np.uint8), -1)
        img_b, img_g, img_r = cv2.split(img)
        b = blue(img, img_b)
        g = green(img, img_g)
        r = red(img, img_r)
        write_image(r, i, "_r.jpeg")
        write_image(g, i, "_g.jpeg")
        write_image(b, i, "_b.jpeg")


def write_image(img, filename: str, new_suffix: str):
    output = pathlib.Path("output")
    if not output.exists():
        output.mkdir()
    path = os.fspath(pathlib.Path("output", pathlib.Path(filename).stem + new_suffix))
    cv2.imencode('.jpeg', img)[1].tofile(path)


def red(img, img_r):
    zeros = np.zeros(img.shape[:2], dtype="uint8")
    merged_r = cv2.merge([zeros, zeros, img_r])
    return merged_r


def green(img, img_g):
    zeros = np.zeros(img.shape[:2], dtype="uint8")
    merged_g = cv2.merge([zeros, img_g, zeros])
    return merged_g


def blue(img, img_b):
    zeros = np.zeros(img.shape[:2], dtype="uint8")
    merged_b = cv2.merge([img_b, zeros, zeros])
    return merged_b


if __name__ == "__main__":
    main()
