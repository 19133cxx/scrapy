# import matplotlib.pyplot as plt
# import cv2
# import numpy as np
# bg = cv2.imread('bg.jpg')
# front = cv2.imread('front.jpg')
# bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
# front= cv2.cvtColor(front, cv2.COLOR_BGR2GRAY)
#
# front=255-front
# front = front[front.any(1)]
# result=cv2.matchTemplate(bg,front,cv2.TM_CCOEFF_NORMED)
# index_max = np.argmax(result)
# x, y = np.unravel_index(index_max, result.shape)
#
# plt.plot(2,2,2)
# plt.imshow(front)
# plt.axis('off')
# plt.title('GRAY')
# plt.show()