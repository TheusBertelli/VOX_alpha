# agenda-api — Integração VOX

API intermediária Kotlin/Spring Boot do módulo VOX.

## Endpoint

`POST /api/vox/transcriptions`

Corpo:

```json
{ "text": "Me lembre de entregar o trabalho amanhã às 18h" }
```

Fluxo: valida texto → encaminha ao microserviço Python (`POST /interpret`) → grava os campos interpretados na coleção MongoDB `vox_reminders` → devolve `id`, título, data, hora, domínio e prioridade.

Também existe `GET /api/vox/health` para verificar se a API está acessível.

## Configuração

Variáveis de ambiente:

- `MONGODB_URI`: padrão `mongodb://localhost:27017/agenda`.
- `VOX_AI_SERVICE_URL`: padrão `http://localhost:8000`.
- `SERVER_PORT`: padrão `8080`.

Com MongoDB e microserviço Python ligados, execute na pasta `agenda-api`:

```bash
./gradlew bootRun
```

No Windows, use `gradlew.bat bootRun`.

## Segurança / implantação

A configuração de CORS e a autorização abertas são destinadas somente ao MVP em desenvolvimento. Antes de publicar, restrinja origens e rotas, integre a autenticação/autorização do restante da agenda e use HTTPS. Os endpoints VOX não recebem áudio, apenas texto.
