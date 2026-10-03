# -*- coding: utf-8 -*-

"""
Armazenamento dos PDFs.

ANDROID:
- espelhado no método comprovadamente funcional do commit
  44296cce241163c94cbe718e1b8cc16419a36ee1;
- grava diretamente em /storage/emulated/0/Download;
- não usa MediaStore;
- não usa ContentValues;
- não usa JavaString/JavaInteger;
- não copia o arquivo depois;
- o ReportLab já cria o PDF diretamente na pasta pública.

UBUNTU / X11:
- mantém a pasta local pdf_gerados para testes.
"""

import gc
import os
import shutil
from pathlib import Path

from kivy.utils import platform


PASTA_DOWNLOAD_ANDROID = os.path.join(
    "/storage/emulated/0",
    "Download"
)

PASTA_DESTINO_ANDROID = os.path.join(
    PASTA_DOWNLOAD_ANDROID,
    "Harmonia Ensaio de Harmonia Avançada"
)

DESTINO_PUBLICO_ANDROID = (
    "Download/Harmonia Ensaio de Harmonia Avançada"
)

RESERVA_CRITICA_BYTES = (
    64 * 1024 * 1024
)


# ============================================================
# PASTA DE SAÍDA
# ============================================================

def obter_pasta_saida_pdf():
    """
    No Android devolve diretamente a mesma pasta pública usada
    pela versão funcional antiga.

    O ReportLab grava o PDF diretamente nela.
    """

    if platform == "android":

        os.makedirs(
            PASTA_DESTINO_ANDROID,
            exist_ok=True,
        )

        return Path(
            PASTA_DESTINO_ANDROID
        )

    base = (
        Path(__file__)
        .resolve()
        .parent
        .parent
    )

    pasta = (
        base
        / "pdf_gerados"
    )

    pasta.mkdir(
        parents=True,
        exist_ok=True,
    )

    return pasta


# ============================================================
# DESTINO MOSTRADO NA INTERFACE
# ============================================================

def obter_destino_exibicao_pdf():

    if platform == "android":
        return (
            DESTINO_PUBLICO_ANDROID
        )

    return str(
        obter_pasta_saida_pdf()
    )


# ============================================================
# ESPAÇO LIVRE
# ============================================================

def _pasta_para_medicao_espaco(
    pasta_referencia=None
):

    if pasta_referencia is not None:

        pasta = Path(
            pasta_referencia
        )

        pasta.mkdir(
            parents=True,
            exist_ok=True,
        )

        return pasta

    return obter_pasta_saida_pdf()


def obter_espaco_livre_bytes(
    pasta_referencia=None
):

    pasta = (
        _pasta_para_medicao_espaco(
            pasta_referencia
        )
    )

    return shutil.disk_usage(
        str(pasta)
    ).free


def verificar_espaco_para_pdf(
    pasta_referencia=None,
    reserva_minima_bytes=
    RESERVA_CRITICA_BYTES,
):

    livre = (
        obter_espaco_livre_bytes(
            pasta_referencia
        )
    )

    if livre < reserva_minima_bytes:

        livre_mb = (
            livre
            / (1024 * 1024)
        )

        minimo_mb = (
            reserva_minima_bytes
            / (1024 * 1024)
        )

        raise RuntimeError(
            "Espaço de armazenamento "
            "criticamente baixo. "
            f"Livre: {livre_mb:.1f} MB. "
            f"Reserve pelo menos "
            f"{minimo_mb:.0f} MB."
        )

    return livre


# ============================================================
# MEMÓRIA
# ============================================================

def manutencao_memoria():

    gc.collect()

    if platform != "android":
        return False

    try:
        from jnius import autoclass

        PythonActivity = autoclass(
            "org.kivy.android.PythonActivity"
        )

        Context = autoclass(
            "android.content.Context"
        )

        MemoryInfo = autoclass(
            "android.app.ActivityManager$MemoryInfo"
        )

        activity = (
            PythonActivity.mActivity
        )

        manager = (
            activity.getSystemService(
                Context.ACTIVITY_SERVICE
            )
        )

        info = MemoryInfo()

        manager.getMemoryInfo(
            info
        )

        if bool(info.lowMemory):

            disponivel_mb = (
                int(info.availMem)
                / (1024 * 1024)
            )

            raise MemoryError(
                "O Android informou memória "
                "criticamente baixa. "
                f"Disponível: "
                f"{disponivel_mb:.0f} MB."
            )

    except MemoryError:
        raise

    except Exception:
        return False

    return False


# ============================================================
# PUBLICAÇÃO
#
# Na versão antiga não existia publicação/cópia.
# O PDF já era criado diretamente no Download.
#
# Esta função permanece apenas para compatibilidade com os
# geradores modulares atuais.
# ============================================================

def publicar_pdf_gerado(
    caminho_pdf
):

    caminho = Path(
        caminho_pdf
    )

    if not caminho.exists():

        raise FileNotFoundError(
            "PDF não encontrado após "
            f"a geração: {caminho}"
        )

    tamanho_bytes = (
        caminho.stat().st_size
    )

    return {
        "nome": caminho.name,
        "caminho": str(caminho),
        "tamanho_bytes": tamanho_bytes,
        "destino_exibicao": (
            DESTINO_PUBLICO_ANDROID
            if platform == "android"
            else str(caminho.parent)
        ),
    }
