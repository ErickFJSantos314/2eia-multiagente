# 2E.IA - Orquestrador Multiagente (GCP + Vertex AI)

Arquitetura de maquina de estados finita orientada a grafo para orquestracao de agentes LLM com Human-in-the-Loop (HITL), usando apenas stack Google Cloud.

## 1) Visao geral

Este repositorio implementa um esqueleto operacional para:

- Camada 1 (HITL): entrada e aprovacao humana.
- Camada 2 (Orquestrador): parser, roteamento, fan-out e reduce.
- Camada 3 (C-Level): critic loop e validacao (CTO, CMO, CFO).
- Camada 4 (Especialistas): geracao de artefatos tecnicos.

Tecnologias principais:

- FastAPI para API de orquestracao.
- Vertex AI (Gemini) para execucao dos agentes.
- Cloud Run para deploy serverless.
- Secret Manager para segredos.
- Firestore (opcional) para memoria de sessoes e historico.
- Cloud Storage (opcional) para artefatos finais.

## 1.1) Time oficial (codinomes internos)

Fundadores (Camada 1):

- Erick (Co-CEO)
- Eder (Co-CEO)

Mapa de cargos e nomes dos agentes:

- Orquestrador (L2): MALUCO
- CTO (L3): ASSOMBRACAO
- CMO (L3): BASTET
- CFO (L3): EMPADA
- Front-end (L4A): QUICO
- Back-end (L4A): MORGUETE
- Tesoureira (L4B): BODE
- Planejamento Financeiro (L4B): MALOTE
- Designer e Conteudo (L4C): TESTONGO
- FP&A (L4B): ISIS

## 1.2) Job descriptions por camada

### Camada 1 - Diretoria (Erick e Eder)

- Missao: direcao estrategica, capital, relacionamento de alto nivel e aprovacao final.
- Papel no sistema: voces sao Input (problema real) e Output (assinatura/aprovacao final).
- Limite operacional: nao codificam, nao desenham, nao fazem copy; aprovam ou vetam.

### Camada 2 - Middleware

Cargo: Orquestrador (MALUCO)

- Missao: quebrar demandas em tarefas, delegar para os diretores corretos, acompanhar e reduzir tudo em um relatorio unico.
- Papel no sistema: unico ponto de contato com os fundadores.
- Personalidade do agente: frio, estruturado, sintetico e obcecado em formato de saida.

### Camada 3 - C-Level (pensadores e validadores)

CTO (ASSOMBRACAO):

- Missao: excelencia de engenharia, escalabilidade e arquitetura limpa.
- Papel no sistema: escolhe stack e padroes (Python, FastAPI, GCP, Cloud Run, Firestore/Postgres) e valida codigo da engenharia.
- Foco: Python direto, infraestrutura, integracoes de API, seguranca e viabilidade tecnica.

CMO (BASTET):

- Missao: aquisicao, conversao e percepcao de marca.
- Papel no sistema: define canal, angulo de vendas, tom de voz e direcionamento visual.
- Foco: conversao, posicionamento B2B, estrategia de campanha e coerencia de mensagem.

CFO (EMPADA):

- Missao: proteger margem e fluxo de caixa.
- Papel no sistema: precifica projetos com base em custo tecnico e viabilidade comercial.
- Foco: ROI, CMV, custo de infraestrutura, LTV e precificacao de servicos.

### Camada 4 - Especialistas (executores)

Sob o CTO (Engenharia - L4A):

- Back-end (MORGUETE): constroi o cerebro da aplicacao (Python, dados, APIs, integracoes e persistencia).
- Front-end/Integracoes (QUICO): constroi landing pages e interface final (HTML/CSS/JS), UX e integracao de borda.

Sob o CFO (Financeiro - L4B):

- Tesoureira (BODE): guarda do caixa diario, entradas/saidas e relatorios operacionais.
- Planejamento Financeiro (MALOTE): projecoes, break-even, cenarios de crescimento e previsao.
- FP&A (ISIS): analise avancada de desempenho, modelagem de metas e previsibilidade financeira.

Sob o CMO (Comunicacao e Imagem - L4C):

- Designer e Conteudo (TESTONGO): copy de conversao, direcionamento visual, prompts tecnicos de imagem e padrao estetico consistente.

Regras de nao sobreposicao:

