# Ponte Nippon

Aplicativo de desktop em Python que reúne, em um só lugar, **checklist de documentação**, **dicionário de frases** e **guia cultural** para brasileiros que querem ir ao Japão (turismo, estudo, moradia ou trabalho).

Funciona **100% offline** e usa apenas a biblioteca padrão do Python.

<img width="1496" height="844" alt="image" src="https://github.com/user-attachments/assets/b98a681b-9293-4c63-9477-e918abe27cb8" />

## Sobre o projeto

Quem se prepara para ir ao Japão costuma depender de pesquisa extensa e de ferramentas espalhadas pela internet. O Ponte Nippon centraliza o básico da preparação inicial: organizar documentos, aprender expressões úteis e entender a etiqueta local.

O projeto parte da experiência do autor, que pretende morar no Japão, e foi validado com um formulário aplicado a 10 pessoas interessadas em ir ao país. Os requisitos, casos de uso e decisões de escopo estão no documento **"Ponte Nippon - Requisitos, Casos de Uso e MVP"** (PDF na raiz deste repositório).

## Funcionalidades

| Módulo | O que faz |
|---|---|
| **Autenticação** | Cadastro e login com e-mail e senha. |
| **Checklist** | Adicionar, listar, concluir/desmarcar, editar e excluir tarefas. O estado é salvo entre execuções. |
| **Dicionário** | Busca de frases em português com a tradução em japonês. |
| **Guia cultural** | Orientações de costumes, etiqueta e comportamento organizadas por situação. |

## Segurança e privacidade

- As senhas são guardadas como **hash com salt (PBKDF2-HMAC-SHA256)**, nunca em texto puro.
- O login é **bloqueado temporariamente após 5 tentativas erradas**; o contador e a hora do bloqueio ficam salvos em `usuarios.json`, então persistem entre execuções.
- O sistema **não armazena documentos pessoais**, apenas o nome das tarefas.
- Entradas inválidas e arquivos de dados ausentes ou corrompidos são tratados: o programa abre normalmente, com a lista vazia, sem encerrar.

## Tecnologias

- Python 3 (somente biblioteca padrão)
- Tkinter (interface gráfica)
- JSON (persistência de contas e tarefas)

## Como executar

**Requisitos:** Python 3 instalado. O Tkinter já vem com o Python no Windows e no macOS. No Linux, pode ser necessário instalar o pacote `python3-tk`.

```bash
# 1. Clone o repositório
git clone https://github.com/luizricardo-engsoft/ponte-nippon.git
cd ponte-nippon

# 2. Execute a versão com interface gráfica
python main.py
```

Também existe uma versão de terminal, com menu em texto:

```bash
python ponte_nippon.py
```

## Como usar

1. Na janela de login, clique para **criar uma conta** com e-mail e senha.
2. Entre com os mesmos dados. A tela principal abre.
3. Pelo menu, acesse:
   - **Checklist:** digite o nome da tarefa e clique em *Adicionar*. Marque como concluída, edite ou exclua conforme avançar. Ao reabrir o programa, tudo continua salvo.
   - **Dicionário:** digite uma frase em português no campo de busca para ver a tradução.
   - **Guia cultural:** consulte costumes e etiqueta por situação.

Os arquivos `usuarios.json` e `checklist.json` são criados e atualizados durante o uso e não fazem parte do repositório, para que contas e dados pessoais não sejam versionados.

## Estrutura do projeto

```
ponte-nippon/
├── main.py             # ponto de entrada (interface gráfica)
├── login.py            # cadastro, login, hash de senha e bloqueio por tentativas
├── interface.py        # telas e checklist (carregar/salvar tarefas)
├── guia_cultural.py    # dicionário de frases e guia cultural
├── ponte_nippon.py     # versão de terminal (menu em texto)
├── documento.json
└── Ponte Nippon - Requisitos, Casos de Uso e MVP.pdf
```

## Escopo do MVP e próximos passos

**Entregue no MVP:** cadastro e login seguros, checklist persistente, dicionário, guia cultural, funcionamento offline.

**Evolução futura:**

- **D7:** centralizar links e materiais de referência (apontado como útil pelo formulário).
- **Categorias no checklist:** organizar tarefas em "Antes da viagem" e "Durante a estadia" (HU08).
- **D4:** conectar brasileiros que pretendem ir ao Japão (exige internet e servidor).
- **D5:** avisos de terremoto e tsunami (exige internet; conflita com o requisito offline).

## Desenvolvimento

Projeto individual desenvolvido como atividade acadêmica da disciplina **Linguagem de Programação**.

- **Instituição:** IFAL — Campus Arapiraca
- **Discente:** Luís Ricardo Rodrigues Sales de Alencar
- **Docente:** Mauricio Junior
- **Ano:** 2026
