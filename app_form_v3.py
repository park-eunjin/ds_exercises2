import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

con = sqlite3.connect('db.db')
cur = con.cursor()


def check_uid(uid):
    cur.execute(f"SELECT COUNT(*) FROM users WHERE uid='{uid}'")
    res = cur.fetchone()
    return res[0]


def check_uemail(uemail):
    cur.execute(f"SELECT COUNT(*) FROM users WHERE uemail='{uemail}'")
    res = cur.fetchone()
    return res[0]


menu = st.sidebar.selectbox('메뉴', options=['가입','목록','검색'])

if menu == '가입':

    st.subheader('회원가입 양식')

    with st.form('my_form', clear_on_submit=True):
        st.info('다음 양식을 모두 입력 후 제출합니다.')
        uid = st.text_input('아이디', max_chars=12).strip()
        uname = st.text_input('성명', max_chars=10).strip()
        uemail = st.text_input('이메일').strip()
        upw = st.text_input('비밀번호', type='password').strip()
        upw_chk = st.text_input('비밀번호 확인', type='password').strip()
        ubd = st.date_input('생년월일')
        ugender = st.radio('성별', options=['남','여'], horizontal=True)

        submitted = st.form_submit_button('제출')
        if submitted:

            if upw != upw_chk:
                st.warning('비밀번호를 확인하세요!')
                st.stop()

            if check_uid(uid):
                st.warning('동일한 아이디가 존재합니다.')
                st.stop()

            if check_uemail(uemail):
                st.warning('동일한 이메일이 존재합니다.')
                st.stop()

            st.success(f'{uid} {uname} {uemail} {upw} {ubd} {ugender}')
            cur.execute(f"INSERT INTO users VALUES ("
                        f"'{uid}','{uname}','{uemail}','{upw}',"
                        f"'{ubd}','{ugender}',CURRENT_DATE)")
            con.commit()

elif menu == '목록':
    st.subheader('회원 목록')
    with st.container():
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        cols = [column[0] for column in cur.description]
        df = pd.DataFrame.from_records(data=rows, columns=cols)
        st.dataframe(df)

elif menu == '검색':
    st.subheader('회원 검색')
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            s_uid = st.text_input('아이디')
        with col2:
            s_btn = st.button('검색')
            d_btn = st.button('삭제')

        if s_btn:

            if check_uid(s_uid) == 0:
                st.warning('해당 아이디는 존재하지 않습니다.')
                st.stop()

            st.session_state['uid'] = s_uid

    if 'uid' in st.session_state:

        cur.execute(f"SELECT * FROM users WHERE uid='{st.session_state['uid']}'")
        rows = cur.fetchall()
        res = rows[0]

        index = 0
        if res[5] == '여':
            index = 1

        with st.form(key='my_form_mod', clear_on_submit=True):

            uname2 = st.text_input('성명', max_chars=10, value=res[1]).strip()
            uemail2 = st.text_input('이메일', value=res[2]).strip()
            upw2 = st.text_input('비밀번호', type='password', value=res[3]).strip()
            upw_chk2 = st.text_input('비밀번호 확인', type='password').strip()
            ubd2 = st.date_input('생년월일', value=datetime.strptime(res[4], "%Y-%m-%d") )
            ugender2 = st.radio('성별', options=['남', '여'], horizontal=True, index=index)

            submitted2 = st.form_submit_button('수정')

            if submitted2:

                if upw2 != upw_chk2:
                    st.warning('비밀번호를 확인하세요!')
                    st.stop()

                if check_uemail(uemail2):
                    st.warning('동일한 이메일이 존재합니다.')
                    st.stop()

                cur.execute(f"UPDATE users SET "
                            f"uname='{uname2}',"
                            f"uemail='{uemail2}',"
                            f"upw='{upw2}',"
                            f"ubd='{ubd2}',"
                            f"ugender='{ugender2}' "
                            f"WHERE uid='{s_uid}'")
                con.commit()

                del st.session_state['uid']