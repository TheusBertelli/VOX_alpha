package com.agenda.vox

import org.springframework.beans.factory.annotation.Value
import org.springframework.http.MediaType
import org.springframework.stereotype.Service
import org.springframework.web.client.ResourceAccessException
import org.springframework.web.client.RestClient
import org.springframework.web.client.RestClientException
import org.springframework.web.client.RestClientResponseException
import org.springframework.web.server.ResponseStatusException
import org.springframework.http.HttpStatus

@Service
class VoxAiClient(
    restClientBuilder: RestClient.Builder,
    @Value("\${vox.ai-service-url:http://localhost:8000}") aiServiceUrl: String,
) {
    private val client = restClientBuilder.baseUrl(aiServiceUrl.trimEnd('/')).build()

    fun interpret(text: String): VoxInterpretation {
        try {
            return client.post()
                .uri("/interpret")
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON)
                .body(VoxTranscriptionRequest(text))
                .retrieve()
                .body(VoxInterpretation::class.java)
                ?: throw ResponseStatusException(
                    HttpStatus.BAD_GATEWAY,
                    "O serviço VOX devolveu uma resposta vazia.",
                )
        } catch (ex: ResourceAccessException) {
            throw ResponseStatusException(
                HttpStatus.SERVICE_UNAVAILABLE,
                "O serviço de interpretação VOX está indisponível. Verifique se o microserviço Python está em execução.",
                ex,
            )
        } catch (ex: RestClientResponseException) {
            throw ResponseStatusException(
                HttpStatus.BAD_GATEWAY,
                "O serviço de interpretação VOX não conseguiu processar o lembrete.",
                ex,
            )
        } catch (ex: RestClientException) {
            throw ResponseStatusException(
                HttpStatus.BAD_GATEWAY,
                "Falha de comunicação com o serviço de interpretação VOX.",
                ex,
            )
        }
    }
}
