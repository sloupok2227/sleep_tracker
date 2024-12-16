import matplotlib.pyplot as plt
import io
import base64

def generate_sleep_chart(sleep_records):
    """Создание графика продолжительности сна"""
    dates = [record.date for record in sleep_records]
    durations = [record.sleep_duration()['hours'] + record.sleep_duration()['minutes'] / 60 for record in sleep_records]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, durations, marker='o', linestyle='-', color='b')
    plt.title('Продолжительность сна')
    plt.xlabel('Дата')
    plt.ylabel('Часы сна')
    plt.grid()
    plt.xticks(rotation=45)

    # Сохранение графика в виде base64
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    return image_base64

def generate_recommendations(sleep_records):
    """Генерация рекомендаций на основе данных о сне"""
    avg_duration = sum(
        record.sleep_duration()['hours'] + record.sleep_duration()['minutes'] / 60 for record in sleep_records
    ) / len(sleep_records) if sleep_records else 0

    recommendations = []
    if avg_duration < 7:
        recommendations.append("Ваш средний сон меньше 7 часов. Постарайтесь спать не менее 7-8 часов в сутки.")
    if any(record.wake_ups > 2 for record in sleep_records):
        recommendations.append("Частые пробуждения ночью могут указывать на стресс. Попробуйте расслабляющие упражнения перед сном.")
    if not recommendations:
        recommendations.append("Ваш сон в норме. Продолжайте в том же духе!")
    return recommendations
