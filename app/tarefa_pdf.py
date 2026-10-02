# -*- coding: utf-8 -*-

from threading import Thread

from app.fluxo_calculo import (
    executar_calculo_e_pdf,
)


# ============================================================
# TAREFA DE GERAÇÃO DE PDF
#
# Este módulo NÃO altera componentes do Kivy.
# Ele apenas executa o cálculo em segundo plano.
#
# A interface será responsável por receber os callbacks
# e atualizar a tela através do Clock do Kivy.
# ============================================================


class TarefaPDF:

    def __init__(
        self,
        tonica,
        modo,
        vozes,
        notas,
        pasta_saida,
        ao_progresso=None,
        ao_concluir=None,
        ao_erro=None,
    ):
        self.tonica = tonica
        self.modo = modo
        self.vozes = vozes

        self.notas = list(
            notas
        )

        self.pasta_saida = (
            pasta_saida
        )

        self.ao_progresso = (
            ao_progresso
        )

        self.ao_concluir = (
            ao_concluir
        )

        self.ao_erro = (
            ao_erro
        )

        self.thread = None

        self.em_execucao = False


    # ========================================================
    # PROGRESSO
    # ========================================================

    def _progresso(
        self,
        atual,
        total,
        parte,
        total_partes,
    ):
        if self.ao_progresso:

            self.ao_progresso(
                atual,
                total,
                parte,
                total_partes,
            )


    # ========================================================
    # EXECUÇÃO INTERNA
    # ========================================================

    def _executar(
        self
    ):
        try:

            fluxo = (
                executar_calculo_e_pdf(
                    tonica=self.tonica,
                    modo=self.modo,
                    vozes=self.vozes,
                    notas=self.notas,
                    pasta_saida=self.pasta_saida,
                    callback_progresso=
                    self._progresso,
                )
            )

        except Exception as erro:

            self.em_execucao = False

            if self.ao_erro:

                self.ao_erro(
                    erro
                )

            return


        self.em_execucao = False

        if self.ao_concluir:

            self.ao_concluir(
                fluxo
            )


    # ========================================================
    # INICIAR THREAD
    # ========================================================

    def iniciar(
        self
    ):
        if self.em_execucao:

            raise RuntimeError(
                "A geração de PDF "
                "já está em andamento."
            )


        self.em_execucao = True


        self.thread = Thread(
            target=self._executar,
            name="GeradorPDF",
            daemon=True,
        )


        self.thread.start()


        return self.thread
