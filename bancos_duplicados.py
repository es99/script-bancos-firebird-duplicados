import os, sys, shutil
from datetime import datetime

sistemas_bancos = {
    'PJFolha': 'DBFOLHA',
    'PJCheque': 'DBCHEQUE',
    'PJDoacao': 'DBDOACAO',
    'PJEstoque': 'DBESTOQUE',
    'PJFrota': 'DBFROTA',
    'PJSuporte': 'PJSUPORTE',
    'PJTomb': 'DBTOMB',
    'PJTributos': 'DBTRIBUTOS'  
}

dbacesso = "DBACESSO"
pathArquivoMorto = 'C:\\Arquivo_morto'

def arquivo_duplicado(dir, filename):
    if filename.endswith('.FDB'):
        file, _ = os.path.splitext(filename)
        if file != sistemas_bancos[dir] and file != dbacesso:
            return True
    return False

def arquivo_morto():
    if not os.path.isdir(pathArquivoMorto):
        try:
            os.makedirs(pathArquivoMorto)
            return True
        except:
            return False
    else:
        return True


def geraRelatorio(arquivos, total):
    dataHoraAtual = datetime.now()
    kb = total / 1024
    MB = kb / 1024
    dataHoraAtual_texto = dataHoraAtual.strftime("%d-%m-%Y-%H-%M-%S")
    path = os.path.join(pathArquivoMorto, dataHoraAtual_texto + ".log")
    with open(path, 'w') as logFile:
        for file in arquivos:
            logFile.write(file + '\n')
        logFile.write("Tamanho total dos bancos duplicados: " + str(MB) + "MB" + "\n")
        logFile.write("="*30 + "fim do log" + "="*30)
    print("log gerado em: ", os.path.abspath(path))

def pesquisa_bancos_duplicados(diretorios):
    arquivos = []
    totalSize = 0
    for diretorio in diretorios:
        path = os.path.join(os.getcwd(), diretorio)
        for folderName, subfolders, filenames in os.walk(path):
            for filename in filenames:
                if arquivo_duplicado(diretorio, filename):
                    totalSize += os.path.getsize(os.path.join(folderName, filename))
                    arquivos.append(filename)
    if len(arquivos) == 0:
        print("Não existem arquivos duplicados de banco de dados, encerrando")
        sys.exit(1)
    else:
        geraRelatorio(arquivos=arquivos, total=totalSize)


if len(sys.argv) != 2:
    print("Deve-se passar um argumento que represente a unidade de disco a ser montada, ex: python c")
    sys.exit(1)
else:
    unidade = sys.argv[1]

unidade += ":\\"

if os.path.exists(unidade.upper()):
    print(f"A unidade {unidade} existe.")
    os.chdir(unidade)
else:
    print(f"{unidade} não existe, encerrando.")
    sys.exit(1)

if arquivo_morto():
    print("Arquivo morto criado ou já existente")
else:
    print("Por algum motivo não foi possível criar o arquivo morto.")
    sys.exit(1)

diretorios_infopublic = []

for filename in os.listdir():
    if os.path.isdir(filename) and filename.startswith('PJ'):
        diretorios_infopublic.append(filename)

pesquisa_bancos_duplicados(diretorios_infopublic)