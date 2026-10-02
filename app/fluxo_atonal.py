# -*- coding: utf-8 -*-

from pathlib import Path

from app.servico_atonal import (
    calcular_resultado_atonal,
)

from app.gerador_pdf_atonal import (
    gerar_pdfs_atonais,
)


# ============================================================
# FLUXO ATONAL
# ============================================================

def executar_calculo_e_pdf_atonal(
    vozes,
    notas,
    pasta_saida,
    callback_progresso=None,
):
    pasta_saida = Path(
        pasta_saida
    )

    resultado = calcular_resultado_atonal(
        notas=notas,
        vozes=vozes,
    )

    total = resultado[
        "total_combinacoes"
    ]

    if total <= 0:
        return {
            "sucesso": True,
            "pdf_gerado": False,
            "mensagem": "Nenhuma combinação ATONAL encontrada.",
            "resultado": resultado,
            "arquivos": [],
        }

    arquivos = gerar_pdfs_atonais(
        resultado,
        pasta_saida,
        callback_progresso=callback_progresso,
    )

    resumo_arquivos = []

    for arquivo in arquivos:
        resumo_arquivos.append(
            {
                "parte": arquivo["parte"],
                "total_partes": arquivo["total_partes"],
                "inicio": arquivo["inicio"],
                "fim": arquivo["fim"],
                "nome": arquivo.get(
                    "nome",
                    Path(str(arquivo["caminho"])).name,
                ),
                "caminho": arquivo["caminho"],
                "tamanho_bytes": arquivo.get(
                    "tamanho_bytes",
                    0,
                ),
                "destino_exibicao": arquivo.get(
                    "destino_exibicao"
                ),
            }
        )

    return {
        "sucesso": True,
        "pdf_gerado": True,
        "mensagem": (
            f"{len(resumo_arquivos)} PDF(s) ATONAL gerado(s)."
        ),
        "resultado": resultado,
        "arquivos": resumo_arquivos,
    }
