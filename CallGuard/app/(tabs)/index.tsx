import { useState, useRef } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { useAudioRecorder, AudioModule, RecordingPresets } from 'expo-audio';

const BACKEND_URL = 'http://172.20.10.11:8000/predict';

export default function HomeScreen() {
  const [isProtected, setIsProtected] = useState(false);
  const [status, setStatus] = useState('Ready to Scan');
  const audioRecorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY);
  const intervalRef = useRef<any>(null);

  async function startProtection() {
    await AudioModule.requestRecordingPermissionsAsync();
    await audioRecorder.prepareToRecordAsync();
	await AudioModule.setAudioModeAsync({ allowsRecording: true, playsInSilentMode: true });   
	audioRecorder.record();
    setIsProtected(true);
    setStatus('Shield Active - Scanning...');

    intervalRef.current = setInterval(async () => {
      await audioRecorder.stop();
      const uri = audioRecorder.uri;
      if (uri) await sendAudio(uri);
      await audioRecorder.prepareToRecordAsync();
      audioRecorder.record();
    }, 3000);
  }

  async function sendAudio(uri: string) {
    const formData = new FormData();
	formData.append('file', { uri, name: 'audio.m4a', type: 'audio/m4a' } as any);
    try {
      const response = await fetch(BACKEND_URL, { method: 'POST', body: formData });
      const result = await response.json();
      console.log('Отговор:', JSON.stringify(result));
      setStatus(result.label || 'Scanning...');
    } catch (e) {
      console.log('Грешка:', e);
    }
  }

  async function stopProtection() {
    clearInterval(intervalRef.current);
    await audioRecorder.stop();
    setIsProtected(false);
    setStatus('Ready to Scan');
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>AI Call Guard</Text>
      <Text style={styles.status}>{status}</Text>
      <TouchableOpacity
        style={[styles.button, isProtected ? styles.stop : styles.start]}
        onPress={isProtected ? stopProtection : startProtection}
      >
        <Text style={styles.buttonText}>
          {isProtected ? 'STOP PROTECTION' : 'START PROTECTION'}
        </Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  status: { fontSize: 18, marginBottom: 30, color: '#555' },
  button: { padding: 20, borderRadius: 10, width: 250, alignItems: 'center' },
  start: { backgroundColor: 'green' },
  stop: { backgroundColor: 'red' },
  buttonText: { color: 'white', fontSize: 16, fontWeight: 'bold' },
});
