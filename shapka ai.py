import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from sklearn.preprocessing import LabelEncoder

# Предварительно подготовленные данные для обучения
training_data = [("как дела", "Дела"),
                 ("как жизнь", "Дела"),
                 ("как поживаешь", "Дела"),
                 ("что нового", "Дела"),
                 ("чего нового", "Дела"),
                 ("у тебя все", "Дела"),
                 ("что делаешь", "Занятие"),
                 ("чем занят", "Занятие"),
                 ("занимаешься", "Занятие"),
                 ("у меня все хорошо", "Настроение"),
                 ("плохо", "Настроение"),
                 ("норм", "Настроение"),
                 ("хорошо", "Настроение"),
                 ("нормально", "Настроение"),
                 ("ничего особенного", "Настроение"),
                 ("ничего особого", "Настроение"),
                 ("пока хорошо", "Настроение")
                 ]

# Создание словаря слов
word_dict = {}
index = 1
for question, _ in training_data:
    words = question.lower().split()
    for word in words:
        if word not in word_dict:
            word_dict[word] = index
            index += 1

# Преобразование текстовых данных в числовой формат
training_input = []
training_output = []
for question, category in training_data:
    words = question.lower().split()
    vector = [word_dict[word] for word in words]
    training_input.append(vector)
    training_output.append(category)

# Преобразование меток в числовой формат
label_encoder = LabelEncoder()
training_output = label_encoder.fit_transform(training_output)

# Преобразование входных данных в одинаковую длину
max_sequence_length = max(len(seq) for seq in training_input)
training_input = tf.keras.preprocessing.sequence.pad_sequences(training_input, maxlen=max_sequence_length)

# Создание модели нейронной сети
model = Sequential()
model.add(Embedding(len(word_dict) + 1, 64, input_length=max_sequence_length))
model.add(LSTM(64))
model.add(Dense(64, activation='relu'))
model.add(Dense(len(label_encoder.classes_), activation='softmax'))

# Компиляция и обучение модели
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(training_input, training_output, epochs=100)
import time
t = time.time()
# Пример использования обученной модели
question = "у тебя все хорошо"
words = question.lower().split()
vector = [word_dict.get(word, 0) for word in words]  # Используем 0 для неизвестных слов
input_data = tf.keras.preprocessing.sequence.pad_sequences([vector], maxlen=max_sequence_length)
predicted_probabilities = model.predict(input_data)[0]
predicted_category_index = tf.argmax(predicted_probabilities)
predicted_category = label_encoder.classes_[predicted_category_index]
print(predicted_category)
tt = time.time()
print(tt-t)