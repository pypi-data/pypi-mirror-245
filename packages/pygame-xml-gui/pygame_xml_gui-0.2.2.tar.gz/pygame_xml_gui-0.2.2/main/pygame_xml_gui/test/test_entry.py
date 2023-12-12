import sys, os, pygame

from ..src.UserInterface import UserInterface

from PygameXtras import PerformanceGraph

RUN_FOR = -1 # seconds

class Program():
    def __init__(self):
        self.win_w, self.win_h = 800, 600
        self.center = (int(self.win_w/2),int(self.win_h/2))
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.win_w, self.win_h))
        self.fpsclock = pygame.time.Clock()
        self.fps = 60

        self.name = "Name"
    
    def confirm_name(self):
        print(f"Name is: {self.name}")

    def main(self):

        fpslist = []

        with open(os.path.join(os.path.dirname(__file__), "test_entry.xml"), "r") as f:
            structure = f.read()

        self.ui = UserInterface()
        self.ui.set_structure(structure)
        self.ui.set_variables({"name": self.name})
        self.ui.set_methods({"confirm_name": self.confirm_name})
        self.ui.set_pos((100, 50))
        
        run = True
        while run:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

            self.ui.update(event_list)
            self.name = self.ui.get_entry(id="name").get()

            self.screen.fill((0,0,0))
            self.ui.draw(self.screen)
            pygame.draw.rect(self.screen, (100,100,100), self.ui.get_rect(), 1)
            fps = self.fpsclock.get_fps()
            fpslist.append(fps)
            pygame.display.set_caption("Seconds left: " + str(round(RUN_FOR - (len(fpslist)/self.fps), 2)))
            if len(fpslist) == RUN_FOR * self.fps:
                run = False
            
            
            pygame.display.flip()
            self.fpsclock.tick(self.fps)

        pygame.display.set_caption("PerformanceGraph")
        PerformanceGraph(60, fpslist)
        
        

Program().main()