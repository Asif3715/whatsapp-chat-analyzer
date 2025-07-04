import streamlit as st
from io import StringIO
import preprocessing
import helper
import matplotlib.pyplot as plt
# Used LLMs for styling
# Page configuration
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #25D366;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .section-header {
        color: #075E54;
        border-bottom: 2px solid #25D366;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .stat-container {
        background: linear-gradient(135deg, #25D366 0%, #075E54 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }
    .stat-label {
        font-size: 1.1rem;
        margin: 0;
        opacity: 0.9;
    }
    .sidebar-header {
        color: #075E54;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">💬 WhatsApp Chat Analyzer</h1>', unsafe_allow_html=True)

# Sidebar styling
st.sidebar.markdown('<div class="sidebar-header">📊 Analysis Control Panel</div>', unsafe_allow_html=True)

# File uploader with custom styling
st.sidebar.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.sidebar.markdown("**📁 Upload Your Chat File**")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=['txt'])
st.sidebar.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    df = preprocessing.preprocess(string_data)

    users_list = df['user'].unique().tolist()
    users_list.remove('group_notification')
    users_list.sort()
    users_list.insert(0, 'Overall Analysis')

    st.sidebar.markdown("**👥 Select User for Analysis**")
    selected_user = st.sidebar.selectbox('Show Analysis wrt', users_list)

    # Analysis button with custom styling
    st.sidebar.markdown("---")
    if st.sidebar.button('🚀 Show Analysis', type="primary"):
        messages, words, media, links = helper.fetch_stats(selected_user, df)

        # Statistics section with enhanced styling
        st.markdown('<h2 class="section-header">📈 Key Statistics</h2>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f'''
            <div class="stat-container">
                <p class="stat-number">{messages}</p>
                <p class="stat-label">Messages</p>
            </div>
            ''', unsafe_allow_html=True)

        with col2:
            st.markdown(f'''
            <div class="stat-container">
                <p class="stat-number">{words}</p>
                <p class="stat-label">Words</p>
            </div>
            ''', unsafe_allow_html=True)

        with col3:
            st.markdown(f'''
            <div class="stat-container">
                <p class="stat-number">{media}</p>
                <p class="stat-label">Media</p>
            </div>
            ''', unsafe_allow_html=True)

        with col4:
            st.markdown(f'''
            <div class="stat-container">
                <p class="stat-number">{links}</p>
                <p class="stat-label">Links</p>
            </div>
            ''', unsafe_allow_html=True)

        # Overall Analysis section
        if selected_user == 'Overall Analysis':
            st.markdown('<h2 class="section-header">🔍 Overall Analysis</h2>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            fig, ax = plt.subplots(figsize=(10, 6))
            x, new_df = helper.overall_analysis(df)

            with col1:
                st.subheader('📊 Most Active Users')
                ax.bar(x.index, x.values, color='#25D366', alpha=0.8)
                plt.xticks(rotation='vertical')
                plt.title('Most Active Users', fontsize=14, fontweight='bold')
                plt.xlabel('Users', fontsize=12)
                plt.ylabel('Messages', fontsize=12)
                plt.tight_layout()
                st.pyplot(fig)

            with col2:
                st.subheader('📋 User Statistics')
                st.dataframe(new_df, use_container_width=True)

        # WordCloud section
        st.markdown('<h2 class="section-header">☁️ Word Cloud</h2>', unsafe_allow_html=True)
        wc = helper.word_cloud(selected_user, df)
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        plt.title('Word Cloud', fontsize=16, fontweight='bold', pad=20)
        st.pyplot(fig)

        # Most frequent words section
        st.markdown('<h2 class="section-header">🔤 Most Frequent Words</h2>', unsafe_allow_html=True)
        most_freq = helper.most_common(selected_user, df)
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(most_freq['Word'], most_freq['Frequency'], color='#25D366', alpha=0.8)
        ax.set_xticklabels(most_freq['Word'], rotation='vertical', ha='right')
        plt.title('Top 25 Most Frequent Words', fontsize=14, fontweight='bold')
        plt.xlabel('Words', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.tight_layout()
        st.pyplot(fig)

        # Most used emojis section
        st.markdown('<h2 class="section-header">😀 Most Frequent Emojis</h2>', unsafe_allow_html=True)
        emojis = helper.emoji_fetch(selected_user, df)
        st.dataframe(emojis, use_container_width=True)

        # Timeline section
        st.markdown('<h2 class="section-header">📅 Timeline Analysis</h2>', unsafe_allow_html=True)
        monthly_counts = helper.timeline(selected_user, df)
        monthly_counts.index = monthly_counts.index.astype(str)
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(monthly_counts.index, monthly_counts.values, marker='o', linewidth=2,
                markersize=6, color='#25D366')
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Number of Messages', fontsize=12)
        ax.set_title('Message Timeline', fontsize=14, fontweight='bold')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

        # Monthly Analysis section
        st.markdown('<h2 class="section-header">📊 Monthly Analysis</h2>', unsafe_allow_html=True)
        months = helper.monthly(selected_user, df)
        fig, ax = plt.subplots(figsize=(12, 6))
        months.plot(kind='bar', ax=ax, color='#25D366', alpha=0.8)
        ax.set_xlabel('Months', fontsize=12)
        ax.set_ylabel('Messages', fontsize=12)
        ax.set_title('Monthly Message Distribution', fontsize=14, fontweight='bold')
        ax.tick_params(axis='x', rotation=90)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

        # Day-wise analysis section
        st.markdown('<h2 class="section-header">📅 Day-wise Analysis</h2>', unsafe_allow_html=True)
        days = helper.daily(selected_user, df)
        fig, ax = plt.subplots(figsize=(12, 6))
        days.plot(kind='bar', ax=ax, color='#25D366', alpha=0.8)
        ax.set_xlabel('Days', fontsize=12)
        ax.set_ylabel('Messages', fontsize=12)
        ax.set_title('Daily Message Distribution', fontsize=14, fontweight='bold')
        ax.tick_params(axis='x', rotation=90)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

else:
    # Landing page when no file is uploaded
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h2>📱 Welcome to WhatsApp Chat Analyzer!</h2>
        <p style="font-size: 1.2rem; color: #666;">
            Upload your WhatsApp chat export file to get started with the analysis.
        </p>
        <p style="color: #888;">
            📁 Click on "Choose a file" in the sidebar to upload your chat file.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>💬 WhatsApp Chat Analyzer | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)