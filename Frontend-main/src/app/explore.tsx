import { ScrollView, StyleSheet, Text, useColorScheme, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { Colors, Spacing } from '@/constants/theme';

const tips = [
  {
    number: '01',
    title: 'Fale naturalmente',
    description: 'Diga o que você precisa fazer e, quando souber, inclua o dia e o horário. Ex.: “Me lembre de estudar para a prova amanhã às 19h”.',
  },
  {
    number: '02',
    title: 'Revise antes de salvar',
    description: 'A transcrição aparece em um campo editável. Corrija nomes, datas ou palavras que o reconhecimento não entendeu.',
  },
  {
    number: '03',
    title: 'Confirme a conexão',
    description: 'O texto é enviado para a agenda-api, que consulta o serviço VOX e armazena o lembrete no MongoDB.',
  },
  {
    number: '04',
    title: 'Permita notificações',
    description: 'Quando data e horário futuros forem identificados, o app tenta agendar uma notificação local. Permita notificações nas configurações do aparelho.',
  },
];

export default function HelpScreen() {
  const scheme = useColorScheme();
  const colors = Colors[scheme === 'dark' ? 'dark' : 'light'];

  return (
    <SafeAreaView style={[styles.safeArea, { backgroundColor: colors.background }]}>
      <ScrollView contentContainerStyle={styles.container}>
        <Text style={[styles.kicker, { color: '#635BDB' }]}>GUIA RÁPIDO</Text>
        <Text style={[styles.title, { color: colors.text }]}>Como usar o VOX</Text>
        <Text style={[styles.subtitle, { color: colors.textSecondary }]}>
          Quatro passos para transformar uma frase em um lembrete.
        </Text>
        <View style={styles.steps}>
          {tips.map((tip) => (
            <View key={tip.number} style={[styles.card, { backgroundColor: colors.backgroundElement }]}>
              <View style={styles.numberCircle}>
                <Text style={styles.numberText}>{tip.number}</Text>
              </View>
              <View style={styles.cardContent}>
                <Text style={[styles.cardTitle, { color: colors.text }]}>{tip.title}</Text>
                <Text style={[styles.cardDescription, { color: colors.textSecondary }]}>
                  {tip.description}
                </Text>
              </View>
            </View>
          ))}
        </View>
        <Text style={[styles.note, { color: colors.textSecondary }]}>
          Observação: a transcrição no celular é configurada para usar reconhecimento no próprio dispositivo. No Android, o idioma português offline precisa estar instalado. A versão inicial do microserviço interpreta comandos com regras locais; um modelo de IA real ainda precisa ser configurado separadamente.
        </Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1 },
  container: { flexGrow: 1, padding: Spacing.three, gap: 12, width: '100%', maxWidth: 680, alignSelf: 'center' },
  kicker: { fontSize: 11, fontWeight: '800', letterSpacing: 1.4, marginTop: Spacing.two },
  title: { fontSize: 30, fontWeight: '800', letterSpacing: -0.6 },
  subtitle: { fontSize: 14, lineHeight: 22, marginBottom: Spacing.two },
  steps: { gap: 12 },
  card: { borderRadius: 20, padding: Spacing.three, flexDirection: 'row', gap: 13 },
  numberCircle: { width: 36, height: 36, borderRadius: 13, backgroundColor: '#635BDB', alignItems: 'center', justifyContent: 'center' },
  numberText: { color: '#FFFFFF', fontSize: 12, fontWeight: '800' },
  cardContent: { flex: 1, gap: 6 },
  cardTitle: { fontSize: 16, fontWeight: '700' },
  cardDescription: { fontSize: 13, lineHeight: 20 },
  note: { fontSize: 12, lineHeight: 18, paddingTop: Spacing.three },
});
