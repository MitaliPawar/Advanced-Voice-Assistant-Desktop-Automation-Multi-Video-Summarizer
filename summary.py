import streamlit as st
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

# Function to fetch video transcript from YouTube
def fetch_video_transcript(youtube_link):
    try:
        video_id = YouTube(youtube_link).video_id
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        st.error(f"Error fetching transcript for {youtube_link}: {str(e)}")
        return None

# Function to generate summary from video transcript
def generate_summary(transcript):
    if not transcript:
        return "No transcript available."

    # Combine all text fragments into a single text
    text = " ".join([fragment['text'] for fragment in transcript])

    # Use Hugging Face pipeline for summarization
    try:
        summarizer = pipeline("summarization")
        # Split text into chunks that are manageable for the summarizer
        max_chunk = 1000
        chunks = [text[i:i + max_chunk] for i in range(0, len(text), max_chunk)]
        summary = ''
        for chunk in chunks:
            result = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
            summary_text = result[0].get('summary_text', '')  # Safely get the summary text
            summary += summary_text + "\n\n"  # Separate summaries with double new lines
        return summary.strip()
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return "Error generating summary."

# Main Streamlit app
def main():
    st.title("Video Summarization App")

    # Allow user to input YouTube links
    youtube_links = st.text_area("Enter YouTube links (one link per line)")

    if st.button("Generate Summaries"):
        if youtube_links:
            links_list = youtube_links.split('\n')
            st.write("Number of YouTube links entered:", len(links_list))

            overall_summary = ""
            for index, youtube_link in enumerate(links_list, start=1):
                if not youtube_link.strip():
                    continue

                # Fetch video transcript from YouTube
                transcript = fetch_video_transcript(youtube_link.strip())

                # Generate summary
                if transcript:
                    summary = generate_summary(transcript)
                    overall_summary += f"Summary for Link {index}:\n{summary}\n\n"
                else:
                    overall_summary += f"No transcript available for Link {index}.\n\n"

            # Display overall summary
            st.subheader("Overall Summary:")
            st.write(overall_summary)

if __name__ == "__main__":
    main()
