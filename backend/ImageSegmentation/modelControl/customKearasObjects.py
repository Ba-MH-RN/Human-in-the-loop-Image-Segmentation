import tensorflow as tf

def getCustomObjects() ->dict:
    return {"meanIoU":meanIoU, "diceLoss":diceLoss}

def diceLoss(y_true, y_pred):
        smooth=1e-6
        gama=2
        y_true, y_pred = tf.cast(
            y_true, dtype=tf.float32), tf.cast(y_pred, tf.float32)
        nominator = 2 * \
            tf.reduce_sum(tf.multiply(y_pred, y_true)) + smooth
        denominator = tf.reduce_sum(
            y_pred ** gama) + tf.reduce_sum(y_true ** gama) + smooth
        result = 1 - tf.divide(nominator, denominator)
        return result

def meanIoU(y_true, y_pred):
    y_true = tf.cast(y_true, tf.dtypes.float64)
    y_pred = tf.cast(y_pred, tf.dtypes.float64)
    I = tf.reduce_sum(y_pred * y_true, axis=(1, 2))
    U = tf.reduce_sum(y_pred + y_true, axis=(1, 2)) - I
    return tf.reduce_mean(I / U)