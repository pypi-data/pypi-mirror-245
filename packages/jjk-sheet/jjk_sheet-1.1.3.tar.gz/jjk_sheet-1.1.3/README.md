# jjk_sheet

**jjk_sheet** é uma biblioteca para a obtenção de dados de uma [ficha](https://docs.google.com/spreadsheets/d/1txN7cAC2WXbPeq5nRSgI-k4hjtBLbEI2KUr61RMuul4/)
do rpg [Feiticeiros e Maldições](https://drive.google.com/file/d/172OB3Pz7-o9BFateI3BEdRiBllpbx34w/view).

---

# Uso

Primeiro será instanciada a ficha passando caminho para o arquivo
`json` que contenha suas credencias do google obtidas [aqui](https://console.cloud.google.com/).

```py
from jjk_sheet import Ficha

ficha = Ficha("your_token_file.json", "https://url.para.sua.ficha/")
```
Com a ficha instanciada agora podemos acessar os dados das tabelas
da sua planilha no GoogleSheets.

---

### Ficha Pessoal

Exemplo para pegar dados da tabela:
```py
ficha.ficha_pessoal.get()

print(ficha.ficha_pessoal.nome)
```

Os atributos disponíveis em `ficha.ficha_pessoal` são:

- `acrobacia`
- `alma_atual`     
- `alma_maximo`    
- `alma_temporario`
- `astucia`        
- `atencao`        
- `atletismo`      
- `ca`
- `campanha`       
- `caracteristicas`
- `carisma`        
- `constituicao`
- `destreza`
- `energia_atual`
- `energia_maximo`
- `energia_temporario`
- `enganacao`
- `especializacao`
- `exp`
- `feiticaria`
- `forca`
- `fortitude`
- `furtividade`
- `grau`
- `habilidades_de_especializacao`
- `historia`
- `iniciativa`
- `integridade`
- `inteligencia`
- `intimidacao`
- `intuicao`
- `investigacao`
- `jogador`
- `luta`
- `maestria`
- `maestrias`
- `medicina`
- `mod_carisma`
- `mod_constituicao`
- `mod_destreza`
- `mod_forca`
- `mod_inteligencia`
- `mod_sabedoria`
- `movimento`
- `nivel`
- `nome`
- `ocultismo`
- `oficio1`
- `oficio2`
- `oficio3`
- `origem`
- `percepcao`
- `performance`
- `persuasao`
- `pontaria`
- `prestidigitacao`
- `reflexos`
- `registro_rapido`
- `religiao`
- `sabedoria`
- `talentos`
- `tecnica`
- `tudo`
- `vida_atual`
- `vida_maximo`
- `vida_temporario`
- `vontade`

---

### Registro e Inventário

Exemplo para pegar dados da tabela:
```py
ficha.reg_e_inv.get()

print(ficha.reg_e_inv.inv)
```

Os atributos disponíveis em `ficha.reg_e_inv` são:

- `altura`
- `aparencia`
- `aura`
- `cabelos`
- `defeitos`
- `espacos_ocupados`      
- `genero`
- `historia_do_personagem`
- `idade`
- `ideais`
- `inv`
- `ligacoes`
- `limite_de_espacos`
- `marcas`
- `nome`
- `olhos`
- `pele`
- `peso`
- `roupas`
- `tamanho`
- `tracos_de_personalidade`
- `tudo`

---

### Perfil Amaldiçoado

Exemplo para pegar dados da tabela:
```py
ficha.perf_amald.get()

print(ficha.perf_amald.nome_da_tecnica)
```

Os atributos disponíveis em `ficha.perf_amald` são:

- `atributo_principal`
- `bunus_acerto`
- `cd_tecnica`
- `descricao_da_tecnica`    
- `energia_atual`
- `energia_maximo`
- `energia_temporario`
- `habilidades_amaldicoadas`
- `habilidades_conhecidas`  
- `habilidades_maximas`     
- `nome_da_tecnica`
- `tecnicas_nv0`
- `tecnicas_nv1`
- `tecnicas_nv2`
- `tecnicas_nv3`
- `tecnicas_nv4`
- `tecnicas_nv5`
- `tudo`

---

### Shikigamis/Corpos Amaldiçoados

Exemplo para pegar dados da tabela:
```py
ficha.invocacoes.get()

for invocacao in ficha.invocacoes.invocacoes:
    print(invocacao.nome)
```

Os atributos disponíveis em `ficha.invocacoes` são:

- `invocacoes`
- `tipo`
- `tudo`

---

##### Invocações

`ficha.invocacoes.invocacoes` retornará uma lista de invocações, caso tenha alguma, onde
cada um delas terá os seguintes atributos:

- `acoes`
- `ca`
- `carisma`     
- `constituicao`
- `destreza`    
- `forca`       
- `inteligencia`
- `mod_carisma`
- `mod_constituicao`
- `mod_destreza`
- `mod_forca`
- `mod_inteligencia`
- `mod_sabedoria`
- `movimento`
- `nome`
- `pericias`
- `sabedoria`
- `vida`
