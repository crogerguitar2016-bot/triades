# -*- coding: utf-8 -*-

from threading import Thread

from app.fluxo_atonal import (
    executar_calculo_e_pdf_atonal,
)


class TarefaPDFAtonal:

    def __init__(
        self,
        vozes,
        notas,
        pasta_saida,
        ao_progresso=None,
        ao_concluir=None,
        ao_erro=None,
    ):
        self.vozes = vozes
        self.notas = list(
            notas
        )
        self.pasta_saida = pasta_saida

        self.ao_progresso = ao_progresso
        self.ao_concluir = ao_concluir
        self.ao_erro = ao_erro

        self.thread = None
        self.em_execucao = False

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

    def _executar(
        self
    ):
        try:
            fluxo = executar_calculo_e_pdf_atonal(
                vozes=self.vozes,
                notas=self.notas,
                pasta_saida=self.pasta_saida,
                callback_progresso=self._progresso,
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

    def iniciar(
        self
    ):
        if self.em_execucao:
            raise RuntimeError(
                "A geração de PDF ATONAL já está em andamento."
            )

        self.em_execucao = True

        self.thread = Thread(
            target=self._executar,
            name="GeradorPDFAtonal",
            daemon=True,
        )

        self.thread.start()

        return self.thread
