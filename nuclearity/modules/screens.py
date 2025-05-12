import pygame, os, cv2, time
from data_exch import shared_data
from logger import make_log

def play(screen_name):
    match screen_name:
        case "startup":
            try:

                pygame.init()
                
                while shared_data["window"] is None:
                    time.sleep(0.01)

                screen = shared_data["window"]

                video_path = "C:/Users/justv/OneDrive/Рабочий стол/nuclearity/resources/videos/startup.mp4"
                cap = cv2.VideoCapture(video_path)
                #pygame.display.set_caption("NUCLEARITY.starting...")
                
                if not cap.isOpened():
                    raise Exception("Could not open video")

                make_log('INFO', 'Video Started')

                screen = shared_data["window"]


                while cap.isOpened():
                    for event in shared_data["events"]:
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                            shared_data["run"] = [False, [False, False]]
                            make_log("INFO", "Exited app")
                    ret, frame = cap.read()
                    if not ret:
                        break

                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

                    screen.blit(frame, (0, 0))
                    pygame.display.update()

                shared_data["run"][1][0] = True
                cap.release()
                #pygame.quit()

                make_log('INFO', 'Video Ended')

            except Exception as e:
                make_log("ERROR", "An error occurred during video playback", description=str(e))
    make_log('INFO', 'Video func exited')

make_log("INFO", "Screens loaded successfully")
