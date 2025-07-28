# 페이지 제목 : 스마트 퀴즈
# icon 넣기
# layout centered
import streamlit as st
import datetime

st.set_page_config(
    page_title='스마트 퀴즈',
    page_icon='🚀',
    layout = 'centered'
)


# 퀴즈 문제 데이터
quiz_questions = [
    {
        "type": "radio",
        "question": "다음 중 Streamlit에서 제목을 표시하는 함수는?",
        "options": ["st.title", "st.header", "st.subheader", "st.write"],
        "correct": 0,
        "explanation": "st.title()은 가장 큰 제목을 표시하는 함수입니다."
    },
    {
        "type": "text",
        "question": "Streamlit에서 텍스트를 입력받는 위젯은? (st.text_input에서 st. 제외하고 입력)",
        "correct": ["text_input"],
        "explanation": "st.text_input은 사용자로부터 텍스트를 입력받는 위젯입니다."
    },
    {
        "type": "slider",
        "question": "Streamlit 앱을 실행할 때 기본 포트 번호는?",
        "min_val": 8000,
        "max_val": 9000,
        "correct": 8501,
        "tolerance": 10,
        "explanation": "Streamlit 앱의 기본 포트는 8501번입니다."
    },
    {
        "type": "number",
        "question": "st.columns(3)을 사용하면 몇 개의 열이 생성되나요?",
        "correct": 3,
        "explanation": "st.columns(3)은 3개의 열을 생성합니다."
    },
    {
        "type": "selectbox",
        "question": "다음 중 Streamlit의 버튼 요소가 아닌 것은?",
        "options": ["st.button", "st.download_button", "st.slider", "st.form_submit_button"],
        "correct": 2,
        "explanation": "st.slider는 슬라이더 위젯이며 버튼 요소가 아닙니다."
    }
]

st.title('🚀 스마트 퀴즈')
st.write("Streamlit의 퀴즈를 풀어보세요!")

if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "answer_submitted" not in st.session_state:
    st.session_state.answer_submitted = False
if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False
if "current_qestion" not in st.session_state:
    st.session_state.current_qestion = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "score" not in st.session_state:
    st.session_state.score = 0

def check_answer(question,user_answer):
    if question['type'] in ['radio','selectbox']:
        return user_answer==question['correct'] 
    elif question['type']=='text':
        ans = ""
        for i in question['correct']:
            ans = i.lower()
        return user_answer in ans
    elif question['type']=='slider':
        return user_answer==question['correct']
    elif question['type']=='number':
        return user_answer==question['correct']
    return False

if not st.session_state.quiz_started:
    st.header("퀴즈 소개")
    st.markdown("""
    - **총 문제 수**: 5문제
    - **문제 유형**: 객관식, 주관식, 슬라이더, 숫자 입력
    - **제한 시간**: 없음
    - **채점 방식**: 즉시 피드백
    """)

    st.info("준비되셨나요? 아래 버튼을 클릭해서 퀴즈를 시작하세요.")

    col1,col2,col3 = st.columns(3)
    
    with col2:
        if st.button('퀴즈 시작하기', type="primary"):
            st.session_state.quiz_started=True
            st.session_state.answer_submitted=False
            st.session_state.show_result=False
            st.rerun()

    st.divider()

    st.subheader("문제 미리보기")
    for i,q in enumerate(quiz_questions):
        st.write(f"**문제 {i+1}** : {q['question']} ({q['type']}유형)")
