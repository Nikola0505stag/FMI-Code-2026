package com.example.audiopipelinetest

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat

class MainActivity : AppCompatActivity() {

    private var isProtected = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val btnToggle = findViewById<Button>(R.id.btnToggleProtection)
        val tvStatus = findViewById<TextView>(R.id.tvStatus)

        btnToggle.setOnClickListener {
            if (!isProtected) {
                checkPermissionsAndStart()
                btnToggle.text = "STOP PROTECTION"
                btnToggle.backgroundTintList = ContextCompat.getColorStateList(this, android.R.color.holo_red_dark)
                tvStatus.text = "Shield Active - Scanning..."
                isProtected = true
            } else {
                stopProtection()
                btnToggle.text = "START PROTECTION"
                btnToggle.backgroundTintList = ContextCompat.getColorStateList(this, android.R.color.holo_green_dark)
                tvStatus.text = "Ready to Scan"
                isProtected = false
            }
        }
    }

    private fun checkPermissionsAndStart() {
        val audioPermission = ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)

        // Проверка за Android 13+ (API 33) за нотификации
        val notificationPermission = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
            ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS)
        } else {
            PackageManager.PERMISSION_GRANTED
        }

        if (audioPermission == PackageManager.PERMISSION_GRANTED && notificationPermission == PackageManager.PERMISSION_GRANTED) {
            startCallGuardService()
        } else {
            // Ако липсва някое от двете, искаме ги наведнъж (можеш да ползваш RequestMultiplePermissions за по-профи,
            // но за MVP и това става)
            requestPermissionLauncher.launch(Manifest.permission.RECORD_AUDIO)
            // За хакатона: ако потребителят приеме микрофона, Сървисът ще тръгне.
        }
    }

    private fun startCallGuardService() {
        val intent = Intent(this, CallGuardService::class.java)
        startForegroundService(intent)
        Toast.makeText(this, "Protection Activated!", Toast.LENGTH_SHORT).show()
    }

    private fun stopProtection() {
        val intent = Intent(this, CallGuardService::class.java)
        stopService(intent)
        Toast.makeText(this, "Protection Deactivated", Toast.LENGTH_SHORT).show()
    }

    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        if (isGranted) startCallGuardService()
        else Toast.makeText(this, "Permission denied", Toast.LENGTH_SHORT).show()
    }
}