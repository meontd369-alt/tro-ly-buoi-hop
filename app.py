import streamlit as st
import google.generativeai as genai
import tempfile
import os

# 1. Cấu hình giao diện chuẩn Trạm Tuân Thủ Thông Minh
st.set_page_config(page_title="AI Thư Ký - Trạm Tuân Thủ Thông Minh", page_icon="🎙️", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    h1, h2, h3 {color: #001F5B;} /* Xanh Navy */
    .stButton>button {background-color: #D4AF37; color: #001F5B; font-weight: bold; border-radius: 8px; width: 100%; border: none; padding: 12px;}
    .stButton>button:hover {background-color: #b5952f; color: #ffffff; box-shadow: 0 4px 8px rgba(0,0,0,0.2);}
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ AI Thư Ký - Smart Compliance Hub")
st.markdown("Hệ thống tự động lắng nghe, lọc nhiễu và xuất biên bản họp chuyên nghiệp.")

# Lấy API Key từ Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

# 2. Định danh nhân sự tham gia
st.subheader("1. Định danh nhân sự tham gia")
col1, col2 = st.columns(2)
with col1:
    g1 = st.text_input("Giọng Nam 1:", placeholder="VD: Giám đốc Hùng")
    g2 = st.text_input("Giọng Nữ 1:", placeholder="VD: Kế toán trưởng Lan")
with col2:
    g3 = st.text_input("Giọng Nam 2:", placeholder="VD: Luật sư Tuấn")
    g4 = st.text_input("Giọng Nữ 2:", placeholder="VD: Nhân sự Mai")

# 3. Tải lên file ghi âm
st.subheader("2. Tải lên file ghi âm cuộc họp")
audio_file = st.file_uploader("Kéo thả file ghi âm (MP3, WAV, M4A) vào đây...", type=["mp3", "wav", "m4a"])

# 4. Xử lý dữ liệu với Gemini 2.5 Flash
if st.button("🚀 Bắt Đầu Rà Soát & Xuất Báo Cáo"):
    if not api_key:
        st.error("Hệ thống chưa được cấp API Key trong phần cài đặt bảo mật.")
    elif not audio_file:
        st.error("Vui lòng tải lên file ghi âm cuộc họp!")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # CẬP NHẬT: Sử dụng mô hình đời mới gemini-2.5-flash
            model = genai.GenerativeModel('gemini-2.5-flash')

            with st.spinner("⏳ AI Thư Ký đang phân tích giọng nói... Vui lòng đợi trong giây lát..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    tmp_file.write(audio_file.read())
                    tmp_file_path = tmp_file.name
                
                # Tải file lên hệ thống
                uploaded_audio = genai.upload_file(path=tmp_file_path)

                prompt = f"""
                Bạn là Thư ký Cấp cao của Trạm Tuân Thủ Thông Minh. Hãy phân tích file audio cuộc họp này.
                
                BƯỚC 1: ĐỊNH DANH GIỌNG NÓI
                Dựa vào cao độ và đặc trưng giọng nói, hãy gắn tên người phát biểu:
                - Giọng Nam 1: {g1 if g1 else 'Người nam 1'}
                - Giọng Nữ 1: {g2 if g2 else 'Người nữ 1'}
                - Giọng Nam 2: {g3 if g3 else 'Người nam 2'}
                - Giọng Nữ 2: {g4 if g4 else 'Người nữ 2'}
                
                BƯỚC 2: RÀ SOÁT & LỌC NHIỄU
                Loại bỏ các từ đệm, giao tiếp thừa. Tập trung vào nội dung công việc.
                
                BƯỚC 3: XUẤT BÁO CÁO (Markdown)
                1. TÓM TẮT MỤC TIÊU CUỘC HỌP
                2. CHI TIẾT NỘI DUNG THẢO LUẬN (Gắn tên chính xác người phát biểu)
                3. DANH SÁCH QUYẾT ĐỊNH ĐÃ CHỐT
                4. PHÂN CÔNG HÀNH ĐỘNG (Ai làm gì - Thời hạn)
                """
                
                response = model.generate_content([prompt, uploaded_audio])
                os.remove(tmp_file_path)

            st.success("✅ Đã hoàn thành Biên bản cuộc họp!")
            st.markdown("---")
            st.markdown("### 📋 BIÊN BẢN CUỘC HỌP CHI TIẾT")
            st.write(response.text)

        except Exception as e:
            st.error(f"Đã xảy ra lỗi hệ thống: {e}")
