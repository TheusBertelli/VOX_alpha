package com.agenda.config

import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.security.config.annotation.web.builders.HttpSecurity
import org.springframework.security.web.SecurityFilterChain
import org.springframework.web.cors.CorsConfiguration
import org.springframework.web.cors.CorsConfigurationSource
import org.springframework.web.cors.UrlBasedCorsConfigurationSource

@Configuration
class SecurityConfig {
    @Bean
    fun securityFilterChain(http: HttpSecurity): SecurityFilterChain {
        http
            .csrf { it.disable() }
            .cors { }
            .authorizeHttpRequests { authorize -> authorize.anyRequest().permitAll() }
        return http.build()
    }

    @Bean
    fun corsConfigurationSource(): CorsConfigurationSource {
        val configuration = CorsConfiguration().apply {
            // Keep the API convenient for local development; restrict this to app/web origins before production.
            allowedOriginPatterns = listOf("*")
            allowedMethods = listOf("GET", "POST", "OPTIONS")
            allowedHeaders = listOf("Content-Type", "Accept", "Authorization")
        }
        return UrlBasedCorsConfigurationSource().apply {
            registerCorsConfiguration("/**", configuration)
        }
    }
}
