"""应急出图：当这台机器装不上 matplotlib 时，用 Pillow 画一张同版式的 alice_bob.png。

和 vector_workshop.py 用的是同一份数据（Alice / Bob 对 4 类电影的评分），
画法也一样：折线 + 圆点/方点 + 图例 + 网格，只是渲染库从 matplotlib 换成 Pillow。

教室里装好 matplotlib 之后，请跑 vector_workshop.py 重新出图（那才是课程要求的做法）。
"""

import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

users = {
    "Alice": np.array([5, 1, 2, 4]),
    "Bob": np.array([4, 2, 1, 5]),
}
GENRES = ["科幻", "爱情", "喜剧", "动作"]

W, H = 820, 500
X0, Y0, X1, Y1 = 90, 60, 770, 420      # 绘图区
Y_MAX = 6

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\simsun.ttc",
]


def load_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def y_of(value):
    return Y1 - (value / Y_MAX) * (Y1 - Y0)


def x_of(index):
    return X0 + (index + 0.5) * (X1 - X0) / len(GENRES)


def main(path="alice_bob.png"):
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)
    f_title, f_axis, f_tick = load_font(20), load_font(15), load_font(14)

    # 网格 + y 轴刻度
    for v in range(0, Y_MAX + 1):
        y = y_of(v)
        draw.line([(X0, y), (X1, y)], fill=(225, 225, 225), width=1)
        draw.text((X0 - 26, y - 9), str(v), fill=(90, 90, 90), font=f_tick)

    # 坐标轴
    draw.rectangle([X0, Y0, X1, Y1], outline=(120, 120, 120), width=1)

    # x 轴刻度
    for i, name in enumerate(GENRES):
        x = x_of(i)
        draw.line([(x, Y1), (x, Y1 + 6)], fill=(120, 120, 120))
        w = draw.textlength(name, font=f_tick)
        draw.text((x - w / 2, Y1 + 12), name, fill=(60, 60, 60), font=f_tick)

    # 两条折线
    styles = {"Alice": ((31, 119, 180), "o"), "Bob": ((214, 39, 40), "s")}
    for name, vec in users.items():
        color, marker = styles[name]
        pts = [(x_of(i), y_of(v)) for i, v in enumerate(vec)]
        draw.line(pts, fill=color, width=3)
        for (x, y), v in zip(pts, vec):
            r = 6
            if marker == "o":
                draw.ellipse([x - r, y - r, x + r, y + r], fill="white", outline=color, width=3)
            else:
                draw.rectangle([x - r, y - r, x + r, y + r], fill="white", outline=color, width=3)
            draw.text((x + 9, y - 22), str(int(v)), fill=color, font=f_tick)

    # 标题与图例
    title = "Alice vs Bob：四类电影评分"
    tw = draw.textlength(title, font=f_title)
    draw.text(((W - tw) / 2, 18), title, fill=(30, 30, 30), font=f_title)

    lx, ly = X1 - 150, Y0 + 14
    for i, (name, (color, marker)) in enumerate(styles.items()):
        y = ly + i * 26
        draw.line([(lx, y), (lx + 34, y)], fill=color, width=3)
        draw.text((lx + 42, y - 9), name, fill=(40, 40, 40), font=f_axis)

    draw.text((16, H - 34), "数据：Alice [5,1,2,4]  Bob [4,2,1,5]  轴：0–6 分",
              fill=(140, 140, 140), font=load_font(12))

    img.save(path)
    print(f"[出图] 已保存 {path}（{W}×{H}）")


if __name__ == "__main__":
    main()
