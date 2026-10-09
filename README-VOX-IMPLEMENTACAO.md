# VOX — Guia de integração do MVP

Este pacote implementa o fluxo proposto no **Plano de Implementação — Transcrição VOX** nos projetos enviados.

## Componentes alterados/adicionados

- `Frontend-main`: tela VOX em português; reconhecimento de fala em tempo real; tratamento de permissão, indisponibilidade do serviço e erros de rede/idioma; edição manual do texto; envio do texto à API; apresentação do resultado interpretado; agendamento de notificação local quando há data e hora futuras.
- `backend-agenda-main/agenda-api`: `POST /api/vox/transcriptions`; validação do texto; cliente HTTP para o serviço Python; gravação MongoDB na coleção `vox_reminders`; resposta estruturada e tratamento de erros.
- `vox-ai-service`: microserviço HTTP Python com endpoints `/health` e `/interpret`, mais testes do parser.

## Limite importante da implementação

O arquivo enviado descreve um microserviço de IA, mas não especifica um fornecedor, modelo, endpoint cloud ou chave de API e não veio um microserviço Python no ZIP original. Para permitir validar o fluxo de ponta a ponta, foi incluído um **parser determinístico inicial** que identifica expressões comuns em português (hoje/amanhã, datas numéricas, dias da semana, horários, domínio e prioridade). Ele **não é um modelo de IA generativa** e não alcançará precisão de 90% para linguagem livre. A função `interpret_text()` é o ponto onde deve ser conectado o provedor/modelo de IA escolhido antes de considerar a meta de precisão do plano atendida.

## Executar localmente

### 1. MongoDB

Inicie uma instância MongoDB local, ou configure `MONGODB_URI` para a instância que deseja usar.

### 2. Microserviço Python

No diretório `vox-ai-service`:

```bash
python -m venv .venv
```

Ative o ambiente virtual e execute:

```bash
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Verificação: `http://localhost:8000/health`.

### 3. Backend Kotlin

Em outro terminal, abra `backend-agenda-main/agenda-api` e execute:

```bash
./gradlew bootRun
```

No Windows:

```bat
gradlew.bat bootRun
```

Verificação: `http://localhost:8080/api/vox/health`.

### 4. Frontend Expo

No diretório `Frontend-main`:

```bash
npm install
```

O ambiente em que os arquivos foram ajustados não conseguiu acessar o registry npm, então o `package-lock.json` precisa ser sincronizado pelo `npm install` local. As dependências adicionadas são `expo-speech-recognition@^57.1.1` e `expo-notifications@~57.0.22`, alinhadas ao Expo SDK 57.

Copie `.env.example` para `.env` e defina a URL:

- Emulador Android: `EXPO_PUBLIC_API_URL=http://10.0.2.2:8080`.
- Celular físico: `EXPO_PUBLIC_API_URL=http://IP-DA-MÁQUINA:8080` (use o IP local do computador).

Gere e execute o build nativo:

```bash
npx expo prebuild
npx expo run:android
```

O Expo Go padrão não inclui o módulo nativo de reconhecimento de voz. Para testar em um dispositivo físico, o celular e o computador devem estar na mesma rede; libere as portas 8000 e 8080 no firewall se necessário.

## Testes realizados neste pacote

No microserviço Python, `python -m unittest -v` valida o parser para frases de teste. Ainda é necessário executar o build Android e testar em aparelhos físicos para validar permissões, reconhecimento de voz, pacotes de idioma offline, conectividade, MongoDB e notificações.

## Exemplo de chamada da API

```bash
curl -X POST http://localhost:8080/api/vox/transcriptions \
  -H "Content-Type: application/json" \
  -d '{"text":"Me lembre de entregar o trabalho amanhã às 18h"}'
```

A resposta segue o contrato:

```json
{
  "id": "id-gerado-pelo-mongodb",
  "text": "Me lembre de entregar o trabalho amanhã às 18h",
  "title": "entregar o trabalho",
  "date": "2026-10-10",
  "time": "18:00",
  "domain": "trabalho",
  "priority": "média",
  "message": "Lembrete salvo com sucesso."
}
```

A data do exemplo depende do dia em que a frase for interpretada.
