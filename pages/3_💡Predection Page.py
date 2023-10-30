import streamlit as st
import chatgptapi
import predictt



with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
st.sidebar.markdown('''
---
Made by [Bensaid Mohamed](mohamed2018bensaid@gmail.com/).
''')
st.title("Predection Page")
st.markdown("###### Type the Review here")
review = st.text_area("",label_visibility='hidden')
st.markdown("###### Select the prediction model ")
option = st.selectbox(
    '',
    ('Naive Bayes', 'GRU+BERT','LSTM+BERT','GPT'))
predict_button = st.button("Predict")

if st.session_state.get('button') != True:
    st.session_state['button'] = predict_button 


if st.session_state['button'] == True:
    if (option=='Naive Bayes'):
        result = predictt.predictnb(review)
    elif(option=='GRU+BERT'):
        result = predictt.predictgru(review)
    elif(option=='LSTM+BERT'):
        result = predictt.predictlstm(review)
    elif(option=='GPT'):
        result = chatgptapi.gptpredict(review)
    else:
        print('error')
    print(result)
    if result > 0.55:
        st.success('This is a positive review', icon="✔")
        reply = chatgptapi.replygen2(review)
        st.text_area('Here is a reply to the reviewer',reply)
    else:
        st.error('This is a negative review', icon="❌")
        reply = chatgptapi.replygen(review)
        st.text_area('Here is a reply to the reviewer',reply)


    correct_guess = st.selectbox("Did the model correctly guess the result?", (" ", "Yes", "No"))
    if correct_guess:
        if correct_guess == "Yes":
            st.write("Great! The model correctly guessed the result.")
            predictt.addrecord(predictt.remove_punctuation_numbers(review), result,1)
        else:
            st.write("Hmm, the model did not correctly guess the result.")
            predictt.addrecord(predictt.remove_punctuation_numbers(review), result,0)
        del st.session_state['button']
        if st.button("Done"):
            print('')
          
