# 📌 Architecture — Obsidian AI Knowledge CLI

## 🎯 Objetivo

Definir a arquitetura técnica do sistema de consulta de conhecimento baseado em arquivos Markdown, utilizando Gemini Flash como modelo de IA.

---

# 🧱 1. Visão Geral

Arquitetura simples e eficiente:

```
CLI → Orquestrador → Leitura → Busca → Contexto → IA (Gemini) → Resposta
```

---

# ⚙️ 2. Componentes do Sistema

## 2.1 CLI (`perguntar.py`)

Responsável por:

* Receber pergunta do usuário
* Receber diretório (opcional)
* Iniciar fluxo

Exemplo:

```bash
python perguntar.py "minha pergunta" --path ./vault
```

---

## 2.2 Orquestrador (`main flow`)

Responsável por:

* Controlar execução
* Integrar todos os módulos

---

## 2.3 Leitor de Arquivos (`file_reader.py`)

Responsável por:

* Percorrer diretórios recursivamente
* Ler arquivos `.md`
* Retornar conteúdo bruto

---

## 2.4 Processador de Texto (`text_processor.py`)

Responsável por:

* Limpar Markdown
* Remover:

  * blocos de código
  * metadados desnecessários
* Retornar texto limpo

---

## 2.5 Motor de Busca (`search_engine.py`)

Responsável por:

* Encontrar trechos relevantes
* Base inicial:

  * match por palavras-chave
* Futuro:

  * TF-IDF
  * embeddings

---

## 2.6 Gerador de Contexto (`context_builder.py`)

Responsável por:

* Selecionar os melhores trechos
* Limitar tamanho total
* Organizar contexto

Formato:

```
[Arquivo: nome.md]
Trecho relevante...

[Arquivo: outro.md]
Trecho...
```

---

## 2.7 Cliente de IA (`gemini_client.py`)

Responsável por:

* Enviar prompt para API do Gemini Flash
* Receber resposta

Modelo:

* Gemini 1.5 Flash (ou equivalente mais recente)

---

## 2.8 Prompt Builder (`prompt_builder.py`)

Responsável por:

* Montar prompt final

Formato:

```
Responda com base apenas nos conteúdos abaixo.

Se não houver informação suficiente, diga isso.

[contexto]

Pergunta: ...
```

---

## 2.9 Output (`printer.py`)

Responsável por:

* Exibir resposta no terminal
* Formatação simples

---

# 🔄 3. Fluxo de Execução

1. Usuário roda CLI
2. CLI captura pergunta
3. Leitor carrega arquivos `.md`
4. Processador limpa texto
5. Motor de busca encontra trechos
6. Context builder organiza
7. Prompt builder monta input
8. Gemini responde
9. Resultado exibido

---

# 🧩 4. Estrutura de Pastas

```
project/
│
├── perguntar.py
├── requirements.txt
│
├── src/
│   ├── file_reader.py
│   ├── text_processor.py
│   ├── search_engine.py
│   ├── context_builder.py
│   ├── prompt_builder.py
│   ├── gemini_client.py
│   └── printer.py
│
├── config/
│   └── settings.json
│
└── vault/ (exemplo)
```

---

# ⚙️ 5. Tecnologias

* Python 3.x
* API Gemini Flash (Google)
* requests (ou httpx)

---

# 🔐 6. Segurança

* API Key armazenada em:

  * variável de ambiente (`GEMINI_API_KEY`)
* Nunca hardcoded

---

# ⚠️ 7. Pontos Críticos

* Limite de tokens do Gemini
* Qualidade da busca
* Latência da API
* Qualidade dos arquivos `.md`

---

# 🚀 8. Evoluções futuras

* embeddings locais leves
* cache de contexto
* indexação incremental
* ranking por relevância
* integração com Obsidian plugin

---

# 🧠 9. Decisões Arquiteturais

### Simplicidade

* Nada pesado local

### Modularidade

* Cada parte isolada

### API-first

* IA externa

### Escalabilidade

* Preparado para embeddings no futuro

---
