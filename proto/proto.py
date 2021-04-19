# %%
import cv2
import ipywidgets as widgets
import matplotlib
import numpy as np
from IPython import get_ipython
from PIL import Image
from matplotlib import pyplot as plt

get_ipython().run_line_magic("matplotlib", "widget")

# 26 x 14
matplotlib.rcParams['figure.figsize'] = [20, 10]

# %%

img = cv2.imread("eg/src.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

fig, ax = plt.subplots(1, 2)
ax[0].axis("off")
ax[1].axis("off")
ax[0].imshow(img)
ax_img = ax[1].imshow(img)
fig.tight_layout()
fig.show()

color = widgets.ColorPicker(
    value="#e8e6de",
    disabled=False,
)


@widgets.interact(color=color, s=(0, 255, 1))
def draw_sat(color, s=131):
    if color[0] != "#":
        return

    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)

    low = np.array([r - s, g - s, b - s])
    high = np.array([r + s, g + s, b + s])

    img2 = img.copy()

    mask = cv2.inRange(img2, low, high)

    img2[mask == 255] = 255

    ax_img.set_data(img2)

# %%


r, g, b = 0xe8, 0xe6, 0xde
s = 131

low = np.array([r - s, g - s, b - s])
high = np.array([r + s, g + s, b + s])

mask = cv2.inRange(img, low, high)
img[mask == 255] = 255
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

fig, ax = plt.subplots()
ax.imshow(img, cmap="gray")
fig.show()

# %%
blurred_img = cv2.GaussianBlur(img, (21, 21), 0)

fig, ax = plt.subplots()
ax.imshow(blurred_img, cmap="gray")
fig.show()

# %%

hist, hist_x = np.histogram(img.flat, bins=256)
hist2, hist2_x = np.histogram(blurred_img.flat, bins=256)

fig, ax = plt.subplots()
ax.set_aspect(1.0)
ax.plot(hist2_x[:-1], hist2 / hist2.max() * 256)
ax.plot(hist_x[:-1], hist / hist.max() * 256)
fig.show()

# %%

digitized = np.digitize(blurred_img, np.arange(8) * 256 / 7)
table = {
    0: np.array([255, 0, 0]),
    1: np.array([255, 255, 0]),
    2: np.array([255, 0, 255]),
    3: np.array([255, 255, 255]),
    4: np.array([0, 0, 0]),
    5: np.array([0, 255, 0]),
    6: np.array([0, 0, 255]),
    7: np.array([0, 255, 255]),
}

sections = np.zeros((digitized.shape[0], digitized.shape[1], 3))
for x in range(digitized.shape[0]):
    for y in range(digitized.shape[1]):
        sections[x, y] = table[digitized[x, y]]


fig, ax = plt.subplots()
ax.imshow(sections)
fig.show()

# %%


def mask_fun(x):
    # return x ** 2 - x ** 3 + x
    return (3 * x ** 3) - (3 * x ** 2) + x
    # return -x * (x - 2)
    # return 1.0 / (2 - x**4)
    # return x


def threshold(gray):
    DISCRETE_LEVEL = 8

    gray = gray / 256
    gray = np.round(gray * DISCRETE_LEVEL) / DISCRETE_LEVEL
    gray = mask_fun(gray)

    return gray * 255


mask = np.vectorize(threshold)(blurred_img)
final = img < mask
# final = img.copy()
# final
# final[img > mask] = 255

fig, ax = plt.subplots(2, 2)
fig.tight_layout()
ax[0, 0].imshow(img, cmap="gray")
ax[0, 1].imshow(final, cmap="gray")
ax[1, 0].imshow(mask)
ax[1, 1].imshow((img > mask), cmap="gray")

fig.show()

fig, ax = plt.subplots()
x = np.arange(256)
ax.set_xlim(0, 256)
ax.set_ylim(0, 256)
ax.set_aspect(1.0)
ax.plot(hist_x[:-1], hist / hist.max() * 256)
ax.plot(hist2_x[:-1], hist2 / hist2.max() * 256)
ax.plot(x, x)
ax.plot(x, mask_fun(x / 256) * 256)
ax.plot(x, threshold(x))
fig.show()


# %%

fig, ax = plt.subplots()
fig.tight_layout()
ax.imshow(final, cmap="gray")
fig.show()

# %%

Image.fromarray(final).save("dist.png")
