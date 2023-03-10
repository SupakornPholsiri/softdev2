# import random
# import colorsys

# def generate_random_colors(num_colors):
#     colors = []
#     for i in range(num_colors):
#         hue = i/num_colors
#         saturation = random.uniform(0.4, 1.0)
#         value = random.uniform(0.4, 1.0)
#         color = colorsys.hsv_to_rgb(hue, saturation, value)
#         r = float(color[0]*255)
#         g = float(color[1]*255)
#         b = float(color[2]*255)
#         colors.append((r, g, b))
#     hex_color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
#     return hex_color

import colorsys
import random

def generate_random_colors(num_colors):
    colors = []
    for i in range(num_colors):
        hue = i/num_colors
        saturation = random.uniform(0.4, 1.0)
        value = random.uniform(0.4, 1.0)
        color = colorsys.hsv_to_rgb(hue, saturation, value)
        r = int(color[0]*255)
        g = int(color[1]*255)
        b = int(color[2]*255)
        hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
        colors.append(hex_color)
    return colors.pop()

print(generate_random_colors(1))