- Especialistas nao decidem estrategia macro.
- C-Level nao executa tarefas operacionais detalhadas.
- Fundadores aprovam e liberam entrega, sem bypass do HITL.

## 2) Estrutura do projeto

```text
EMPRESA/
  app/
    main.py
    config.py
    schemas.py
    orchestrator.py
    agents.py
    vertex_client.py
    brain_store.py
  data/
    brand/
      brand_profile.example.yaml
      content_history.example.md
  prompts/
    system/
      orchestrator.md
      cto.md
      cmo.md
      cfo.md
      backend_specialist.md
      frontend_specialist.md
      designer_specialist.md
      treasurer.md
      financial_planning.md
      fpa.md
  .env.example
  requirements.txt
  Dockerfile
  cloudbuild.yaml
```

## 3) Pre-requisitos

- Projeto GCP ativo com billing.
- Vertex AI API habilitada.
- Cloud Run API habilitada.
- Secret Manager API habilitada.
- Artifact Registry API habilitada.
- Cloud Build API habilitada.
- Python 3.11+.
- gcloud CLI autenticado.

Comandos iniciais:

```bash
gcloud auth login
gcloud config set project SEU_PROJECT_ID
gcloud services enable aiplatform.googleapis.com run.googleapis.com secretmanager.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com firestore.googleapis.com storage.googleapis.com
```

## 4) Configuracao local

1. Copie o arquivo de ambiente:

```bash
cp .env.example .env
```

2. Preencha os valores no .env.

3. Crie ambiente virtual e instale dependencias:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. Rode localmente:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

## 5) Fluxo da maquina de estados

1. HITL envia o briefing para endpoint /v1/orchestrate.
2. Orquestrador classifica intencao e gera plano de delegacao.
3. Fan-out para C-Level (CTO, CMO, CFO).
4. C-Level dispara especialistas da camada 4.
5. Critic loop valida artefatos e solicita refinamento quando necessario.
6. Fan-in consolida tudo em payload unico.
7. HITL aprova e dispara entrega externa (email, webhook, CRM).

## 6) CEREBRO DE DADOS (Brand Brain)

Use os arquivos abaixo como base de contexto persistente:

- data/brand/brand_profile.example.yaml: identidade da marca (tom, fontes, paletas, proposta).
- data/brand/content_history.example.md: historico de campanhas, aprendizados e decisoes.

No bootstrap de producao, recomendo:

- Firestore para memoria de sessao e memoria por cliente.
- Cloud Storage para artefatos finais e snapshots de briefing.
- Secret Manager para segredos e tokens.

## 7) Deploy em Cloud Run

### Opcao A: Cloud Build (recomendado)

```bash
gcloud builds submit --config cloudbuild.yaml .
```

### Opcao B: Build + Deploy manual

```bash
gcloud builds submit --tag REGION-docker.pkg.dev/SEU_PROJECT_ID/2eia/2eia-orchestrator:latest

gcloud run deploy 2eia-orchestrator \
  --image REGION-docker.pkg.dev/SEU_PROJECT_ID/2eia/2eia-orchestrator:latest \
  --platform managed \
  --region REGION \
  --allow-unauthenticated \
  --set-env-vars GCP_PROJECT_ID=SEU_PROJECT_ID,GCP_REGION=REGION,VERTEX_MODEL=gemini-1.5-pro
```

## 8) Seguranca e governanca

- Nunca commitar .env real.
- Preferir service account com menor privilegio.
- Guardar segredos no Secret Manager.
- Ativar logs estruturados e tracing (Cloud Logging/Trace).
- Definir limites de custo por ambiente (budgets + alerts).

## 9) Proximos passos recomendados

1. Conectar Firestore no brain_store.py para memoria persistente real.
2. Adicionar fila Pub/Sub para workloads longos.
3. Criar endpoint de aprovacao HITL com status draft/approved/rejected.
4. Adicionar testes de contrato para prompts e schemas.
5. Integrar notificacao final via Gmail API ou webhook.

## 10) Endpoints iniciais

- GET /health
- POST /v1/orchestrate

Exemplo de payload:

```json
{
  "session_id": "sess-001",
  "input": "Fechamos com uma pizzaria. Preciso de landing page, copy e stack de automacao.",
  "client": "Pizzaria Exemplo"
}
```
