from flask import Flask
from flask import render_template, request 
import fire
import json
import os
import numpy as np
import tensorflow as tf

import model, sample, encoder

import pdb


app = Flask(__name__)


class joker:
    def __init__(
        self,
        model_name='jokes',
        seed=None,
        nsamples=4,
        batch_size=1,
        length=100,
        temperature=0.85,
        top_k=40,
        top_p=0.0
    ):
        self.batch_size = batch_size
        self.enc = encoder.get_encoder(model_name)
        hparams = model.default_hparams()
        with open(os.path.join('models', model_name, 'hparams.json')) as fp:
            hparams.override_from_dict(json.load(fp))

        self.sess = tf.Session()
        self.context = tf.placeholder(tf.int32, [batch_size, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)
        self.output = sample.sample_sequence(
            hparams=hparams,
            length=length,
            context=self.context,
            batch_size=batch_size,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p
        )

        self.sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join('models', model_name))
        saver.restore(self.sess, ckpt)

    def generate(self, text):
        context_tokens = self.enc.encode(text)
        out = self.sess.run(self.output, feed_dict={
            self.context: [context_tokens for _ in range(self.batch_size)]
        })[: len(context_tokens):]
        for i in range(self.batch_size):
            result = self.enc.decode(out[i])
            if "<|endoftext|>" in result:
                return result.split("<|endoftext|>")[0].strip()
            else:
                return "Failed"


session = joker()

@app.route('/')
def interactive_session():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_joke():
    return session.generate(request.form["joke_title"])

if __name__ == '__main__':
    session = joker()
    result = session.generate("title: Why did the chicken cross the road?")
    print(result)
