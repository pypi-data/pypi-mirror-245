import os.path
import gspread
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class Ficha:
    def __init__(self, token_path, url):
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        sheet_id = gspread.utils.extract_id_from_url(url)
        
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        client = gspread.authorize(creds)
        sheet = build("sheets", "v4", credentials=creds).spreadsheets()
        
        self.ficha_pessoal = FichaPessoal(sheet, client, sheet_id)
        self.reg_e_inv = RegistroEInventario(sheet, client, sheet_id)
        self.perf_amald = PerfilAmaldicoado(sheet, client, sheet_id)
        self.invocacoes = Invocacoes(sheet, client, sheet_id)


class FichaPessoal:
    def __init__(self, sheet, client, sheet_id):
        tabela = "Ficha Pessoal!"
        self.sheet = sheet
        self.client = client
        self.sheet_id = sheet_id
        self.pl = None
        self.tudo = tabela + "A1:BQ44"
        self.nome = tabela + "F3"
        self.nivel = tabela + "V3"
        self.maestria = tabela + "V4"
        self.exp = tabela + "V5"
        self.origem = tabela + "AH3"
        self.especializacao = tabela + "AH4"
        self.tecnica = tabela + "AH5"
        self.jogador = tabela + "AU3"
        self.campanha = tabela + "AU4"
        self.grau = tabela + "AU5"
        self.atencao = tabela + "AM15"
        self.iniciativa = tabela + "AP15"
        self.movimento = tabela + "AS15"
        self.ca = tabela + "AW9"
        self.caracteristicas = tabela + "AC32"
        self.forca = tabela + "G12"
        self.destreza = tabela + "G14"
        self.constituicao = tabela + "G16"
        self.inteligencia = tabela + "T12"
        self.sabedoria = tabela + "T14"
        self.carisma = tabela + "T16"
        self.mod_forca = tabela + "K12"
        self.mod_destreza = tabela + "K14"
        self.mod_constituicao = tabela + "K16"
        self.mod_inteligencia = tabela + "X12"
        self.mod_sabedoria = tabela + "X14"
        self.mod_carisma = tabela + "X16"
        self.vida_atual = tabela + "AC7"
        self.vida_maximo = tabela + "AF7"
        self.vida_temporario = tabela + "AI7"
        self.alma_atual = tabela + "AM7"
        self.alma_maximo = tabela + "AP7"
        self.alma_temporario = tabela + "AS7"
        self.energia_atual = tabela + "AC15"
        self.energia_maximo = tabela + "AF15"
        self.energia_temporario = tabela + "AI15"
        self.maestrias = tabela + "AW31:AW36"
        self.registro_rapido = tabela + "AC26:AS29"
        self.habilidades_de_especializacao = tabela + "BF5:BF29"
        self.talentos = tabela + "BF34:BF43"
        self.atletismo = tabela + "L22"			
        self.luta = tabela + "L23"			
        self.acrobacia = tabela + "L24"			
        self.furtividade = tabela + "L25"			
        self.pontaria = tabela + "L26"			
        self.prestidigitacao = tabela + "L27"			
        self.reflexos = tabela + "L28"			
        self.fortitude = tabela + "L29"			
        self.integridade = tabela + "L30"			
        self.intuicao = tabela + "L31"			
        self.medicina = tabela + "L32"			
        self.percepcao = tabela + "L33"			
        self.ocultismo = tabela + "L34"
        self.astucia = tabela + "Z22"
        self.feiticaria = tabela + "Z23"
        self.investigacao = tabela + "Z24"
        self.historia = tabela + "Z25"
        self.oficio1 = tabela + "Z26"
        self.oficio2 = tabela + "Z27"
        self.oficio3 = tabela + "Z28"
        self.religiao = tabela + "Z29"
        self.persuasao = tabela + "Z30"
        self.enganacao = tabela + "Z31"
        self.intimidacao = tabela + "Z32"
        self.performance = tabela + "Z33"
        self.vontade = tabela + "Z34"
    
    def get(self):
        result = (
          self.sheet.values()
          .get(spreadsheetId=self.sheet_id, range=self.tudo)
          .execute()
        )
        values = result.get("values",  [])
        self.pl = pl = self.client.open_by_key(self.sheet_id).get_worksheet(0)
        
        self.tudo = values
        self.nome = values[2][5]
        self.nivel = values[2][21]
        self.maestria = values[3][21]
        self.exp = values[4][21]
        self.origem = values[2][33]
        self.especializacao = values[3][33]
        self.tecnica = values[4][33]
        self.jogador = values[2][-1]
        self.campanha = values[3][46]
        self.grau = values[4][46]
        self.atencao = values[14][38]
        self.iniciativa = values[14][41]
        self.movimento = values[14][44]
        self.ca = values[8][48]
        self.caracteristicas = values[31][28]
        self.forca = values[11][6]
        self.destreza = values[13][12]
        self.constituicao = values[15][6]
        self.inteligencia = values[11][19]
        self.sabedoria = values[13][19]
        self.carisma = values[15][19]
        self.mod_forca = values[11][10]
        self.mod_destreza = values[13][10]
        self.mod_constituicao = values[15][10]
        self.mod_inteligencia = values[11][23]
        self.mod_sabedoria = values[13][23]
        self.mod_carisma = values[15][23]
        self.vida_atual = values[6][28]
        self.vida_maximo = values[6][31]
        self.vida_temporario = values[6][34]
        self.alma_atual = values[6][38]
        self.alma_maximo = values[6][41]
        self.alma_temporario = values[6][44]
        self.energia_atual = values[14][28]
        self.energia_maximo = values[14][31]
        self.energia_temporario = values[14][34]
        self.maestrias = [values[i][48] for i in range(30, 36) if values[i][48] != ""]#[values[30][48], values[31][48], values[32][48], values[33][48], values[34][48], values[35][48]]
        self.registro_rapido = [
          {"arma": values[i][28],
          "bonus": values[i][32],
          "dano": values[i][34],
          "critico": values[i][38],
          "tipo": values[i][41],
          "alcance": values[i][44]
          } for i in range(25, 29) if all([c < len(values[i]) for c in [28, 32, 34, 38, 41, 44]]) and values[i][28] != ""
          ]
        
        self.habilidades_de_especializacao = [(values[i][57], pl.get_note(n)) for i, n in [(c, f"BF{c+1}") for c in range(4, 29)] if values[i][57] != ""]
        self.talentos = [(values[i][57], pl.get_note(n)) for i, n in [(c, f"BF{c+1}") for c in range(33,43)] if values[i][57] != ""]
        self.atletismo = values[21][11]
        self.luta = values[22][11]
        self.acrobacia = values[23][11]
        self.furtividade = values[24][11]
        self.pontaria = values[25][11]
        self.prestidigitacao = values[26][11]
        self.reflexos = values[27][11]
        self.fortitude = values[28][11]
        self.integridade = values[29][11]
        self.intuicao = values[30][11]
        self.medicina = values[31][11]
        self.percepcao = values[32][11]
        self.ocultismo = values[33][11]
        self.astucia = values[21][25]
        self.feiticaria = values[22][25]
        self.investigacao = values[23][25]
        self.historia = values[24][25]
        self.oficio1 = values[25][25]
        self.oficio2 = values[26][25]
        self.oficio3 = values[27][25]
        self.religiao = values[28][25]
        self.persuasao = values[29][25]
        self.enganacao = values[30][25]
        self.intimidacao = values[31][25]
        self.performance = values[32][25]
        self.vontade = values[33][25]


