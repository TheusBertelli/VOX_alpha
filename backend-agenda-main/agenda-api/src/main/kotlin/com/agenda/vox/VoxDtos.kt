package com.agenda.vox

import jakarta.validation.constraints.NotBlank
import jakarta.validation.constraints.Size

/** Request accepted from the mobile app. Audio is never uploaded to the API. */
data class VoxTranscriptionRequest(
    @field:NotBlank(message = "O texto do lembrete não pode ficar vazio.")
    @field:Size(max = 2000, message = "O texto do lembrete deve ter no máximo 2.000 caracteres.")
    val text: String,
)

data class VoxInterpretation(
    val title: String,
    val date: String? = null,
    val time: String? = null,
    val domain: String = "pessoal",
    val priority: String = "média",
)

data class VoxTranscriptionResponse(
    val id: String,
    val text: String,
    val title: String,
    val date: String?,
    val time: String?,
    val domain: String,
    val priority: String,
    val message: String = "Lembrete salvo com sucesso.",
)

data class VoxApiError(val message: String)
