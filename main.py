from itertools import product
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

CAMPOS_HARMONICOS = {
    "C": {"C": ["C","E","G"], "Dm":["D","F","A"], "Em":["E","G","B"], "F":["F","A","C"], "G":["G","B","D"], "Am":["A","C","E"], "B°":["B","D","F"]},
    "G": {"G":["G","B","D"], "Am":["A","C","E"], "Bm":["B","D","F#"], "C":["C","E","G"], "D":["D","F#","A"], "Em":["E","G","B"], "F#°":["F#","A","C"]},
    "D": {"D":["D","F#","A"], "Em":["E","G","B"], "F#m":["F#","A","C#"], "G":["G","B","D"], "A":["A","C#","E"], "Bm":["B","D","F#"], "C#°":["C#","E","G"]},
    "A": {"A":["A","C#","E"], "Bm":["B","D","F#"], "C#m":["C#","E","G#"], "D":["D","F#","A"], "E":["E","G#","B"], "F#m":["F#","A","C#"], "G#°":["G#","B","D"]},
    "E": {"E":["E","G#","B"], "F#m":["F#","A","C#"], "G#m":["G#","B","D#"], "A":["A","C#","E"], "B":["B","D#","F#"], "C#m":["C#","E","G#"], "D#°":["D#","F#","A"]},
    "B": {"B":["B","D#","F#"], "C#m":["C#","E","G#"], "D#m":["D#","F#","A#"], "E":["E","G#","B"], "F#":["F#","A#","C#"], "G#m":["G#","B","D#"], "A#°":["A#","C#","E"]},
    "F#": {"F#":["F#","A#","C#"], "G#m":["G#","B","D#"], "A#m":["A#","C#","E#"], "B":["B","D#","F#"], "C#":["C#","E#","G#"], "D#m":["D#","F#","A#"], "E#°":["E#","G#","B"]},
    "F": {"F":["F","A","C"], "Gm":["G","Bb","D"], "Am":["A","C","E"], "Bb":["Bb","D","F"], "C":["C","E","G"], "Dm":["D","F","A"], "E°":["E","G","Bb"]},
    "Bb": {"Bb":["Bb","D","F"], "Cm":["C","Eb","G"], "Dm":["D","F","A"], "Eb":["Eb","G","Bb"], "F":["F","A","C"], "Gm":["G","Bb","D"], "A°":["A","C","Eb"]},
    "Eb": {"Eb":["Eb","G","Bb"], "Fm":["F","Ab","C"], "Gm":["G","Bb","D"], "Ab":["Ab","C","Eb"], "Bb":["Bb","D","F"], "Cm":["C","Eb","G"], "D°":["D","F","Ab"]},
    "Ab": {"Ab":["Ab","C","Eb"], "Bbm":["Bb","Db","F"], "Cm":["C","Eb","G"], "Db":["Db","F","Ab"], "Eb":["Eb","G","Bb"], "Fm":["F","Ab","C"], "G°":["G","Bb","Db"]},
    "Db": {"Db":["Db","F","Ab"], "Ebm":["Eb","Gb","Bb"], "Fm":["F","Ab","C"], "Gb":["Gb","Bb","Db"], "Ab":["Ab","C","Eb"], "Bbm":["Bb","Db","F"], "C°":["C","Eb","Gb"]}
}

ACORDES_AUMENTADOS = {
    "C+": ["C","E","G#"], "C#+": ["C#","F","A"], "D+": ["D","F#","A#"], "D#+": ["D#","G","B"],
    "E+": ["E","G#","B#"], "F+": ["F","A","C#"], "F#+": ["F#","A#","D"], "G+": ["G","B","D#"],
    "G#+": ["G#","C","E"], "A+": ["A","C#","F"], "A#+": ["A#","D","F#"], "B+": ["B","D#","G"],
    "Fb+": ["Fb","Ab","C"]
}

def normalize_note_input(s):
    s = s.strip().replace("♯", "#").replace("♭", "b")
    if not s: return s
    if len(s) == 1: return s.upper()
    return s[0].upper() + s[1:]

def escolher_pasta():
    candidatos = [
        "/sdcard/Download",
        "/storage/emulated/0/Download",
        "/sdcard/Downloads",
        os.path.expanduser("\~/storage/downloads"),
        os.path.expanduser("\~/Downloads"),
        "."
    ]
    for pasta in candidatos:
        if os.path.isdir(pasta) and os.access(pasta, os.W_OK):
            return pasta
    return "."

