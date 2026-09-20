import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
from pptx import Presentation
import io

# --- إعدادات الصفحة والتصميم (RTL & Professional UI) ---
st.set_page_config(
    page_title="MindSphere AI | الأكاديمي الذكي",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص واجهة المستخدم لدعم العربية (RTL) وتنسيق الألوان
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .stSidebar {
        direction: rtl;
        text-align: right;
    }
    .card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-right: 5px solid #4f46e5;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- دوال استخراج النصوص من الملفات ---
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def extract_text_from_pptx(uploaded_file):
    prs = Presentation(uploaded_file)
    text = ""
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    text += paragraph.text + "\n"
    return text

# --- الشريط الجانبي (Sidebar) ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=80)
    st.title("MindSphere AI")
    st.markdown("---")
    
    # حقل إدخال مفتاح الـ API
    api_key = st.text_input("🔑 أدخل مفتاح Google Gemini API Key:", type="password")
    
    st.markdown("---")
    st.markdown("### 📌 معلومات النظام")
    st.info("هذا النظام مصمم لتحليل المحاضرات الأكاديمية والملفات وتقديم ملخصات واختبارات ذكية.")

# --- الواجهة الرئيسية ---
st.title("🧠 MindSphere AI - منصة التحليل الأكاديمي المتقدم")
st.markdown("ارفع ملف محاضرتك (`PDF` أو `PPTX`) ودع الذكاء الاصطناعي يحلله ويقدم لك ملخصات، أسئلة، خرائط ذهنية، وترجمة فورية.")

# رفع الملف
uploaded_file = st.file_uploader("📂 اختر ملف المحاضرة (PDF أو PPTX):", type=["pdf", "pptx"])

if uploaded_file is not None:
    # استخراج النص بناءً على نوع الملف
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    with st.spinner("🔄 جاري استخراج قراءة المحتوى من الملف..."):
        if file_extension == "pdf":
            document_text = extract_text_from_pdf(uploaded_file)
        elif file_extension == "pptx":
            document_text = extract_text_from_pptx(uploaded_file)
        else:
            document_text = ""

    if document_text.strip() == "":
        st.error("⚠️ عذراً، لم يتم العثور على نص داخل الملف. تأكد من أن الملف يحتوي على نصوص واضحة.")
    else:
        st.success(f"✅ تم استخراج النصوص بنجاح من الملف: **{uploaded_file.name}**")
        
        # زر بدء التحليل المعرفي
        if st.button("🚀 بدء التحليل المعرفي العميق"):
            if not api_key:
                st.warning("⚠️ الرجاء إدخال مفتاح **Google Gemini API Key** في الشريط الجانبي أولاً!")
            else:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # نظام التبويبات الأربعة
                    tab1, tab2, tab3, tab4 = st.tabs(["📚 الملخص الأكاديمي", "❓ بنك الأسئلة", "🗺️ الخريطة الذهنية", "🌐 الترجمة الفورية"])
                    
                    with st.spinner("🤖 الذكاء الاصطناعي يعالج المحتوى الآن..."):
                        
                        # 1. الملخص الأكاديمي
                        with tab1:
                            st.subheader("📌 الملخص الأكاديمي الشامل")
                            prompt_summary = f"قم بعمل ملخص أكاديمي احترافي وعميق ومقسّم إلى نقاط رئيسية ومفاهيم جوهرية للنص التالي:\n\n{document_text[:15000]}"
                            response_summary = model.generate_content(prompt_summary)
                            st.markdown(response_summary.text)
                        
                        # 2. بنك الأسئلة
                        with tab2:
                            st.subheader("📝 أسئلة تقييمية للمحتوى")
                            prompt_quiz = f"بناءً على النص التالي، قم بتوليد 10 أسئلة مراجعة أكاديمية مع خياراتها أو إجاباتها النموذجية:\n\n{document_text[:15000]}"
                            response_quiz = model.generate_content(prompt_quiz)
                            st.markdown(response_quiz.text)
                        
                        # 3. الخريطة الذهنية
                        with tab3:
                            st.subheader("🗺️ الهيكل المعرفي والخريطة الذهنية (Markdown)")
                            prompt_map = f"قم بتحويل المفاهيم الأساسية في النص التالي إلى خريطة ذهنية منظمة باستخدام هيكل Markdown الشجري (Bullet points هرمية):\n\n{document_text[:15000]}"
                            response_map = model.generate_content(prompt_map)
                            st.markdown(response_map.text)
                        
                        # 4. الترجمة الفورية
                        with tab4:
                            st.subheader("🌐 الترجمة الأكاديمية المتقدمة")
                            target_lang = st.selectbox("اختر اللغة المستهدفة للترجمة:", ["الإنجليزية", "الفرنسية", "الإسبانية", "الألمانية"])
                            if st.button("تنفيذ الترجمة الشاملة الآن"):
                                with st.spinner(f"جاري الترجمة إلى {target_lang}..."):
                                    prompt_trans = f"قم بترجمة أهم أفكار ومفاهيم النص التالي إلى اللغة {target_lang} بأسلوب أكاديمي احترافي:\n\n{document_text[:10000]}"
                                    response_trans = model.generate_content(prompt_trans)
                                    st.markdown(response_trans.text)

                except Exception as e:
                    st.error(f حدث خطأ أثناء الاتصال بنموذج الذكاء الاصطناعي: `{e}`")
