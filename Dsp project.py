import numpy as np
import librosa
import soundfile as sf
import noisereduce as nr
import os

def find_audio_files():
    """Find all audio files in the folder"""
    print("Searching for audio files...")
    audio_files = []
    
    for file in os.listdir('.'):
        if file.lower().endswith(('.mp3', '.wav', '.m4a', '.flac')):
            audio_files.append(file)
    
    return audio_files

def load_audio(file_path):
    """Load audio file"""
    print(f"Loading {file_path}...")
    audio, sr = librosa.load(file_path, sr=None)
    print(f"File loaded: {file_path}")
    print(f"Sample rate: {sr} Hz")
    print(f"Duration: {len(audio) / sr:.2f} seconds")
    print(f"Number of samples: {len(audio)}")
    return audio, sr

def main():
    print("Audio Noise Reduction Program")
    print("=" * 50)
    
    # Search for audio files
    audio_files = find_audio_files()
    
    if not audio_files:
        print("No audio files found in the folder!")
        print("\nPlease check:")
        print("1. Audio file is in the same folder as this program")
        print("2. File extension is .mp3, .wav, .m4a, or .flac")
        print("3. File is not hidden")
        print("\nFiles in current folder:")
        for file in os.listdir('.'):
            print(f"   - {file}")
        return
    
    print(f"\nFound {len(audio_files)} audio file(s):")
    for i, file in enumerate(audio_files, 1):
        print(f"   {i}. {file}")
    
    # Use the first audio file found
    input_file = audio_files[0]
    print(f"\nProcessing file: {input_file}")
    
    try:
        # Load audio directly - librosa can handle MP3
        audio, sr = load_audio(input_file)
        
    except Exception as e:
        print(f"Error loading file: {e}")
        print("\nSuggested solutions:")
        print("1. Make sure the file is not corrupted")
        print("2. Try a WAV file instead of MP3")
        print("3. Make sure libraries are installed: pip install librosa noisereduce soundfile")
        return
    
    # Audio processing
    print("\nProcessing audio and removing noise...")
    
    # Take first 2 seconds as noise sample
    noise_duration = 2  # seconds
    noise_samples = int(noise_duration * sr)
    
    if len(audio) > noise_samples:
        noise_sample = audio[:noise_samples]
        print(f"Taking noise sample from first {noise_duration} seconds")
    else:
        noise_sample = audio
        print("File is short, using entire file as noise sample")
    
    # Apply noise reduction
    try:
        reduced_noise = nr.reduce_noise(
            y=audio, 
            sr=sr, 
            y_noise=noise_sample,
            stationary=True, 
            prop_decrease=0.8,
            time_constant_s=2.0
        )
        print("Noise reduction applied successfully")
        
    except Exception as e:
        print(f"Error in audio processing: {e}")
        print("Using alternative settings...")
        # Alternative settings
        reduced_noise = nr.reduce_noise(
            y=audio, 
            sr=sr, 
            stationary=True, 
            prop_decrease=0.7
        )
    
    # Save results
    output_file = "Sound with no noise.wav"
    try:
        sf.write(output_file, reduced_noise, sr)
        print(f"Cleaned audio saved as: {output_file}")
        
        # Show output file info
        file_size = os.path.getsize(output_file) / 1024 / 1024
        print(f"Output file size: {file_size:.2f} MB")
        
    except Exception as e:
        print(f"Error saving file: {e}")
        return
    
    print("\nAudio processing completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    main()
