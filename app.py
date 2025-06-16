import streamlit as st
import time
from datetime import timedelta

# Configuração da página
st.set_page_config(
    page_title="Pomodoro Timer",
    page_icon="🍅",
    layout="centered"
)

# CSS customizado
st.markdown("""
<style>
.time-display {
    font-size: 5rem;
    font-weight: bold;
    text-align: center;
    margin: 1rem 0;
    color: #2c3e50;
    font-family: monospace;
}
.status-text {
    font-size: 1.2rem;
    text-align: center;
    margin: 1rem 0;
    font-weight: 600;
}
.stButton>button {
    width: 100%;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# Estados da sessão
if 'pomodoro_count' not in st.session_state:
    st.session_state.pomodoro_count = 0
if 'current_state' not in st.session_state:
    st.session_state.current_state = "ready"
if 'end_time' not in st.session_state:
    st.session_state.end_time = None
if 'paused' not in st.session_state:
    st.session_state.paused = False
if 'remaining' not in st.session_state:
    st.session_state.remaining = None

# Funções do timer
def start_timer(minutes):
    st.session_state.end_time = time.time() + minutes * 60
    st.session_state.paused = False
    st.session_state.remaining = None

def format_time(seconds):
    return str(timedelta(seconds=int(seconds))[2:7] if seconds > 0 else "00:00")

def get_remaining_time():
    if st.session_state.paused and st.session_state.remaining:
        return st.session_state.remaining
    elif st.session_state.end_time:
        return max(0, st.session_state.end_time - time.time())
    return 0

# Interface principal
st.title("🍅 Pomodoro Timer")

# Timer display
remaining = get_remaining_time()
st.markdown(f'<div class="time-display">{format_time(remaining)}</div>', unsafe_allow_html=True)

# Status
status = {
    "ready": "Pronto para começar",
    "working": "⏳ Trabalhando",
    "short_break": "☕ Pausa Curta",
    "long_break": "🌴 Pausa Longa"
}.get(st.session_state.current_state, "Pronto")
st.markdown(f'<div class="status-text">{status}</div>', unsafe_allow_html=True)

# Controles
col1, col2 = st.columns(2)
with col1:
    if st.session_state.current_state == "ready":
        if st.button("Começar (25 min)"):
            st.session_state.current_state = "working"
            start_timer(25)
    elif st.session_state.paused:
        if st.button("Continuar"):
            st.session_state.end_time = time.time() + st.session_state.remaining
            st.session_state.paused = False
    else:
        if st.button("Pausar"):
            st.session_state.remaining = st.session_state.end_time - time.time()
            st.session_state.paused = True

with col2:
    if st.button("Reiniciar"):
        st.session_state.current_state = "ready"
        st.session_state.end_time = None
        st.session_state.paused = False

# Atualização automática
if remaining > 0 or st.session_state.current_state != "ready":
    time.sleep(0.5)
    st.rerun()
elif st.session_state.end_time is not None and remaining <= 0:
    if st.session_state.current_state == "working":
        st.session_state.pomodoro_count += 1
        st.session_state.current_state = "long_break" if st.session_state.pomodoro_count % 4 == 0 else "short_break"
        start_timer(15 if st.session_state.current_state == "long_break" else 5)
    else:
        st.session_state.current_state = "working"
        start_timer(25)
    st.rerun()
