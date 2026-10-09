package com.agenda.vox

import org.springframework.data.mongodb.repository.MongoRepository

interface VoxReminderRepository : MongoRepository<VoxReminder, String>
