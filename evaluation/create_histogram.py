import numpy as np
import matplotlib.pyplot as plt

ious_per_image = np.loadtxt('ious_per_image.txt')
n, bins, patches = plt.hist(
    ious_per_image, 51, density=False, facecolor='g', alpha=0.75)
plt.grid(True)
plt.xlabel('IOU')
plt.ylabel('Occurences')
plt.title('IOU distribution on regional images, mean=0.49315')
plt.savefig('ious_regional')
plt.show()
