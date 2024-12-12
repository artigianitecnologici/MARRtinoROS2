import time
import os
import pygame
import multiprocessing
import logging
from PIL import Image

# Frame count dictionary for various emotions
frame_count = {
    'blink': 39, 'happy': 60, 'sad': 47, 'dizzy': 67, 'excited': 24,
    'neutral': 61, 'happy2': 20, 'angry': 20, 'happy3': 26, 'bootup3': 124, 'blink2': 20
}

# Define available emotions
emotion = ['angry', 'sad', 'excited']
normal = ['neutral', 'blink2']

# Initialize multiprocessing queue and event
q = multiprocessing.Queue()
event = multiprocessing.Event()

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 480))  # Adjust resolution as needed
pygame.display.set_caption('Emotion Display')

def sound(emotion):
    """Play sound associated with the emotion."""
    os.system("aplay ./sound/" + emotion + ".wav")

def show(emotion, count):
    """Display frames for the specified emotion on the main screen using pygame."""
    for _ in range(count):
        try:
            for i in range(frame_count[emotion]):
                image_path = f'./emotions/{emotion}/frame{i}.png'
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (800, 480))  # Adjust size as needed
                screen.blit(image, (0, 0))
                pygame.display.update()
                time.sleep(0.05)  # Adjust frame delay as necessary
        except IOError as e:
            logging.info(e)
        except KeyboardInterrupt:
            pygame.quit()
            logging.info("Exiting display")
            exit()

def bootup():
    """Display bootup sequence and a simple blink effect."""
    show('bootup3', 1)
    for _ in range(1):
        p2 = multiprocessing.Process(target=show, args=('blink2', 3))
        p2.start()
        p2.join()

if __name__ == '__main__':
    # Initial bootup display
    bootup()
    
    # Main loop to handle emotions
    try:
        while True:
            if event.is_set():
                event.clear()
                emotion = q.get()
                q.empty()
                print(f"Displaying emotion: {emotion}")
                p2 = multiprocessing.Process(target=show, args=(emotion, 4))
                p3 = multiprocessing.Process(target=sound, args=(emotion,))
                p2.start()
                p3.start()
                p2.join()
                p3.join()
            else:
                neutral = normal[0]
                p2 = multiprocessing.Process(target=show, args=(neutral, 4), name='neutral_display')
                p2.start()
                p2.join()
    except KeyboardInterrupt:
        pygame.quit()

