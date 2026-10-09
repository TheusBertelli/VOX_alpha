package com.agenda.vox

import jakarta.validation.Valid
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.server.ResponseStatusException

@RestController
@RequestMapping("/api/vox")
class VoxController(
    private val voxAiClient: VoxAiClient,
    private val repository: VoxReminderRepository,
) {
    @PostMapping("/transcriptions")
    fun createFromTranscription(
        @Valid @RequestBody request: VoxTranscriptionRequest,
    ): VoxTranscriptionResponse {
        val text = request.text.trim()
        if (text.isBlank()) {
            throw ResponseStatusException(HttpStatus.BAD_REQUEST, "Digite ou transcreva um lembrete antes de enviar.")
        }

        val interpreted = voxAiClient.interpret(text)
        if (interpreted.title.isBlank()) {
            throw ResponseStatusException(
                HttpStatus.BAD_GATEWAY,
                "O serviço VOX não conseguiu identificar um título para o lembrete.",
            )
        }

        val saved = repository.save(
            VoxReminder(
                text = text,
                title = interpreted.title.trim(),
                date = interpreted.date,
                time = interpreted.time,
                domain = interpreted.domain.ifBlank { "pessoal" },
                priority = interpreted.priority.ifBlank { "média" },
            ),
        )

        return VoxTranscriptionResponse(
            id = saved.id ?: throw ResponseStatusException(
                HttpStatus.INTERNAL_SERVER_ERROR,
                "O lembrete foi processado, mas não foi possível recuperar seu identificador.",
            ),
            text = saved.text,
            title = saved.title,
            date = saved.date,
            time = saved.time,
            domain = saved.domain,
            priority = saved.priority,
        )
    }

    @GetMapping("/health")
    fun health(): Map<String, String> = mapOf(
        "status" to "ok",
        "service" to "agenda-api-vox",
    )
}
