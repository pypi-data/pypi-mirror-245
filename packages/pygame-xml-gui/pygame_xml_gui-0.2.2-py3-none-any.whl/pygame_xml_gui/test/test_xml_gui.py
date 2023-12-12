import sys, os, pygame

from ..src.UserInterface import UserInterface
import random

from PygameXtras import PerformanceGraph

RUN_FOR = -1 # seconds

class Point:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

class Program():
    def __init__(self):
        self.win_w, self.win_h = 800, 600
        self.center = (int(self.win_w/2),int(self.win_h/2))
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.win_w, self.win_h))
        self.fpsclock = pygame.time.Clock()
        self.fps = 60

    def print_name(self, point: Point):
        print(point.name)

    def round(self, point: Point):
        for p in self.points:
            if p is point:
                p.pos = (round(p.pos[0]), round(p.pos[1]))
                self.ui.refresh()
                return
    
    def delete(self, point: Point):
        self.points.remove(point)
        self.ui.refresh()

    def add_random(self):
        self.points.append(
            Point("Random" + str(random.randint(0,100)), (round(random.random()*100, 4), round(random.random()*100, 4)))
        )
        self.ui.refresh()

    def main(self):

        fpslist = []

        with open(os.path.join(os.path.dirname(__file__), "test.xml"), "r") as f:
            structure = f.read()

        self.points = [Point("Point1", (1,1)), Point("Point2", (2,2))]
        
        self.ui = UserInterface()
        self.ui.set_structure(structure)
        self.ui.set_variables({
            "points": self.points
        })
        self.ui.set_pos((150, 50))
        self.ui.set_methods({
            "print_name": self.print_name,
            "round": self.round,
            "delete": self.delete,
            "add_random": self.add_random
        })
        
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

            self.screen.fill((0,0,0))
            self.ui.draw(self.screen)
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