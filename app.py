import streamlit as st
import google.generativeai as genai
import tempfile
import os

# 1. Cấu hình giao diện chuẩn nhận diện thương hiệu
st.set_page_config(page_title="Trợ Lý Buổi Họp - Trạm Tuân Thủ Thông Minh", page_icon="🎙️", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    h1, h2, h3 {color: #001F5B;} /* Xanh Navy */
    .stButton>button {background-color: #D4AF37; color: #001F5B; font-weight: bold; border-radius: 5px; width: 100%;} /* Vàng Gold */
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Trợ Lý Buổi Họp - Trạm Tuân Thủ Thông Minh")
st.markdown("Hệ thống tự động lắng nghe âm thanh, lọc nhiễu và xuất biên bản họp chuyên nghiệp.")

# Lấy API Key từ "két sắt" của Streamlit (Người dùng sẽ không thấy mã này)
api_key = st.secrets.get("GOOGLE_API_KEY")

# 2. Định danh nhân sự (Thiết lập 4 giọng đọc)
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

# 4. Xử lý dữ liệu
if st.button("🚀 Bắt Đầu Rà Soát & Xuất Báo Cáo"):
    if not api_key:
        st.error("Hệ thống chưa được cấp API Key trong phần cài đặt bảo mật.")
    elif not audio_file:
        st.error("Vui lòng tải lên file ghi âm cuộc họp!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')

            with st.spinner("⏳ Hệ thống đang phân tích giọng nói và viết báo cáo. Quá trình này có thể mất 1-2 phút..."):
                # Lưu tạm file âm thanh để AI đọc
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    tmp_file.write(audio_file.read())
                    tmp_file_path = tmp_file.name
                
                uploaded_audio = genai.upload_file(path=tmp_file_path)

                prompt = f"""
                Bạn là Thư ký Cấp cao của Trạm Tuân Thủ Thông Minh. Hãy phân tích file audio cuộc họp này.
                
                BƯỚC 1: ĐỊNH DANH GIỌNG NÓI
                - Giọng Nam 1: {g1 if g1 else 'Người nam 1'}
                - Giọng Nữ 1: {g2 if g2 else 'Người nữ 1'}
                - Giọng Nam 2: {g3 if g3 else 'Người nam 2'}
                - Giọng Nữ 2: {g4 if g4 else 'Người nữ 2'}
                
                BƯỚC 2: RÀ SOÁT & LỌC NHIỄU
                Loại bỏ từ đệm, giao tiếp thừa. Hợp nhất ý lặp lại.
                
                BƯỚC 3: XUẤT BÁO CÁO (Trình bày chuẩn Markdown)
                1. TÓM TẮT MỤC TIÊU
                2. NỘI DUNG THẢO LUẬN CHÍNH (Gắn tên người nói)
                3. QUYẾT ĐỊNH ĐÃ CHỐT
                4. PHÂN CÔNG CÔNG VIỆC
                """
                
                response = model.generate_content([prompt, uploaded_audio])
                os.remove(tmp_file_path)

            st.success("✅ Đã hoàn thành Báo cáo Cuộc họp!")
            st.markdown("### 📋 BIÊN BẢN CUỘC HỌP CHUYÊN NGHIỆP")
            st.write(response.text)

        except Exception as e:

            st.error(f"Đã xảy ra lỗi hệ thống: {e}")
