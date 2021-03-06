import tensorflow as tf
import threading

lock = threading.Lock()

def generate_text(model, start_string, char2idx, idx2char, temperature=0.1):
    

    lock.acquire() # will block if lock is already held
    # Evaluation step (generating text using the learned model)

    # Number of characters to generate
    num_generate = 200

    # Converting our start string to numbers (vectorizing)
    input_eval = [char2idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)

    # Empty string to store our results
    text_generated = []

    print(temperature)

    # Here batch size == 1
    model.reset_states()
    for i in range(num_generate):
        predictions = model(input_eval)
        # remove the batch dimension
        predictions = tf.squeeze(predictions, 0)

        # using a categorical distribution to predict the word returned by the model
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

        # We pass the predicted word as the next input to the model
        # along with the previous hidden state
        input_eval = tf.expand_dims([predicted_id], 0)

        text_generated.append(idx2char[predicted_id])
    lock.release()

    return (start_string + ''.join(text_generated))