class RegistroEInventario:
    def __init__(self, sheet, client, sheet_id):
        tabela = "Registro e Inventário!"
        self.sheet = sheet
        self.client = client
        self.sheet_id = sheet_id
        self.pl = None
        self.tudo = tabela + "A1:BQ31"
        self.nome = tabela + "E2"
        self.aparencia = tabela + "B5"
        self.idade = tabela + "N4"
        self.altura = tabela + "N5"
        self.peso = tabela + "N6"
        self.genero = tabela + "N7"
        self.cabelos = tabela + "N8"
        self.olhos = tabela + "N9"
        self.pele = tabela + "N10"
        self.aura = tabela + "N11"
        self.roupas = tabela + "N12"
        self.tamanho = tabela + "N13"
        self.marcas = tabela + "N14"
        self.tracos_de_personalidade = tabela + "B16"
        self.ideais = tabela + "B20"
        self.ligacoes = tabela + "B24"
        self.defeitos = tabela + "B28"
        self.inv = tabela + "V5:BA28"
        self.espacos_ocupados = tabela + "AF30"
        self.limite_de_espacos = tabela + "AW30"
        self.historia_do_personagem = tabela + "BD4"
        
    def get(self):
        result = (
          self.sheet.values()
          .get(spreadsheetId=self.sheet_id, range=self.tudo)
          .execute()
        )
        values = result.get("values",  [])
        self.pl = pl = self.client.open_by_key(self.sheet_id).get_worksheet(1)
        
        self.tudo = values
        self.nome = values[1][4] if 14 < len(values[1]) else ""
        self.aparencia = values[4][1] if 1 < len(values[4]) else ""
        self.aparencia = self.aparencia if self.aparencia != "" else pl.acell('B5', value_render_option='FORMULA').value.replace("'", '"')
        self.aparencia = self.aparencia if "IMAGE" not in self.aparencia else self.aparencia[self.aparencia.find('"')+1:self.aparencia.rfind('"')]
        self.idade = values[3][13] if 13 < len(values[3]) else ""
        self.altura = values[4][13] if 13 < len(values[4]) else ""
        self.peso = values[5][13] if 13 < len(values[5]) else ""
        self.genero = values[6][13] if 13 < len(values[6]) else ""
        self.cabelos = values[7][13] if 13 < len(values[7]) else ""
        self.olhos = values[8][13] if 13 < len(values[8]) else ""
        self.pele = values[9][13] if 13 < len(values[9]) else ""
        self.aura = values[10][13] if 13 < len(values[10]) else ""
        self.roupas = values[11][13] if 13 < len(values[11]) else ""
        self.tamanho = values[12][13] if 13 < len(values[12]) else ""
        self.marcas = values[13][13] if 13 < len(values[13]) else ""
        self.tracos_de_personalidade = values[15][1] if 1 < len(values[15]) else ""
        self.ideais = values[19][1] if 1 < len(values[19]) else ""
        self.ligacoes = values[23][1] if 1 < len(values[23]) else ""
        self.defeitos = values[27][1] if 1 < len(values[27]) else ""
        inv_col1 = [
            {
                "item": values[i][21],
                "nota": pl.get_note(f"V{i+1}"),
                "quantidade": values[i][31],
                "espacos": values[i][33],
                "custo": values[i][35]
            } for i in range(4, 28) if all([c < len(values[i]) for c in [21, 31, 33, 35]]) and values[i][21] != ""
        ]
        inv_col2 = [
            {
                "item": values[i][38],
                "nota": pl.get_note(f"AM{i+1}"),
                "quantidade": values[i][48],
                "espacos": values[i][50],
                "custo": values[i][52]
            } for i in range(4, 28) if all([c < len(values[i]) for c in [38, 48, 50, 52]]) and values[i][38] != ""
        ]
        self.inv = inv_col1 + inv_col2
        self.espacos_ocupados = values[29][31] if 31 < len(values[29]) else ""
        self.limite_de_espacos = values[29][48] if 48 < len(values[29]) else ""
        self.historia_do_personagem = values[3][55] if 55 < len(values[3]) else ""


