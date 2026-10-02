# -*- coding: utf-8 -*-

from kivy.app import App

from app.interface import TelaPrincipal


class Harmonia21App(App):

    def build(self):
        self.title = "Harmonia Funcional Avançada"
        return TelaPrincipal()


if __name__ == "__main__":
    Harmonia21App().run()
