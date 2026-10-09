# VOX — Frontend Expo

Frontend mobile do módulo de transcrição e criação de lembretes por voz.

## Requisitos

- Node.js e npm.
- Backend `agenda-api` em execução na porta `8080`.
- Microserviço Python `vox-ai-service` em execução na porta `8000`.
- MongoDB em execução para persistir os lembretes.
- Android Studio/SDK para gerar e executar o app Android.

## Configuração inicial

1. Instale as dependências com `npm install`.
2. Copie `.env.example` para `.env` e configure `EXPO_PUBLIC_API_URL`:
   - Emulador Android: `http://10.0.2.2:8080`.
   - Celular físico: `http://IP-DA-SUA-MÁQUINA:8080`. O computador e o celular precisam estar na mesma rede e a porta 8080 liberada no firewall.
3. Este projeto usa `expo-speech-recognition` e `expo-notifications`. Se estiver atualizando uma cópia antiga do projeto, execute `npm install` para sincronizar o `package-lock.json`; o arquivo de lock incluído pode precisar ser regenerado porque o ambiente em que esta alteração foi feita não tinha acesso ao registry npm.
4. Gere o projeto nativo e instale o build de desenvolvimento:

   ```bash
   npx expo prebuild
   npx expo run:android
   ```

   O Expo Go padrão não contém o módulo nativo de reconhecimento de voz. Não use apenas `npx expo start` para validar o reconhecimento de voz Android.

## Uso

1. Toque em **Começar a falar** e conceda acesso ao microfone.
2. Diga o lembrete em português.
3. Revise ou corrija a transcrição no campo editável.
4. Toque em **Salvar lembrete**. O app envia somente `{ "text": "..." }` para `POST /api/vox/transcriptions`.
5. Caso a interpretação retorne uma data e um horário futuros, o app tenta agendar uma notificação local. Se o usuário negar notificações, o lembrete continua salvo na API.

## Reconhecimento offline

Em dispositivos móveis, a captura está configurada com `requiresOnDeviceRecognition` para priorizar processamento de voz no próprio aparelho. No Android, o idioma português precisa estar instalado no serviço de reconhecimento de voz. Se o pacote não estiver disponível, o app exibe um aviso e mantém a opção de digitar o lembrete.

## Configuração de rede para desenvolvimento

O arquivo `app.json` habilita tráfego HTTP sem TLS para facilitar testes com o backend local. Isso é apenas para desenvolvimento: em produção, use HTTPS e desative `android.usesCleartextTraffic`.
