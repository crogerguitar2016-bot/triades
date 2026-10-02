# -*- coding: utf-8 -*-

"""
Armazenamento e proteção de recursos para os PDFs.

ANDROID:
- os PDFs são gerados primeiro na pasta privada do aplicativo;
- depois são publicados em Download/Harmonizador via MediaStore;
- o arquivo temporário privado é removido após a publicação;
- a cópia para o MediaStore é feita em blocos, sem carregar o PDF inteiro na RAM.

UBUNTU / X11:
- mantém a saída de testes em projeto/pdf_gerados.
"""

import gc
import os
import shutil
from pathlib import Path

from kivy.utils import platform


DESTINO_PUBLICO_ANDROID = "Download/Harmonizador"
RESERVA_CRITICA_BYTES = 64 * 1024 * 1024  # 64 MiB
TAMANHO_BLOCO_COPIA = 1024 * 1024          # 1 MiB


# ============================================================
# PASTA TEMPORÁRIA / PASTA DE TESTE
# ============================================================

def obter_pasta_saida_pdf():
    """
    Retorna uma pasta de sistema de arquivos para o ReportLab.

    No Android, esta pasta é privada e funciona como área temporária.
    Depois que cada PDF é fechado, ele é publicado em
    Download/Harmonizador e o temporário é apagado.
    """
    if platform == "android":
        from kivy.app import App

        app = App.get_running_app()

        if app is None:
            raise RuntimeError(
                "Aplicativo Android ainda não foi inicializado."
            )

        pasta = Path(app.user_data_dir) / "pdf_gerados_temporarios"

    else:
        base = (
            Path(__file__)
            .resolve()
            .parent
            .parent
        )
        pasta = base / "pdf_gerados"

    pasta.mkdir(
        parents=True,
        exist_ok=True,
    )

    return pasta


# ============================================================
# DESTINO MOSTRADO AO USUÁRIO
# ============================================================

def obter_destino_exibicao_pdf():
    if platform == "android":
        return DESTINO_PUBLICO_ANDROID

    return str(
        obter_pasta_saida_pdf()
    )


# ============================================================
# ESPAÇO LIVRE
# ============================================================

def _pasta_para_medicao_espaco(pasta_referencia=None):
    if pasta_referencia is not None:
        pasta = Path(pasta_referencia)
        pasta.mkdir(
            parents=True,
            exist_ok=True,
        )
        return pasta

    return obter_pasta_saida_pdf()


def obter_espaco_livre_bytes(pasta_referencia=None):
    pasta = _pasta_para_medicao_espaco(
        pasta_referencia
    )

    return shutil.disk_usage(
        str(pasta)
    ).free


def verificar_espaco_para_pdf(
    pasta_referencia=None,
    reserva_minima_bytes=RESERVA_CRITICA_BYTES,
):
    """
    Não limita a quantidade de combinações.
    Apenas interrompe quando o armazenamento já está criticamente baixo.
    """
    livre = obter_espaco_livre_bytes(
        pasta_referencia
    )

    if livre < reserva_minima_bytes:
        livre_mb = livre / (1024 * 1024)
        minimo_mb = reserva_minima_bytes / (1024 * 1024)

        raise RuntimeError(
            "Espaço de armazenamento criticamente baixo. "
            f"Livre: {livre_mb:.1f} MB. "
            f"Reserve pelo menos {minimo_mb:.0f} MB e tente novamente."
        )

    return livre


# ============================================================
# MEMÓRIA
# ============================================================

def manutencao_memoria():
    """
    Libera objetos Python alcançáveis pelo coletor e, no Android,
    verifica se o próprio sistema já sinalizou estado de pouca memória.

    A quantidade de combinações nunca é usada para bloquear a geração.
    """
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
        ActivityManagerMemoryInfo = autoclass(
            "android.app.ActivityManager$MemoryInfo"
        )

        activity = PythonActivity.mActivity
        manager = activity.getSystemService(
            Context.ACTIVITY_SERVICE
        )

        info = ActivityManagerMemoryInfo()
        manager.getMemoryInfo(info)

        if bool(info.lowMemory):
            disponivel_mb = (
                int(info.availMem)
                / (1024 * 1024)
            )

            raise MemoryError(
                "O Android informou memória criticamente baixa "
                "durante a geração do PDF. "
                f"Memória disponível aproximada: {disponivel_mb:.0f} MB. "
                "A geração foi interrompida antes que o sistema "
                "encerrasse o aplicativo. Feche outros aplicativos "
                "e tente novamente."
            )

    except MemoryError:
        raise

    except Exception:
        # A proteção de memória é complementar. Se a consulta ao Android
        # não estiver disponível em algum aparelho, a geração continua.
        return False

    return False


