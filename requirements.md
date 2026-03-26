# 📌 Requirements — Obsidian AI Knowledge CLI

## 🎯 Objetivo

Definir de forma clara os requisitos funcionais e não funcionais para o sistema de consulta de conhecimento baseado em arquivos Markdown.

---

# 🧩 1. Requisitos Funcionais (Functional Requirements)

## RF-01 — Entrada via CLI

O sistema deve:

* Receber uma pergunta em linguagem natural via terminal
* Exemplo:

```bash
python perguntar.py "como funciona meu fluxo de QA?"
```

---

## RF-02 — Leitura da base de conhecimento

O sistema deve:

* Receber um diretório contendo arquivos `.md`
* Ler todos os arquivos dentro desse diretório
* Suportar subpastas (recursivo)

---

## RF-03 — Processamento de conteúdo

O sistema deve:

* Extrair texto dos arquivos Markdown
* Ignorar elementos irrelevantes (ex: código, metadata opcional)

---

## RF-04 — Busca de relevância

O sistema deve:

* Identificar trechos relevantes com base na pergunta
* Utilizar inicialmente:

  * busca por palavras-chave
  * correspondência simples (TF-IDF opcional no futuro)

---

## RF-05 — Seleção de contexto

O sistema deve:

* Selecionar os trechos mais relevantes
* Limitar o tamanho total do contexto (ex: 2k–5k tokens)
* Priorizar qualidade ao invés de quantidade

---

## RF-06 — Montagem do prompt

O sistema deve:

* Construir um prompt estruturado contendo:

  * instrução para a IA
  * trechos selecionados
  * pergunta do usuário

Exemplo:

```text
Responda com base apenas nos conteúdos abaixo:

[trecho 1]
[trecho 2]

Pergunta: ...
```

---

## RF-07 — Integração com API de IA

O sistema deve:

* Enviar o prompt para uma API externa (ex: Gemini)
* Receber a resposta

---

## RF-08 — Exibição da resposta

O sistema deve:

* Mostrar a resposta no terminal
* Formatar de forma legível

---

## RF-09 — Configuração do diretório

O sistema deve permitir:

* Definir o diretório via CLI ou config
* Exemplo futuro:

```bash
python perguntar.py "..." --path ./meu_obsidian
```

---

## RF-10 — Tratamento de erros

O sistema deve:

* Lidar com:

  * diretório inexistente
  * arquivos vazios
  * falha na API
* Exibir mensagens claras

---

# ⚙️ 2. Requisitos Não Funcionais

## RNF-01 — Performance

* Deve responder rapidamente (< 5s ideal)
* Leitura eficiente de arquivos

---

## RNF-02 — Leveza

* Sem uso de GPU
* Sem modelos locais pesados
* Apenas leitura + API externa

---

## RNF-03 — Usabilidade

* Interface simples via CLI
* Uso intuitivo

---

## RNF-04 — Portabilidade

* Rodar em:

  * Windows
  * Linux
  * Android (Termux)

---

## RNF-05 — Manutenibilidade

* Código modular
* Fácil adicionar:

  * embeddings
  * novos métodos de busca

---

# 🧪 3. Regras de Negócio

* A resposta deve ser baseada nos arquivos fornecidos
* A IA não deve inventar informações fora do contexto (quando possível)
* Se não houver informação suficiente:

  * informar ao usuário

---

# ⚠️ 4. Limitações iniciais

* Busca semântica limitada (sem embeddings avançados)
* Dependência de qualidade dos arquivos `.md`
* Limite de contexto da API

---

# 📊 5. Critérios de Aceitação

✔ Usuário faz pergunta via CLI
✔ Sistema lê arquivos `.md`
✔ Trechos relevantes são selecionados
✔ IA responde com base nesses trechos
✔ Resposta é exibida corretamente

---

# 🚀 6. Escalabilidade futura

* embeddings (FAISS ou similares)
* ranking semântico
* cache de respostas
* indexação incremental
* múltiplos vaults (Obsidian)

---
