package com.agenda.vox

import org.springframework.data.annotation.Id
import org.springframework.data.mongodb.core.mapping.Document
import java.time.Instant

@Document(collection = "vox_reminders")
data class VoxReminder(
    @Id val id: String? = null,
    val text: String,
    val title: String,
    /** ISO date (yyyy-MM-dd), or null when the user did not mention one. */
    val date: String? = null,
    /** Local time (HH:mm), or null when the user did not mention one. */
    val time: String? = null,
    val domain: String = "pessoal",
    val priority: String = "média",
    val createdAt: Instant = Instant.now(),
)
