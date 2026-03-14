package com.example.audiopipelinetest // Провери дали това съвпада с твоя пакет!

import android.app.*
import android.content.Intent
import android.os.IBinder
import androidx.core.app.NotificationCompat
import android.util.Log

class CallGuardService : Service() {

    // Инстанция на твоя аудио двигател
    private val audioManager = AudioCaptureManager()
    private val CHANNEL_ID = "CallGuardChannel"

    override fun onCreate() {
        super.onCreate()
        // 1. Създаваме канала за нотификации (задължително за Android 8+)
        createNotificationChannel()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        Log.d("CallGuardService", "Сървисът стартира...")

        // 2. Създаваме нотификацията, която потребителят ще вижда горе
        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("AI Call Guard е активен")
            .setContentText("Следя за измами в реално време...")
            .setSmallIcon(android.R.drawable.ic_btn_speak_now) // Системна иконка на микрофон
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .build()

        // 3. ПРАВИМ СЪРВИСА FOREGROUND (Критична стъпка!)
        // Това казва на Android: "Не ме убивай, ползвам микрофона за важна работа."
        startForeground(1, notification)

        // 4. Пускаме записването
        audioManager.startRecording()

        // START_STICKY означава, че ако системата все пак убие сървиса при недостиг на памет,
        // тя ще се опита да го пусне отново веднага щом може.
        return START_STICKY
    }

    override fun onDestroy() {
        Log.d("CallGuardService", "Сървисът е спрян.")
        // Спираме записа, за да освободим микрофона
        audioManager.stopRecording()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? {
        return null // Не ни трябва Binding за това MVP
    }

    private fun createNotificationChannel() {
        val serviceChannel = NotificationChannel(
            CHANNEL_ID,
            "Call Guard Service Channel",
            NotificationManager.IMPORTANCE_DEFAULT
        )
        val manager = getSystemService(NotificationManager::class.java)
        manager?.createNotificationChannel(serviceChannel)
    }
}