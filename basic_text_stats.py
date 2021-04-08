import pickle
import numpy as np

img_text = pickle.load(open("pickle/texts.pkl", "rb"))
# print(img_text.keys())

text_lens_no_0 = [len(x) for x in img_text.values() if len(x) > 0]
print('count', len(img_text))
print('no text in', len([len(x) for x in img_text.values() if len(x) == 0]), 'images')
print('min', np.min([len(x) for x in img_text.values()]))
print('max', np.max([len(x) for x in img_text.values()]))

print('q1', np.quantile(text_lens_no_0, 0.25))
print('median', np.median(text_lens_no_0))
print('q3', np.quantile(text_lens_no_0, 0.75))

words_separate = [' '.join(x).split(' ') for x in img_text.values()]

text_lens_no_0 = [len(x) for x in img_text.values() if len(x) > 0]
print('min', np.min([len(x) for x in words_separate]))
print('max', np.max([len(x) for x in words_separate]))
print('q1', np.quantile([len(x) for x in words_separate], 0.25))
print('median', np.median([len(x) for x in words_separate]))
print('q3', np.quantile([len(x) for x in words_separate], 0.75))