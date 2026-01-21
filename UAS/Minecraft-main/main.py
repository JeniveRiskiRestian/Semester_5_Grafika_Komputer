from settings import *                # Import semua pengaturan (resolusi, warna, versi OpenGL, dsb)
import moderngl as mgl                 # Library ModernGL untuk rendering 3D dengan OpenGL
import pygame as pg                    # Pygame untuk window, input, dan loop utama
import sys                             # Sistem exit
from shader_program import ShaderProgram  # Modul shader untuk transformasi & rendering
from scene import Scene                # Modul scene berisi objek 3D
from player import Player              # Modul player / kamera
from textures import Textures          # Modul untuk memuat tekstur / material


class VoxelEngine:
    def __init__(self):
        pg.init()  # Inisialisasi Pygame

        # Set atribut OpenGL sebelum membuat window
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, MAJOR_VER)  # Versi OpenGL major
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, MINOR_VER)  # Versi minor
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)  # Core profile
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, DEPTH_SIZE)  # Depth buffer untuk z-buffer
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, NUM_SAMPLES)  # Anti-aliasing

        # Membuat window OpenGL dengan double buffering
        pg.display.set_mode(WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF)

        # Membuat konteks ModernGL untuk rendering 3D
        self.ctx = mgl.create_context()

        # Mengaktifkan fitur grafika 3D: depth test, face culling, blending
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.gc_mode = 'auto'  # Auto clean GPU resources

        self.clock = pg.time.Clock()  # Clock untuk menghitung delta_time dan FPS
        self.delta_time = 0           # Selisih waktu antar frame
        self.time = 0                 # Waktu total program (detik)

        pg.event.set_grab(True)      # Kunci mouse di window
        pg.mouse.set_visible(False)  # Hide cursor (FPS style camera)

        self.is_running = True       # Flag loop utama
        self.on_init()               # Inisialisasi objek 3D, shader, player, scene, textures

    def on_init(self):
        self.textures = Textures(self)          # Load tekstur / material voxel
        self.player = Player(self)              # Inisialisasi player / kamera
        self.shader_program = ShaderProgram(self)  # Shader untuk transformasi & rendering
        self.scene = Scene(self)                # Scene berisi semua objek 3D

    def update(self):
        self.player.update()           # Update posisi & rotasi kamera
        self.shader_program.update()   # Update transformasi dan matriks shader
        self.scene.update()            # Update animasi / perubahan objek 3D

        self.delta_time = self.clock.tick()        # Hitung waktu frame terakhir
        self.time = pg.time.get_ticks() * 0.001    # Total waktu program dalam detik
        pg.display.set_caption(f'{self.clock.get_fps() :.0f}')  # Update FPS di title bar

    def render(self):
        self.ctx.clear(color=BG_COLOR)  # Clear buffer warna & depth
        self.scene.render()             # Render semua objek 3D di scene
        pg.display.flip()               # Swap buffer untuk menampilkan frame

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False  # Quit program jika window ditutup atau ESC
            self.player.handle_event(event=event)  # Kirim input ke player (gerak/rotasi kamera)

    def run(self):
        while self.is_running:
            self.handle_events()  # Tangani input keyboard/mouse
            self.update()         # Update logika, transformasi, shader, scene
            self.render()         # Render frame baru
        pg.quit()                 # Bersihkan Pygame
        sys.exit()                # Keluar dari program


if __name__ == '__main__':
    app = VoxelEngine()  # Buat instance engine
    app.run()            # Jalankan loop utama