class PerfilAmaldicoado:
    def __init__(self, sheet, client, sheet_id):
        tabela = "Perfil Amaldiçoado!"
        self.sheet = sheet
        self.client = client
        self.sheet_id = sheet_id
        self.pl = None
        self.tudo = tabela + "A1:BJ33"
        self.habilidades_conhecidas = tabela + "F4"
        self.habilidades_maximas = tabela + "F6"
        self.atributo_principal = tabela + "B10"
        self.nome_da_tecnica = tabela + "B15"
        self.descricao_da_tecnica = tabela + "B18"
        self.energia_atual = tabela + "I4"
        self.energia_maximo = tabela + "L4"
        self.energia_temporario = tabela + "O4"
        self.habilidades_amaldicoadas = tabela + "S7:S31"
        self.tecnicas_nv0 = tabela + "AD5:AD14"
        self.tecnicas_nv1 = tabela + "AM5:AM14"
        self.tecnicas_nv2 = tabela + "AV5:AV14"
        self.tecnicas_nv3 = tabela + "AD16:AD25"
        self.tecnicas_nv4 = tabela + "AM16:AM25"
        self.tecnicas_nv5 = tabela + "AV16:AV25"
        self.cd_tecnica = tabela + "BF3"
        self.bonus_acerto = tabela + "BF8"
        
        
    def get(self):
        result = (
          self.sheet.values()
          .get(spreadsheetId=self.sheet_id, range=self.tudo)
          .execute()
        )
        values = result.get("values",  [])
        self.pl = pl = self.client.open_by_key(self.sheet_id).get_worksheet(2)
        
        self.tudo = values
        self.habilidades_conhecidas = values[3][5]
        self.habilidades_maximas = values[5][5]
        self.atributo_principal = values[9][1]
        self.nome_da_tecnica = values[14][1]
        self.descricao_da_tecnica = values[17][1]
        self.energia_atual = values[3][8]
        self.energia_maximo = values[3][11]
        self.energia_temporario = values[3][14]
        self.habilidades_amaldicoadas = [(values[i][18], pl.get_note(f"S{i+1}")) for i in range(6, 31) if values[i][18] != ""]
        self.tecnicas_nv0 = [(values[i][29], pl.get_note(f"AD{i+1}")) for i in range(4, 14) if 29 < len(values[i]) and values[i][29] != ""]
        self.tecnicas_nv1 = [(values[i][38], pl.get_note(f"AM{i+1}")) for i in range(4, 14) if 38 < len(values[i]) and values[i][38] != ""]
        self.tecnicas_nv2 = [(values[i][47], pl.get_note(f"AV{i+1}")) for i in range(4, 14) if 47 < len(values[i]) and values[i][47] != ""]
        self.tecnicas_nv3 = [(values[i][29], pl.get_note(f"AD{i+1}")) for i in range(15, 25) if 29 < len(values[i]) and values[i][29] != ""]
        self.tecnicas_nv4 = [(values[i][38], pl.get_note(f"AM{i+1}")) for i in range(15, 25) if 38 < len(values[i]) and values[i][38] != ""]
        self.tecnicas_nv5 = [(values[i][47], pl.get_note(f"AV{i+1}")) for i in range(15, 25) if 47 < len(values[i]) and values[i][47] != ""]
        self.cd_tecnica = values[2][57] if 57 < len(values[2]) else None
        self.bonus_acerto = values[7][57] if 57 < len(values[7]) else None
        