elif st.session_state.quiz_started and not st.session_state.quiz_finished:
    current_q=st.session_state.current_qestion
    question=quiz_questions[current_q]

    st.progress((current_q+1)/len(quiz_questions))

    st.subheader(f'문제 {current_q+1}')
    st.write(question['question'])

    if not st.session_state.answer_submitted:
        user_answer=None
        
        if question['type']=='radio':
            user_answer=st.radio(
                "정답을 선택하세요:",
                options= range(len(question["options"])),
                format_func=lambda x: question['options'][x],
                key=f"radio_{current_q}"
            )
        elif question['type']=='text':
            user_answer=st.text_input(
                '답을 입력하세요:',
                placeholder="정답을 입력하세요...").strip().lower()
        elif question['type']=='slider':
            user_answer=st.slider(
                "슬라이더를 조정하세요:",
                min_value=question['min_val'],
                max_value=question['max_val'],
                value=((question['min_val']+question['max_val'])//2)
            )
        elif question['type']=='number':
            user_answer=st.number_input(
                '숫자를 입력하세요:',step=1)
        elif question['type']=='selectbox':
            user_answer=st.selectbox(
                "정답을 선택하세요:",
                options= range(len(question["options"])),
                format_func=lambda x: question['options'][x],
                key=f"selectbox_{current_q}"
            )
    
        # st.divider()

        col1,col2,col3 = st.columns(3)

        with col2:
            if st.button("답안 제출", type="primary"):
                # 문제 타입이 text인경우 입력값을 작성하지 않은 경우
                # st.warning 이용해서 답을 입력해주세요!
                if question['type']=='text' and not user_answer:
                    st.warning('답을 입력해주세요!')
                else:
                    is_collect = check_answer(question,user_answer)

                    st.session_state.answers.append({
                        'question':question['question'],
                        'user_answer':user_answer,
                        'correct_answer':question['correct'],
                        'is_collect':is_collect,
                        'explanation':question['explanation']
                    })

                    if is_collect:
                        st.session_state.score+=1

                    st.session_state.answer_submitted=True
                    st.session_state.show_result=True
                    st.rerun()

    elif st.session_state.show_result:
        last_answer=st.session_state.answers[-1]

        if last_answer['is_collect']:
            st.success('정답입니다')
        else:
            st.error('틀렸습니다') # st.info(), st.warning

        st.info(f"해설:{last_answer['explanation']}")

        # st.divider()

        col1,col2,col3 = st.columns(3)

        with col2:
            if current_q < len(quiz_questions)-1:
                if st.button("다음문제"):
                    st.session_state.current_qestion+=1
                    st.session_state.answer_submitted=False
                    st.session_state.show_result=False
                    st.rerun()
            else:
                if st.button('결과보기',type="primary"):
                    st.session_state.quiz_finished=True
                    st.rerun()
else:
    # st.write('결과창')
    
    st.header('퀴즈 완료')

    total_questions=len(quiz_questions)
    score_percentage=(st.session_state.score/total_questions)*100

    def display_stat(title, value):
        st.markdown(f"""
            <div style="
                padding: 1rem; 
                background-color: var(--stat-bg, #f0f2f6); 
                border: 1px solid var(--stat-border, transparent);
                border-radius: 10px; 
                text-align: center;
                box-shadow: var(--stat-shadow, 0 1px 3px rgba(0,0,0,0.1));
            ">
                <div style="
                    font-size: 18px; 
                    font-weight: bold; 
                    color: var(--title-color, #262730);
                    margin-bottom: 0.5rem;
                ">{title}</div>
                <div style="
                    font-size: 32px; 
                    font-weight: bold; 
                    color: var(--text-color, #262730);
                ">{value}</div>
            </div>
            <br>
            <style>
                /* 라이트모드 기본값 */
                :root {{
                    --stat-bg: #f0f2f6;
                    --stat-border: transparent;
                    --stat-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    --title-color: #262730;
                    --text-color: #262730;
                }}
                
                /* 다크모드 스타일 */
                @media (prefers-color-scheme: dark) {{
                    :root {{
                        --stat-bg: #2b2b35;
                        --stat-border: #404040;
                        --stat-shadow: 0 1px 3px rgba(0,0,0,0.3);
                        --title-color: #fafafa;
                        --text-color: #fafafa;
                    }}
                }}
                
                /* Streamlit 다크모드 */
                [data-theme="dark"] {{
                    --stat-bg: #2b2b35;
                    --stat-border: #404040;
                    --stat-shadow: 0 1px 3px rgba(0,0,0,0.3);
                    --title-color: #fafafa;
                    --text-color: #fafafa;
                }}
            </style>
        """, unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)

    with col1:
        display_stat('총 문제 수',total_questions)
    with col2:
        display_stat('맞힌 문제 수',st.session_state.score)
    with col3:
        display_stat('정답률', f'{score_percentage:.1f}')

    # 100점 일때 
    if score_percentage==100:
        st.success('완벽합니다! 모든 문제를 맞히셨네요!')
    # 80점 이상일 때
    elif score_percentage>=80:
        st.success('훌륭해요! 대부분의 문제를 맞히셨습니다!')
    # 60점 이상일 때
    elif score_percentage>=60:
        st.info('괜찮아요! 조금 더 공부하면 완벽할거에요.')
    # 그 외
    else:
        st.error('다시 도전해보세요! 더 좋은 결과가 있을 거에요.')

    st.divider()

    st.subheader('상세 결과')

    for i, answer in enumerate(st.session_state.answers):
        with st.expander(f"**문제 {i+1}**:{'✅' if answer['is_collect'] else '✖️'}"):
            st.write(f'문제 : {answer["question"]}')

            # radio, selectbox
            if isinstance(answer['user_answer'], int) and 'options' in quiz_questions[i]:
                st.write(f"내 답 : {quiz_questions[i]['options'][answer['user_answer']]}")
                st.write(f"정답 : {quiz_questions[i]['options'][answer['correct_answer']]}")
            else:
                st.write(f"내 답 : {answer['user_answer']}")
                # text_input
                if isinstance(answer['correct_answer'],list):
                    st.write(f"정답 : {', '.join(answer['correct_answer'])}")
                # number_input, slider
                else:
                    st.write(f"정답 : {answer['correct_answer']}")

            st.write('해설 : ',answer['explanation'])

    # st.divider()

    col1,col2,col3 = st.columns(3)
    with col2:
        if st.button('다시 도전하기', type='primary'):
            st.session_state.quiz_started = False
            st.session_state.answer_submitted = False
            st.session_state.show_result = False
            st.session_state.quiz_finished = False
            st.session_state.current_qestion = 0
            st.session_state.answers = []
            st.session_state.score = 0
            st.rerun()

        # collect_str=''
        # if answer['is_collect']:
        #     collect_str='✅' 
        # else:
        #     collect_str='✖️'   
        # with st.expander(f'문제:{i+1}:{collect_str}')

st.divider()

st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 0.8em; margin-top: 2rem;'>
    🧠 스마트 퀴즈 v1.1 | 다양한 문제 유형으로 지식을 테스트해보세요!
    </div>
    """,
    unsafe_allow_html=True
)
    # st.slider('나이를 선택하세요.',
    #  min_value=0,max_value=130,value=20)
    # st.slider('월급의 몇퍼센트를 저축하시나요?',
    #  min_value=0.0,max_value=100.0,value=(20.0,30.0)
    #  ,step=0.5)
    # #  import datetime
    # s=st.slider('점심 식사 시간이 몇시부터 몇시까지 인가요?',
    #  value=(datetime.time(11,0),datetime.time(13,0))
    #  ,step=datetime.timedelta(minutes=15))
    # st.write(s)
    # 라디오 = st.radio('내가 사는 지역은?',
    # options=['제주','서울','부산'],
    # captions=['jeju','seoul','busan'],
    # index=None)
    # st.write(라디오)
    # if 라디오=='제주':
    #     st.write('정답')
    # else:
    #     st.write('정답 아님')
    # l=['축구','배드민턴','야구','농구','수영']
    # 선택박스 = st.selectbox('좋아하는 운동을 선택하세요.',l,
    # index=None, placeholder="운동 종목을 선택하세요...")
    # if 선택박스 in l:
    #     st.write(선택박스)