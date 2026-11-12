# Acompanhamento do Desenvolvimento --- Ponte Nippon

> **Tipo de registro:** retrospectivo. Este documento organiza as etapas
> identificáveis no projeto; não representa uma ata ou um registro
> contemporâneo de reuniões semanais.

## Etapas do desenvolvimento

  -----------------------------------------------------------------------
  Etapa                   Atividades              Resultado identificado
  ----------------------- ----------------------- -----------------------
  1\. Definição da        Organização da ideia e  Escopo inicial do
  proposta                dos objetivos da        projeto definido.
                          aplicação voltada à     
                          preparação              
                          Brasil--Japão.          

  2\. Estrutura inicial   Organização dos         Base do programa
                          arquivos Python e       organizada.
                          criação do ponto de     
                          entrada da aplicação.   

  3\. Autenticação        Implementação de        Sistema de autenticação
                          cadastro, login,        integrado à aplicação.
                          validação de senha e    
                          controle de tentativas. 

  4\. Interface gráfica   Construção da janela    Interface gráfica com
                          principal, menu lateral páginas integradas.
                          e navegação entre       
                          páginas.                

  5\. Dicionário e guia   Inclusão de busca de    Recursos informativos
  cultural                traduções e             disponíveis na
                          apresentação de         aplicação.
                          informações culturais.  

  6\. Checklist           Implementação de        Checklist com
                          operações para          persistência dos dados.
                          adicionar, marcar,      
                          editar e excluir        
                          tarefas, com            
                          armazenamento em JSON.  

  7\. Revisão e           Revisão das             Projeto preparado para
  preparação              funcionalidades         apresentação.
                          existentes e            
                          organização da          
                          demonstração do         
                          sistema.                
  -----------------------------------------------------------------------

## Funcionalidades identificadas

-   Login e cadastro de usuários.
-   Armazenamento de dados de autenticação em `usuarios.json`.
-   Interface gráfica desenvolvida com Tkinter.
-   Navegação entre as páginas da aplicação.
-   Dicionário de português para japonês.
-   Guia cultural.
-   Checklist de tarefas com persistência em `documento.json`.

## Tecnologias e recursos utilizados

-   **Python:** linguagem principal do projeto.
-   **Tkinter:** construção da interface gráfica.
-   **JSON:** armazenamento local de usuários e tarefas.
-   **Git/GitHub:** versionamento e organização dos arquivos do projeto.

## Pontos para continuidade

-   Revisar e testar as funcionalidades antes de cada entrega.
-   Melhorar o tratamento de entradas inválidas.
-   Revisar a documentação para manter os nomes dos arquivos e campos
    iguais aos utilizados no código.
-   Registrar novas atividades com suas datas reais a partir desta
    versão.

------------------------------------------------------------------------

**Observação:** as etapas acima foram organizadas retrospectivamente a
partir da estrutura e das funcionalidades identificadas no projeto. A
divisão em etapas não confirma datas, reuniões ou entregas semanais
específicas.