def main():
    print("=" * 50)
    print("      CAMPO HARMÔNICO - VERSÃO TERMINAL")
    print("      Professor: Carlos Rogério  |  C Roger")
    print("=" * 50)
    print()

    while True:
        texto = input("Digite as notas (ex: C, A, F# ou Bb) - ordem importa:\n> ").strip()
        if texto: break
        print("Você precisa digitar pelo menos uma nota.\n")

    notas_user = [normalize_note_input(n) for n in texto.split(",") if n.strip()]
    print(f"\nNotas recebidas: {', '.join(notas_user)}")

    print("\nCampos disponíveis:")
    keys = list(CAMPOS_HARMONICOS.keys()) + ["ATONAL"]
    for i, k in enumerate(keys, 1):
        print(f"  {i:2}. {k}")

    while True:
        escolha = input("\nEscolha o número do Campo Harmônico (ou digite o nome):\n> ").strip()
        if escolha.isdigit():
            idx = int(escolha) - 1
            if 0 <= idx < len(keys):
                campo_escolhido = keys[idx]
                break
        else:
            escolha_up = escolha.upper() if escolha.upper() != "ATONAL" else "ATONAL"
            encontrado = False
            for k in keys:
                if k.upper() == escolha_up or k == escolha:
                    campo_escolhido = k
                    encontrado = True
                    break
            if encontrado:
                break
            print("Opção inválida. Tente novamente.")

    print(f"\nCampo escolhido: {campo_escolhido}")

    nome = input("\nNome do arquivo PDF (deixe em branco para automático):\n> ").strip()
    if not nome:
        nome = f"Campo_Harmonico_{campo_escolhido}"
    nome = nome.replace("/", "_").replace("\\", "_")
    if not nome.lower().endswith(".pdf"):
        nome += ".pdf"

    colunas = []

    if campo_escolhido == "ATONAL":
        todos_acordes = []
        for campo in CAMPOS_HARMONICOS.values():
            for acorde, notas_acorde in campo.items():
                if (acorde, notas_acorde) not in todos_acordes:
                    todos_acordes.append((acorde, notas_acorde))
        for acorde, notas_acorde in ACORDES_AUMENTADOS.items():
            if (acorde, notas_acorde) not in todos_acordes:
                todos_acordes.append((acorde, notas_acorde))

        for nota in notas_user:
            coluna = []
            for acorde, notas_acorde in todos_acordes:
                if nota in notas_acorde and acorde not in coluna:
                    coluna.append(acorde)
            colunas.append(coluna)
    else:
        campo = CAMPOS_HARMONICOS.get(campo_escolhido)
        if not campo:
            print(f"Erro: Campo {campo_escolhido} não encontrado.")
            return

        for nota in notas_user:
            raizes, terceiras, quintas = [], [], []
            for acorde, notas_acorde in campo.items():
                if len(notas_acorde) >= 1 and nota == notas_acorde[0]:
                    raizes.append(acorde)
                elif len(notas_acorde) >= 2 and nota == notas_acorde[1]:
                    terceiras.append(acorde)
                elif len(notas_acorde) >= 3 and nota == notas_acorde[2]:
                    quintas.append(acorde)
            coluna = []
            for lst in (raizes, terceiras, quintas):
                for a in lst:
                    if a not in coluna:
                        coluna.append(a)
            colunas.append(coluna)

    for idx, col in enumerate(colunas):
        if not col:
            print(f"\nNenhum acorde encontrado para a nota {notas_user[idx]}.")
            return

    combinacoes = list(product(*colunas))
    print(f"\nTotal de combinações: {len(combinacoes)}")

    pasta_destino = escolher_pasta()
    caminho_pdf = os.path.join(pasta_destino, nome)

    try:
        c = canvas.Canvas(caminho_pdf, pagesize=A4)
        largura, altura = A4
        y = altura - 50

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "PROFESSOR: CARLOS ROGÉRIO")
        c.setFont("Helvetica-Bold", 14)
        c.drawString(300, y, "C ROGER")
        y -= 30

        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Campo Harmônico: {campo_escolhido}")
        y -= 20
        c.drawString(50, y, f"Notas digitadas: {', '.join(notas_user)}")
        y -= 25

        c.setFont("Helvetica", 10)
        for i, nota in enumerate(notas_user, start=1):
            col = colunas[i-1]
            descr = f"Col {i} ({nota}): " + " | ".join(col)
            c.drawString(50, y, descr)
            y -= 14
            if y < 70:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = altura - 50

        y -= 6
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Combinações:")
        y -= 18
        c.setFont("Helvetica", 10)

        for idx, comb in enumerate(combinacoes, start=1):
            linha = f"{idx}. {' - '.join(comb)}"
            c.drawString(50, y, linha)
            y -= 14
            if y < 60:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = altura - 50

        c.save()
        print("\n" + "=" * 50)
        print("PDF gerado com sucesso!")
        print(f"Arquivo: {caminho_pdf}")
        print("=" * 50)

    except Exception as e:
        print(f"\nErro ao salvar o PDF: {e}")
        print("Tente rodar o programa em outra pasta ou verifique as permissões.")

if __name__ == "__main__":
    main()