class Invocacao:
    def __init__(self, values, pl):
        self.nome = values[0][1]
        if len(values[2]) == 0:
            self.vida = None
            self.ca = None
            self.movimento = None
            self.forca = None
            self.destreza = None
            self.constituicao = None
            self.inteligencia = None
            self.sabedoria = None
            self.carisma = None
            self.mod_forca = None
            self.mod_destreza = None
            self.mod_constituicao = None
            self.mod_inteligencia = None
            self.mod_sabedoria = None
            self.mod_carisma = None
            self.acoes = None
            self.pericias = None
        
        else:
            self.vida = values[2][3]
            self.ca = values[2][6]
            self.movimento = values[2][9]
            self.forca = values[9][6]
            self.destreza = values[10][6]
            self.constituicao = values[11][6]
            self.inteligencia = values[12][6]
            self.sabedoria = values[13][6]
            self.carisma = values[14][6]
            self.mod_forca = values[9][9]
            self.mod_destreza = values[10][9]
            self.mod_constituicao = values[11][9]
            self.mod_inteligencia = values[12][9]
            self.mod_sabedoria = values[13][9]
            self.mod_carisma = values[14][9]
            acoes_col1 = [(values[i][2], pl.get_note(f"C{i+5}")) for i in range(16, 21) if 2 < len(values[i]) and values[i][2] != ""]
            acoes_col2 = [(values[i][8], pl.get_note(f"I{i+5}")) for i in range(16, 21) if 8 < len(values[i]) and values[i][8] != ""]
            self.acoes = acoes_col1 + acoes_col2
            self.pericias = [
                {
                    "nome": values[i][3],
                    "atributo": values[i][7],
                    "bonus": values[i][9]
                } for i in range(23, 35) if i < len(values) and all([c < len(values[i]) for c in [3, 7, 9]]) and values[i][3] != ""
            ]


class Invocacoes:
    def __init__(self, sheet, client, sheet_id):
        tabela = "Shikigamis/Corpos Amaldiçoados!"
        self.sheet = sheet
        self.client = client
        self.sheet_id = sheet_id
        self.pl = None
        self.tudo = tabela + "A1:BS75"
        self.tipo = tabela + "B2"
        self.invocacoes = ["A5:O39", "O5:AC39", "AC5:AQ39", "AQ5:BE39", "BE5:BS39", "A41:O75", "O41:AC75", "AC41:AQ75", "AQ41:BE75", "BE41:BS75"]
    
    def get(self):
        result = (
          self.sheet.values()
          .get(spreadsheetId=self.sheet_id, range=self.tipo)
          .execute()
        )
        values = result.get("values",  [])
        self.pl = pl = self.client.open_by_key(self.sheet_id).get_worksheet(3)
        
        self.tipo = values[0][0]
        self.invocacoes = [Invocacao(values, pl) for values in pl.batch_get(self.invocacoes) if not len(values[2]) == 0]
        
