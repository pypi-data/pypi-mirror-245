import glob  # 내가 지정한 파이썬 파일들을 한번에 가져와서 리스트 형태로 반환하는 패키지

from PIL import Image  # 이미지 처리를 위한 패키지


class GifConverter:
    def __init__(self, path_in=None, path_out=None, resize=(320, 240)):
        """
        :param path_in: 원본 여러 이미지 경로(Ex: images/*.png)
        :param path_out: 결과 이미지 경로(Ex: output/filename.gif)
        :param resize: 리사이징 크기(320, 240)
        """
        self.path_in = path_in or "./*.png"  # 사용자가 혹시 path_in을 입력하지 않았을 경우(png 파일이 현재 디렉터리에 있다면)
        self.path_out = path_out or "./output.gif"
        self.resize = resize

    def convert_png_to_gif(self):
        img, *images = (Image.open(f).resize(self.resize, Image.LANCZOS) for f in sorted(glob.glob(self.path_in)))

        try:
            img.save(
                fp=self.path_out,
                format="GIF",
                append_images=images,
                save_all=True,
                duration=500,
                loop=0,
            )
        except OSError:
            print("Cannot convert!", img)  # noqa: T201


if __name__ == "__main__":
    c = GifConverter("./project/images/*.png", "./project/image_out/result.gif", (320, 240))
    c.convert_png_to_gif()
