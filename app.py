import streamlit as st
import time
from datetime import timedelta

# Configuração da página
st.set_page_config(
    page_title="FocusFlow Pomodoro Timer",
    page_icon="🍅",
    layout="centered",
    initial_sidebar_state="collapsed"
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
    font-family: 'Courier New', monospace;
}
.status-text {
    font-size: 1.5rem;
    text-align: center;
    margin: 1rem 0;
    font-weight: 600;
}
.pomodoro-count {
    text-align: center;
    margin: 1rem 0;
    font-size: 1rem;
    color: #7f8c8d;
}
.stButton>button {
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    transition: all 0.3s ease;
}
</style>
""", unsafe_allow_html=True)

# Estados da sessão
if 'pomodoro_count' not in st.session_state:
    st.session_state.pomodoro_count = 0
if 'current_state' not in st.session_state:
    st.session_state.current_state = "ready"  # ready, working, short_break, long_break
if 'end_time' not in st.session_state:
    st.session_state.end_time = None
if 'paused' not in st.session_state:
    st.session_state.paused = False
if 'remaining' not in st.session_state:
    st.session_state.remaining = None
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

# Configurações padrão
DEFAULT_WORK = 25
DEFAULT_SHORT_BREAK = 5
DEFAULT_LONG_BREAK = 15

# Configurações do usuário
with st.sidebar:
    st.title("⚙️ Configurações")
    work_time = st.number_input("Tempo de trabalho (minutos)", min_value=1, max_value=60, value=DEFAULT_WORK)
    short_break = st.number_input("Pausa curta (minutos)", min_value=1, max_value=30, value=DEFAULT_SHORT_BREAK)
    long_break = st.number_input("Pausa longa (minutos)", min_value=1, max_value=60, value=DEFAULT_LONG_BREAK)
    pomodoros_before_long = st.number_input("Pomodoros antes da pausa longa", min_value=1, max_value=10, value=4)
    st.markdown("---")
    st.markdown("### Sobre a Técnica Pomodoro")
    st.markdown("""
    - 🍅 25 minutos de trabalho focado
    - ☕ 5 minutos de pausa curta
    - 🌴 15 minutos de pausa longa após 4 pomodoros
    - 🔁 Repita o ciclo para máxima produtividade
    """)
    st.markdown("[Saiba mais](https://investidorsardinha.r7.com/aprender/tecnica-pomodoro-timer/)")

# Funções do timer
def start_timer(minutes):
    st.session_state.end_time = time.time() + minutes * 60
    st.session_state.paused = False
    st.session_state.remaining = None
    st.session_state.last_update = time.time()

def pause_timer():
    if st.session_state.end_time and not st.session_state.paused:
        st.session_state.paused = True
        st.session_state.remaining = st.session_state.end_time - time.time()
        st.session_state.last_update = time.time()

def resume_timer():
    if st.session_state.paused and st.session_state.remaining:
        st.session_state.end_time = time.time() + st.session_state.remaining
        st.session_state.paused = False
        st.session_state.remaining = None
        st.session_state.last_update = time.time()

def reset_timer():
    st.session_state.end_time = None
    st.session_state.paused = False
    st.session_state.remaining = None
    st.session_state.current_state = "ready"
    st.session_state.last_update = time.time()

def format_time(seconds):
    return str(timedelta(seconds=int(seconds))[2:7]  # Formato MM:SS

def get_remaining_time():
    if st.session_state.paused and st.session_state.remaining:
        return st.session_state.remaining
    elif st.session_state.end_time:
        remaining = st.session_state.end_time - time.time()
        return max(0, remaining)
    return 0

def handle_timer_end():
    if st.session_state.current_state == "working":
        st.session_state.pomodoro_count += 1
        if st.session_state.pomodoro_count % pomodoros_before_long == 0:
            st.session_state.current_state = "long_break"
            start_timer(long_break)
        else:
            st.session_state.current_state = "short_break"
            start_timer(short_break)
    else:
        st.session_state.current_state = "working"
        start_timer(work_time)

# Interface principal
st.title("🍅 FocusFlow Pomodoro Timer")
st.markdown("### A técnica definitiva para produtividade")

col1, col2, col3 = st.columns([1,2,1])

with col2:
    # Display do timer
    remaining_seconds = get_remaining_time()
    time_display = st.empty()
    
    if remaining_seconds > 0:
        time_display.markdown(f"<div class='time-display'>{format_time(remaining_seconds)}</div>", unsafe_allow_html=True)
    else:
        time_display.markdown(f"<div class='time-display ready'>00:00</div>", unsafe_allow_html=True)

    # Status atual
    status_text = {
        "ready": "Pronto para começar",
        "working": "Trabalho Focado",
        "short_break": "Pausa Curta",
        "long_break": "Pausa Longa"
    }.get(st.session_state.current_state, "Pronto para começar")
    
    st.markdown(f"<div class='status-text'>{status_text}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='pomodoro-count'>Pomodoros completos: {st.session_state.pomodoro_count}</div>", unsafe_allow_html=True)

    # Controles
    col_controls1, col_controls2, col_controls3 = st.columns(3)
    
    with col_controls1:
        if st.session_state.current_state == "ready":
            if st.button("Começar Pomodoro", use_container_width=True, key="start"):
                st.session_state.current_state = "working"
                start_timer(work_time)
                st.rerun()
        elif st.session_state.current_state == "working":
            if st.button("Pausar", use_container_width=True, disabled=st.session_state.paused, key="pause"):
                pause_timer()
                st.rerun()
            if st.button("Continuar", use_container_width=True, disabled=not st.session_state.paused, key="resume"):
                resume_timer()
                st.rerun()
    
    with col_controls2:
        if st.session_state.current_state != "ready":
            if st.button("Pular", use_container_width=True, key="skip"):
                handle_timer_end()
                st.rerun()
    
    with col_controls3:
        if st.session_state.current_state != "ready":
            if st.button("Reiniciar", use_container_width=True, key="reset"):
                reset_timer()
                st.rerun()

# Vídeo de fundo durante o trabalho (opcional)
if st.session_state.current_state == "working" and remaining_seconds > 0:
    st.markdown("---")
    st.markdown("### Ambiente de Foco")
    st.video("https://www.youtube.com/watch?v=jfKfPfyJRdk")

# Atualização automática
if remaining_seconds > 0 and time.time() - st.session_state.last_update > 0.1:
    st.session_state.last_update = time.time()
    st.rerun()
elif st.session_state.end_time is not None and remaining_seconds <= 0:
    handle_timer_end()
    st.rerun()
