# Duplicate a tensorflow graph
This is a fork from
https://stackoverflow.com/questions/37801137/duplicate-a-tensorflow-graph

## Q by MBZ:
What is the best way of duplicating a TensorFlow graph and keep it uptodate?

Ideally I want to put the duplicated graph on another device (e.g. from GPU to
CPU) and then time to time update the copy.

## A by rdadolf:
Short answer: You probably want checkpoint files
(permalink:https://github.com/tensorflow/tensorflow/blob/r1.1/tensorflow/docs_src/programmers_guide/variables.md#checkpoint-files).

### Long answer:

Let's be clear about the setup here. I'll assume that you have two devices,
A and B, and you are training on A and running inference on B. Periodically,
you'd like to update the parameters on the device running inference with new
parameters found during training on the other. The tutorial linked above is
a good place to start. It shows you how tf.train.Saver objects work, and you
shouldn't need anything more complicated here.

### Here is an example:



```
import tensorflow as tf


def build_net(graph, device):
    with graph.as_default():
        with graph.device(device):
            # Input placeholders
            inputs = tf.placeholder(tf.float32, [None, 784])
            labels = tf.placeholder(tf.float32, [None, 10])
            # Initialization
            w0 = tf.get_variable('w0', shape=[784, 256], initializer=tf.contrib.layers.xavier_initializer())
            w1 = tf.get_variable('w1', shape=[256, 256], initializer=tf.contrib.layers.xavier_initializer())
            w2 = tf.get_variable('w2', shape=[256, 10], initializer=tf.contrib.layers.xavier_initializer())
            b0 = tf.Variable(tf.zeros([256]))
            b1 = tf.Variable(tf.zeros([256]))
            b2 = tf.Variable(tf.zeros([10]))
            # Inference network
            h1 = tf.nn.relu(tf.matmul(inputs, w0) + b0)
            h2 = tf.nn.relu(tf.matmul(h1, w1) + b1)
            output = tf.nn.softmax(tf.matmul(h2, w2) + b2)
            # Training network
            cross_entropy = tf.reduce_mean(-tf.reduce_sum(labels * tf.log(output), reduction_indices=[1]))
            optimizer = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
            # Your checkpoint function
            saver = tf.train.Saver()
            return tf.global_variables_initializer(), inputs, labels, output, optimizer, saver

```

The code for the training program:


```
def programA_main():
    from tensorflow.examples.tutorials.mnist import input_data
    mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
    # Build training network on device A
    graphA = tf.Graph()
    init, inputs, labels, _, training_net, saver = build_net(graphA, '/cpu:0')
    with tf.Session(graph=graphA) as sess:
        sess.run(init)
        for step in range(1, 10000):
            batch = mnist.train.next_batch(50)
            sess.run(training_net, feed_dict={inputs: batch[0], labels: batch[1]})
            if step % 100 == 0:
                saver.save(sess, '/tmp/graph.checkpoint')
                print('saved checkpoint')
```

'''
...and code for an inference program:
'''

```
def programB_main():
    from tensorflow.examples.tutorials.mnist import input_data
    mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
    # Build inference network on device B
    graphB = tf.Graph()
    init, inputs, _, inference_net, _, saver = build_net(graphB, '/cpu:0')
    with tf.Session(graph=graphB) as sess:
        batch = mnist.test.next_batch(50)

        saver.restore(sess, '/tmp/graph.checkpoint')
        print('loaded checkpoint')
        out = sess.run(inference_net, feed_dict={inputs: batch[0]})
        print(out[0])

        import time
        time.sleep(2)

        saver.restore(sess, '/tmp/graph.checkpoint')
        print('loaded checkpoint')
        out = sess.run(inference_net, feed_dict={inputs: batch[0]})
        print(out[1])
```


If you fire up the training program and then the inference program, you'll
see the inference program produces two different outputs (from the same input
batch). This is a result of it picking up the parameters that the training
program has checkpointed.

Now, this program obviously isn't your end point. We don't do any real
synchronization, and you'll have to decide what "periodic" means with respect
to checkpointing. But this should give you an idea of how to sync parameters
from one network to another.

One final warning: this does not mean that the two networks are necessarily
deterministic. There are known non-deterministic elements in TensorFlow
(e.g., this), so be wary if you need exactly the same answer. But this is
the hard truth about running on multiple devices.

Good luck!

```
if __name__ == '__main__':
    programA_main()
    programB_main()
```
