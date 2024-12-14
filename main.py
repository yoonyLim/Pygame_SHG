import sys
import pygame as pg
import content.simulation_manger as sim
from content.physics.cluster import Cluster
from content.physics.particle import Particle
from content.UI.textbox import TextBox
from content.UI.button import Button

def main():
    pg.init()
    pg.display.set_caption("Spatial Hash Grid: Particle Cluster Optimization")

    cluster = Cluster(pg.Rect(0, 0, sim.SCREEN_WIDTH, sim.SCREEN_HEIGHT), sim.NUM_PARTICLES, sim.ENERGY_LOSS, sim.GRAVITY)

    while sim.SIM_LOOP:
        sim.CLOCK.tick(sim.FPS)

        FPS_text = TextBox(10, 10, "FPS: " + str(round(sim.CLOCK.get_fps(), 2)), sim.FONT_FAMILY, sim.FONT_SIZE, sim.FONT_COLOR, "topleft")
        num_particles_text = TextBox(10, 30, "# of Particles: " + str(sim.NUM_PARTICLES), sim.FONT_FAMILY, sim.FONT_SIZE, sim.FONT_COLOR, "topleft")
        using_SHG_text = TextBox(10, 50, "Using SHG: " + str(sim.USE_SHG), sim.FONT_FAMILY, sim.FONT_SIZE, sim.FONT_COLOR, "topleft")
        chasing_mouse_text = TextBox(10, 70, "Chasing Mouse: " + str(sim.PLANET_LIKE), sim.FONT_FAMILY, sim.FONT_SIZE, sim.FONT_COLOR, "topleft")

        change_mode_btn = Button(sim.SCREEN_WIDTH - 100, 20, "| Toggle SHG |", sim.FONT_FAMILY, sim.FONT_SIZE, sim.FONT_COLOR, 0)
        chase_mouse_btn = Button(sim.SCREEN_WIDTH - 100, 50, "| Toggle Chase Mouse |", sim.FONT_FAMILY, sim.FONT_SIZE, sim.FONT_COLOR, 1)

        TXT_LIST = [FPS_text, num_particles_text, using_SHG_text, chasing_mouse_text]
        BTN_LIST = [change_mode_btn, chase_mouse_btn]

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sim.SIM_LOOP = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if change_mode_btn.checkForInput(pg.mouse.get_pos()):
                    sim.USE_SHG = not sim.USE_SHG
                elif chase_mouse_btn.checkForInput(pg.mouse.get_pos()):
                    sim.PLANET_LIKE = not sim.PLANET_LIKE
                else:
                    new_particle = Particle(pg.mouse.get_pos()[0] * 1.0, pg.mouse.get_pos()[1] * 1.0, mass=100, radius=30.0, color=(255, 0, 0, 255))
                    cluster.particles.append(new_particle)
                    sim.NUM_PARTICLES += 1

        if sim.PLANET_LIKE:
            sim.PLANET_CENTER = [pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]]

        sim.SCREEN.fill(sim.BG_COLOR)

        ## main simulation ##
        if sim.USE_SHG:
            cluster.update_SHG()
        else:
            cluster.update()
        
        cluster.draw(sim.SCREEN)

        for texts in TXT_LIST:
            texts.update()

        for btn in BTN_LIST:
            btn.update()

        ## update screen ##
        pg.display.update()
        
        print(sim.CLOCK.get_fps())

    pg.quit()
    sys.exit()

if  __name__ == "__main__":
    main()