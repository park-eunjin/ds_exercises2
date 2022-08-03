import os.path

import cv2
import streamlit as st
from keras.models import load_model
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas

# 경로 설정
file_path = os.path.dirname(__file__)

# 모델파일 폴더 생성
save_dir = os.path.join(file_path, 'model')

# 학습된 모델 불러오기
model_file = 'minist_model.h5'
model = load_model(os.path.join(save_dir, model_file))

# 헤더 출력
st.subheader('손글씨 숫자 인식')

SIZE = 192

canvas_result = st_canvas(
    fill_color='#000000',
    stroke_width=20,
    stroke_color='#FFFFFF',
    background_color='#000000',
    width=SIZE,
    height=SIZE,
    drawing_mode='freedraw',
    update_streamlit=False,
    key='canvas')

if canvas_result.image_data is not None:
    img = cv2.resize(canvas_result.image_data.astype('uint8'), (28, 28))
    rescaled = cv2.resize(img, (SIZE, SIZE), interpolation=cv2.INTER_NEAREST)
    st.write('모델 입력 형태')
    st.image(rescaled)

if st.button('Predict'):
    test_x = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = model.predict(np.reshape(test_x, (1, 28 * 28)))
    st.success(np.argmax(res[0]))
    st.bar_chart(res[0])