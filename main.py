import sys
import pygame as pg
import content.simulation_manger as sim
from content.physics.cluster import Cluster
from content.physics.particle import Particle
from content.UI.textbox import TextBox

def main():
    pg.init()
    pg.display.set_caption("Spatial Hash Grid: Particle Cluster Optimization")

    cluster = Cluster(pg.Rect(0, 0, sim.SCREEN_WIDTH, sim.SCREEN_HEIGHT), sim.NUM_PARTICLES, sim.ENERGY_LOSS, sim.GRAVITY)

    while sim.SIM_LOOP:
        sim.CLOCK.tick(sim.FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sim.SIM_LOOP = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                new_particle = Particle(pg.mouse.get_pos()[0] * 1.0, pg.mouse.get_pos()[1] * 1.0, mass=100, radius=30.0, color=(255, 0, 0, 255))
                cluster.particles.append(new_particle)

        if sim.PLANET_LIKE:
            sim.PLANET_CENTER = [pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]]

        sim.SCREEN.fill(sim.BG_COLOR)

        ## main simulation ##
        if sim.USE_SHG:
            cluster.update_SHG()
        else:
            cluster.update()
        
        cluster.draw(sim.SCREEN)

        FPS_text = TextBox(10, 10, "FPS: " + str(round(sim.CLOCK.get_fps(), 2)), sim.FONT_FAMILY, sim.FONT_SIZE, sim.FONT_COLOR, "topleft")
        num_particles_text = TextBox(10, 30, "# of Particles: " + str(sim.NUM_PARTICLES), sim.FONT_FAMILY, sim.FONT_SIZE, sim.FONT_COLOR, "topleft")

        TXT_LIST = [FPS_text, num_particles_text]

        for texts in TXT_LIST:
            texts.update()

        ## update screen ##
        pg.display.update()

    pg.quit()
    sys.exit()

if  __name__ == "__main__":
    main()