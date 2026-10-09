package com.agenda.config

import com.agenda.vox.VoxApiError
import jakarta.validation.ConstraintViolationException
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.MethodArgumentNotValidException
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.RestControllerAdvice
import org.springframework.web.server.ResponseStatusException

@RestControllerAdvice
class ApiExceptionHandler {
    @ExceptionHandler(ResponseStatusException::class)
    fun handleResponseStatus(ex: ResponseStatusException): ResponseEntity<VoxApiError> =
        ResponseEntity.status(ex.statusCode).body(VoxApiError(ex.reason ?: "A requisição não pôde ser concluída."))

    @ExceptionHandler(MethodArgumentNotValidException::class)
    fun handleValidation(ex: MethodArgumentNotValidException): ResponseEntity<VoxApiError> {
        val message = ex.bindingResult.fieldErrors.firstOrNull()?.defaultMessage
            ?: "Os dados enviados são inválidos."
        return ResponseEntity.badRequest().body(VoxApiError(message))
    }

    @ExceptionHandler(ConstraintViolationException::class)
    fun handleConstraintViolation(ex: ConstraintViolationException): ResponseEntity<VoxApiError> =
        ResponseEntity.status(HttpStatus.BAD_REQUEST).body(VoxApiError(ex.message ?: "Os dados enviados são inválidos."))
}
