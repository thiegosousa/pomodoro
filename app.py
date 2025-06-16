import streamlit as st
import time

# Configuração da página
st.set_page_config(
    page_title="FocusFlow Pomodoro Timer",
    page_icon="🍅",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS customizado para UX moderna ---
st.markdown("""
<style>
.time-display {
    font-size: 5rem;
    font-weight: bold;
    text-align: center;
    margin: 1.5rem 0 0.5rem 0;
    color: #e74c3c;
    font-family: 'Courier New', monospace;
    letter-spacing: 2px;
}
.status-text {
    font-size: 1.3rem;
    text-align: center;
    margin: 0.5rem 0 1rem 0;
    font-weight: 600;
    color: #34495e;
}
.pomodoro-count {
    text-align: center;
    margin: 0.5rem 0 1.5rem 0;
    font-size: 1rem;
    color: #7f8c8d;
}
.stButton>button {
    border: none;
    border-radius: 8px;
    padding: 0.7rem 1.5rem;
    font-weight: 600;
    font-size: 1.1rem;
    background: #e74c3c;
    color: #fff;
    margin: 0.3rem 0.5rem;
    transition: background 0.2s;
}
.stButton>button:hover {
    background: #c0392b;
}
.video-container {
    position: relative;
    width: 100%;
    height: 0;
    padding-bottom: 56.25%; /* 16:9 */
    margin-top: 20px;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0,0,0,0.08);
}
.video-container iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: none;
}
.controls-container {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 20px;
    flex-wrap: wrap;
}
.control-button {
    flex: 1;
    min-width: 120px;
}
@media (max-width: 600px) {
    .time-display { font-size: 2.5rem; }
    .status-text { font-size: 1rem; }
    .video-container { padding-bottom: 40%; }
}
</style>
""", unsafe_allow_html=True)

# --- Estados da sessão ---
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
if 'mode' not in st.session_state:
    st.session_state.mode = "Pomodoro"  # ou "Custom"
if 'running' not in st.session_state:
    st.session_state.running = False

# --- Configurações padrão ---
DEFAULT_WORK = 25
DEFAULT_SHORT_BREAK = 5
DEFAULT_LONG_BREAK = 15

# --- Configurações do usuário ---
with st.sidebar:
    st.title("⚙️ Configurações")
    work_time = st.number_input("Tempo de trabalho (min)", min_value=1, max_value=60, value=25)
    short_break = st.number_input("Pausa curta (min)", min_value=1, max_value=30, value=5)
    long_break = st.number_input("Pausa longa (min)", min_value=1, max_value=60, value=15)
    st.markdown("---")
    st.markdown("### Sobre a Técnica Pomodoro")
    st.markdown("""
    - 🍅 **Trabalho Focado:** 25 minutos de concentração intensa
    - ☕ **Pausa Curta:** 5 minutos para descanso
    - 🌴 **Pausa Longa:** 15 minutos após 4 pomodoros
    - 🔁 Repita o ciclo para máxima produtividade
    """)
    st.markdown("[Saiba mais sobre a técnica Pomodoro](https://investidorsardinha.r7.com/aprender/tecnica-pomodoro-timer/)")
    st.markdown("---")
    st.markdown("Desenvolvido com ❤️ usando Python e Streamlit")

# --- Ajuste os tempos do timer conforme configuração ---
if 'current_state' in st.session_state:
    if st.session_state.current_state == "working":
        tempo = work_time
    elif st.session_state.current_state == "short_break":
        tempo = short_break
    elif st.session_state.current_state == "long_break":
        tempo = long_break
    else:
        tempo = work_time
else:
    tempo = work_time

# --- Funções do timer ---
def start_timer(minutes):
    st.session_state.end_time = time.time() + minutes * 60
    st.session_state.paused = False
    st.session_state.remaining = None
    st.session_state.running = True

def pause_timer():
    if st.session_state.end_time and not st.session_state.paused:
        st.session_state.paused = True
        st.session_state.remaining = st.session_state.end_time - time.time()

def resume_timer():
    if st.session_state.paused and st.session_state.remaining:
        st.session_state.end_time = time.time() + st.session_state.remaining
        st.session_state.paused = False
        st.session_state.remaining = None

def reset_timer():
    st.session_state.end_time = None
    st.session_state.paused = False
    st.session_state.remaining = None
    st.session_state.current_state = "ready"
    st.session_state.running = False

def format_time(seconds):
    if seconds <= 0:
        return "00:00"
    minutes = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{minutes:02d}:{secs:02d}"

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

# --- Interface principal ---
st.title("🍅 FocusFlow Pomodoro Timer")
st.markdown("### A técnica definitiva para melhorar sua produtividade")

# --- Display do timer ---
remaining_seconds = get_remaining_time()
time_display = st.empty()

time_class = ""
if st.session_state.current_state == "working":
    time_class = "time-display working-display"
elif st.session_state.current_state in ["short_break", "long_break"]:
    time_class = "time-display break-display"
else:
    time_class = "time-display ready-display"

if remaining_seconds > 0:
    time_display.markdown(f"<div class='{time_class}'>{format_time(remaining_seconds)}</div>", unsafe_allow_html=True)
else:
    time_display.markdown(f"<div class='time-display ready-display'>00:00</div>", unsafe_allow_html=True)

# --- Status atual ---
status_text = {
    "ready": "Pronto para começar",
    "working": "⏳ Trabalho Focado",
    "short_break": "☕ Pausa Curta",
    "long_break": "🌴 Pausa Longa"
}.get(st.session_state.current_state, "Pronto para começar")

st.markdown(f"<div class='status-text'>{status_text}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='pomodoro-count'>Pomodoros completos: {st.session_state.pomodoro_count}</div>", unsafe_allow_html=True)

# --- Controles ---
st.markdown('<div class="controls-container">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("▶️ Pomodoro", use_container_width=True, key="start_pomodoro"):
        st.session_state.current_state = "working"
        start_timer(work_time)
        st.rerun()
with col2:
    if st.button("☕ Pausa Curta", use_container_width=True, key="start_short_break"):
        st.session_state.current_state = "short_break"
        start_timer(short_break)
        st.rerun()
with col3:
    if st.button("🌴 Pausa Longa", use_container_width=True, key="start_long_break"):
        st.session_state.current_state = "long_break"
        start_timer(long_break)
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# --- Botões de Pausar/Continuar ---
if st.session_state.current_state in ["working", "short_break", "long_break"]:
    if not st.session_state.paused:
        if st.button("⏸️ Pausar Timer", use_container_width=True, key="pause_timer"):
            pause_timer()
            st.rerun()
    else:
        if st.button("▶️ Continuar Timer", use_container_width=True, key="resume_timer"):
            resume_timer()
            st.rerun()

# --- Vídeo de fundo durante o trabalho ---
if st.session_state.mode == "Pomodoro" and st.session_state.running:
    st.markdown("---")
    st.markdown("### Ambiente de Foco")
    st.markdown("""
        <div class="video-container">
            <iframe src="https://www.youtube.com/embed/jfKfPfyJRdk?autoplay=1&mute=0&controls=0&loop=1&playlist=jfKfPfyJRdk"
                    frameborder="0"
                    allow="autoplay; encrypted-media"
                    allowfullscreen>
            </iframe>
        </div>
    """, unsafe_allow_html=True)
    st.caption("Música relaxante para ajudar na concentração")

# --- Atualização automática do timer ---
if remaining_seconds > 0:
    time.sleep(1)
    st.rerun()
elif st.session_state.end_time is not None and remaining_seconds <= 0:
    handle_timer_end()
    st.rerun()
