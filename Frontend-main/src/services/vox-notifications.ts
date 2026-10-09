import * as Notifications from 'expo-notifications';
import { Platform } from 'react-native';

import type { VoxInterpretation } from './vox-api';

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldPlaySound: true,
    shouldSetBadge: false,
    shouldShowBanner: true,
    shouldShowList: true,
  }),
});

export type LocalReminderResult = 'scheduled' | 'missing-date' | 'past-date' | 'permission-denied';

/** Schedules an on-device notification when the interpretation contains a future date and time. */
export async function scheduleLocalReminder(
  reminder: VoxInterpretation,
): Promise<LocalReminderResult> {
  if (!reminder.date || !reminder.time) return 'missing-date';

  const [year, month, day] = reminder.date.split('-').map(Number);
  const [hour, minute] = reminder.time.split(':').map(Number);
  const triggerDate = new Date(year, month - 1, day, hour, minute, 0, 0);

  if (
    !Number.isFinite(triggerDate.getTime()) ||
    triggerDate.getFullYear() !== year ||
    triggerDate.getMonth() !== month - 1 ||
    triggerDate.getDate() !== day ||
    triggerDate.getHours() !== hour ||
    triggerDate.getMinutes() !== minute
  ) {
    throw new Error('A data ou o horário retornado pela interpretação não é válido.');
  }

  if (triggerDate.getTime() <= Date.now()) return 'past-date';

  if (Platform.OS === 'android') {
    await Notifications.setNotificationChannelAsync('vox-reminders', {
      name: 'Lembretes VOX',
      importance: Notifications.AndroidImportance.MAX,
      vibrationPattern: [0, 250, 150, 250],
      sound: 'default',
    });
  }

  let { status } = await Notifications.getPermissionsAsync();
  if (status !== 'granted') {
    ({ status } = await Notifications.requestPermissionsAsync());
  }
  if (status !== 'granted') return 'permission-denied';

  await Notifications.scheduleNotificationAsync({
    content: {
      title: reminder.title || 'Lembrete VOX',
      body: 'Está na hora do seu lembrete.',
      sound: 'default',
      data: { reminderId: reminder.id },
    },
    trigger: {
      type: Notifications.SchedulableTriggerInputTypes.DATE,
      date: triggerDate,
      ...(Platform.OS === 'android' ? { channelId: 'vox-reminders' } : {}),
    },
  });

  return 'scheduled';
}
