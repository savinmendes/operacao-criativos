import cv2, numpy as np, warnings
warnings.filterwarnings("ignore")
from PIL import Image
from simple_lama_inpainting import SimpleLama
Y0, Y1 = 820, 990
f = cv2.imread('cand/q60.png')
BM = np.load('../ad01/_tmp/boxmasks.npy', mmap_mode='r')
m = np.array(BM[60]).astype(np.uint8)
print(m.shape, m.sum())
mk = np.zeros(f.shape[:2], np.uint8)
mk[Y0:Y1] = cv2.dilate(m, np.ones((9, 9), np.uint8))
# reforco: amarelo forte na faixa
hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
yel = ((hsv[..., 0] > 18) & (hsv[..., 0] < 40) & (hsv[..., 1] > 120) & (hsv[..., 2] > 170)).astype(np.uint8)
yel[:Y0] = 0; yel[Y1:] = 0
mk = np.maximum(mk, cv2.dilate(yel, np.ones((11, 11), np.uint8)))
cv2.imwrite('cand/mask60.png', mk * 255)
r = SimpleLama()(Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)), Image.fromarray(mk * 255))
r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:f.shape[0], :f.shape[1]]
cv2.imwrite('cand/q60_lama.png', r)
print('ok')
