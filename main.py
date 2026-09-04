import webbrowser
import time

def rickroll():
    """
    The ultimate rickroll function!
    """
    print("🎵 Loading something awesome... 🎵")
    time.sleep(2)
    
    rickroll_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print("You've been rickrolled! 🎶")
    print(f"Opening: {rickroll_url}")
    time.sleep(1)
    
    webbrowser.open(rickroll_url)
    
    print("\n🎤 Never gonna give you up! 🎤")
    print("🎤 Never gonna let you down! 🎤")
    print("🎤 Never gonna run around and desert you! 🎤\n")

if __name__ == "__main__":
    rickroll()
