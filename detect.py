# detect.py
import argparse
import os
from dotenv import load_dotenv
from src.analysis import detector

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="AI Error Detector for Dharma Talks")
    parser.add_argument("input_video", help="Path to the raw video file")
    parser.add_argument("--output", help="Path to save the FCPXML file", default="output_markers.fcpxml")
    
    args = parser.parse_args()
    
    workspace = os.getenv("WORKSPACE_DIR", "./workspace")
    
    print(f"🚀 Starting Error Detection for: {args.input_video}")
    detector.detect_errors_in_video(args.input_video, args.output, workspace)

if __name__ == "__main__":
    main()