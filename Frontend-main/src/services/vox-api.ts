import { Platform } from 'react-native';

export type VoxInterpretation = {
  id: string;
  text: string;
  title: string;
  date: string | null;
  time: string | null;
  domain: string;
  priority: string;
  message?: string;
};

/**
 * Configure EXPO_PUBLIC_API_URL in .env for a physical device.
 * Android emulator can reach the host computer through 10.0.2.2.
 */
const API_BASE_URL = (
  process.env.EXPO_PUBLIC_API_URL ||
  (Platform.OS === 'android' ? 'http://10.0.2.2:8080' : 'http://localhost:8080')
).replace(/\/+$/, '');

export async function createVoxReminder(text: string): Promise<VoxInterpretation> {
  const response = await fetch(`${API_BASE_URL}/api/vox/transcriptions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    // The API receives the recognized/edited text only; no audio file is sent.
    body: JSON.stringify({ text: text.trim() }),
  });

  const body: unknown = await response.json().catch(() => null);
  if (!response.ok) {
    const apiMessage =
      body && typeof body === 'object' && 'message' in body && typeof body.message === 'string'
        ? body.message
        : `Não foi possível salvar o lembrete (HTTP ${response.status}).`;
    throw new Error(apiMessage);
  }

  if (!body || typeof body !== 'object' || !('id' in body) || !('title' in body)) {
    throw new Error('A API retornou uma resposta inesperada. Verifique a configuração do backend.');
  }

  return body as VoxInterpretation;
}
