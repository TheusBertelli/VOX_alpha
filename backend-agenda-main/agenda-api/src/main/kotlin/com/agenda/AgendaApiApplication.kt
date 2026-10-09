package com.agenda

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class AgendaApiApplication

fun main(args: Array<String>) {
	runApplication<AgendaApiApplication>(*args)
}