# ============================================================
# PUBLICAÇÃO NO DOWNLOAD/HARMONIZADOR
# ============================================================

def _publicar_android_mediastore(caminho):
    from jnius import autoclass

    PythonActivity = autoclass(
        "org.kivy.android.PythonActivity"
    )
    ContentValues = autoclass(
        "android.content.ContentValues"
    )
    MediaStoreDownloads = autoclass(
        "android.provider.MediaStore$Downloads"
    )
    MediaStoreMediaColumns = autoclass(
        "android.provider.MediaStore$MediaColumns"
    )
    BuildVersion = autoclass(
        "android.os.Build$VERSION"
    )
    JavaInteger = autoclass(
        "java.lang.Integer"
    )

    activity = PythonActivity.mActivity
    resolver = activity.getContentResolver()

    # Android 10+ (API 29+): Scoped Storage / MediaStore.
    if int(BuildVersion.SDK_INT) >= 29:
        values = ContentValues()

        values.put(
            MediaStoreMediaColumns.DISPLAY_NAME,
            caminho.name,
        )
        values.put(
            MediaStoreMediaColumns.MIME_TYPE,
            "application/pdf",
        )
        values.put(
            MediaStoreMediaColumns.RELATIVE_PATH,
            DESTINO_PUBLICO_ANDROID,
        )
        values.put(
            MediaStoreMediaColumns.IS_PENDING,
            JavaInteger.valueOf(1),
        )

        uri = resolver.insert(
            MediaStoreDownloads.EXTERNAL_CONTENT_URI,
            values,
        )

        if uri is None:
            raise RuntimeError(
                "O Android não conseguiu criar o PDF em "
                f"{DESTINO_PUBLICO_ANDROID}."
            )

        saida = None

        try:
            saida = resolver.openOutputStream(
                uri,
                "w",
            )

            if saida is None:
                raise RuntimeError(
                    "Não foi possível abrir o destino do PDF "
                    "no armazenamento do Android."
                )

            with caminho.open("rb") as origem:
                while True:
                    bloco = origem.read(
                        TAMANHO_BLOCO_COPIA
                    )

                    if not bloco:
                        break

                    # PyJNIus converte bytes/bytearray para byte[].
                    try:
                        saida.write(bloco)
                    except Exception:
                        saida.write(
                            bytearray(bloco)
                        )

            saida.flush()
            saida.close()
            saida = None

            liberar = ContentValues()
            liberar.put(
                MediaStoreMediaColumns.IS_PENDING,
                JavaInteger.valueOf(0),
            )

            resolver.update(
                uri,
                liberar,
                None,
                None,
            )

            return str(uri)

        except Exception:
            try:
                if saida is not None:
                    saida.close()
            except Exception:
                pass

            try:
                resolver.delete(
                    uri,
                    None,
                    None,
                )
            except Exception:
                pass

            raise

    # Android 9 ou anterior: gravação direta, compatível com a permissão
    # WRITE_EXTERNAL_STORAGE já existente no projeto.
    pasta_download = Path(
        "/storage/emulated/0/Download/Harmonizador"
    )
    pasta_download.mkdir(
        parents=True,
        exist_ok=True,
    )

    destino = pasta_download / caminho.name

    with caminho.open("rb") as origem:
        with destino.open("wb") as saida:
            shutil.copyfileobj(
                origem,
                saida,
                length=TAMANHO_BLOCO_COPIA,
            )

    return str(destino)


def publicar_pdf_gerado(caminho_pdf):
    """
    Publica um PDF finalizado e retorna seus metadados.

    No Android, o arquivo temporário é excluído somente depois de a
    publicação pública ter sido concluída com sucesso.
    """
    caminho = Path(
        caminho_pdf
    )

    if not caminho.exists():
        raise FileNotFoundError(
            f"PDF temporário não encontrado: {caminho}"
        )

    tamanho_bytes = caminho.stat().st_size

    verificar_espaco_para_pdf(
        caminho.parent
    )

    if platform == "android":
        destino = _publicar_android_mediastore(
            caminho
        )

        # O PDF já está em Download/Harmonizador. A cópia privada não é
        # necessária e ocuparia espaço em dobro.
        try:
            caminho.unlink()
        except FileNotFoundError:
            pass

        return {
            "nome": caminho.name,
            "caminho": destino,
            "tamanho_bytes": tamanho_bytes,
            "destino_exibicao": DESTINO_PUBLICO_ANDROID,
        }

    return {
        "nome": caminho.name,
        "caminho": str(caminho),
        "tamanho_bytes": tamanho_bytes,
        "destino_exibicao": str(caminho.parent),
    }
